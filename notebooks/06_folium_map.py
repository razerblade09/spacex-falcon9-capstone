"""
Phase 6: Interactive Visual Analytics - Folium Map
====================================================
Builds an interactive map showing:
  1. All 4 launch site locations as markers
  2. Individual launch records at each site, colored green (success) / red (failure)
  3. Distance lines from the launch site to the nearest coastline, city,
     railway, and highway (proximity analysis)
"""
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from math import sin, cos, sqrt, atan2, radians

import os
# Repo root, resolved relative to this file so the script runs from any checkout.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

geo = pd.read_csv(f'{ROOT}/data/spacex_launch_geo.csv')
geo.columns = geo.columns.str.strip()
print(geo.columns.tolist())
print(geo.shape)

site_df = geo.groupby('Launch Site').first().reset_index()[['Launch Site', 'Lat', 'Long']]
print(site_df)

# Center map on Cape Canaveral / KSC area
site_map = folium.Map(location=[28.57, -80.65], zoom_start=5)

# --- 1. Launch site markers ---
for _, row in site_df.iterrows():
    folium.Circle(
        [row['Lat'], row['Long']], radius=1000, color='#3B60E4', fill=True
    ).add_child(folium.Popup(row['Launch Site'])).add_to(site_map)
    folium.map.Marker(
        [row['Lat'], row['Long']],
        icon=folium.DivIcon(
            icon_size=(150, 36), icon_anchor=(0, 0),
            html=f'<div style="font-size:12px;color:#3B60E4;font-weight:bold">{row["Launch Site"]}</div>'
        )
    ).add_to(site_map)

# --- 2. Individual launch outcomes, clustered ---
marker_cluster = MarkerCluster().add_to(site_map)
for _, row in geo.iterrows():
    color = 'green' if row['class'] == 1 else 'red'
    folium.Marker(
        [row['Lat'], row['Long']],
        icon=folium.Icon(color='white', icon_color=color)
    ).add_to(marker_cluster)

# --- 3. Proximity analysis: distance from KSC LC-39A to nearby features ---
def calculate_distance(lat1, lon1, lat2, lon2):
    """Haversine great-circle distance in km."""
    R = 6373.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

launch_site_lat, launch_site_lon = 28.573255, -80.646895  # KSC LC-39A

# Nearest-feature coordinates. The coastline point was read off the map; the
# city, railway and highway points come from OpenStreetMap (Overpass API) as
# the closest place=city node (Titusville) and the closest node of a way
# tagged railway=rail (NASA Railroad) and highway=secondary (Kennedy Parkway
# North), searched within 25-40 km of the launch site.
PROXIMITY = [
    ('coastline', 28.56367, -80.57163, 'coastline'),
    ('city',      28.61262, -80.80795, 'Titusville'),
    ('railway',   28.57295, -80.65392, 'NASA Railroad'),
    ('highway',   28.57195, -80.65542, 'Kennedy Pkwy N'),
]

distances = {
    key: calculate_distance(launch_site_lat, launch_site_lon, lat, lon)
    for key, lat, lon, _ in PROXIMITY
}

for (key, lat, lon, name) in PROXIMITY:
    label = f'{distances[key]:.2f} KM to {name}'
    folium.Marker(
        [lat, lon],
        icon=folium.DivIcon(icon_size=(220, 36), icon_anchor=(0, 0),
                             html=f'<div style="font-size:11px;color:#d62728;font-weight:bold">{label}</div>')
    ).add_to(site_map)
    folium.PolyLine(
        locations=[[launch_site_lat, launch_site_lon], [lat, lon]],
        weight=2, color='#d62728'
    ).add_to(site_map)

site_map.save(f'{ROOT}/images/launch_site_map.html')
print()
print("Proximity analysis - distances from KSC LC-39A:")
for key, lat, lon, name in PROXIMITY:
    print(f"  {name:<16} {distances[key]:>8.2f} km")
print("Map saved to images/launch_site_map.html")
