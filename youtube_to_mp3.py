import os
from io import BytesIO
from tempfile import NamedTemporaryFile

from pytubefix import YouTube
from pytubefix.helpers import reset_cache
try:
    # Try MoviePy v2.x import first
    from moviepy import AudioFileClip
except ImportError:
    try:
        # Fall back to MoviePy v1.x import
        from moviepy.editor import AudioFileClip
    except ImportError as e:
        raise ImportError(f"Could not import AudioFileClip from moviepy: {e}")
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

reset_cache()

class URLItem(BaseModel):
    url: str

@app.get("/")
async def status():
    po_token_mode = os.getenv("PO_TOKEN_MODE", "AUTO").upper()
    po_token_configured = bool(os.getenv("PO_TOKEN"))
    visitor_data_configured = bool(os.getenv("VISITOR_DATA"))
    
    return {
        "message": "YouTube to MP3 Service",
        "status": "running",
        "po_token": {
            "mode": po_token_mode,
            "po_token_configured": po_token_configured,
            "visitor_data_configured": visitor_data_configured
        }
    }


@app.post("/convert/")
async def convert(url_item: URLItem):
    try:
        # Get PoToken configuration from environment variables
        po_token = os.getenv("PO_TOKEN")
        visitor_data = os.getenv("VISITOR_DATA")
        po_token_mode = os.getenv("PO_TOKEN_MODE", "AUTO").upper()  # AUTO or MANUAL
        
        # Configure YouTube instance based on PoToken settings
        if po_token_mode == "AUTO":
            # Automatic PoToken generation with WEB client (requires nodejs)
            print(f"Using automatic PoToken generation with WEB client")
            yt = YouTube(
                url_item.url,
                client='WEB',
                use_oauth=False,
                allow_oauth_cache=True
            )
        elif po_token and po_token_mode == "MANUAL":
            # Manual PoToken mode with extracted token and visitor data
            print(f"Using manual PoToken with extracted token")
            if visitor_data:
                yt = YouTube(
                    url_item.url,
                    use_po_token=True,
                    po_token=po_token,
                    visitor_data=visitor_data,
                    use_oauth=False,
                    allow_oauth_cache=True
                )
            else:
                yt = YouTube(
                    url_item.url,
                    use_po_token=True,
                    po_token=po_token,
                    use_oauth=False,
                    allow_oauth_cache=True
                )
        else:
            # Default mode without PoToken
            print(f"Using default YouTube client (no PoToken)")
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
