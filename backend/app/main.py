from fastapi import FastAPI
from app.api import upload, process, ask

app = FastAPI()

app.include_router(upload.router)
app.include_router(process.router)
app.include_router(ask.router)