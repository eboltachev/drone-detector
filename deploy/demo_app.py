from fastapi.staticfiles import StaticFiles

from app.main import app


app.mount("/", StaticFiles(directory="/app/static", html=True), name="frontend")
