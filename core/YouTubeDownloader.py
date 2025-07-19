import os
import sys
import requests
from core.Setup import Setup
from core.Auxiliates import *

class YouTubeDownloader(Setup):
    def __init__(self):
        super().__init__()
        self.last_video = None

    def download_mp3(self, link, playlist):
        if not os.path.exists(os.path.join(self.base_dir, "saida", f"{playlist}")):
            os.mkdir(os.path.join(self.base_dir, "saida", f"{playlist}"))
        os.chdir(os.path.join(self.base_dir, "saida", f"{playlist}"))
        message(msg=f"Baixando {link}...")
        os.system(f"yt-dlp --extract-audio --audio-format mp3 {link}")
        os.chdir(self.base_dir)

    def main(self):
        for arquivo in self.files:
            with open(os.path.join("listas", arquivo), "r", encoding="utf-8") as f:
                arquivo = arquivo.split('.')[0]
                lines = f.readlines()
                if lines == []:
                    message(f"Nenhum item conteúdo encontrado no arquivo {arquivo}.")
                    log_write(f"Nenhum item conteúdo encontrado no arquivo `{arquivo}`", self.file_log)
                    self.file_log.close()
                    pause()
                    sys.exit(0)

                contador = 1
                key_atual = 0
                for line in lines:
                    query = line.strip()
                    self.params["key"] = self.keys[key_atual]
                    self.params["q"] = f"{query} - {arquivo}"
                    response = requests.get(self.url_base, params=self.params, headers=self.headers)
                    if response.status_code == 200:
                        data = response.json()
                        if data["items"]:
                            video_id = data["items"][0]["id"]["videoId"]
                            message(f"Video {contador}/{len(lines)} found for {query}: {video_id}")
                            self.download_mp3(f"https://www.youtube.com/watch?v={video_id}", arquivo)
                            self.last_video = f"https://www.youtube.com/watch?v={video_id}"
                            contador += 1
                            if contador == len(lines) + 1:
                                message(f"Todos os videos do arquivo {arquivo} foram baixados.")
                                log_write(f"Todos os videos do arquivo `{arquivo}` foram baixados.", self.file_log)
                                self.file_log.close()
                    elif response.status_code == 403:
                        error = f"Cotas do dia para key `{self.keys[key_atual]}` finalizadas.\n"
                        error += f"Tentiva falha de baixar video: `{query} - {arquivo.replace("-", " ")}` {self.last_video or  ''}"
                        message(f"{error}")
                        log_write(error, self.file_log)
                        if contador != (len(self.keys) - 1):
                            key_atual += 1
                        else:
                            error = f"Todas as keys utilizadas.\n"
                            message(error)
                            log_write(error, self.file_log)
                            pause()
                            sys.exit(0)
