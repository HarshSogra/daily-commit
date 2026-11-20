# Daily Commit

A small GitHub Actions project that updates `data/activity.json` automatically every day.

## How it works

1. GitHub Actions runs on a daily schedule.
2. `scripts/update.py` generates the day's activity entry.
3. The entry is written to `data/activity.json`.
4. Git commits the change.
5. Git pushes the commit back to `main`.

This repository is primarily a learning project for scheduled automation with GitHub Actions and Python.

## Live Stats

| Metric | Value |
|---|---:|
| Total daily updates | **96** |
| Current streak | **4 day(s)** |
| Latest update | **2026-11-20** |
| Latest day | **Friday** |
| Year progress | **88.77%** |
| Last run (UTC) | **00:46:51** |

> This section is refreshed automatically by GitHub Actions every day.

