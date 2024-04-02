import logging
import os
import pathlib
import sys

from uvicorn import Config, Server


def uvicorn_with_logging_file(
    app_path: pathlib.Path,
    foldername="Logging",
    filename="server.log",
    app=None,
    host="127.0.0.1",
    port=8000,
):
    try:
        if getattr(sys, "frozen", False):  # Überprüft, ob das Programm eingefroren ist
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = app_path.resolve()
        log_file_path = os.path.join(application_path, str(foldername), str(filename))
        log_dir = os.path.dirname(log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logging.basicConfig(filename=log_file_path, level=logging.INFO)
        config = Config(app=app, host=host, port=port, log_config=None)
        server = Server(config)
        server.run()
    except KeyboardInterrupt:
        print("Unterbrochen")
        sys.exit(1)


def remove_logging(lgging_folder: str, log_file: str):
    try:
        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
            log_file_path = os.path.join(application_path, lgging_folder, log_file)
        if os.path.exists(log_file_path):
            with open(log_file_path, "w"):
                pass
        else:
            return "Die Serverlog-Datei wurde nicht gefunden."
    except Exception as e:
        return e


def get_logging(lgging_folder: str, log_file: str):
    try:
        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
            log_file_path = os.path.join(
                application_path, str(lgging_folder), str(log_file)
            )
        if os.path.exists(log_file_path):
            with open(log_file_path, "rb") as log:
                log_read = log.read()
                return log_read
        else:
            return FileNotFoundError()
    except Exception as e:
        return e
