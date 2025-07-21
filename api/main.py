# ask video to ia
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

load_dotenv()

#model chat de academ
class ChatRequest(BaseModel):
    userId: str
    courseSlug: str
    chapterId: str
    videoUrl: str
    userMessage: str
    

#----------


url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o tu dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/chat/video")
async def chat_with_video(data: ChatRequest):
    # Extraer datos
    video_url = data.videoUrl
    user_message = data.userMessage

    # 1. Obtener transcripción desde Supabase
    response = supabase.table("transcripts").select("text").eq("video_url", video_url).execute()
    transcript = response.data[0]["text"] if response.data else None

    if not transcript:
        return {"botResponse": "No encontré transcripción para este video."}

    # 2. Crear prompt para Groq o cualquier otro modelo
    prompt = f"""
    El usuario está viendo el video: {video_url}
    Transcripción disponible: {transcript[:500]}... [truncado]
    Pregunta del usuario: {user_message}
    
    """

    system_message = """
    Quiero que te comportes como un experto en 'TouchDesigner'.
    "https://docs.derivative.ca/" es la documentacion oficial de TouchDesigner.
    
    Eres un profesor que responde preguntas sobre videos, se te entregara el texto del video y la pregunta del usuario. Tienes que responder siempre en el idioma del que sea el "user_message". 
    Siempre responde de tu a tu, recuerda que eres un profesor.
    Solo entrega la respuesta, no pongas nada extra.
    """
    # ia section
    client = Groq(api_key=os.getenv("GROK_API_KEY_RESPONSE"))
    
    respuesta = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    print("respuesta",respuesta.choices[0].message.content)


    #--------------

    # 3. Simular respuesta del modelo (aquí integrarías Groq luego)
    bot_response = respuesta.choices[0].message.content

    # 4. (Opcional) Guardar el historial en Supabase o Neon
    # Aquí podrías insertar en una tabla de historial si quieres persistencia

    return {"botResponse": bot_response}

@app.post("/api/get-videos")
async def get_videos():
    """
    Obtiene todos los videos de la base de datos
    """
    response = supabase.table("transcripts").select("video_url").execute()
    
    if response.data:
        return response.data
    return {"error": "Video no encontrado"}


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/video/{url}")
async def video(url: str):
    """
    Ejemplo: url: "https://www.youtube.com/watch?v=8R-cetf_sZ4"
    Pasarle el exactamente lo que vengas despues de "watch?v="
    """
    print(url)
    url_complete = f"https://www.youtube.com/watch?v={url}"
    return {"video": url_complete}

@app.get("/video-info/{video_id}")
async def get_video_info(video_id: str):
    """
    Busca en la base de datos el video
    Ejemplo: video_id: "8R-cetf_sZ4"
    Pasarle el exactamente lo que vengas despues de "watch?v="
    """
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    response = supabase.table("transcripts").select("id, video_url, text").eq("video_url", video_url).execute()
    if response.data:
        return response.data[0]
    return {"error": "Video no encontrado"}

@app.post("/ask-video")
async def ask_video():


    return {"message": "ask video"}



