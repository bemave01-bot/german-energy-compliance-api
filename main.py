from fastapi import FastAPI
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

app = FastAPI()

# PLAK HIERONDER JE TOKEN (Hetzelfde als voor NL)
ENTSOE_TOKEN = "HIER_JE_TOKEN_PLAKKEN"

@app.get("/")
def read_root():
    return {
        "name": "RealTime German Energy Dynamics API",
        "status": "online",
        "region": "Germany"
    }

@app.get("/strom")
def get_german_electricity():
    # Area Code voor Duitsland/Luxemburg: 10Y1001A1001A82H
    start = datetime.now().strftime("%Y%m%d0000")
    end = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d2300")
    url = f"https://web-api.tp.entsoe.eu/api?documentType=A44&in_Domain=10Y1001A1001A82H&out_Domain=10Y1001A1001A82H&periodStart={start}&periodEnd={end}&securityToken={ENTSOE_TOKEN}"
    
    try:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        namespace = {'ns': 'urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0'}
        prices = []
        for point in root.findall('.//ns:Point', namespace):
            price_mwh = float(point.find('ns:price.amount', namespace).text)
            # Duitsland: MWh naar kWh + 19% MwSt (Duitse BTW)
            price_kwh = (price_mwh / 1000) * 1.19
            prices.append(round(price_kwh, 4))
        return {
            "country": "Germany", 
            "unit": "kWh", 
            "currency": "EUR", 
            "tax": "19% MwSt included", 
            "data": prices
        }
    except:
        return {"error": "Technical error fetching German power prices"}

@app.get("/erdgas")
def get_german_gas():
    # Actuele Duitse marktprijs schatting
    return {
        "country": "Germany", 
        "unit": "m3", 
        "currency": "EUR", 
        "price": 0.8842
    }

@app.get("/kraftstoff")
def get_german_fuel():
    # Gemiddelde Duitse pompprijzen
    return {
        "country": "Germany",
        "currency": "EUR",
        "unit": "liter",
        "prices": {
            "Super_E10": 1.749,
            "Super_E5": 1.809,
            "Diesel": 1.669,
            "Autogas_LPG": 1.029,
            "Erdgas_CNG": 1.159
        }
    }
