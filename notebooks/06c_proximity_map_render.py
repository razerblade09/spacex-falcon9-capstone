"""
Phase 6c: Static render of the proximity analysis
==================================================
Renders the Folium proximity analysis to a PNG for the slide deck and report,
so the printed deliverables show the same distances the interactive map does.

Two panels, both drawn over OpenStreetMap raster tiles:
  Top    - regional view: launch site, nearest coastline point, nearest city
  Bottom - site view: launch site, nearest railway, nearest highway

Feature coordinates come from 06_folium_map.py (single source of truth).
"""
import io
import math
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TILE_URL = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
HEADERS = {'User-Agent': 'spacex-falcon9-capstone/1.0 (educational coursework)'}
TILE_PX = 256

LAUNCH_SITE = (28.573255, -80.646895)  # KSC LC-39A
SITE_NAME = 'KSC LC-39A'

# Nearest-feature coordinates, matching 06_folium_map.py. The coastline point
# was read off the map; the city, railway and highway points come from
# OpenStreetMap (Overpass API). The last value is the label offset in points,
# set per feature so labels do not collide.
FEATURES = {
    'coastline': (28.56367, -80.57163, 'Nearest coastline', (14, -30)),
    'city':      (28.61262, -80.80795, 'Titusville (nearest city)', (10, 26)),
    'railway':   (28.57295, -80.65392, 'NASA Railroad', (-8, 34)),
    'highway':   (28.57195, -80.65542, 'Kennedy Pkwy N', (-8, -40)),
}


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
    lat_rad = math.radians(lat)
    y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
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


def draw_panel(ax, z, bbox, keys, title, session):
    lat_min, lat_max, lon_min, lon_max = bbox
    basemap, bounds = fetch_basemap(lat_min, lat_max, lon_min, lon_max, z, session)
    ax.imshow(basemap)

    sx, sy = to_pixels(*LAUNCH_SITE, z, bounds)
    for key in keys:
        flat, flon, label, offset = FEATURES[key]
        fx, fy = to_pixels(flat, flon, z, bounds)
        dist = haversine_km(*LAUNCH_SITE, flat, flon)
        ax.plot([sx, fx], [sy, fy], color='#d62728', lw=2.2, zorder=3)
        ax.scatter([fx], [fy], s=90, c='#d62728', edgecolor='white', lw=1.5, zorder=4)
        ax.annotate(f'{label}\n{dist:.2f} km', (fx, fy), textcoords='offset points',
                    xytext=offset, fontsize=10, fontweight='bold',
                    color='#7d1a1a', ha='center', va='center', zorder=5,
                    arrowprops=dict(arrowstyle='-', color='#d62728', lw=1),
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#d62728', alpha=0.95))

    ax.scatter([sx], [sy], s=320, marker='^', c='#3B60E4', edgecolor='white', lw=2, zorder=6)
    ax.annotate(SITE_NAME, (sx, sy), textcoords='offset points', xytext=(12, 10),
                fontsize=11, fontweight='bold', color='#1b2f8a', zorder=6,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#3B60E4', alpha=0.9))

    # Clip to the requested bbox so the panel is not padded out to tile edges.
    x_lo, y_hi = to_pixels(lat_min, lon_min, z, bounds)
    x_hi, y_lo = to_pixels(lat_max, lon_max, z, bounds)
    ax.set_xlim(x_lo, x_hi)
    ax.set_ylim(y_hi, y_lo)
    ax.set_title(title, fontsize=13, fontweight='bold', color='#1a1a2e', pad=10)
    ax.set_xticks([])
    ax.set_yticks([])


def main():
    session = requests.Session()
    fig, axes = plt.subplots(2, 1, figsize=(12, 7.2))

    draw_panel(axes[0], 12, (28.5300, 28.6400, -80.8800, -80.4900),
               ['coastline', 'city'], 'Regional view — coastline and nearest city', session)
    draw_panel(axes[1], 15, (28.5665, 28.5800, -80.6720, -80.6260),
               ['railway', 'highway'], 'Site view — nearest railway and highway', session)

    fig.suptitle(f'Proximity analysis — distances from {SITE_NAME}',
                 fontsize=16, fontweight='bold', color='#1a1a2e')
    fig.text(0.5, 0.015, 'Basemap © OpenStreetMap contributors',
             ha='center', fontsize=8, color='#666666')
    fig.tight_layout(rect=[0, 0.03, 1, 0.94])

    out = f'{ROOT}/images/folium_map_screenshot.png'
    fig.savefig(out, dpi=150, facecolor='white', bbox_inches='tight')
    print('Saved', out)
    for key, (flat, flon, label, _) in FEATURES.items():
        print(f'  {label:<26} {haversine_km(*LAUNCH_SITE, flat, flon):>8.2f} km')


if __name__ == '__main__':
    main()
