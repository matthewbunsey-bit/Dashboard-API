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
    api_key = "b160f070fc964b11fcc912ea2a23b440"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat=29.66&lon=-95.04&units=imperial&appid={api_key}"
    
    weather_main = "Weather error"
    weather_desc = ""
    feels_like = ""
    wind = ""
    rain = ""
    sunrise_str = ""
    sunset_str = ""
    
    try:
        r = requests.get(url, timeout=10).json()
        if r.get("cod") == 200:
            temp = r["main"]["temp"]
            desc = r["weather"][0]["description"].title()
            weather_main = f"{temp:.0f}°F {desc}"
            weather_desc = desc
            
            feels_like = f"Feels like {r['main']['feels_like']:.0f}°F"
            wind_speed = r["wind"].get("speed", 0)
            wind = f"Wind {wind_speed:.0f} mph"
            
            rain_amount = r.get("rain", {}).get("1h", 0)
            rain = f"Rain {rain_amount} mm/h" if rain_amount > 0 else "No rain"
            
            # Sunrise / Sunset
            sunrise_unix = r["sys"]["sunrise"]
            sunset_unix = r["sys"]["sunset"]
            tz = pytz.timezone("America/Chicago")
            sunrise_str = datetime.fromtimestamp(sunrise_unix, tz).strftime("%I:%M %p")
            sunset_str = datetime.fromtimestamp(sunset_unix, tz).strftime("%I:%M %p")
    except:
        weather_main = "Weather fetch error"

    # Live time
    cst = pytz.timezone("America/Chicago")
    current_time = datetime.now(cst).strftime("%I:%M:%S %p %Z")

    return {
        "weather": weather_main,
        "weather-desc": weather_desc,
        "feels_like": feels_like,
        "wind": wind,
        "rain": rain,
        "sunrise": sunrise_str,
        "sunset": sunset_str,
        "market": "🟩 Bullish (static)",
        "time": current_time,
        "fact": "Octopuses have three hearts"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
