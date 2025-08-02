from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import openai
import os
import uvicorn

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")  # O pon tu clave aquí

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>OpenAI Local</title>
</head>
<body>
    <h1>Prueba OpenAI local</h1>
    <textarea id="inputText" rows="5" cols="60" placeholder="Escribe tu consulta aquí"></textarea><br>
    <button onclick="sendRequest()">Enviar</button>
    <h3>Respuesta:</h3>
    <pre id="response"></pre>

<script>
async function sendRequest() {
    const input = document.getElementById('inputText').value;
    const responseElem = document.getElementById('response');
    responseElem.textContent = "Cargando...";

    const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt: input})
    });
    const data = await res.json();
    if (data.error) {
        responseElem.textContent = "Error: " + data.error;
    } else {
        responseElem.textContent = data.response;
    }
}
</script>
</body>
</html>
"""

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
