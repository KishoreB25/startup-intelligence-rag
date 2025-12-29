def extract_signals(text: str, source_type: str) -> dict:
    signals = {
        "startup_name": None,
        "investor_name": None,
        "funding_stage": None,
        "preferred_stage": None,
        "sector_focus": [],
        "market_focus": [],
        "location_startup": None,
        "location_investor": None,
        "location_vc": None,
        "confidence_score": 0.6
    }

    if "Series A" in text:
        signals["funding_stage"] = "Series A"
    elif "Seed" in text:
        signals["funding_stage"] = "Seed"

    if "AI" in text:
        signals["sector_focus"].append("AI")
    if "FinTech" in text:
        signals["sector_focus"].append("FinTech")

    if "India" in text:
        signals["location_startup"] = "India"

    return signals
