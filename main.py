from fastapi import FastAPI
import requests

app = FastAPI()

# 1. LANDINGSPAGINA & HEALTH CHECK
@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {
        "api_name": "Germany Energy & Fuel Pro API",
        "status": "operational",
        "region": "Germany (DE)",
        "vat_rate": "19% (Standard)",
        "endpoints": ["/strom", "/erdgas", "/kraftstoff"]
    }

# 2. STROOM (Live EPEX Spot Marktdata)
@app.get("/strom")
def get_strom():
    try:
        r = requests.get("https://api.awattar.de/v1/marketdata", timeout=5).json()
        market_price_mwh = r['data'][0]['marketprice']
        
        # Berekening per kWh
        price_kwh_net = round(market_price_mwh / 1000, 4)
        vat_amount = round(price_kwh_net * 0.19, 4)
        total_price = round(price_kwh_net + vat_amount, 4)
        
        return {
            "commodity": "Electricity",
            "market": "EPEX Spot DE/LU",
            "unit": "kWh",
            "currency": "EUR",
            "pricing": {
                "net_market_price": price_kwh_net,
                "vat_19": vat_amount,
                "total_inc_vat": total_price
            },
            "info": "Excludes grid fees, renewable levies, and local taxes."
        }
    except:
        return {"error": "External power market source unavailable"}

# 3. ERDGAS (Met 10.55 factor en CO2-belasting)
@app.get("/erdgas")
def get_gas():
    # Marktmodel gebaseerd op Duitse THE (Trading Hub Europe) standaarden
    base_market_kwh = 0.0390   # Marktprijs
    co2_tax = 0.0082           # BEHG CO2-Tax 2024/2025
    grid_fees = 0.0210         # Netznutzungsentgelte
    
    net_kwh = base_market_kwh + co2_tax + grid_fees
    total_kwh_vat = round(net_kwh * 1.19, 4)
    
    # De cruciale conversie naar m3 (H-Gas standaard factor 10.55)
    price_per_m3 = round(total_kwh_vat * 10.55, 4)

    return {
        "commodity": "Natural Gas (H-Gas)",
        "unit": "m3",
        "conversion_factor": "10.55 kWh/m3",
        "currency": "EUR",
        "total_price_m3": price_per_m3,
        "transparency_breakdown_per_kwh": {
            "net_market_price": base_market_kwh,
            "co2_tax_de": co2_tax,
            "grid_fees": grid_fees,
            "vat_19_percent": "Included"
        }
    }

# 4. KRAFTSTOFF (Inclusief HVO100 en LPG)
@app.get("/kraftstoff")
def get_fuel():
    # Actuele afgeronde retailprijzen Duitsland (inclusief alle belastingen)
    return {
        "commodity": "Motor Fuel",
        "region": "Germany",
        "unit": "Liter",
        "currency": "EUR",
        "prices": {
            "Super_E5": 1.829,
            "Super_E10": 1.769,
            "Diesel": 1.689,
            "HVO100": 1.859,
            "LPG_Autogas": 1.049
        },
        "tax_status": "All-in (Includes 19% VAT, Energy Tax, and CO2-Price)"
    }
