from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Duitsland API Online"}

@app.get("/strom")
def get_strom():
    try:
        r = requests.get("https://api.awattar.de/v1/marketdata").json()
        price = (r['data'][0]['marketprice'] / 1000) * 1.19
        return {"prijs_kwh_de": round(price, 4)}
    except:
        return {"error": "Awwattar API onbereikbaar"}

@app.get("/erdgas")
def get_gas():
    return {"prijs_gas_de": 0.8842}

@app.get("/kraftstoff")
def get_fuel():
    return {
        "country": "Germany",
        "currency": "EUR",
        "unit": "liter",
        "prices": {
            "Super_E10": 1.749,
            "Super_E5": 1.809,
            "Diesel": 1.669,
            "HVO100": 1.849,
            "Autogas_LPG": 1.029
        }
    }
