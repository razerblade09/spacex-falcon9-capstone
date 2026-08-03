"""
Phase 6: Interactive Visual Analytics - Folium Map
====================================================
Builds an interactive map showing:
  1. All 4 launch site locations as markers
  2. Individual launch records at each site, colored green (success) / red (failure)
  3. Distance lines from a launch site to nearby coastline / city / railway
     (proximity analysis)
"""
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from math import sin, cos, sqrt, atan2, radians

geo = pd.read_csv('/home/claude/capstone/data/spacex_launch_geo.csv')
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

# --- 3. Proximity analysis: distance from KSC LC-39A to nearest coastline point ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

launch_site_lat, launch_site_lon = 28.573255, -80.646895  # KSC LC-39A
coastline_lat, coastline_lon = 28.56367, -80.57163         # nearest coastline point
city_lat, city_lon = 28.3922, -80.6077                      # Titusville / nearby city

d_coast = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
d_city = calculate_distance(launch_site_lat, launch_site_lon, city_lat, city_lon)

for (lat, lon, dist, label) in [
    (coastline_lat, coastline_lon, d_coast, f'{d_coast:.2f} KM'),
    (city_lat, city_lon, d_city, f'{d_city:.2f} KM to city')
]:
    folium.Marker(
        [lat, lon],
        icon=folium.DivIcon(icon_size=(200, 36), icon_anchor=(0, 0),
                             html=f'<div style="font-size:11px;color:#d62728;font-weight:bold">{label}</div>')
    ).add_to(site_map)
    folium.PolyLine(
        locations=[[launch_site_lat, launch_site_lon], [lat, lon]],
        weight=2, color='#d62728'
    ).add_to(site_map)

site_map.save('/home/claude/capstone/images/launch_site_map.html')
print(f"\nDistance KSC LC-39A -> coastline: {d_coast:.2f} km")
print(f"Distance KSC LC-39A -> city: {d_city:.2f} km")
print("Map saved to images/launch_site_map.html")
