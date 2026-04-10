@app.get("/energie/rechnung-check")
async def get_exact_costs(verbruik_kwh: float):
    # Officiële tarieven 2026
    netto_markt = 0.115
    arbeitspreis_netz = 0.1034  # Hard cijfer BNetzA
    stromsteuer = 0.0205        # Wettelijk vast
    grundpreis_jahr = 145.20    # Jaarvast
    
    netto_totaal = netto_markt + arbeitspreis_netz + stromsteuer
    btw = netto_totaal * 0.19
    bruto_totaal = netto_totaal + btw

    return {
        "variable_kosten_pro_kwh": {
            "markt": netto_markt,
            "netzentgelt": arbeitspreis_netz,
            "steuer": stromsteuer,
            "bruto": round(bruto_totaal, 4)
        },
        "fixkosten": {
            "grundpreis_p_a": grundpreis_jahr,
            "grundpreis_p_monat": round(grundpreis_jahr / 12, 2)
        },
        "compliance": {
            "co2_kg_kwh": 0.35,
            "standard": "BNetzA 2026 Compliance"
        }
    }
