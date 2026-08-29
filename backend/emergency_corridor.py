"""
backend/emergency_corridor.py
Emergency Corridor Engine for WariSeva AI.

Coordinates temporary crowd-clearance passage when an ambulance carrying
a critical patient is stuck in dense pilgrimage processions during Wari.
Coordinates Ambulance/Hospital, Command Centre, and nearby Volunteers.
"""

from datetime import datetime

# In-memory prototype state store for active corridor requests
_corridor_state = {
    "EM-28471": {
        "emergency_id": "EM-28471",
        "patient_name": "Tukaram Shinde",
        "patient_zone": "Zone 04 — Saswad Palkhi Maidan",
        "status": "IDLE",  # IDLE, REQUESTED, ASSIGNED, EN_ROUTE, AT_LOCATION, CLEARING, CLEAR, MOVING, COMPLETED
        "status_label": "Standby",
        "requested_at": None,
        "updated_at": None,
        "ambulance": {
            "unit_id": "AMB-01",
            "driver_name": "Dr. Arvind Shinde (Mobile Ambulance 1)",
            "phone": "+91 98700 11111",
            "current_location": "Saswad Palkhi Maidan Sector 4 (Crossing Gate 2)",
            "coordinates": [18.3470, 74.0330],
            "choke_reason": "Severe crowd bottleneck at temple procession crossing"
        },
        "destination_hospital": {
            "hospital_id": "HOSP-001",
            "name": "Saswad Rural Sub-District Hospital",
            "address": "Saswad-Hadapsar Road, Purandar",
            "coordinates": [18.3490, 74.0345],
            "bed_reserved": True
        },
        "nearby_volunteers": [
            {
                "wari_id": "V-001",
                "name": "Ramesh Kulkarni",
                "phone": "+91 98200 11111",
                "distance_m": 120,
                "eta_sec": 45,
                "status": "AVAILABLE",
                "skills": "First Aid Certified, Crowd Assistance",
                "role": "Lead Corridor Marshall"
            },
            {
                "wari_id": "V-002",
                "name": "Suresh Patil",
                "phone": "+91 98200 22222",
                "distance_m": 250,
                "eta_sec": 90,
                "status": "AVAILABLE",
                "skills": "Crowd Guidance, Dindi Marshall",
                "role": "Flank Safety Coordinator"
            },
            {
                "wari_id": "V-003",
                "name": "Aniket Deshmukh",
                "phone": "+91 98200 33333",
                "distance_m": 400,
                "eta_sec": 140,
                "status": "AVAILABLE",
                "skills": "Basic Triage, Youth Seva Marshall",
                "role": "Advance Route Clearance"
            }
        ],
        "assigned_volunteers": [],
        "timeline": []
    }
}

STATUS_LABELS = {
    "IDLE": "Standby",
    "REQUESTED": "🟡 Corridor Requested (Awaiting Command Centre)",
    "ASSIGNED": "🔵 Volunteers Assigned (Dispatched to Ambulance)",
    "EN_ROUTE": "🚶 Volunteers En Route to Location",
    "AT_LOCATION": "📍 Volunteers on Scene at Ambulance",
    "CLEARING": "📢 Volunteers Clearing Crowd Aside",
    "CLEAR": "🟢 Corridor Clear (Safe Passage Open)",
    "MOVING": "🚑 Ambulance Moving Through Passage",
    "COMPLETED": "✅ Corridor Completed (Ambulance Cleared)"
}

def get_corridor(emergency_id="EM-28471"):
    if emergency_id not in _corridor_state:
        # Clone default prototype structure
        default_data = dict(_corridor_state["EM-28471"])
        default_data["emergency_id"] = emergency_id
        _corridor_state[emergency_id] = default_data
    return _corridor_state[emergency_id]

def request_corridor(emergency_id="EM-28471"):
    c = get_corridor(emergency_id)
    c["status"] = "REQUESTED"
    c["status_label"] = STATUS_LABELS["REQUESTED"]
    now_str = datetime.now().strftime("%H:%M:%S")
    c["requested_at"] = now_str
    c["updated_at"] = now_str
    c["assigned_volunteers"] = []
    c["timeline"].append({
        "time": now_str,
        "stage": "REQUESTED",
        "actor": "AMBULANCE AMB-01",
        "message": "Ambulance blocked in severe crowd. Requested Emergency Corridor."
    })
    return c

def assign_volunteers(emergency_id="EM-28471", volunteer_ids=None):
    c = get_corridor(emergency_id)
    if not volunteer_ids:
        volunteer_ids = ["V-001", "V-002", "V-003"]
    
    assigned = [v for v in c["nearby_volunteers"] if v["wari_id"] in volunteer_ids]
    c["assigned_volunteers"] = assigned
    c["status"] = "ASSIGNED"
    c["status_label"] = STATUS_LABELS["ASSIGNED"]
    now_str = datetime.now().strftime("%H:%M:%S")
    c["updated_at"] = now_str
    c["timeline"].append({
        "time": now_str,
        "stage": "ASSIGNED",
        "actor": "COMMAND CENTRE",
        "message": f"Command Centre assigned {len(assigned)} nearby volunteers to create clearance corridor."
    })
    return c

def update_status(emergency_id="EM-28471", new_status="CLEARING", actor="VOLUNTEER V-001"):
    c = get_corridor(emergency_id)
    if new_status in STATUS_LABELS:
        c["status"] = new_status
        c["status_label"] = STATUS_LABELS[new_status]
        now_str = datetime.now().strftime("%H:%M:%S")
        c["updated_at"] = now_str
        c["timeline"].append({
            "time": now_str,
            "stage": new_status,
            "actor": actor,
            "message": f"Emergency Corridor status updated to: {STATUS_LABELS[new_status]}"
        })
    return c

def reset_corridor(emergency_id="EM-28471"):
    c = get_corridor(emergency_id)
    c["status"] = "IDLE"
    c["status_label"] = STATUS_LABELS["IDLE"]
    c["requested_at"] = None
    c["updated_at"] = None
    c["assigned_volunteers"] = []
    c["timeline"] = []
    return c
