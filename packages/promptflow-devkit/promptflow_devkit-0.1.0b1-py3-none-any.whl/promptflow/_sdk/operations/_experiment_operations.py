# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import copy
import shutil
from pathlib import Path
from typing import List, Optional, Union

from promptflow._sdk._constants import MAX_LIST_CLI_RESULTS, ExperimentStatus, ListViewType
from promptflow._sdk._errors import ExperimentExistsError, RunOperationError
from promptflow._sdk._orm.experiment import Experiment as ORMExperiment
from promptflow._sdk._telemetry import ActivityType, TelemetryMixin, monitor_operation
from promptflow._sdk._utils import safe_parse_object_list
from promptflow._sdk.entities._experiment import Experiment
from promptflow._utils.logger_utils import get_cli_sdk_logger

logger = get_cli_sdk_logger()


class ExperimentOperations(TelemetryMixin):
    """ExperimentOperations."""

    def __init__(self, client, **kwargs):
        super().__init__(**kwargs)
        self._client = client

    @monitor_operation(activity_name="pf.experiment.list", activity_type=ActivityType.PUBLICAPI)
    def list(
        self,
        max_results: Optional[int] = MAX_LIST_CLI_RESULTS,
        *,
        list_view_type: ListViewType = ListViewType.ACTIVE_ONLY,
    ) -> List[Experiment]:
        """List experiments.

        :param max_results: Max number of results to return. Default: 50.
        :type max_results: Optional[int]
        :param list_view_type: View type for including/excluding (for example) archived experiments.
            Default: ACTIVE_ONLY.
        :type list_view_type: Optional[ListViewType]
        :return: List of experiment objects.
        :rtype: List[~promptflow.entities.Experiment]
        """
        orm_experiments = ORMExperiment.list(max_results=max_results, list_view_type=list_view_type)
        return safe_parse_object_list(
            obj_list=orm_experiments,
            parser=Experiment._from_orm_object,
            message_generator=lambda x: f"Error parsing experiment {x.name!r}, skipped.",
        )

    @monitor_operation(activity_name="pf.experiment.get", activity_type=ActivityType.PUBLICAPI)
    def get(self, name: str) -> Experiment:
        """Get an experiment entity.

        :param name: Name of the experiment.
        :type name: str
        :return: experiment object retrieved from the database.
        :rtype: ~promptflow.entities.Experiment
        """
        from promptflow._sdk._submitter.experiment_orchestrator import ExperimentOrchestrator

        ExperimentOrchestrator.get_status(name)
        return Experiment._from_orm_object(ORMExperiment.get(name))

    @monitor_operation(activity_name="pf.experiment.create_or_update", activity_type=ActivityType.PUBLICAPI)
    def create_or_update(self, experiment: Experiment, **kwargs) -> Experiment:
        """Create or update an experiment.

        :param experiment: Experiment object to create or update.
        :type experiment: ~promptflow.entities.Experiment
        :return: Experiment object created or updated.
        :rtype: ~promptflow.entities.Experiment
        """
        orm_experiment = experiment._to_orm_object()
        try:
            orm_experiment.dump()
            return self.get(experiment.name)
        except ExperimentExistsError:
            logger.info(f"Experiment {experiment.name!r} already exists, updating.")
            existing_experiment = orm_experiment.get(experiment.name)
            existing_experiment.update(
                status=orm_experiment.status,
                description=orm_experiment.description,
                last_start_time=orm_experiment.last_start_time,
                last_end_time=orm_experiment.last_end_time,
                node_runs=orm_experiment.node_runs,
                inputs=orm_experiment.inputs,
                data=orm_experiment.data,
            )
            return self.get(experiment.name)

    @monitor_operation(activity_name="pf.experiment.start", activity_type=ActivityType.PUBLICAPI)
    def start(self, experiment: Experiment, stream=False, inputs=None, **kwargs) -> Experiment:
        """
        Start an experiment.

        :param experiment: Experiment object.
        :type experiment: ~promptflow.entities.Experiment
        :param stream: Indicates whether to stream the experiment execution logs to the console.
        :type stream: bool
        :param inputs: Input dict to override.
        :type inputs: Dict[str, str]
        :return: Experiment object started.
        :rtype: ~promptflow.entities.Experiment
        """
        from promptflow._sdk._submitter.experiment_orchestrator import ExperimentOrchestrator

        if experiment._source_path:
            # Update snapshot for anonymous experiment
            logger.debug("Start saving snapshot and update node.")
            snapshots = experiment._output_dir / "snapshots"
            if snapshots.exists():
                shutil.rmtree(snapshots)
            experiment._save_snapshot_and_update_node()

        # Update experiment inputs
        experiment = copy.deepcopy(experiment)
        inputs = inputs or {}
        for name, value in inputs.items():
            exp_input = next(filter(lambda exp_input: exp_input.name == name, experiment.inputs), None)
            if exp_input:
                exp_input.default = value
                continue
            exp_data = next(filter(lambda exp_data: exp_data.name == name, experiment.data), None)
            if exp_data:
                exp_data.path = Path(value).absolute().as_posix()
                continue
            logger.warning(f"Input {name} doesn't exist in experiment.")
        experiment = self.create_or_update(experiment)

        if experiment.status in [ExperimentStatus.QUEUING, ExperimentStatus.IN_PROGRESS]:
            raise RunOperationError(
                f"Experiment {experiment.name} is {experiment.status}, cannot be started repeatedly."
            )
        if stream:
            return ExperimentOrchestrator(self._client, experiment).start(**kwargs)
        else:
            return ExperimentOrchestrator(self._client, experiment).async_start(**kwargs)

    @monitor_operation(activity_name="pf.experiment.stop", activity_type=ActivityType.PUBLICAPI)
    def stop(self, experiment: Experiment, **kwargs) -> Experiment:
        """Stop an experiment.

        :param experiment: Experiment name.
        :type experiment: ~promptflow.entities.Experiment
        :return: Experiment object started.
        :rtype: ~promptflow.entities.Experiment
        """
        from promptflow._sdk._submitter.experiment_orchestrator import ExperimentOrchestrator

        ExperimentOrchestrator(self._client, experiment).stop()
        return self.get(experiment.name)

    def _test(
        self, flow: Union[Path, str], experiment: Union[Path, str], inputs=None, environment_variables=None, **kwargs
    ):
        """Test flow in experiment.

        :param flow: Flow dag yaml file path.
        :type flow: Union[Path, str]
        :param experiment: Experiment yaml file path.
        :type experiment: Union[Path, str]
        :param inputs: Input parameters for flow.
        :type inputs: dict
        :param environment_variables: Environment variables for flow.
        :type environment_variables: dict
        """
        from .._load_functions import _load_experiment_template
        from .._submitter.experiment_orchestrator import ExperimentOrchestrator

        experiment_template = _load_experiment_template(experiment)
        output_path = kwargs.get("output_path", None)
        session = kwargs.get("session", None)
        return ExperimentOrchestrator(client=self._client, experiment=None).test(
            flow,
            experiment_template,
            inputs,
            environment_variables,
            output_path=output_path,
            session=session,
        )
