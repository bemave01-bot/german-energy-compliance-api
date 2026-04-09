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
        r = requests.get("https://api.awattar.de/v1/marketdata", timeout=5).json()
        market_price_mwh = r['data'][0]['marketprice']
        # Omrekening naar kWh en 19% BTW
        price_kwh_net = round(market_price_mwh / 1000, 4)
        total_price = round(price_kwh_net * 1.19, 4)
        return {
            "country": "Germany",
            "unit": "kWh",
            "market_price_net": price_kwh_net,
            "total_price_inc_vat": total_price,
            "vat_rate": "19%",
            "info": "EPEX Spot Day-Ahead Market"
        }
    except Exception:
        return {"error": "External market data currently unavailable"}

@app.get("/erdgas")
def get_gas():
    # THE Spot Market based calculation (Pro-level transparency)
    base_market_kwh = 0.0382
    co2_tax = 0.0082
    grid_fees = 0.0250
    
    net_price_kwh = base_market_kwh + co2_tax + grid_fees
    total_price_kwh = round(net_price_kwh * 1.19, 4)
    # Conversie naar m3 (Duitse standaard 10.55)
    price_per_m3 = round(total_price_kwh * 10.55, 4)
    
    return {
        "country": "Germany",
        "unit": "m3",
        "price_all_in": price_per_m3,
        "details": {
            "price_per_kwh": total_price_kwh,
            "conversion_factor": "10.55 kWh/m3",
            "vat_rate": "19%",
            "components": ["Market Price", "CO2 Tax (BEHG)", "Grid Fees"]
        }
    }

@app.get("/kraftstoff")
def get_fuel():
    return {
        "country": "Germany",
        "unit": "liter",
        "currency": "EUR",
        "prices": {
            "Super_E10": 1.749,
            "Super_E5": 1.809,
            "Diesel": 1.669,
            "HVO100": 1.849,
            "Autogas_LPG": 1.029
        },
        "tax_status": "Included",
        "note": "Retail pump prices including 19% VAT and energy taxes."
    }
