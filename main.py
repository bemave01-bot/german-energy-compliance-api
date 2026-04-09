from fastapi import FastAPI
import requests

app = FastAPI()

# Deze regel zorgt ervoor dat Render ziet dat je API 'Leeft'
@app.get("/")
def home():
    return {"status": "Online", "message": "Duitse Energie API"}

@app.get("/strom")
def strom():
    r = requests.get("https://api.awattar.de/v1/marketdata").json()
    return {"elektriciteit_eur_kwh": round(r['data'][0]['marketprice'] / 1000, 4)}

@app.get("/erdgas")
def gas():
    # Simpele versie waar je nu naar keek
    return {"prijs_gas_m3": 0.8842}

@app.get("/kraftstoff")
def fuel():
    return {"diesel": 1.669, "super_e10": 1.749}
