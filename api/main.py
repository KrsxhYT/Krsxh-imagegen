from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import requests
from io import BytesIO

app = FastAPI()

# ------------ Helpers ---------------- #

def imagegen(prompt: str) -> str:
    return f"https://img.hazex.workers.dev?prompt={prompt}&improve=true&format=potrait"


def fetch_image(url: str):
    """Download image bytes from URL."""
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        return None

    return BytesIO(response.content)


# ------------ Root Info ---------------- #

@app.get("/")
async def home():
    return {
        "message": "Direct Image Generator API",
        "usage": "GET /gen?prompt=your_text",
        "POST_usage": "POST /gen  { 'prompt': 'your_text' }",
        "developer": "@Krsxh"
    }


# ------------ GET Route (Direct Image Response) ---------------- #

@app.get("/gen")
async def generate_get(prompt: str | None = None):

    if not prompt or prompt.strip() == "":
        return JSONResponse(
            content={
                "result": "failed",
                "message": "Missing prompt!",
                "usage": "/gen?prompt=a cute cat"
            }
        )

    img_url = imagegen(prompt)
    img_data = fetch_image(img_url)

    if img_data is None:
        return JSONResponse(
            content={
                "result": "failed",
                "message": "Failed to load image!"
            }
        )

    return StreamingResponse(img_data, media_type="image/jpeg")


# ------------ POST Route (Direct Image Response) ---------------- #

@app.post("/gen")
async def generate_post(request: Request):

    data = await request.json()
    prompt = data.get("prompt")

    if not prompt or prompt.strip() == "":
        return JSONResponse(
            content={
                "result": "failed",
                "message": "Missing 'prompt' in JSON body!"
            }
        )

    img_url = imagegen(prompt)
    img_data = fetch_image(img_url)

    if img_data is None:
        return JSONResponse(
            content={
                "result": "failed",
                "message": "Failed to load image!"
            }
        )

    return StreamingResponse(img_data, media_type="image/jpeg")
