# ask video to ia
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

from fastapi import FastAPI




url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


app = FastAPI()

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
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    response = supabase.table("transcripts").select("id, video_url, text").eq("video_url", video_url).execute()
    if response.data:
        return response.data[0]
    return {"error": "Video no encontrado"}

@app.post("/ask-video")
async def ask_video():
    return {"message": "ask video"}
