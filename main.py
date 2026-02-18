# AI-overlay
AI backend for MT5 overlay
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()

# Store latest prediction globally for dashboard
latest_prediction = {
    "symbol": "",
    "prediction": "",
    "confidence": 0,
    "entry": 0,
    "stop_loss": 0,
    "take_profit": 0,
    "timestamp": ""
}

# Request format from MT5
class Candle(BaseModel):
    symbol: str
    data: list  # list of candles [{"open":..., "high":..., "low":..., "close":...}, ...]

@app.post("/predict")
async def predict(candle: Candle):
    global latest_prediction

    # --- AI logic (placeholder demo) ---
    trend = random.choice(["up", "down", "neutral"])
    confidence = round(random.uniform(0.6, 0.95) * 100, 2)

    # Last close price as base for calculations
    last_close = candle.data[-1]["close"] if candle.data else 1.0

    # Simple TP/SL calculation
    if trend == "up":
        entry = last_close
        stop_loss = round(last_close * 0.998, 5)  # 0.2% below
        take_profit = round(last_close * 1.004, 5)  # 0.4% above
    elif trend == "down":
        entry = last_close
        stop_loss = round(last_close * 1.002, 5)  # 0.2% above
        take_profit = round(last_close * 0.996, 5)  # 0.4% below
    else:
        entry = stop_loss = take_profit = last_close

    latest_prediction = {
        "symbol": candle.symbol,
        "prediction": trend,
        "confidence": confidence,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return latest_prediction

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    trend_class = latest_prediction['prediction']
    html_content = f"""
    <html>
    <head>
        <title>Forex AI Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #0f0f1a;
                color: #eee;
                text-align: center;
                padding-top: 60px;
            }}
            .card {{
                background: #1b1b2a;
                margin: auto;
                padding: 30px;
                border-radius: 12px;
                width: 350px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
            }}
            h1 {{ color: #9f6eff; }}
            .up {{ color: #00ff88; }}
            .down {{ color: #ff4d4d; }}
            .neutral {{ color: #ffd700; }}
            .timestamp {{ font-size: 12px; color: #aaa; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>AI Prediction</h1>
            <h2>{latest_prediction['symbol']}</h2>
            <h3 class="{trend_class}">
                {latest_prediction['prediction'].upper() if latest_prediction['prediction'] else "No Data Yet"}
            </h3>
            <p>Confidence: {latest_prediction['confidence']}%</p>
            <p>Entry: {latest_prediction['entry']}</p>
            <p>Stop Loss: {latest_prediction['stop_loss']}</p>
            <p>Take Profit: {latest_prediction['take_profit']}</p>
            <div class="timestamp">Updated: {latest_prediction['timestamp']}</div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

