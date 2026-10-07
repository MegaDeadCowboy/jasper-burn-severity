"""Spectral indices and FIREMON dNBR severity classes."""
import numpy as np
import xarray as xr

# USGS FIREMON dNBR thresholds (lower bounds); see docs/project_brief.md
SEVERITY_BINS = [-np.inf, 0.10, 0.27, 0.44, 0.66, np.inf]
SEVERITY_LABELS = ["Unburned", "Low", "Moderate-low", "Moderate-high", "High"]


def _nd(a, b):
    return (a - b) / (a + b)


def ndvi(ds: xr.Dataset) -> xr.DataArray:
    """NDVI = (B08 - B04) / (B08 + B04)."""
    return _nd(ds["B08"], ds["B04"]).rename("ndvi")


def nbr(ds: xr.Dataset) -> xr.DataArray:
    """NBR = (B8A - B12) / (B8A + B12). Both 20 m bands."""
    return _nd(ds["B8A"], ds["B12"]).rename("nbr")


def dnbr(nbr_pre: xr.DataArray, nbr_post: xr.DataArray) -> xr.DataArray:
    return (nbr_pre - nbr_post).rename("dnbr")


def classify_severity(d: xr.DataArray) -> xr.DataArray:
    """Return integer classes 0-4 (index into SEVERITY_LABELS); NaN stays NaN."""
    cls = xr.apply_ufunc(np.digitize, d, kwargs={"bins": SEVERITY_BINS[1:-1]}, dask="allowed")
    return cls.where(d.notnull()).rename("severity")
