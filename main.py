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
    
    try:from fastapi import FastAPI
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
    # 1. Real weather - La Porte/Dayton coords, your key
    weather_key = "b160f070fc964b11fcc912ea2a23b440"
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat=29.66&lon=-95.04&units=imperial&appid={weather_key}"
    weather_str = "Weather error"
    weather_desc = ""
    try:
        w = requests.get(weather_url, timeout=10).json()
        if w.get("cod") == 200:
            temp = w["main"]["temp"]
            desc = w["weather"][0]["description"].title()
            weather_str = f"{temp:.0f}°F {desc}"
            weather_desc = desc
        else:
            weather_str = "Weather API failed"
    except:
        weather_str = "Weather fetch error"

    # 2. Real market - S&P 500 (SPY ETF) via Alpha Vantage free endpoint
    market_str = "Market unavailable"
    try:
        market_url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=SPY"
        m = requests.get(market_url, timeout=10).json()
        quote = m.get("Global Quote", {})
        if quote:
            price = quote.get("05. price", "N/A")
            change_pct = quote.get("10. change percent", "N/A")
            sign = "🟩" if float(change_pct.strip("%") or 0) >= 0 else "🟥"
            market_str = f"SPY ${price} ({sign}{change_pct})"
    except:
        market_str = "Market fetch error"

    # 3. Real current time in CST
    cst = pytz.timezone("America/Chicago")
    current_time = datetime.now(cst).strftime("%I:%M %p %Z")  # e.g. "11:42 AM CST"

    # 4. Random fun fact from free API
    fact_str = "Fact unavailable"
    try:
        fact_url = "https://uselessfacts.jsph.pl/random.json?language=en"
        f = requests.get(fact_url, timeout=5).json()
        fact_str = f.get("text", "No fact available")
    except:
        fact_str = "Octopuses have three hearts (fallback)"

    return {
        "weather": weather_str,
        "weather-desc": weather_desc,
        "market": market_str,
        "time": current_time,
        "fact": fact_str
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
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
