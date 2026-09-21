from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Montar archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Nota la nueva estructura: request pasa primero, y el diccionario va limpio
    return templates.TemplateResponse(request, "index.html", {"app_name": "Mi App Web"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)