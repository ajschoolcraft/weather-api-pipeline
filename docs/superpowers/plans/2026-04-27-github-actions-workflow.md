# GitHub Actions Weather Pipeline Workflow — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Schedule the weather forecast pipeline to run daily at 6 AM UTC via GitHub Actions, committing updated data back to the repo.

**Architecture:** Single-job GitHub Actions workflow triggered on cron and manual dispatch. The job checks out the repo, runs `weather.py`, and commits `weather_data.csv` if it changed.

**Tech Stack:** GitHub Actions, Python 3.14, pip

---

### Task 1: Create the workflow file

**Files:**
- Create: `.github/workflows/weather-pipeline.yml`

- [ ] **Step 1: Create the workflow directory**

```bash
mkdir -p .github/workflows
```

- [ ] **Step 2: Write the workflow file**

Create `.github/workflows/weather-pipeline.yml` with this content:

```yaml
name: Weather Forecast Pipeline

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  fetch-and-commit:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.14'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run weather pipeline
        env:
          WEATHER_API_KEY: ${{ secrets.WEATHER_API_KEY }}
        run: python weather.py

      - name: Commit and push updated data
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add weather_data.csv
          if git diff --cached --quiet; then
            echo "No changes to commit"
          else
            git commit -m "Update weather data — $(date -u +%Y-%m-%d)"
            git push
          fi
```

- [ ] **Step 3: Verify the YAML is valid**

```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/weather-pipeline.yml'))"
```

If `pyyaml` isn't available, visually confirm indentation is correct (all `uses`, `run`, `with`, `env` keys indented under their step).

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/weather-pipeline.yml
git commit -m "Add GitHub Actions workflow for daily weather pipeline"
```

---

### Task 2: Remove weather_data.csv from version control tracking (optional cleanup)

The CSV is currently committed. Since the workflow will auto-commit fresh data daily, the existing copy is fine to leave. However, the `.env` file is already in `.gitignore` — no changes needed there.

This task is a no-op unless you want to stop tracking the CSV. Skip it.

---

### Post-Implementation: Manual Setup Required

These steps happen in the GitHub UI, not in code:

1. Go to the repository on GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `WEATHER_API_KEY`
4. Value: the API key from your `.env` file (`faeaa5fd73c342b3a04175137261304`)
5. Click **Add secret**

After pushing the workflow file and adding the secret, you can test by going to **Actions** → **Weather Forecast Pipeline** → **Run workflow**.
