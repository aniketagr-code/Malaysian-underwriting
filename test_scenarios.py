import json
from backend.app.schemas import QuoteRequest
from backend.app.engine import generate_quote

scenarios = [
    {
        "id": "Scenario 1 (22yo M, Proton Saga, KL, private, 0 NCD)",
        "payload": {
            "driver_age": 22,
            "gender": "M",
            "traffic_violations": 0,
            "ncd_percentage": 0.0,
            "territory": "Urban (KL, Selangor, Penang, Johor)",
            "flood_zone": "Low",
            "vehicle_value": 35000,
            "engine_capacity": 1300,
            "vehicle_category": "Private Car",
            "valuation_type": "Market Value",
            "vehicle_age": 2,
            "usage_type": "Private"
        }
    },
    {
        "id": "Scenario 2 (45yo F, Honda City, Penang, private, 55 NCD)",
        "payload": {
            "driver_age": 45,
            "gender": "F",
            "ncd_percentage": 55.0,
            "territory": "Urban (KL, Selangor, Penang, Johor)",
            "flood_zone": "Low",
            "vehicle_value": 70000,
            "engine_capacity": 1500,
            "vehicle_category": "Private Car",
            "valuation_type": "Market Value",
            "vehicle_age": 4,
            "usage_type": "Private"
        }
    },
    {
        "id": "Scenario 3 (30yo M, Hilux, Kelantan, commercial, 25 NCD)",
        "payload": {
            "driver_age": 30,
            "gender": "M",
            "ncd_percentage": 25.0,
            "territory": "Rural (West Malaysia)",
            "flood_zone": "High",
            "vehicle_value": 120000,
            "engine_capacity": 2400,
            "vehicle_category": "Commercial Pickup",
            "valuation_type": "Market Value",
            "vehicle_age": 3,
            "usage_type": "Commercial"
        }
    },
    {
        "id": "Scenario 4 (28yo M, BMW 320i, KL, private, 38.33 NCD)",
        "payload": {
            "driver_age": 28,
            "gender": "M",
            "ncd_percentage": 38.33,
            "territory": "Urban (KL, Selangor, Penang, Johor)",
            "flood_zone": "Low",
            "vehicle_value": 250000,
            "engine_capacity": 2000,
            "vehicle_category": "Luxury Car",
            "valuation_type": "Market Value",
            "vehicle_age": 5,
            "usage_type": "Private"
        }
    },
    {
        "id": "Scenario 5 (35yo F, Myvi, JB, Grab, 0 NCD)",
        "payload": {
            "driver_age": 35,
            "gender": "F",
            "ncd_percentage": 0.0,
            "territory": "Urban (KL, Selangor, Penang, Johor)",
            "flood_zone": "High",
            "vehicle_value": 45000,
            "engine_capacity": 1500,
            "vehicle_category": "Private Car",
            "valuation_type": "Market Value",
            "vehicle_age": 1,
            "usage_type": "E-hailing Commercial"
        }
    }
]

results = []
for s in scenarios:
    req = QuoteRequest(**s["payload"])
    res = generate_quote(req)
    results.append({
        "scenario": s["id"],
        "composite_score": res["composite_score"],
        "decision": res["decision"]
    })

with open("prefix_results.json", "w") as f:
    json.dump(results, f, indent=2)
