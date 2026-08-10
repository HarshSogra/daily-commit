import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "activity.json"
README_FILE = ROOT / "README.md"

MESSAGES = [
    "Daily automation heartbeat",
    "Scheduled repository maintenance",
    "Daily system check completed",
    "Automation pipeline ran successfully",
    "Repository activity refreshed",
]


def calculate_streak(activity, today):
    dates = {
        date.fromisoformat(item["date"])
        for item in activity
        if item.get("date")
    }

    streak = 0
    current = today
    while current in dates:
        streak += 1
        current -= timedelta(days=1)

    return streak


with DATA_FILE.open("r", encoding="utf-8") as file:
    activity = json.load(file)

now = datetime.now(timezone.utc)
today = now.date()
day_of_year = today.timetuple().tm_yday
is_leap_year = today.replace(month=12, day=31).timetuple().tm_yday == 366
days_in_year = 366 if is_leap_year else 365

today_entry = {
    "date": today.isoformat(),
    "day": today.strftime("%A"),
    "week": today.isocalendar().week,
    "day_of_year": day_of_year,
    "year_progress_percent": round(day_of_year / days_in_year * 100, 2),
    "time_utc": now.strftime("%H:%M:%S"),
    "message": MESSAGES[len(activity) % len(MESSAGES)],
    "status": "success",
}

# Keep one entry per UTC calendar day.
if not any(item.get("date") == today_entry["date"] for item in activity):
    activity.append(today_entry)

activity.sort(key=lambda item: item.get("date", ""))

with DATA_FILE.open("w", encoding="utf-8") as file:
    json.dump(activity, file, indent=2)
    file.write("\n")

streak = calculate_streak(activity, today)
total_updates = len(activity)
latest = activity[-1]

stats_block = f"""## Live Stats

| Metric | Value |
|---|---:|
| Total daily updates | **{total_updates}** |
| Current streak | **{streak} day(s)** |
| Latest update | **{latest['date']}** |
| Latest day | **{latest.get('day', 'N/A')}** |
| Year progress | **{latest.get('year_progress_percent', 0):.2f}%** |
| Last run (UTC) | **{latest.get('time_utc', 'N/A')}** |

> This section is refreshed automatically by GitHub Actions every day.

"""

readme = README_FILE.read_text(encoding="utf-8")
marker = "## Live Stats\n"

if marker in readme:
    readme = readme.split(marker, 1)[0].rstrip() + "\n\n" + stats_block
else:
    readme = readme.rstrip() + "\n\n" + stats_block

README_FILE.write_text(readme, encoding="utf-8")

print(f"Daily activity updated for {today.isoformat()}")
print(f"Current streak: {streak} day(s)")
print(f"Total updates: {total_updates}")
