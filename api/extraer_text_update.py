import os
from dotenv import load_dotenv
from glob import glob
import yt_dlp
from yt_dlp.utils import DownloadError
from groq import Groq, RateLimitError, APIStatusError

from time import sleep
load_dotenv()
from hashlib import md5


client = Groq(api_key=os.getenv("GROQ_API_KEY"))
JSON_PATH = "./api/data_url/video_urls.json"


#obtener la url para convertir audio to text
#trascribir video de yotube a text



def transcribe_youtube_audio(youtube_url:str) -> str:
    """
    Transcribe audio de un video de YouTube a texto.
    """
    # Generar nombre único por video
    video_id = youtube_url.split("v=")[-1].split("&")[0]
    unique_suffix = md5(youtube_url.encode()).hexdigest()[:8]
    output_base = f"./audio_temp/audio_{unique_suffix}"
    output_path = output_base + ".%(ext)s"

    

    for f in glob("./audio_temp/*"):
        try:
            os.remove(f)
        except PermissionError:
            print(f"⚠️ Archivo bloqueado: {f} — esperando 0.5s...")
            sleep(0.5)
            try:
                os.remove(f)
            except Exception:
                print(f"❌ Todavía bloqueado: {f}")

    try:
        yfl_opts = { 
            "format": "bestaudio/best",
            "outtmpl": output_path,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            'quiet': True,
        }
            

        with yt_dlp.YoutubeDL(yfl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            duracion_segundos = info.get("duration")
            print(f"⏱️ Duración del video: {duracion_segundos} segundos")


        mp3_files = glob(output_base + "*.mp3")
        if not mp3_files:
            raise FileNotFoundError("No se encontraron archivos mp3")
        audio_path = mp3_files[0]
        
    
        transcription = None
        try:
            print("Transcribiendo audio...")
            if duracion_segundos and duracion_segundos > 600:
                print(f"⚠️ Video demasiado largo ({duracion_segundos}s), se omite.")
                try:
                    os.remove(audio_path)
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar el archivo de audio: {audio_path}")
                return None


            with open(audio_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=audio_file,
                    model="distil-whisper-large-v3-en",
                    response_format="text",
                    language="en",
                    temperature=0.0,
                )
            print("Transcripción exitosa")
        except RateLimitError as e:
            print(f"⚠️ Límite de audio alcanzado: {e}")
        except APIStatusError as e:
            if e.status_code == 413:
                print(f"⚠️ Archivo demasiado grande para Groq: {youtube_url}")
            else:
                print(f"⚠️ Error de Groq API ({e.status_code}): {e}")
        except Exception as e:
            print(f"❌ Error inesperado al transcribir: {youtube_url}")
            print(f"Motivo: {str(e)}")

        try:
            os.remove(audio_path)
        except Exception as e:
            print(f"⚠️ No se pudo eliminar el archivo de audio: {audio_path}")



        if transcription:
            print("✅ Transcripción terminada correctamente.")
            return transcription
        else:
            print(f"⚠️ No se obtuvo transcripción: {youtube_url}")
            return None


        


    except DownloadError as e:
        print(f"❌ yt_dlp no pudo descargar: {youtube_url}")
        print(f"Motivo: {str(e)}")
        return None




# este texto tiene que enviarse a supabase (base de datos)

