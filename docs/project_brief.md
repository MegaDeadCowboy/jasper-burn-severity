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
