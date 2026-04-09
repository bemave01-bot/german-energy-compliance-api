from fastapi import FastAPI
import requests
from datetime import datetime

app = FastAPI()

def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S CET")

@app.get("/")
def csrd_compliance_root():
    return {
        "api_name": "Germany ESG & Energy Compliance Interface",
        "compliance_standards": ["CSRD-ready", "EU Taxonomy", "Scope 1-2 Reporting"],
        "jurisdiction": "European Union / Germany",
        "reporting_year": "2026",
        "status": "Audit-Ready"
    }

@app.get("/compliance/emissions")
def get_emission_factors():
    # Officiële CO2-emissiefactoren (gemiddelden voor rapportage)
    return {
        "description": "Standard Emission Factors for CSRD Reporting (DE)",
        "unit": "kg CO2e",
        "scope_1_direct": {
            "natural_gas_m3": 2.01,
            "diesel_liter": 2.67,
            "super_e5_liter": 2.31,
            "lpg_liter": 1.61,
            "hvo100_liter": 0.25  # HVO100 heeft een enorme reductie!
        },
        "scope_2_indirect": {
            "electricity_kwh_de_grid_avg": 0.380, 
            "note": "Based on German Energy Mix 2025"
        }
    }

@app.get("/compliance/history")
def get_historical_benchmarks():
    # Historische data voor accountantsvergelijkingen
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

@app.get("/strom")
def get_strom_pro():
    # Live data inclusief Carbon Intensity voor Scope 2
    r = requests.get("https://api.awattar.de/v1/marketdata").json()
    net_price = round(r['data'][0]['marketprice'] / 1000, 4)
    return {
        "commodity": "Electricity",
        "market": "EPEX Spot DE/LU",
        "current_pricing_kwh": {"net": net_price, "inc_vat": round(net_price * 1.19, 4)},
        "scope_2_intensity": "0.380 kg CO2e/kWh",
        "timestamp": get_now()
    }

# (De andere endpoints /erdgas en /kraftstoff blijven zoals ze waren, maar voeg get_now() toe)
