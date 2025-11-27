from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse

app = FastAPI()

# ------------ Helpers ---------------- #

def imagegen(prompt: str) -> str:
    """Generate AI image URL."""
    return f"https://img.hazex.workers.dev?prompt={prompt}&improve=true&format=potrait"


# ------------ Root Info ---------------- #

@app.get("/")
async def home():
    return {
        "message": "Direct Image Generator API",
        "usage": "GET /gen?prompt=your_text",
        "POST_usage": "POST /gen { 'prompt': 'your_text' }",
        "developer": "@Krsxh"
    }


# ------------ GET Route (Direct Image) ---------------- #

@app.get("/gen")
async def generate_get(prompt: str | None = None):

    if not prompt or prompt.strip() == "":
        return {
            "result": "failed",
            "message": "Missing prompt!",
            "usage": "/gen?prompt=a cute cat"
        }

    final_image_link = imagegen(prompt)

    # DIRECT IMAGE OUTPUT
    return RedirectResponse(final_image_link)


# ------------ POST Route (Direct Image) ---------------- #

@app.post("/gen")
async def generate_post(request: Request):

    data = await request.json()
    prompt = data.get("prompt")

    if not prompt or prompt.strip() == "":
        return JSONResponse(
            content={
                "result": "failed",
                "message": "Missing 'prompt' in JSON body!",
                "usage": { "prompt": "your_prompt_here" }
            }
        )

    final_image_link = imagegen(prompt)

    # DIRECT IMAGE OUTPUT
    return RedirectResponse(final_image_link)
