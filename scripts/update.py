import json
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "activity.json"

with DATA_FILE.open("r", encoding="utf-8") as file:
    activity = json.load(file)

now = datetime.now(timezone.utc)
entry = {
    "date": now.strftime("%Y-%m-%d"),
    "time_utc": now.strftime("%H:%M:%S"),
    "message": "Daily automated update",
}

# Keep one entry per UTC calendar day.
if not any(item.get("date") == entry["date"] for item in activity):
    activity.append(entry)

with DATA_FILE.open("w", encoding="utf-8") as file:
    json.dump(activity, file, indent=2)
    file.write("\n")

print(f"Daily activity updated for {entry['date']}")
