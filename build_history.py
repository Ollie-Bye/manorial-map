import csv
import json

def generate_history():
    # 1. Load Spatial Data (Identity)
    spatial_lookup = {}
    try:
        with open('spatial.csv', mode='r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                spatial_lookup[row['unit_id']] = {
                    "name": row['name'],
                    "prefix": row['prefix'],
                    "type": row['type'],
                    "description": row['description']
                }
    except FileNotFoundError:
        print("Error: spatial.csv not found.")
        return

    # 2. Load Temporal Data (Tenure & Boundaries)
    history_json = {}
    try:
        with open('temporal.csv', mode='r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                uid = row['unit_id']
                if uid not in history_json:
                    history_json[uid] = []
                
                # Logic: Combine Name and Title for the UI 'lord' field
                # If there is a title, add a comma, otherwise just use the name
                full_lord = row['lord_name']
                if row['lord_title']:
                    full_lord += f", {row['lord_title']}"
                
                # Build the record based on your exact temporal columns
                record = {
                    "start": int(row['start']),
                    "end": int(row['end']),
                    "lord_id": row['lord_id'],
                    "lord": full_lord, # The 'calculated' display name
                    "lord_family": row['lord_family'],
                    "overlord": row['overlord'],
                    "moiety": row['moiety_fraction'],
                    "geometry_file": row['geometry_file'],
                    # Pull these from Spatial lookup based on unit_id
                    "prefix": spatial_lookup.get(uid, {}).get('prefix', 'Manor of'),
                    "type": spatial_lookup.get(uid, {}).get('type', 'seigneurial')
                }
                history_json[uid].append(record)
    except FileNotFoundError:
        print("Error: temporal.csv not found.")
        return

    # 3. Export to JSON
    with open('dorset_history.json', 'w', encoding='utf-8') as f:
        json.dump(history_json, f, indent=2)
    print("Success! dorset_history.json has been created.")

if __name__ == "__main__":
    generate_history()