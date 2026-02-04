from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()



latest_motion = None

class MotionData(BaseModel):
    motion: int

@app.post("/motion")
def receive_motion(data: MotionData):
    global latest_motion
    latest_motion = data.motion
    return {"status": "received"}

@app.get("/latest")
def get_latest():
    return {"motion": latest_motion}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <h1>Motion Dashboard</h1>
    <h2 id="motion">Sensing...</h2>
    <h3 id="msg"></h3>

    <script>
    async function fetchTemp() {
        const res = await fetch('/latest');
        const data = await res.json();

        if (data.motion === null) {
            document.getElementById("motion").innerText = "* *";
            document.getElementById("msg").innerText = "";
            return;
        }

        document.getElementById("motion").innerText = data.motion;

        let msg;
        if (data.motion == 1)
            msg = "MOTION DETECTED !!";
        else
            msg = "NO MOTION";

        document.getElementById("msg").innerText = msg;
    }

    setInterval(fetchTemp, 3000);
    fetchTemp();
    </script>
    """
"""
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return 
    <h1>Motion Dashboard</h1>
    <h2 id="motion">Sensing...</h2>
    <h3 id="msg"></h3>

    <script>
    async function fetchMotion() {
        const res = await fetch('/latest');
        const data = await res.json();

        if (data.motion === null) {
            document.getElementById("motion").innerText = "* *";
            return;
        }



        if (data.motion == 1) msg = "MOTION DETECTED !!";
        else msg = "* * *";

        document.getElementById("msg").innerText = msg;
    }

    setInterval(fetchMotion, 3000); // every 3 seconds
    fetchMotion();
    </script>
    """
    









