"""
backend/green_corridor.py
Green Corridor: Emergency Route Optimization Engine for WariSeva AI.

Prioritizes emergency arrival time, congestion index, and road accessibility
over raw geographical distance. Evaluates real-life pilgrimage scenarios
where a longer peripheral bypass is significantly faster than a shorter congested road.
"""

import json
import os

def load_hospitals_data():
    hospitals_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hospitals.json')
    if os.path.exists(hospitals_file):
        with open(hospitals_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def calculate_route_suitability(distance_km, congestion_percent, traffic_delay_min, accessibility_rating):
    """
    Multi-factor emergency route scoring.
    Higher score indicates a superior emergency route.
    Penalizes congestion and delays heavily while treating distance as secondary.
    """
    base_score = 100.0
    congestion_penalty = congestion_percent * 0.55
    delay_penalty = traffic_delay_min * 2.5
    distance_penalty = distance_km * 0.2
    accessibility_bonus = 15.0 if accessibility_rating == 'HIGH' else (5.0 if accessibility_rating == 'MODERATE' else -15.0)

    score = base_score - congestion_penalty - delay_penalty - distance_penalty + accessibility_bonus
    return round(max(5.0, min(99.0, score)), 1)

def get_green_corridor_plan(emergency_id="EM-28471"):
    """
    Evaluates emergency route options from the ambulance origin to candidate hospitals.
    Demonstrates that Route B (longer distance, low congestion) is superior to
    Route A (shorter distance, severe procession bottleneck).
    """
    hospitals = load_hospitals_data()
    hosp_001 = next((h for h in hospitals if h['hospital_id'] in ('HOSP-001', 'H-001')), None)
    if not hosp_001 and hospitals:
        hosp_001 = hospitals[0]

    hosp_name = hosp_001['name'] if hosp_001 else "Saswad Rural Sub-District Hospital"
    hosp_coords = [hosp_001['latitude'], hosp_001['longitude']] if hosp_001 else [18.3490, 74.0345]

    ambulance_location = {
        "unit_id": "MR-001",
        "label": "Ambulance 1 — Advanced Life Support",
        "current_zone": "Zone 04 — Saswad Sector",
        "coordinates": [18.3390, 74.0260],
        "driver": "Ganesh Patil",
        "status": "EN_ROUTE"
    }

    destination_hospital = {
        "hospital_id": hosp_001['hospital_id'] if hosp_001 else "HOSP-001",
        "name": hosp_name,
        "coordinates": hosp_coords,
        "address": hosp_001.get('address', 'Saswad-Hadapsar Road, Purandar'),
        "emergency_icu_available": True,
        "trauma_beds_reserved": 1
    }

    # Route A: Direct Procession Highway (Shorter distance, severely congested)
    route_a = {
        "route_id": "ROUTE-A",
        "name": "Route A — Direct Palkhi Procession Highway",
        "type": "DIRECT_CONGESTED",
        "distance_km": 4.8,
        "estimated_eta_min": 26,
        "congestion_level": "SEVERE",
        "congestion_percent": 88,
        "road_accessibility": "LOW",
        "bottlenecks": [
            "Saswad Mandir Chowk (Heavy Pedestrian Flow)",
            "Palkhi Ratha Barricades (Temporary One-Way)"
        ],
        "is_recommended": False,
        "selection_badge": "ALTERNATIVE (CONGESTED)",
        "decision_rationale": "Geographically shorter by 3.6 km, but severe pedestrian density and Palkhi procession choke points cause an estimated 26-minute delay.",
        "polyline": [
            [18.3390, 74.0260],
            [18.3410, 74.0278],
            [18.3435, 74.0295],
            [18.3460, 74.0320],
            [18.3490, 74.0345]
        ],
        "color": "#FF5252",
        "dash_array": "6, 6"
    }
    route_a["suitability_score"] = calculate_route_suitability(
        route_a["distance_km"], route_a["congestion_percent"], 18, route_a["road_accessibility"]
    )

    # Route B: Peripheral Bypass Link Road (Longer distance, low congestion — GREEN CORRIDOR)
    route_b = {
        "route_id": "ROUTE-B",
        "name": "Route B — Peripheral Bypass Link Road (Green Corridor)",
        "type": "GREEN_CORRIDOR_BYPASS",
        "distance_km": 8.4,
        "estimated_eta_min": 13,
        "congestion_level": "LOW",
        "congestion_percent": 18,
        "road_accessibility": "HIGH",
        "bottlenecks": [
            "Clear Outer Ring Bypass with Active Traffic Marshalling"
        ],
        "is_recommended": True,
        "selection_badge": "RECOMMENDED GREEN CORRIDOR 🟢",
        "decision_rationale": "Recommended Green Corridor: Despite being 3.6 km longer, low traffic congestion allows the ambulance to reach the hospital 13 minutes faster.",
        "time_saved_min": 13,
        "polyline": [
            [18.3390, 74.0260],
            [18.3375, 74.0310],
            [18.3400, 74.0370],
            [18.3450, 74.0385],
            [18.3490, 74.0345]
        ],
        "color": "#00E676",
        "dash_array": None
    }
    route_b["suitability_score"] = calculate_route_suitability(
        route_b["distance_km"], route_b["congestion_percent"], 1, route_b["road_accessibility"]
    )

    return {
        "success": True,
        "emergency_id": emergency_id,
        "feature": "GREEN_CORRIDOR",
        "status": "ACTIVE",
        "data_mode": "SIMULATED TRAFFIC (DEMO)",
        "disclaimer": "Demo simulated traffic data. Prioritizes arrival speed over distance for emergency dispatch.",
        "ambulance": ambulance_location,
        "destination": destination_hospital,
        "recommended_route_id": "ROUTE-B",
        "routes": [route_b, route_a],
        "summary": {
            "recommended_route": "Route B (Peripheral Bypass)",
            "optimized_eta_min": 13,
            "time_saved_min": 13,
            "traffic_condition": "LOW (18%)",
            "primary_reason": "Longer route chosen due to significantly lower congestion and 13-minute faster emergency arrival."
        }
    }
