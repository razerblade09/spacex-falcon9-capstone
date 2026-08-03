import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

geo = pd.read_csv('/home/claude/capstone/data/spacex_launch_geo.csv')
geo.columns = geo.columns.str.strip()

fig, ax = plt.subplots(figsize=(9, 6))
success = geo[geo['class'] == 1]
fail = geo[geo['class'] == 0]

ax.scatter(fail['Long'], fail['Lat'], c='#E4572E', s=70, label='Failure', edgecolor='white', zorder=3)
ax.scatter(success['Long'], success['Lat'], c='#17BEBB', s=70, label='Success', edgecolor='white', zorder=3)

site_df = geo.groupby('Launch Site').first().reset_index()[['Launch Site', 'Lat', 'Long']]
for _, row in site_df.iterrows():
    ax.scatter(row['Long'], row['Lat'], c='#3B60E4', s=250, marker='^', edgecolor='black', zorder=4)
    ax.annotate(row['Launch Site'], (row['Long'], row['Lat']), textcoords="offset points",
                xytext=(8, 8), fontsize=9, fontweight='bold', color='#3B60E4')

ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude')
ax.set_title('SpaceX Launch Sites & Landing Outcomes (Geographic View)', fontsize=13, fontweight='bold')
ax.legend(loc='lower left')
ax.set_facecolor('#EAF2FF')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/home/claude/capstone/images/folium_static_view.png', dpi=150)
print("Saved folium_static_view.png")
