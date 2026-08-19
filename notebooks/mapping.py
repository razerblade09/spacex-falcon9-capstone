"""
Shared map-rendering helpers
=============================
Slippy-map tile maths and OpenStreetMap basemap stitching, used by the static
renders in 06b_static_map_fallback.py and 06c_proximity_map_render.py so both
draw on the same tiles the interactive Folium map uses.
"""
import io
import math

import requests
from PIL import Image

TILE_URL = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
HEADERS = {'User-Agent': 'spacex-falcon9-capstone/1.0 (educational coursework)'}
TILE_PX = 256


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance in km — same formula as 06_folium_map.py."""
    R = 6373.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def deg_to_tile(lat, lon, z):
    """Slippy-map tile coordinates (fractional) for a lat/lon at zoom z."""
    n = 2.0 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
    return x, y


def fetch_basemap(lat_min, lat_max, lon_min, lon_max, z, session):
    """Download and stitch the OSM tiles covering a bounding box.

    Returns the stitched image plus the fractional tile bounds it spans, which
    is what lets us place lat/lon points on it in pixel space.
    """
    x0, y1 = deg_to_tile(lat_min, lon_min, z)
    x1, y0 = deg_to_tile(lat_max, lon_max, z)
    tx0, tx1 = int(math.floor(x0)), int(math.floor(x1))
    ty0, ty1 = int(math.floor(y0)), int(math.floor(y1))

    canvas = Image.new('RGB', ((tx1 - tx0 + 1) * TILE_PX, (ty1 - ty0 + 1) * TILE_PX))
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            r = session.get(TILE_URL.format(z=z, x=tx, y=ty), headers=HEADERS, timeout=30)
            r.raise_for_status()
            tile = Image.open(io.BytesIO(r.content)).convert('RGB')
            canvas.paste(tile, ((tx - tx0) * TILE_PX, (ty - ty0) * TILE_PX))
    return canvas, (tx0, ty0, tx1 + 1, ty1 + 1)


def to_pixels(lat, lon, z, bounds):
    """Map a lat/lon onto pixel coordinates within a stitched basemap."""
    tx0, ty0, _, _ = bounds
    x, y = deg_to_tile(lat, lon, z)
    return (x - tx0) * TILE_PX, (y - ty0) * TILE_PX


def clip_axes(ax, lat_min, lat_max, lon_min, lon_max, z, bounds):
    """Clip an axes to a bbox so the panel is not padded out to tile edges."""
    x_lo, y_hi = to_pixels(lat_min, lon_min, z, bounds)
    x_hi, y_lo = to_pixels(lat_max, lon_max, z, bounds)
    ax.set_xlim(x_lo, x_hi)
    ax.set_ylim(y_hi, y_lo)
    ax.set_xticks([])
    ax.set_yticks([])
