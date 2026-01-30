import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/dashboard")
def dashboard():
    return {
"weather": "THIS IS THE NEW VERSION MOTHERFUCKER",
        "market": "🟩 Bullish",
        "time": "Live",
        "fact": "Octopuses have three hearts"
    }
