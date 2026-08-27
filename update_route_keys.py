with open('backend/app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """        'routes': {
            'direct_route': {
                'name': 'Direct Procession Route (Congested)',
                'distance_m': direct_dist_m,
                'distance_km': round(direct_dist_km, 2),
                'crowd_level': crowd_density,
                'congestion_delay_min': congestion_delay_min,
                'total_eta_min': direct_total_eta,
                'eta_text': f"{direct_total_eta} min (Slow • Heavy Crowd)",
                'is_recommended': False,
                'color': '#FF5252',
                'waypoints': direct_waypoints
            },
            'safe_bypass_route': {
                'name': 'WariSeva Safe Bypass Corridor (Fastest Safe)',
                'distance_m': safe_dist_m,
                'distance_km': round(safe_dist_km, 2),
                'crowd_level': 'LOW',
                'congestion_delay_min': safe_delay_min,
                'total_eta_min': safe_total_eta,
                'eta_text': f"{safe_total_eta} min (Fastest Safe Corridor)",
                'time_saved_min': time_saved_min,
                'is_recommended': True,
                'color': '#00E676',
                'waypoints': safe_waypoints
            }
        }"""

replacement = """        'routes': {
            'direct_route': {
                'name': 'Direct Procession Route (Congested)',
                'distance_m': direct_dist_m,
                'distance_km': round(direct_dist_km, 2),
                'distance_text': f"{direct_dist_m}m" if direct_dist_m < 1000 else f"{round(direct_dist_km, 1)} km",
                'crowd_level': crowd_density,
                'congestion_delay_min': congestion_delay_min,
                'total_eta_min': direct_total_eta,
                'estimated_time_text': f"{direct_total_eta} min",
                'eta_text': f"{direct_total_eta} min (Slow • Heavy Crowd)",
                'is_recommended': False,
                'color': '#FF5252',
                'waypoints': direct_waypoints
            },
            'safe_bypass_route': {
                'name': 'WariSeva Safe Bypass Corridor (Fastest Safe)',
                'distance_m': safe_dist_m,
                'distance_km': round(safe_dist_km, 2),
                'distance_text': f"{safe_dist_m}m" if safe_dist_m < 1000 else f"{round(safe_dist_km, 1)} km",
                'crowd_level': 'LOW',
                'congestion_delay_min': safe_delay_min,
                'total_eta_min': safe_total_eta,
                'estimated_time_text': f"{safe_total_eta} min",
                'eta_text': f"{safe_total_eta} min (Fastest Safe Corridor)",
                'time_saved_min': time_saved_min,
                'time_saved_text': f"⚡ Saves {time_saved_min} min",
                'is_recommended': True,
                'color': '#00E676',
                'waypoints': safe_waypoints
            },
            'time_saved_text': f"⚡ Saves {time_saved_min} min"
        }"""

assert target in code, "Could not find target in backend/app.py"
code = code.replace(target, replacement)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated route dictionary in backend/app.py with comprehensive text aliases!")
