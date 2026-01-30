from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>My Dashboard</title>
      <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
      <style>
        body { background: #0f172a; color: white; font-family: system-ui, sans-serif; }
        .card { background: #1e293b; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4); transition: transform 0.2s; }
        .card:hover { transform: translateY(-4px); }
        .refresh { font-size: 0.875rem; color: #94a3b8; }
      </style>
    </head>
    <body class="min-h-screen flex items-center justify-center p-6">
      <div class="max-w-5xl w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

        <div class="card col-span-1 md:col-span-2 lg:col-span-1">
          <h2 class="text-xl font-bold mb-2 text-cyan-400">Weather</h2>
          <p id="weather" class="text-4xl font-semibold">--</p>
          <p class="text-lg mt-1" id="weather-desc">--</p>
        </div>

        <div class="card">
          <h2 class="text-xl font-bold mb-2 text-green-400">Market</h2>
          <p id="market" class="text-5xl font-bold">--</p>
        </div>

        <div class="card">
          <h2 class="text-xl font-bold mb-2 text-purple-400">Time</h2>
          <p id="time" class="text-5xl font-mono font-bold">--</p>
        </div>

        <div class="card col-span-1 md:col-span-2 lg:col-span-1">
          <h2 class="text-xl font-bold mb-2 text-yellow-400">Random Fact</h2>
          <p id="fact" class="text-xl italic">--</p>
        </div>

      </div>

      <div class="fixed bottom-4 right-4 text-right refresh">
        <p>Last updated: <span id="last-update">--</span></p>
        <p>Auto-refresh every 60s</p>
      </div>

      <script>
        async function updateDashboard() {
          try {
            const res = await fetch('/dashboard');
            const data = await res.json();
            document.getElementById("weather").textContent = data.weather || "--";
            document.getElementById("market").textContent = data.market || "--";
            document.getElementById("time").textContent = data.time || "--";
            document.getElementById("fact").textContent = data.fact || "--";
            document.getElementById("last-update").textContent = new Date().toLocaleTimeString();
          } catch (err) {
            console.error(err);
            document.getElementById("last-update").textContent = "Error";
          }
        }
        updateDashboard();
        setInterval(updateDashboard, 60000);
      </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/dashboard")
def dashboard():
    # Real weather for La Porte, TX (coords you requested)
    api_key = "PASTE_YOUR_OPENWEATHERMAP_API_KEY_HERE"  # Replace this with your actual key
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
            weather_desc = desc  # Extra for the sub-line if you want it
    except:
        weather_str = "Weather error"
        weather_desc = ""

    return {
        "weather": weather_str,
        "weather-desc": weather_desc,  # This populates the smaller text under weather if present
        "market": "🟩 Bullish (static)",
        "time": "Live",
        "fact": "Octopuses have three hearts"
    }
