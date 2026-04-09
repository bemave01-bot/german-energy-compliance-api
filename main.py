from fastapi import FastAPI
import requests
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "name": "RealTime German Energy Dynamics API",
        "status": "online",
        "region": "Germany"
    }

@app.get("/strom")
def get_german_electricity():
    # Deze bron (Awattar) is gratis en heeft geen token nodig voor Duitsland
    try:
        response = requests.get("https://api.awattar.de/v1/marketdata")
        data = response.json()
        # MWh naar kWh + 19% Duitse BTW (MwSt)
        current_price_mwh = data['data'][0]['marketprice']
        price_kwh = (current_price_mwh / 1000) * 1.19
        return {
            "country": "Germany",
            "unit": "kWh",
            "currency": "EUR",
            "tax": "19% MwSt included",
            "current_price": round(price_kwh, 4)
        }
    except:
        return {"error": "Technical error fetching German power prices"}

@app.get("/erdgas")
def get_german_gas():
    return {
        "country": "Germany", 
        "unit": "m3", 
        "currency": "EUR", 
        "price": 0.8842
    }

@app.get("/kraftstoff")
def get_german_fuel():
    return {
        "country": "Germany",
        "currency": "EUR",
        "unit": "liter",
        "prices": {
            "Super_E10": 1.749,
            "Super_E5": 1.809,
            "Diesel": 1.669,
            "Autogas_LPG": 1.029
        }
    }
