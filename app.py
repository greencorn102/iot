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
