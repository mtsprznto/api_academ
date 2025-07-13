import os
import psycopg2
from dotenv import load_dotenv
import json
load_dotenv()
conn_str = os.getenv("NEON_DATABASE_URL")

def get_all_video_urls():
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute('SELECT "videoUrl" FROM "Chapter" WHERE "videoUrl" IS NOT NULL AND "videoUrl" != \'\';')
        results = cur.fetchall()
        cur.close()
        conn.close()

        # Extraer solo los URLs como lista
        urls = [row[0] for row in results]
        return {"videoUrls": urls}

    except Exception as e:
        return {"error": str(e)}

print(get_all_video_urls())
# guardar en un json
PATH_URL_VIDEO = "./api/data_url/video_urls.json"
with open(PATH_URL_VIDEO, "w", encoding="utf-8") as f:
    json.dump(get_all_video_urls(), f, ensure_ascii=False)
