from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import router as api_router  

app = FastAPI(title="FastAPI Modular Example")

origins = [
    "http://localhost:8501",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include router ---
app.include_router(api_router)
