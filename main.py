<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Dashboard</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <style>
    body { background: rgb(15,23,42); color: white; font-family: system-ui, sans-serif; }
    .card { 
      background: rgb(30,41,59); 
      border-radius: 1.5rem; 
      padding: 2rem; 
      box-shadow: 0 15px 30px rgba(0,0,0,0.6); 
      transition: all 0.3s ease; 
      border: 1px solid rgb(71,85,105); 
    }
    .card:hover { transform: translateY(-8px); box-shadow: 0 25px 50px rgba(0,0,0,0.7); }
    .icon { font-size: 3.5rem; margin-bottom: 1rem; }
    .title { font-size: 1.5rem; font-weight: bold; margin-bottom: 0.75rem; }
    .value { font-size: 3.5rem; font-weight: 700; }
    .sub { font-size: 1.25rem; opacity: 0.8; }
    .refresh { font-size: 0.9rem; color: rgb(148,163,184); }
  </style>
</head>
<body class="min-h-screen flex items-center justify-center p-8">
  <div class="max-w-6xl w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">

    <div class="card">
      <div class="icon">🌤️</div>
      <div class="title text-cyan-300">Weather</div>
      <div id="weather" class="value">--</div>
      <div id="weather-desc" class="sub">--</div>
    </div>

    <div class="card">
      <div class="icon">📈</div>
      <div class="title text-green-300">Market</div>
      <div id="market" class="value">--</div>
    </div>

    <div class="card">
      <div class="icon">🕒</div>
      <div class="title text-purple-300">Time</div>
      <div id="time" class="value">--</div>
    </div>

    <div class="card">
      <div class="icon">💡</div>
      <div class="title text-yellow-300">Fact</div>
      <div id="fact" class="value text-xl leading-relaxed">--</div>
    </div>

  </div>

  <div class="fixed bottom-6 right-6 text-right refresh">
    <p>Last updated: <span id="last-update">--</span></p>
    <p>Auto-refresh every 60s</p>
  </div>

  <script>
    async function updateDashboard() {
      try {
        const res = await fetch('/dashboard');
        const data = await res.json();
        document.getElementById("weather").textContent = data.weather || "--";
        document.getElementById("weather-desc").textContent = data["weather-desc"] || "";
        document.getElementById("market").textContent = data.market || "--";
        document.getElementById("time").textContent = data.time || "--";
        document.getElementById("fact").textContent = data.fact || "--";
        document.getElementById("last-update").textContent = new Date().toLocaleTimeString();
      } catch (err) {
        console.error(err);
        document.getElementById("last-update").textContent = "Fetch error";
      }
    }
    updateDashboard();
    setInterval(updateDashboard, 60000);
  </script>
</body>
</html>
