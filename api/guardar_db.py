# AQUI SE GUARDA EN LA BASE DE DATOS
from dotenv import load_dotenv
import os
from supabase import create_client, Client

from extraer_text_update import transcribe_youtube_audio
import json


load_dotenv()
client: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

JSON_PATH = "./api/data_url/video_urls.json"

def guardar_db(video_url:str,text: str):
    data = {
        "video_url": video_url,
        "text": text
    }
    try:
        response = supabase.table("transcripts").insert(data).execute()
        print("Guardado en la base de datos")
        return response
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")
        return None

# url_video = "https://www.youtube.com/watch?v=8R-cetf_sZ4"
# text= transcribe_youtube_audio(url_video)
# guardar_db(url_video,text)

def procesar_videos_desde_json():
    """
    Procesa los videos desde el archivo JSON, los envia para traducir los videos (obtener texto del video youtube) y luego los guarda en la base de datos.
    """
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        video_urls = data.get("videoUrls", [])

    for url in video_urls:
        print(f"🎧 Transcribiendo: {url}")
        texto = transcribe_youtube_audio(url)
        if texto:
            guardar_db(url, texto)
        else:
            print(f"⚠️ Falló la transcripción: {url}")

procesar_videos_desde_json()


