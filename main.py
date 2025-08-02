# https://platform.openai.com/settings/organization/billing/overview

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import openai
import os
import uvicorn

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

from template import HTML_PAGE

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_PAGE

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        return JSONResponse({"error": "No hay prompt enviado"}, status_code=400)

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        return {"response": answer}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
