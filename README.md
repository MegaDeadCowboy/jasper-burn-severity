# jasper-burn-severity

Burn severity mapping for the 2024 Jasper Wildfire (Jasper National Park, Alberta) from Sentinel-2 L2A imagery.

> Work in progress. Severity map, validation results, and findings will be added here as each notebook is completed.

Companion repo: [fire-weather-windows](https://github.com/MegaDeadCowboy/fire-weather-windows) (before the fire / after the fire).

## Setup
```bash
pip install -r requirements.txt
```
Runs in Google Colab or locally. Large inputs go in `data/` (git-ignored).

## Layout
- `notebooks/` 01_data · 02_indices · 03_validation · 04_recovery · 05_beetle
- `src/` shared functions
- `figures/` exported figures
- `docs/project_brief.md` scope and decision log
