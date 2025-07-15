# AQUI SE GUARDA EN LA BASE DE DATOS
from dotenv import load_dotenv
import os
from supabase import create_client, Client

from extraer_text_update import transcribe_youtube_audio
import json


load_dotenv()

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






def procesar_videos_desde_json():
    """
    Procesa los videos desde el archivo JSON, los transcribe, guarda en Supabase
    y elimina los que fueron guardados exitosamente del archivo JSON.
    """
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            video_urls = data.get("videoUrls", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al leer JSON: {e}")
        return

    urls_pendientes = []

    for url in video_urls:
        print(f"🎧 Transcribiendo: {url}")
        texto = transcribe_youtube_audio(url)

        if texto:
            response = guardar_db(url, texto)
            # Verificamos si Supabase respondió correctamente
            if response:
                print(f"✅ Guardado en DB y eliminado del JSON: {url}")
                continue  # No lo agregamos a pendientes
            else:
                print(f"⚠️ Error al guardar en Supabase: {url}")
                urls_pendientes.append(url)
        else:
            print(f"⚠️ Falló la transcripción: {url}")
            urls_pendientes.append(url)

    # Guardamos nuevamente el archivo JSON solo con las URLs pendientes
    try:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump({"videoUrls": urls_pendientes}, f, indent=4, ensure_ascii=False)
        print(f"📝 JSON actualizado. Videos pendientes: {len(urls_pendientes)}")
    except Exception as e:
        print(f"Error al actualizar JSON: {e}")

procesar_videos_desde_json()