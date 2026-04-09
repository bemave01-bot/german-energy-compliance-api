from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Germany Energy API Online", "endpoints": ["/strom", "/erdgas", "/kraftstoff"]}

@app.get("/strom")
def get_strom():
    try:
        r = requests.get("https://api.awattar.de/v1/marketdata").json()
        price_kwh = round(r['data'][0]['marketprice'] / 1000, 4)
        return {
            "unit": "kWh",
            "market_price_net": price_kwh,
            "total_inc_vat": round(price_kwh * 1.19, 4),
            "vat": "19%"
        }
    except:
        return {"error": "Source offline"}

@app.get("/erdgas")
def get_gas():
    # Vastgestelde professionele berekening (Markt + Tax + Grid)
    price_kwh = 0.1030  # All-in prijs incl 19% BTW
    return {
        "unit": "m3",
        "price_all_in": round(price_kwh * 10.55, 4),
        "details": {"price_per_kwh": price_kwh, "vat": "19%"}
    }

@app.get("/kraftstoff")
def get_fuel():
    return {
        "unit": "liter",
        "prices": {
            "Super_E10": 1.749, "Super_E5": 1.809, "Diesel": 1.669, "HVO100": 1.849, "LPG": 1.029
        }
    }
