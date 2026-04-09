from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "api_name": "Germany Energy & Fuel Pro API",
        "status": "operational",
        "endpoints": ["/strom", "/erdgas", "/kraftstoff"]
    }

@app.get("/strom")
def get_strom():
    try:
        r = requests.get("https://api.awattar.de/v1/marketdata").json()
        market_price_mwh = r['data'][0]['marketprice']
        price_kwh_ex_vat = round(market_price_mwh / 1000, 4)
        vat_rate = 0.19
        total_price = round(price_kwh_ex_vat * (1 + vat_rate), 4)
        return {
            "country": "Germany",
            "unit": "kWh",
            "market_price_net": price_kwh_ex_vat,
            "total_price_inc_vat": total_price,
            "vat_rate": "19%",
            "info": "EPEX Spot Day-Ahead"
        }
    except:
        return {"error": "Source unavailable"}

@app.get("/erdgas")
def get_gas():
    # THE Spot Market based calculation
    base_market_kwh = 0.0382
    fees_and_co2 = 0.0332
    total_kwh_inc_vat = round((base_market_kwh + fees_and_co2) * 1.19, 4)
    price_per_m3 = round(total_kwh_inc_vat * 10.55, 4)
    return {
        "country": "Germany",
        "unit": "m3",
        "price_all_in": price_per_m3,
        "details": {
            "price_per_kwh": total_kwh_inc_vat,
            "conversion_factor": "10.55 kWh/m3",
            "vat_rate": "19%",
            "components": ["Market Price", "CO2 Tax", "Grid Fees"]
        }
    }

@app.get("/kraftstoff")
def get_fuel():
    return {
        "country": "Germany",
        "unit": "liter",
        "prices": {
            "Super_E10": 1.749,
            "Super_E5": 1.809,
            "Diesel": 1.669,
            "HVO100": 1.849,
            "Autogas_LPG": 1.029
        },
        "tax_status": "Included",
        "note": "Prices include Mineralölsteuer and 19% VAT."
    }
