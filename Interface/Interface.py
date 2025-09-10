import threading
import requests
from io import BytesIO
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkScrollableFrame, CTkImage
from PIL import Image
import os
import subprocess

# Dummy data for search results
DUMMY_RESULTS = [
    {
        "title": "Video 1",
        "thumbnail": "https://cdn.pixabay.com/photo/2016/11/21/06/53/beautiful-natural-image-1844362_640.jpg",
    },
    {
        "title": "Video 2",
        "thumbnail": "https://labetno.ufpa.br/images/galeria_em_artigos/image03_grd.png",
    },
    {
        "title": "Video 3",
        "thumbnail": "https://static.vecteezy.com/ti/fotos-gratis/t2/36324708-ai-gerado-cenario-do-uma-tigre-caminhando-dentro-a-floresta-foto.jpg",
    },
]

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Video/Mp3 Downloader")
        self.geometry("1024x768")
        self.minsize(800, 600)

        # Search bar
        self.search_frame = CTkFrame(self)
        self.search_frame.pack(padx=20, pady=20, fill="x")

        self.search_entry = CTkEntry(self.search_frame, placeholder_text="Pesquisar vídeo ou música...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.search_button = CTkButton(self.search_frame, text="Pesquisar", command=self.start_search)
        self.search_button.pack(side="left")

        # Results area
        self.results_frame = CTkScrollableFrame(self, height=600)
        self.results_frame.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        # Label de status
        self.status_label = CTkLabel(self, text="", font=("Arial", 14))
        self.status_label.pack(pady=(0,10))

    def start_search(self):
        query = self.search_entry.get().strip()
        if not query:
            return

        # Mostra status
        self.status_label.configure(text="Pesquisando...")

        # Thread para não travar interface
        threading.Thread(target=self.search, args=(query,), daemon=True).start()

    def search(self, query):
        # Limpa resultados anteriores
        self.clear_results()

        # Aqui você faria a busca real usando a query
        results = DUMMY_RESULTS  

        # Adiciona resultados
        for result in results:
            self.add_result_item(result)

        # Atualiza status (no main thread)
        self.after(0, lambda: self.status_label.configure(text="Pesquisa concluída!"))

    def clear_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def add_result_item(self, result):
        item_frame = CTkFrame(self.results_frame)
        item_frame.pack(fill="x", pady=10, padx=10)

        # Thumbnail
        try:
            if result["thumbnail"].startswith("http"):
                response = requests.get(result["thumbnail"])
                response.raise_for_status()
                img = Image.open(BytesIO(response.content)).resize((80, 60))
            else:
                img = Image.open(result["thumbnail"]).resize((80, 60))

            photo = CTkImage(light_image=img, dark_image=img, size=(80, 60))
            thumbnail_label = CTkLabel(item_frame, image=photo, text="")
            thumbnail_label.image = photo
        except Exception as e:
            print("Erro ao carregar imagem:", e)
            thumbnail_label = CTkLabel(item_frame, text="[Sem imagem]", width=80, height=60)

        thumbnail_label.pack(side="left", padx=10)

        # Title
        title_label = CTkLabel(item_frame, text=result["title"], font=("Arial", 16))
        title_label.pack(side="left", padx=10, fill="x", expand=True)

        # Download buttons
        btn_mp3 = CTkButton(item_frame, text="Baixar MP3", command=lambda: self.download(result, "mp3"))
        btn_mp3.pack(side="right", padx=5)
        btn_mp4 = CTkButton(item_frame, text="Baixar MP4", command=lambda: self.download_mp3(result, "mp4"))
        btn_mp4.pack(side="right", padx=5)

    def download(self, result, format_type):
        print(f"Baixando '{result['title']}' como {format_type.upper()}")
    
    def download_mp3(self, link, playlist="default"):
        # Cria a pasta de saída se não existir
        output_dir = os.path.join(self.base_dir, "saida", playlist)
        os.makedirs(output_dir, exist_ok=True)

        # Mensagem de status
        self.after(0, lambda: self.status_label.configure(text=f"Baixando {link}..."))

        # Executa yt-dlp
        try:
            subprocess.run(
                ["yt-dlp", "--extract-audio", "--audio-format", "mp3", "-o", f"{output_dir}/%(title)s.%(ext)s", link],
                check=True
            )
            self.after(0, lambda: self.status_label.configure(text=f"Download concluído: {link}"))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Erro ao baixar: {e}"))


    

if __name__ == "__main__":
    app = App()
    app.mainloop()
