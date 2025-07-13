import yt_dlp
import os
from groq import Groq, RateLimitError
from dotenv import load_dotenv
from glob import glob
import subprocess


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
JSON_PATH = "./api/data_url/video_urls.json"


#obtener la url para convertir audio to text
#trascribir video de yotube a text

def cortar_audio(original_path: str, destino_path: str, inicio: int = 0, duracion: int = 300):
    comando = [
        "ffmpeg",
        "-i", original_path,
        "-ss", str(inicio),
        "-t", str(duracion),
        "-c", "copy",
        destino_path
    ]
    subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def transcribe_youtube_audio(youtube_url:str) -> str:
    output_base = "./audio_temp/temp_audio"
    output_path = output_base + ".%(ext)s"

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
        ydl.download([youtube_url])
    mp3_files = glob(output_base + "*.mp3")
    if not mp3_files:
        raise FileNotFoundError("No se encontraron archivos mp3")
    audio_path = mp3_files[0]
    

    cortar_audio(audio_path, audio_path, inicio=0, duracion=300)
    audio_path = "audio_temp/cortado.mp3"

    try:
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="distil-whisper-large-v3-en",
                response_format="text",
                language="en",
                temperature=0.0,
            )
        
    except RateLimitError as e:
        print(f"Limite de audio alcanzado: {e}")
        return None
    except groq.APIStatusError as e:
        if e.status_code == 413:
            print(f"⚠️ Archivo demasiado grande para Groq: {youtube_url}")
            return None
    
    os.remove(audio_path)

    return transcription


# este texto tiene que enviarse a supabase (base de datos)
