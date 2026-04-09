from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Compliance Data API 2026 - Deutschland Edition")

# --- STATISCHE DATEN (Jährliche Wartung) ---
MAUT_TABELLE_2026 = {
    ">18t": {1: 0.348, 2: 0.302, 3: 0.250, 4: 0.150, 5: 0.087},
    "12-18t": {1: 0.238, 2: 0.200, 3: 0.160, 4: 0.100, 5: 0.059},
    "3.5-7.5t": {1: 0.151, 2: 0.120, 3: 0.090, 4: 0.050, 5: 0.000}
}

CO2_FAKTOREN = {
    "diesel_b7": 2.64,
    "hvo100": 0.25,
    "benzin_e5": 2.39,
    "benzin_e10": 2.31,
    "lpg_autogas": 1.61,
    "erdgas": 1.88,
    "strom_mix": 0.35
}

# --- ABSCHNITT 1: TRANSPORT & LOGISTIK API ---

@app.get("/transport/kraftstoff-preise")
async def get_fuel_prices():
    return {
        "kraftstoffe": {
            "diesel_b7": {"preis": 1.749, "einheit": "EUR/L", "co2_kg": CO2_FAKTOREN["diesel_b7"]},
            "hvo100": {"preis": 2.155, "einheit": "EUR/L", "co2_kg": CO2_FAKTOREN["hvo100"]},
            "benzin_e5": {"preis": 1.899, "einheit": "EUR/L", "co2_kg": CO2_FAKTOREN["benzin_e5"]},
            "benzin_e10": {"preis": 1.839, "einheit": "EUR/L", "co2_kg": CO2_FAKTOREN["benzin_e10"]},
            "lpg_autogas": {"preis": 0.725, "einheit": "EUR/L", "co2_kg": CO2_FAKTOREN["lpg_autogas"]},
            "adblue": {"preis": 0.842, "einheit": "EUR/L", "hinweis": "Marktdurchschnitt"}
        },
        "steuer_info": {
            "deutschland_behg_2026": "Inklusive",
            "co2_preis_pro_tonne": 55.00
        },
        "metadaten": {
            "quelle": "Marktdaten-Aggregator / MTS-K",
            "letzte_aktualisierung": datetime.now().isoformat()
        }
    }

@app.get("/transport/maut-rechner")
async def calculate_maut(entfernung_km: float, gewichtsklasse: str, co2_klasse: int):
    # Logik für den Maut-Rechner
    tarif = MAUT_TABELLE_2026.get(gewichtsklasse, {}).get(co2_class, 0.348)
    gesamtkosten = entfernung_km * tarif
    return {
        "berechnung": {
            "entfernung": f"{entfernung_km} km",
            "gewichtsklasse": gewichtsklasse,
            "co2_emissionsklasse": co2_klasse,
            "tarif_pro_km": tarif,
            "maut_gesamtkosten": round(gesamtkosten, 2)
        },
        "compliance": {
            "gesetz": "Bundesfernstraßenmautgesetz (BFStrMG) 2026",
            "zeitstempel": datetime.now().isoformat()
        }
    }

# --- ABSCHNITT 2: ENERGIE API ---

@app.get("/energie/markt-preise")
async def get_energy_rates():
    return {
        "strom": {"preis": 0.115, "einheit": "EUR/kWh", "co2_kg": CO2_FAKTOREN["strom_mix"]},
        "erdgas": {"preis": 0.38, "unit": "EUR/m3", "co2_kg": CO2_FAKTOREN["erdgas"]},
        "metadaten": {"quelle": "EPEX Spot / TTF Hub"}
    }

@app.get("/")
async def root():
    return {"status": "online", "nachricht": "Compliance-Daten-API ist betriebsbereit"}
