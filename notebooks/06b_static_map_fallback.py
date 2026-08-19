"""
Phase 6b: Static render of the Folium launch-site map
======================================================
Renders the launch sites and individual launch records to a PNG for the slide
deck and report, standing in for a screenshot of the interactive Folium map.

Every launch at a site shares that site's coordinates, so the individual
records are laid out on a ring around the site marker — the static equivalent
of expanding a Folium MarkerCluster. Green = successful first-stage landing,
red = failed or no landing attempt.

Two panels, both drawn over OpenStreetMap raster tiles:
  Left  - Cape Canaveral, Florida (CCAFS LC-40, CCAFS SLC-40, KSC LC-39A)
  Right - Vandenberg, California (VAFB SLC-4E)
"""
import math
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib.lines import Line2D

from mapping import clip_axes, fetch_basemap, to_pixels

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SUCCESS_COLOR = '#17BEBB'
FAILURE_COLOR = '#E4572E'
SITE_COLOR = '#3B60E4'

# Panels: (bbox as lat_min, lat_max, lon_min, lon_max), zoom, title, ring radius
PANELS = [
    ((28.500, 28.640, -80.760, -80.480), 12,
     'Cape Canaveral, Florida — 3 launch sites', 24),
    ((34.560, 34.700, -120.750, -120.470), 12,
     'Vandenberg, California — 1 launch site', 24),
]

# CCAFS LC-40 and SLC-40 are the same pad under two names and sit ~100 m apart,
# so their record clusters are drawn offset from the marker and joined to it by
# a leader line. Values are pixel offsets from the site's true position.
CLUSTER_OFFSETS = {
    'CCAFS LC-40': (-58, 78),
    'CCAFS SLC-40': (92, -30),
}

# Label placement relative to each cluster, chosen so the callouts in the Cape
# Canaveral panel do not overlap each other.
LABEL_OFFSETS = {
    'KSC LC-39A': (-46, -68),
    'CCAFS LC-40': (0, 66),
    'CCAFS SLC-40': (30, -58),
}


def ring_offsets(n, radius_px):
    """Pixel offsets placing n markers evenly on a ring (two rings if crowded)."""
    if n == 0:
        return []
    per_ring = 14
    offsets = []
    for i in range(n):
        ring = i // per_ring
        idx = i % per_ring
        count = min(per_ring, n - ring * per_ring)
        angle = 2 * math.pi * idx / count - math.pi / 2
        r = radius_px * (1 + 0.62 * ring)
        offsets.append((r * math.cos(angle), r * math.sin(angle)))
    return offsets


def draw_panel(ax, geo, bbox, z, title, radius_px, session):
    lat_min, lat_max, lon_min, lon_max = bbox
    basemap, bounds = fetch_basemap(lat_min, lat_max, lon_min, lon_max, z, session)
    ax.imshow(basemap)

    sites = geo[(geo['Lat'].between(lat_min, lat_max)) &
                (geo['Long'].between(lon_min, lon_max))]
    for site, rows in sites.groupby('Launch Site'):
        lat, lon = rows['Lat'].iloc[0], rows['Long'].iloc[0]
        sx, sy = to_pixels(lat, lon, z, bounds)
        ox, oy = CLUSTER_OFFSETS.get(site, (0, 0))
        cx, cy = sx + ox, sy - oy
        outcomes = rows['class'].tolist()

        if (ox, oy) != (0, 0):
            ax.plot([sx, cx], [sy, cy], color=SITE_COLOR, lw=1, ls=':', zorder=3)
        n_rings = 1 + (len(outcomes) - 1) // 14
        for (dx, dy), outcome in zip(ring_offsets(len(outcomes), radius_px), outcomes):
            ax.scatter([cx + dx], [cy + dy], s=42, zorder=4, lw=0.8, edgecolor='white',
                       c=SUCCESS_COLOR if outcome == 1 else FAILURE_COLOR)
        ax.scatter([sx], [sy], s=170, marker='^', c=SITE_COLOR,
                   edgecolor='white', lw=1.5, zorder=5)
        default_dy = -(radius_px * (1 + 0.62 * (n_rings - 1)) + 30)
        label_offset = LABEL_OFFSETS.get(site, (0, default_dy))
        ax.annotate(f"{site}\n{len(outcomes)} launches · {int(sum(outcomes))} landed",
                    (cx, cy), textcoords='offset points', xytext=label_offset,
                    fontsize=9, fontweight='bold', color='#1b2f8a', ha='center', zorder=6,
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=SITE_COLOR, alpha=0.92))

    clip_axes(ax, lat_min, lat_max, lon_min, lon_max, z, bounds)
    ax.set_title(title, fontsize=13, fontweight='bold', color='#1a1a2e', pad=10)


def main():
    geo = pd.read_csv(f'{ROOT}/data/spacex_launch_geo.csv')
    geo.columns = geo.columns.str.strip()

    session = requests.Session()
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.4))
    for ax, (bbox, z, title, radius) in zip(axes, PANELS):
        draw_panel(ax, geo, bbox, z, title, radius, session)

    legend = [
        Line2D([0], [0], marker='^', color='none', markerfacecolor=SITE_COLOR,
               markeredgecolor='white', markersize=12, label='Launch site'),
        Line2D([0], [0], marker='o', color='none', markerfacecolor=SUCCESS_COLOR,
               markeredgecolor='white', markersize=10, label='Landing success'),
        Line2D([0], [0], marker='o', color='none', markerfacecolor=FAILURE_COLOR,
               markeredgecolor='white', markersize=10, label='Landing failure / no attempt'),
    ]
    fig.legend(handles=legend, loc='lower center', ncol=3, frameon=False, fontsize=11)

    total, landed = len(geo), int(geo['class'].sum())
    fig.suptitle(f'SpaceX launch sites and landing outcomes — {total} launch records, '
                 f'{landed} successful landings',
                 fontsize=15, fontweight='bold', color='#1a1a2e')
    fig.text(0.995, 0.005, 'Basemap © OpenStreetMap contributors',
             ha='right', fontsize=8, color='#666666')
    fig.tight_layout(rect=[0, 0.07, 1, 0.95])

    out = f'{ROOT}/images/folium_static_view.png'
    fig.savefig(out, dpi=150, facecolor='white', bbox_inches='tight')
    print('Saved', out)
    print(geo.groupby('Launch Site')['class'].agg(launches='size', landed='sum'))


if __name__ == '__main__':
    main()
