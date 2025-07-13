# ask video to ia
from fastapi import FastAPI

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

#obtener la url para convertir audio to text


@app.post("/ask-video")
async def ask_video():
    return {"message": "ask video"}
