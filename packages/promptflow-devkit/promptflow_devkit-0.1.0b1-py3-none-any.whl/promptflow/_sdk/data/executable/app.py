import os
import sys

from main import start
from streamlit.runtime import exists
from streamlit.web import cli as st_cli

from promptflow._cli._pf._connection import create_connection


def is_yaml_file(file_path):
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # Check if the file extension is ".yaml" or ".yml"
    return file_extension.lower() in (".yaml", ".yml")


def create_connections(directory_path) -> None:
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_yaml_file(file_path):
                create_connection(file_path)


if __name__ == "__main__":

    create_connections(os.path.join(os.path.dirname(__file__), "connections"))
    if exists():
        start()
    else:
        main_script = os.path.join(os.path.dirname(__file__), "main.py")
        sys.argv = [
            "streamlit",
            "run",
            main_script,
            "--global.developmentMode=false",
            "--client.toolbarMode=viewer",
            "--browser.gatherUsageStats=false",
        ]
        st_cli.main(prog_name="streamlit")
