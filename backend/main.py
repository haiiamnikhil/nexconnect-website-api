import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
from backend.routes import admin, public

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NexConnect API", version="1.0.0")

# ALLOWED_ORIGINS: comma-separated list of allowed origins.
# Example: "https://nexconnect.com,https://www.nexconnect.com"
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200")
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(public.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the NexConnect API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000)
