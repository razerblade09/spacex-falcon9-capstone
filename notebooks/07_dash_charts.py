import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os
# Repo root, resolved relative to this file so the script runs from any checkout.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dash_df = pd.read_csv(f'{ROOT}/data/spacex_launch_dash.csv')
dash_df.columns = dash_df.columns.str.strip()
print(dash_df.columns.tolist())

# --- Pie chart: success rate by site (all sites) ---
site_success = dash_df.groupby('Launch Site')['class'].sum()
fig, ax = plt.subplots(figsize=(7, 7))
colors = ['#3B60E4', '#17BEBB', '#E4572E', '#F3A712']
ax.pie(site_success.values, labels=site_success.index, autopct='%1.1f%%',
       colors=colors, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
ax.set_title('Total Successful Launches by Site', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ROOT}/images/dash_pie_all_sites.png', dpi=150)
plt.close()

# --- Pie chart: success vs failure for the top site ---
top_site = dash_df['Launch Site'].value_counts().idxmax()
site_data = dash_df[dash_df['Launch Site'] == top_site]
counts = site_data['class'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(counts.values, labels=['Failure', 'Success'], autopct='%1.1f%%',
       colors=['#E4572E', '#17BEBB'], startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
ax.set_title(f'Success vs Failure - {top_site}', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{ROOT}/images/dash_pie_top_site.png', dpi=150)
plt.close()

# --- Scatter: Payload vs Outcome, colored by booster version category ---
fig, ax = plt.subplots(figsize=(9, 6))
categories = dash_df['Booster Version Category'].unique()
colors_map = plt.cm.tab10(range(len(categories)))
for cat, col in zip(categories, colors_map):
    subset = dash_df[dash_df['Booster Version Category'] == cat]
    ax.scatter(subset['Payload Mass (kg)'], subset['class'], label=cat, color=col, s=70, alpha=0.8, edgecolor='white')
ax.set_yticks([0, 1])
ax.set_yticklabels(['Failure', 'Success'])
ax.set_xlabel('Payload Mass (kg)')
ax.set_title('Payload Mass vs Launch Outcome by Booster Version', fontsize=13, fontweight='bold')
ax.legend(title='Booster Version', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'{ROOT}/images/dash_payload_scatter.png', dpi=150)
plt.close()

print("Dash-style charts saved: dash_pie_all_sites.png, dash_pie_top_site.png, dash_payload_scatter.png")
print(f"Top site: {top_site}")
