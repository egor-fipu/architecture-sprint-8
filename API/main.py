from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth import verify_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://localhost:3000"] если ограничивать
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

@app.get("/reports")
def get_reports(user=Depends(verify_token)):
    return {
        "message": "Fake reports data",
        "user": user["preferred_username"]
    }
