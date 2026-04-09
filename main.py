from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Duitsland API Online"}

@app.get("/strom")
def get_strom():
    r = requests.get("https://api.awattar.de/v1/marketdata").json()
    price = (r['data'][0]['marketprice'] / 1000) * 1.19
    return {"prijs_kwh_de": round(price, 4)}

@app.get("/erdgas")
def get_gas():
    return {"prijs_gas_de": 0.8842}

@app.get("/kraftstoff")
def get_fuel():
    return {"diesel": 1.669, "e10": 1.749, "e5": 1.809}
