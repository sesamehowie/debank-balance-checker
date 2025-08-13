import os
from pathlib import Path
from yaml import safe_load


class Config:
    ROOT = Path(os.getcwd())
    FILES_PATH = os.path.join(ROOT, Path("files"))
    RESULTS_PATH = os.path.join(ROOT, Path("results"))
    WALLETS_FILE = os.path.join(FILES_PATH, Path("wallets.txt"))
    CONFIG_FILE_PATH = os.path.join(ROOT, Path("config.yaml"))
    RESULTS_FILE_PATH = os.path.join(RESULTS_PATH, Path("results.csv"))

    def __init__(self):
        self.config = self.load_config()
        self.RAPID_API_KEY = self.config["rapid_api_key"]
        self.SLEEP_ON_ERRORS = self.config["sleep_on_errors"]
        self.SLEEP_BETWEEN_ACCS = self.config["sleep_between_accs"]
        self.RETRIES = self.config["request_retries"]

    def load_config(self):
        data = None

        with open(self.CONFIG_FILE_PATH, "r") as f:
            data = f.read()

        if not data:
            raise Exception(f"Failed to read yaml config at {self.CONFIG_FILE_PATH}")
        else:
            return safe_load(data)
