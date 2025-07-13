import os
import json
from core.Auxiliates import message

class Setup:
    def __init__(self):
        self.folders = ["saida", "listas", "logs"]
        self.setup_folders()
        self.keys = self.load_api_keys()
        self.files = self.get_files()

    def setup_folders(self):
        for folder in self.folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                message(f"Created folder: {folder}")

    def get_files(self):
        files = []
        for folder in "listas":
            if os.path.exists(folder):
                files.extend(os.listdir(folder))
        return files

    def load_api_keys(self):
        with open("config.json", "r") as f:
            config = json.load(f)
            return config["YOUTUBE_API_KEY"]
