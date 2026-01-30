import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
        "weather": "72°F Sunny",
        "market": "🟩 Bullish",
        "time": "Live",
        "fact": "Octopuses have three hearts"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Railway's port if set
    uvicorn.run(app, host="0.0.0.0", port=port)
