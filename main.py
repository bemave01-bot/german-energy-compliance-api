from fastapi import FastAPI
import requests
from datetime import datetime

app = FastAPI()

# Hulpfunctie voor tijdstempel
def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S CET")

# 1. LANDING & COMPLIANCE STATUS
@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {
        "api_name": "Germany ESG & Energy Compliance Interface",
        "compliance_standards": ["CSRD-ready", "EU Taxonomy", "Scope 1-2 Reporting"],
        "jurisdiction": "European Union / Germany",
        "status": "Operational",
        "timestamp": get_now()
    }

# 2. CSRD EMISSIEFACTOREN (Scope 1 & 2)
@app.get("/compliance/emissions")
def get_emission_factors():
    return {
        "description": "Standard Emission Factors for CSRD Reporting (DE)",
        "unit": "kg CO2e",
        "scope_1_direct": {
            "natural_gas_m3": 2.01,
            "diesel_liter": 2.67,
            "super_e5_liter": 2.31,
            "lpg_liter": 1.61,
            "hvo100_liter": 0.25
        },
        "scope_2_indirect": {
            "electricity_kwh_de_grid_avg": 0.380, 
            "note": "Based on German Energy Mix 2025"
        }
    }

# 3. HISTORISCHE BENCHMARKS
@app.get("/compliance/history")
def get_historical_benchmarks():
    return {
        "historical_averages_germany": {
            "2024": {
                "electricity_mwh_avg": 67.20,
                "gas_mwh_avg": 34.50,
                "diesel_avg_liter": 1.72,
                "co2_price_tonne": 45.00
            },
            "2025": {
                "electricity_mwh_avg": 72.10,
                "gas_mwh_avg": 38.10,
                "diesel_avg_liter": 1.68,
                "co2_price_tonne": 55.00
            }
        },
        "data_source": "Statistisches Bundesamt / Federal Network Agency"
    }

# 4. STROOM (Live + History Trend)
@app.get("/strom")
def get_strom():
    try:
        r = requests.get("https://api.awattar.de/v1/marketdata", timeout=5).json()
        market_price_mwh = r['data'][0]['marketprice']
        net_kwh = round(market_price_mwh / 1000, 4)
        return {
            "commodity": "Electricity",
            "market": "EPEX Spot DE/LU",
            "pricing": {"net": net_kwh, "inc_vat": round(net_kwh * 1.19, 4)},
            "scope_2_intensity": "0.380 kg CO2e/kWh",
            "timestamp": get_now()
        }
    except:
        return {"error": "Source temporary unavailable"}

# 5. ERDGAS (Compliance Model)
@app.get("/erdgas")
def get_gas():
    base_market = 0.0390
    co2_tax = 0.0082
    grid_fees = 0.0210
    total_kwh = round((base_market + co2_tax + grid_fees) * 1.19, 4)
    return {
        "commodity": "Natural Gas",
        "standard": "DIN EN 437 (H-Gas)",
        "units": {
            "price_per_kwh_inc_vat": total_kwh,
            "total_price_per_m3": round(total_kwh * 10.55, 4),
            "currency": "EUR"
        },
        "compliance": "CSRD Scope 1 Ready",
        "timestamp": get_now()
    }

# 6. KRAFTSTOFF (Brandstof)
@app.get("/kraftstoff")
def get_fuel():
    return {
        "commodity": "Motor Fuel",
        "prices": {
            "Diesel": 1.689,
            "HVO100": 1.859,
            "Super_E10": 1.769,
            "LPG": 1.049
        },
        "legal_notice": "Includes German Energy Tax and 19% VAT.",
        "timestamp": get_now()
    }
