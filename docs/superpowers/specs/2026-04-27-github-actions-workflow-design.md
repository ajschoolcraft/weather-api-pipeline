# GitHub Actions Workflow for Weather Pipeline

## Overview

Schedule the weather forecast pipeline (`weather.py`) to run daily via GitHub Actions, committing updated forecast data back to the repository.

## Trigger

- **Scheduled:** `cron: '0 6 * * *'` — daily at 6:00 AM UTC (~1-2 AM Eastern)
- **Manual:** `workflow_dispatch` — on-demand from the Actions tab

## Workflow Structure

Single-job workflow (`fetch-and-commit`) on `ubuntu-latest`.

### Steps

1. **Checkout repo** — `actions/checkout@v4`
2. **Set up Python 3.14** — `actions/setup-python@v5`
3. **Install dependencies** — `pip install -r requirements.txt`
4. **Run pipeline** — `python weather.py` with `WEATHER_API_KEY` from GitHub Actions secrets
5. **Commit and push** — commit `weather_data.csv` to `main` using a bot identity; skip if unchanged

### Permissions

The workflow requires `contents: write` to push commits.

### Secrets

| Secret Name       | Description                          | Where to Add                          |
|-------------------|--------------------------------------|---------------------------------------|
| `WEATHER_API_KEY` | WeatherAPI.com API key               | Settings → Secrets and variables → Actions |

### Git Identity for Automated Commits

- **Name:** `github-actions[bot]`
- **Email:** `github-actions[bot]@users.noreply.github.com`

### Commit Behavior

- Only commits when `weather_data.csv` has changed (no empty commits)
- Commit message: `Update weather data — <date>`

## File Location

`.github/workflows/weather-pipeline.yml`

## What the User Must Do

1. Add `WEATHER_API_KEY` as a repository secret in GitHub Settings → Secrets and variables → Actions
2. Push the workflow file to `main`
