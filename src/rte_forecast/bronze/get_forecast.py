import os
import json
import requests
from datetime import datetime, timedelta

# ================================================================
# 1️⃣ Your VALID RTE access token (update manually whenever needed)
# ================================================================
TOKEN = "OkcT6LX3xpy8Hs6KGoxL8PK5IcODCBkGPpxq1UbW3O7YzkvermhZH0"

# ================================================================
# 2️⃣ API endpoint
# ================================================================
URL = "https://digital.iservices.rte-france.com/open_api/generation_forecast/v3/total_forecast"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# ================================================================
# 3️⃣ Folder save helper (Bronze → raw json)
# ================================================================
def save_data(date_str, data):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    folder = f"data/bronze/rte/{date.year}/{date.month:02d}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/{date.day:02d}_D-1.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"💾 Saved D-1 data → {path}")

# ================================================================
# 4️⃣ Check for null quantities
# ================================================================
def all_quantities_null(data):
    try:
        points = data["total_forecast"][0]["points"]
        return all(p["quantity"] is None for p in points)
    except Exception:
        return True

# ================================================================
# 5️⃣ Date range — from 2023-01-01 to today
# ================================================================
start_date = datetime(2023, 1, 1)
end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

# ================================================================
# 6️⃣ Fetch loop — strictly D-1 Bronze ingestion
# ================================================================
current = start_date

while current <= end_date:
    next_day = current + timedelta(days=1)
    date_str = current.strftime("%Y-%m-%d")

    print(f"\n📡 Fetching D-1 forecast for {date_str}...")

    # Skip if already collected
    folder = f"data/bronze/rte/{current.year}/{current.month:02d}"
    path = f"{folder}/{current.day:02d}_D-1.json"

    if os.path.exists(path):
        print(f"⏭️ Skipping {date_str} (already exists)")
        current = next_day
        continue

    params = {
        "type": "D-1",
        "start_date": current.strftime("%Y-%m-%dT00:00:00Z"),
        "end_date": next_day.strftime("%Y-%m-%dT00:00:00Z"),
    }

    try:
        response = requests.get(URL, headers=HEADERS, params=params)

        if response.status_code == 200:
            data = response.json()

            if all_quantities_null(data):
                print("⚠️ D-1 file contains only null quantities — skipping.")
            else:
                save_data(date_str, data)

        elif response.status_code == 401:
            print("🔑 Token expired — regenerate using get_token.py")
            break

        else:
            print(f"❌ Error for {date_str}: HTTP {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"⚠️ Exception on {date_str}: {e}")

    current = next_day

print("\n🎉 Bronze Layer Collection Completed (2023 → Today)")
