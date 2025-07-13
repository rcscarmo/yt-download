import os
import json
import requests
from datetime import datetime


# ABRE ARQUIVO DE CONFIGURACAO E CARREGA A CHAVE DA API DO YOUTUBE
with open("config.json", "r") as f:
    config = json.load(f)
    KEYS = config["YOUTUBE_API_KEY"]

# URL BASE DA API DO YOUTUBE
URL_BASE = "https://youtube.googleapis.com/youtube/v3/search"

# PARAMETROS DA REQUEST
params = { "part": "snippet", "maxResults": 1, "type": "video", "key": KEYS[0] }

# CABECALHO
HEADERS = { "User-Agent": "curl/7.81.0" }

# DIRETORIO RAIZ DO PROJETO
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DATA ATUAL
HOJE = datetime.today().strftime("%Y-%m-%d")


# CRIA PASTAS NECESSARIAS CASO NAO EXISTAM
def setup():
    folders = ["saida", "listas", "logs"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")


# DADO UM LINK DO YOUTUBE, BAIXA O AUDIO EM MP3
def download_mp3(link, playlist):
    if not os.path.exists(os.path.join(BASE_DIR, "saida", f"{playlist}")):
        os.mkdir(os.path.join(BASE_DIR, "saida", f"{playlist}"))
    os.chdir(os.path.join(BASE_DIR, "saida", f"{playlist}"))
    print(f"Baixando {link}...")
    os.system(f"yt-dlp --extract-audio --audio-format mp3 {link}")
    os.chdir(BASE_DIR)


# FUNCAO PRINCIPAL QUE LÊ OS ARQUIVOS DE LISTA E BUSCA OS VIDEOS NO YOUTUBE
def main():
    arquivos = os.listdir("listas")
    for arquivo in arquivos:
        last_video = ""
        with open(os.path.join("listas", arquivo), "r", encoding="utf-8") as f:
            lines = f.readlines()
            arquivo = arquivo.split('.')[0]
            for line in lines:
                query = line.strip().replace(" ", "+")
                params["q"] = f"{query} - {arquivo}"
                response = requests.get(URL_BASE, params=params, headers=HEADERS)
                if response.status_code == 200:
                    data = response.json()
                    if data["items"]:
                        video_id = data["items"][0]["id"]["videoId"]
                        print(f"Video found for {query}: {video_id}")
                        download_mp3(f"https://www.youtube.com/watch?v={video_id}", arquivo)
                        last_video = f"https://www.youtube.com/watch?v={video_id}"
                elif response.status_code == 403:
                    with open(os.path.join("logs", f"error_log_{HOJE}.txt"), "a", encoding="utf-8") as log_file:
                        log_file.write(f"Cotas do dia finalizadas.{datetime.now()}\n")
                        log_file.write(f"Ultimo video baixado: {last_video}\n")
                        log_file.write(f"============================================================\n")
                        exit()
                        
            with open(os.path.join("logs", f"error_log_{HOJE}.txt"), "a", encoding="utf-8") as log_file:
                log_file.write(f"Download completed for {arquivo} at {datetime.now()}\n")
                log_file.write(f"============================================================\n")


# EXECUTA A FUNCAO PRINCIPAL
if __name__ == "__main__":
    setup()
    main()

