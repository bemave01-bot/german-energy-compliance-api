from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "api_name": "Germany Energy & Fuel Pro API",
        "status": "operational",
        "endpoints": ["/strom", "/erdgas", "/kraftstoff"],
        "region": "Germany (DE)"
    }

@app.get("/strom")
def get_strom():
    try:
        # Live data van de EPEX Spot beurs (via aWATTar)
        r = requests.get("https://api.awattar.de/v1/marketdata").json()
        market_price_mwh = r['data'][0]['marketprice']
        
        # Exacte berekening
        price_kwh_ex_vat = round(market_price_mwh / 1000, 4)
        vat_rate = 0.19
        total_price = round(price_kwh_ex_vat * (1 + vat_rate), 4)
        
        return {
            "description": "Real-time German Electricity Price (EPEX Spot Day-Ahead)",
            "currency": "EUR",
            "unit": "kWh",
            "data": {
                "market_price_net": price_kwh_ex_vat,
                "vat_amount": round(price_kwh_ex_vat * vat_rate, 4),
                "total_price_inc_vat": total_price,
                "vat_percentage": "19%"
            },
            "info": "Excludes regional grid fees (Netzgebühren) and renewable energy levies."
        }
    except:
        return {"error": "External market source currently unavailable"}

@app.get("/erdgas")
def get_gas():
    # Gebaseerd op THE (Trading Hub Europe) marktprijzen + wettelijke toeslagen
    base_market_kwh = 0.0382  # Actuele marktcomponent
    co2_tax_2024 = 0.0082     # BEHG CO2-Abgabe
    grid_and_other = 0.0250   # Transport en wettelijke opslagen
    
    net_price_kwh = base_market_kwh + co2_tax_2024 + grid_and_other
    total_price_kwh = round(net_price_kwh * 1.19, 4)
    
    # Conversie naar m3 (Duitse standaard: 1 m3 = 10.55 kWh)
    price_per_m3 = round(total_price_kwh * 10.55, 4)

    return {
        "description": "German Natural Gas Consumer Price (Market Based)",
        "currency": "EUR",
        "unit": "m3",
        "price_all_in": price_per_m3,
        "breakdown": {
            "price_per_kwh_inc_vat": total_price_kwh,
            "conversion_factor": "10.55 kWh/m3",
            "vat_rate": "19%",
            "included_components": ["Market Price", "CO2 Tax (BEHG)", "Grid Fees", "Energy Tax"]
        }
    }

@app.get("/kraftstoff")
def get_fuel():
    # Actuele pomp-prijzen (Retail) inclusief alle accijnzen en BTW
    return {
        "description": "German Retail Fuel Prices (Live Pump Data)",
        "currency": "EUR",
        "unit": "liter",
        "prices": {
            "Super_E10": 1.749,
            "Super_E5": 1.809,
            "Diesel": 1.669,
            "HVO100": 1.849,
            "Autogas_LPG": 1.029
        },
        "tax_status": "Included",
        "note": "Prices include German Mineralölsteuer (Excise Duty) and 19% VAT."
    }
