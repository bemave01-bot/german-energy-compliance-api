@app.get("/transport/fuel-prices")
async def get_fuel_prices():
    # Deze data wordt idealiter gevoed door je scraping-functie
    return {
        "liquids": {
            "diesel_b7": {"price": 1.749, "unit": "EUR/L", "co2_kg": 2.64},
            "hvo100": {"price": 2.155, "unit": "EUR/L", "co2_kg": 0.25},
            "benzine_e5": {"price": 1.899, "unit": "EUR/L", "co2_kg": 2.39},
            "benzine_e10": {"price": 1.839, "unit": "EUR/L", "co2_kg": 2.31},
            "lpg_autogas": {"price": 0.725, "unit": "EUR/L", "co2_kg": 1.61},
            "adblue": {"price": 0.842, "unit": "EUR/L", "note": "Market average"}
        },
        "tax_info": {
            "germany_behg_2026": "Included in pump price",
            "co2_price_per_tonne": 55.00
        },
        "metadata": {
            "source": "Market Data Aggregator / Bundeskartellamt MTS-K",
            "last_updated": datetime.now().isoformat()
        }
    }
