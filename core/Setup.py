import os
import sys
import json
import subprocess
from core.Auxiliates import *

class Setup:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(os.path.basename(__file__)))
        self.setup_folders()
        self.keys = self.load_api_keys()
        self.files = self.get_files()
        self.verificacoes()
        self.url_base = "https://youtube.googleapis.com/youtube/v3/search"
        self.params = {"part": "snippet", "maxResults": 1, "type": "video"}
        self.headers = {"User-Agent": "curl/7.81.0"}
        self.hoje = datetime.today().strftime("%Y-%m-%d")
        self.file_log = open(os.path.join("logs", f"error_log_{self.hoje}.txt"), "a", encoding="utf-8")

    def setup_folders(self):
        folders = ["saida", "listas", "logs"]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                message(f"Created folder: {folder}")

    def get_files(self):
        return os.listdir(os.path.join(self.base_dir, "listas"))

    def load_api_keys(self):
        with open("config.json", "r") as f:
            config = json.load(f)
            return config["YOUTUBE_API_KEY"]
        
    def verificacoes(self):
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            message(f"FFmpeg: Nao instalado ou nao encontrado. Instale o FFmpeg e tente novamente.")
            pause()
            sys.exit(0)

        if self.keys == []:
            message("YouTube API key not found in config.json. Please add it.".upper())
            pause()
            sys.exit(0)
        
        if self.files == []:
            message("No files found in the 'listas' folder.".upper())
            pause()
            sys.exit(0)
