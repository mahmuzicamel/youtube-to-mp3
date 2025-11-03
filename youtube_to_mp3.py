import os
from io import BytesIO
from tempfile import NamedTemporaryFile

from pytubefix import YouTube
from pytubefix.helpers import reset_cache
from moviepy.editor import AudioFileClip
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

reset_cache()

class URLItem(BaseModel):
    url: str


@app.post("/download_audio_post/")
async def download_audio_post(url_item: URLItem):
    try:
        yt = YouTube(
            url_item.url,
            use_oauth=False,
            allow_oauth_cache=True
        )

        stream = yt.streams.get_audio_only()
        if not stream:
            raise HTTPException(status_code=404, detail="Kein Audiostream gefunden")

        print(f"Downloading: {yt.title}")
        # Lade m4a in temp Datei
        with NamedTemporaryFile(suffix=".m4a", delete=False) as tmp_in:
            tmp_in_path = tmp_in.name
            stream.stream_to_buffer(tmp_in)
            tmp_in.flush()

        # MoviePy braucht einen Dateipfad – also auslesen, konvertieren
        with NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_out:
            tmp_out_path = tmp_out.name

        clip = AudioFileClip(tmp_in_path)
        clip.write_audiofile(tmp_out_path)
        clip.close()

        # MP3 in Speicher laden
        with open(tmp_out_path, "rb") as f:
            mp3_data = f.read()

        # Temporäre Dateien löschen
        os.remove(tmp_in_path)
        os.remove(tmp_out_path)

        # In-Memory zurückgeben
        buf = BytesIO(mp3_data)
        buf.seek(0)
        filename = f"{yt.title}.mp3".replace("/", "_")
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        return StreamingResponse(buf, media_type="audio/mpeg", headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler: {e}")
