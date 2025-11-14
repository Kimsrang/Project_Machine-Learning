import os
import json
import requests
from datetime import datetime, timedelta

# RTE endpoint (Generation Forecast v3)
BASE_URL = "https://digital.iservices.rte-france.com/open_api/generation_forecast/v3/forecasts"

# 👇 Paste a valid access token here (from get_token.py)
ACCESS_TOKEN = "YOUR_NEW_TOKEN_HERE"

HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

def save_bronze_data(date_str, data):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    folder_path = f"data/bronze/rte/{date.year}/{date.month:02d}"
    os.makedirs(folder_path, exist_ok=True)
    file_path = f"{folder_path}/{date.day:02d}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[OK] Saved {file_path}")

# Loop daily (example: January 2020)
start_date = datetime(2020, 1, 1)
end_date = datetime(2020, 1, 10)

date = start_date
while date <= end_date:
    date_str = date.strftime("%Y-%m-%d")
    next_day = date + timedelta(days=1)

    print(f"📡 Fetching RTE data for {date_str}...")

    params = {
        "production_type": "WIND",  # or SOLAR, HYDRO, etc.
        "type": "D-1",
        "start_date": date.strftime("%Y-%m-%dT00:00:00Z"),
        "end_date": next_day.strftime("%Y-%m-%dT00:00:00Z")
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        save_bronze_data(date_str, data)
    else:
        print(f"❌ Failed {date_str}: {response.status_code}")
        print(response.text)

    date += timedelta(days=1)
