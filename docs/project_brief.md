# Project Brief: Jasper Burn Severity

## Why
- A portfolio project to close the raster/remote-sensing gap. All prior GIS work is vector (PostGIS, Leaflet, ArcGIS Online).
- Target application: PNNL Data Scientist II, GEOINT/Remote Sensing (#12025), which closes **Oct 23, 2026**. Submit by **Oct 21**.
- It also strengthens forest management and USFS applications.
- Companion repo: `github.com/MegaDeadCowboy/fire-weather-windows`. Frame the pair as "before the fire / after the fire."

## Fire
- **2024 Jasper Wildfire**, Jasper National Park, Alberta.
- Started July 22, 2024 from lightning. Declared out April 1, 2025.
- Area burned: about 32,700 ha (Sept 7, 2024 under-control estimate). Some sources say 39,000 ha.
- The fire burned part of the Jasper townsite. Mask the townsite out of forest statistics.

## Research questions
1. Map burn severity from Sentinel-2 imagery.
2. Measure how well it agrees with the official burned-area perimeter.
3. Track early recovery: NDVI by severity class over the 2025 and 2026 growing seasons.
4. **Headline question:** did pre-fire mountain pine beetle mortality predict severity? Use the 2016–2023 NDVI decline as a mortality proxy and correlate it with dNBR. *Verify the beetle outbreak history with a Parks Canada source before writing it up.*

## Data
- **Imagery:** Sentinel-2 L2A from Microsoft Planetary Computer (STAC, no account needed). Cloud-mask with the SCL band and use median composites.
  - Pre-fire window: Jul–Aug 2023 (or June to mid-July 2024).
  - Post-fire window: Jul–Aug 2025, the extended assessment.
- **Validation:** NBAC (National Burned Area Composite, Natural Resources Canada), 1972–2024 release. It has perimeters only, no severity classes. Get it from the CWFIS Datamart, or from the GEE community catalog.
- **Stretch:** Sentinel-1 radar (SAR) backscatter change.

## Methods
- NDVI = (B8 − B4) / (B8 + B4)
- NBR = (B8A − B12) / (B8A + B12)
- dNBR = NBR_pre − NBR_post
- Severity classes use the USGS FIREMON dNBR thresholds:

| Class | dNBR range |
|---|---|
| Unburned | < 0.10 |
| Low | 0.10–0.27 |
| Moderate-low | 0.27–0.44 |
| Moderate-high | 0.44–0.66 |
| High | > 0.66 |

- **Validation metrics:** burned vs. unburned agreement against the NBAC perimeter (IoU, confusion matrix, area difference).
- **Stretch goals:** a Random Forest pixel classifier compared against the thresholds; dNBR reproduced in Google Earth Engine (about 30 lines) for a GEE skill claim.

## Stack
Python, pystac-client, planetary-computer, stackstac or rioxarray, rasterio/GDAL, xarray, geopandas, matplotlib, and scikit-learn for the stretch.

## Repo layout
```
jasper-burn-severity/
  notebooks/  01_data · 02_indices · 03_validation · 04_recovery · 05_beetle
  src/        shared functions
  figures/
  docs/project_brief.md
  README.md   lead with the severity map
```

## Timeline
| When | Work |
|---|---|
| Oct 10–11 | Notebooks 01–03, through validation |
| Oct 12–16 | 04 recovery, 05 beetle, README |
| Oct 17–18 | Stretch: SAR and/or RF classifier |
| Oct 19–20 | PNNL resume and cover letter (handled in the Getting a Job project) |
| Oct 21 | Submit |

## Target resume bullet (claim only what's finished)
*Mapped burn severity for the 2024 Jasper Wildfire (Alberta) from Sentinel-2 imagery (STAC, rasterio/GDAL), validating burned area against Canada's National Burned Area Composite and testing whether pre-fire mountain pine beetle mortality predicted fire severity.*

Resume convention: give the project a real end date once it's done. Only active work stays "Present."

## Decision Log
- 2026-10-07: Chose Jasper 2024 over Beachie Creek 2020 for the beetle question and the Canada angle. Validation uses NBAC instead of MTBS, which only covers the US.
- 2026-10-07: Validation uses the single-year NBAC_2024_20260513.zip (from the newer 1972–2025 release, CWFIS /downloads/nbac/) instead of the 1 GB full shapefile; the GEE community catalog copy stops at 2023.
- 2026-10-07: All bands (incl. NDVI B04/B08) resampled to one 20 m UTM 11N grid; SCL keep-list {2,4,5,6,7} keeps class 2 (dark area) so fresh char is not masked; baseline ≥04.00 scenes get the −1000 DN offset removed.
- 2026-10-08: Notebook data/ lives on Google Drive (MyDrive/jasper-burn-severity/data) because each Colab notebook gets its own runtime; 01 writes there and 02+ read from it.
- 2026-10-08: No dNBR offset applied: median dNBR in the 2 km unburned ring is 0.005 (n=724,442), so FIREMON thresholds are used as-is.
- 2026-10-08: Pre-fire vegetation mask NDVI ≥ 0.10 for validation and severity stats: commission outside NBAC is mainly the Athabasca River channel and lakes (non-fire dNBR change); 0.10 removes water/rock with the lowest area difference (+0.45%) while keeping sparse burnable cover.
- 2026-10-08: Commission patches outside the NBAC perimeter reviewed in SWIR false colour (figures/commission_patches.png): water, plus one 42 ha non-burn clearing; NBAC perimeter accepted as reference.
- 2026-10-08: 04 recovery uses monthly Jun–Sep 2025/2026 composites; a month is dropped if > 5% of perimeter pixels have zero clear observations (dropped Jun 2026: 2 scenes, 16.3%).
- 2026-10-08: Headline recovery metric is control-adjusted % of pre-fire NDVI (class/control ratio vs the same ratio in Jul–Aug 2023), because the unburned control is ~14% greener in 2025–26 than in 2023.
- 2026-10-08: 05 beetle mortality proxy = Landsat 8/9 C2 L2 (Planetary Computer landsat-c2-l2, Tier 1) Jul–Aug NDVI decline 2013→2023 on the 20 m grid, replacing 2016–2023 Sentinel-2, because Parks Canada figures (via press) show ~21,500 ha colonized by 2016 (first recorded 1999, collapse after 2019 cold snap); Sentinel-2 earliest-summer→2023 kept as a robustness check.
- 2026-10-08: 05 Landsat baseline pools Jul–Aug 2013 + 2014, with no scene cloud filter (per-pixel QA_PIXEL bits 0–5 mask): 2013 alone left 40.1% of perimeter pixels with zero clear obs (only path 045 covers the full perimeter); summer 2014 is still pre-mortality because red needles lag attack by ~1 yr. Baseline zero-clear 0.8%, median 3 clear obs (2023: 0.0%, 3).
- 2026-10-08: 05 headline severity metric is RdNBR = dNBR / √|NBR_pre| (Miller & Thode 2007; pixels with |NBR_pre| < 0.05 dropped), with dNBR reported alongside: dNBR gave a weak negative mortality link (1 km block rho −0.164, p=0.003) that vanished under RdNBR (rho −0.084, p=0.13), i.e. mostly the low pre-fire NBR of dead stands capping dNBR.
- 2026-10-08: 05 headline mortality proxy uses path-045-only Landsat composites (baseline 6 scenes, zero-clear 0.8%; 2023 6 scenes, 0.0%): multi-path composites had a path-044 footprint seam (500 m strip decline step 0.054 → 0.007 with 045 only). Result: RdNBR 1 km block rho +0.008, p=0.88 (dNBR −0.103, p=0.062). Early/late split (2013–14→2017→2023) stays multi-path as supplementary because 045-only 2017 is 8.5% zero-clear.
- 2026-10-08: 05 Sentinel-2 2017→2023 positive association (RdNBR block rho +0.28) reported as non-robust: Landsat over the same years shows none (rho −0.012, p=0.83; proxy agreement rho 0.48) and the S2 proxy shares the 2023 S2 composite with NBR_pre.
