from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "online", "region": "Germany"}

@app.get("/strom")
def get_strom():
    try:
        r = requests.get("https://api.awattar.de/v1/marketdata").json()
        price = (r['data'][0]['marketprice'] / 1000) * 1.19
        return {"country": "Germany", "unit": "kWh", "price": round(price, 4)}
    except:
        return {"error": "API error"}

@app.get("/erdgas")
def get_gas():
    return {"country": "Germany", "unit": "m3", "price": 0.8842}

@app.get("/kraftstoff")
def get_fuel():
    return {
        "country": "Germany",
        "prices": {"Super_E10": 1.749, "Super_E5": 1.809, "Diesel": 1.669}
    }
