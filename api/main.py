from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import requests
from io import BytesIO

app = FastAPI()

# ------------ Helpers ---------------- #

def imagegen(prompt: str) -> str:
    return f"https://img.hazex.workers.dev?prompt={prompt}&improve=true&format=potrait"


def fetch_image_no_redirect(url: str):
    """Download final image bytes, even if server redirects multiple times."""
    
    session = requests.Session()
    
    # follow_redirects=False to stop auto redirect in browser
    response = session.get(url, allow_redirects=True, stream=True)

    if response.status_code != 200:
        return None
    
    return BytesIO(response.content)


# ------------ Root Info ---------------- #

@app.get("/")
async def home():
    return {
        "message": "Direct Image Generator API (No Redirect Version)",
        "usage": "/gen?prompt=your_prompt",
        "developer": "@Krsxh"
    }


# ------------ GET Route ---------------- #

@app.get("/gen")
async def generate_get(prompt: str | None = None):

    if not prompt or prompt.strip() == "":
        return {"result": "failed", "message": "Missing prompt!"}

    img_url = imagegen(prompt)
    img_data = fetch_image_no_redirect(img_url)

    if img_data is None:
        return {"result": "failed", "message": "Image fetch failed!"}

    return StreamingResponse(img_data, media_type="image/jpeg")


# ------------ POST Route ---------------- #

@app.post("/gen")
async def generate_post(request: Request):

    data = await request.json()
    prompt = data.get("prompt")

    if not prompt or prompt.strip() == "":
        return {"result": "failed", "message": "Missing prompt!"}

    img_url = imagegen(prompt)
    img_data = fetch_image_no_redirect(img_url)

    if img_data is None:
        return {"result": "failed", "message": "Image fetch failed!"}

    return StreamingResponse(img_data, media_type="image/jpeg")
