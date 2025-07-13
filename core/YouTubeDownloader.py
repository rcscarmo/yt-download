import os
import requests
from datetime import datetime
from core.Setup import Setup
from core.Auxiliates import *

class YouTubeDownloader(Setup):
    def __init__(self):
        super().__init__()
        self.url_base = "https://youtube.googleapis.com/youtube/v3/search"
        self.params = {"part": "snippet", "maxResults": 1, "type": "video"}
        self.headers = {"User-Agent": "curl/7.81.0"}
        self.base_dir = os.path.dirname(os.path.abspath(os.path.basename(__file__)))
        self.last_video = None
        hoje = datetime.today().strftime("%Y-%m-%d")
        self.file_log = open(os.path.join("logs", f"error_log_{hoje}.txt"), "a", encoding="utf-8")

    def download_mp3(self, link, playlist):
        if not os.path.exists(os.path.join(self.base_dir, "saida", f"{playlist}")):
            os.mkdir(os.path.join(self.base_dir, "saida", f"{playlist}"))
        os.chdir(os.path.join(self.base_dir, "saida", f"{playlist}"))
        message(msg=f"Baixando {link}...")
        os.system(f"yt-dlp --extract-audio --audio-format mp3 {link}")
        os.chdir(self.base_dir)

    def main(self):
        arquivos = os.listdir("listas")
        if arquivos == []:
            message("Nenhum arquivo encontrado na pasta `listas`.")
            log_write(f"Nenhum arquivo encontrado na pasta `listas`", self.file_log)
            self.file_log.close()
            exit()
        
        for arquivo in arquivos:
            with open(os.path.join("listas", arquivo), "r", encoding="utf-8") as f:
                arquivo = arquivo.split('.')[0]
                lines = f.readlines()
                if lines == []:
                    message(f"Nenhum item conteúdo encontrado no arquivo {arquivo}.")
                    log_write(f"Nenhum item conteúdo encontrado no arquivo `{arquivo}`", self.file_log)
                    self.file_log.close()
                    exit()

                for line in lines:
                    query = line.strip().replace(" ", "+")
                    self.params["key"] = self.keys[0]
                    self.params["q"] = f"{query} - {arquivo}"
                    response = requests.get(self.url_base, params=self.params, headers=self.headers)
                    if response.status_code == 200:
                        data = response.json()
                        if data["items"]:
                            video_id = data["items"][0]["id"]["videoId"]
                            message(f"Video found for {query}: {video_id}")
                            self.download_mp3(f"https://www.youtube.com/watch?v={video_id}", arquivo)
                            self.last_video = f"https://www.youtube.com/watch?v={video_id}"
                    elif response.status_code == 403:
                        error = f"Cotas do dia finalizadas.\nUltimo tentativa de baixar video: `{query}` - {self.last_video}"
                        log_write(error, self.file_log)
                        self.file_log.close()
                        exit()
