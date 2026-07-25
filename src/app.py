from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_app():
    app = FastAPI()
    web_path = Path(__file__).parent.parent / "web"
    app.mount("/", StaticFiles(directory=str(web_path), html=True), name="static")
    return app

app = create_app()
