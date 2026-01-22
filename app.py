from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

LOW_THRESHOLD = 10
HIGH_THRESHOLD = 35

latest_temp = None

class TempData(BaseModel):
    temperature: float

@app.post("/temperature")
def receive_temperature(data: TempData):
    global latest_temp
    latest_temp = data.temperature
    return {"status": "received"}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <h1>Temperature Dashboard</h1>
    <h2 id="temp">Loading...</h2>
    <h3 id="msg"></h3>

    <script>
    async function fetchTemp() {
        const res = await fetch('/latest');
        const data = await res.json();

        if (data.temperature === null) {
            document.getElementById("temp").innerText = "No data yet";
            return;
        }

        document.getElementById("temp").innerText =
            "Current Temperature: " + data.temperature + " °C";

        let msg = "Temperature normal";

        if (data.temperature < 10) msg = "⚠️ Temperature too LOW!";
        else if (data.temperature > 35) msg = "🔥 Temperature too HIGH!";

        document.getElementById("msg").innerText = msg;
    }

    setInterval(fetchTemp, 3000); // every 3 seconds
    fetchTemp();
    </script>
    """

"""
@app.get("/", response_class=HTMLResponse)
def dashboard():
    if latest_temp is None:
        return "<h2>No data yet</h2>"

    message = "Temperature is normal"

    if latest_temp < LOW_THRESHOLD:
        message = "⚠️ Temperature too LOW!"
    elif latest_temp > HIGH_THRESHOLD:
        message = "🔥 Temperature too HIGH!"

    return f"""
    <h1>Temperature Dashboard</h1>
    <h2>Current Temperature: {latest_temp} °C</h2>
    <h3>{message}</h3>
    """
"""
