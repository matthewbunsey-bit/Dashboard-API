from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("dashboard.html") as f:
        return f.read()

@app.get("/dashboard")
def dashboard():
    api_key = "b160f070fc964b11fcc912ea2a23b440"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat=29.66&lon=-95.04&units=imperial&appid={api_key}"
    
    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:
            weather_str = "Weather fetch failed"
            weather_desc = ""
        else:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"].title()
            weather_str = f"{temp:.0f}°F {desc}"
            weather_desc = desc
    except:
        weather_str = "Weather error"
        weather_desc = ""

    return {
        "weather": weather_str,
        "weather-desc": weather_desc,
        "market": "🟩 Bullish (static)",
        "time": "Live",
        "fact": "Octopuses have three hearts"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
