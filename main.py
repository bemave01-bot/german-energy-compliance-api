from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="German Energy Compliance API 2026")

@app.get("/energie/compliance-check")
async def energy_compliance(kwh_verbruik: float = 1.0):
    # Harde cijfers 2026 (BNetzA & Fiscale wetgeving)
    netto_markt_avg = 0.1182
    netz_arbeitspreis = 0.1034  # BNetzA 2026
    stromsteuer = 0.0205
    grundpreis_jahr = 145.20
    
    netto_totaal = netto_markt_avg + netz_arbeitspreis + stromsteuer
    btw = netto_totaal * 0.19
    bruto_totaal = netto_totaal + btw

    return {
        "fiskal_data": {
            "currency": "EUR",
            "netto_pro_kwh": round(netto_totaal, 4),
            "bruto_pro_kwh": round(bruto_totaal, 4),
            "mwst_19_procent": round(btw, 4),
            "jaar_vastrecht_netto": grundpreis_jahr
        },
        "solar_compliance": {
            "einspeiseverguetung_2026": 0.0778,
            "status": "EEG_READY",
            "recommendation": "STROM_EIGENVERBRAUCH_OPTIMAL"
        },
        "co2_reporting": {
            "co2_kg_kwh": 0.35,
            "scope": "Scope 2 (Indirect)",
            "method": "BNetzA / UBA Standard 2026"
        },
        "info": "Values for Germany 2026 / Accountant Ready"
    }
