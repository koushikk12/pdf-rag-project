from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()   # ✅ FIRST create the app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers AFTER middleware
from app.api import upload, process

app.include_router(upload.router)
app.include_router(process.router)