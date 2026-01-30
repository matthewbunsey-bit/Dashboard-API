from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
from datetime import datetime
import pytz

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("dashboard.html") as f:
        return f.read()

@app.get("/dashboard")
def dashboard():
    # Weather
    api_key = "b160f070fc964b11fcc912ea2a23b440"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat=29.66&lon=-95.04&units=imperial&appid={api_key}"
    weather_str = "Weather error"
    weather_desc = ""
    try:
        response = requests.get(url, timeout=10).json()
        if response.get("cod") == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"].title()
            weather_str = f"{temp:.0f}°F {desc}"
            weather_desc = desc
        else:
            weather_str = "Weather API failed"
    except Exception:
        weather_str = "Weather fetch error"

    # Time - CST
    cst = pytz.timezone("America/Chicago")
    current_time = datetime.now(cst).strftime("%I:%M %p %Z")

    return {
        "weather": weather_str,
        "weather-desc": weather_desc,
        "market": "🟩 Bullish (static)",
        "time": current_time,
        "fact": "Octopuses have three hearts"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
