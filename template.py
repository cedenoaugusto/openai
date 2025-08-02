HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Proyecto OpenAI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap 5 CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light text-dark">
    <div class="container py-5">
        <h1 class="mb-4 text-center">💬 OpenAI</h1>

        <div class="mb-3">
            <label for="inputText" class="form-label">Escribe tu consulta:</label>
            <textarea id="inputText" class="form-control" rows="5" placeholder="Escribe tu consulta aquí..."></textarea>
        </div>

        <div class="d-grid gap-2">
            <button onclick="sendRequest()" class="btn btn-primary btn-lg">Enviar</button>
        </div>

        <div class="mt-5">
            <h4>Respuesta:</h4>
            <textarea id="response" class="form-control" rows="5" placeholder="Escribe tu consulta aquí..."></textarea>
        </div>
    </div>

    <!-- Script para manejar la petición -->
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
