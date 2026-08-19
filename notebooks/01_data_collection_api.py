"""
Phase 1: Data Collection - SpaceX REST API
============================================
Goal: Pull Falcon 9 launch records from the SpaceX API and build a clean
dataframe with one row per launch, including booster, payload, and
launch-site details we'll need later to predict first-stage landing success.

API docs: https://github.com/r-spacex/SpaceX-API
"""

import requests
import pandas as pd
import numpy as np
import datetime
import json

import os
# Repo root, resolved relative to this file so the script runs from any checkout.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pd.set_option('display.max_columns', None)

# ---------------------------------------------------------------
# Step 1: Get all past launches
# ---------------------------------------------------------------
spacex_url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)
print("Status code:", response.status_code)

data = pd.json_normalize(response.json())
print("Raw launches pulled:", data.shape)
print(data.columns.tolist())

# Keep only the columns we need, and only launches that used Falcon 9
# (Falcon 1 launches are early/irrelevant to this landing-prediction task)
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# Drop rows with multiple cores or multiple payloads (complex multi-manifest
# launches) to keep one booster <-> one payload per row, per IBM's spec
data = data[data['cores'].map(len) == 1]
data = data[data['payloads'].map(len) == 1]

# Extract single values from the list columns
data['cores'] = data['cores'].map(lambda x: x[0])
data['payloads'] = data['payloads'].map(lambda x: x[0])

# Convert date and keep launches up to a cutoff date (per IBM lab spec)
data['date'] = pd.to_datetime(data['date_utc']).dt.date
data = data[data['date'] <= datetime.date(2020, 11, 13)]

print("\nAfter filtering to single-core/single-payload Falcon 9 launches:", data.shape)

# ---------------------------------------------------------------
# Step 2: Helper functions to look up booster / payload / launchpad /
# core details from their respective API endpoints (the /launches
# endpoint only gives IDs, not the actual attributes)
# ---------------------------------------------------------------

BoosterVersion, PayloadMass, Orbit, LaunchSite = [], [], [], []
Outcome, Flights, GridFins, Reused, Legs, LandingPad = [], [], [], [], [], []
Block, ReusedCount, Serial, Longitude, Latitude = [], [], [], [], []

def getBoosterVersion(data):
    for x in data['rocket']:
        if x:
            r = requests.get("https://api.spacexdata.com/v4/rockets/" + str(x)).json()
            BoosterVersion.append(r['name'])

def getLaunchSite(data):
    for x in data['launchpad']:
        if x:
            r = requests.get("https://api.spacexdata.com/v4/launchpads/" + str(x)).json()
            Longitude.append(r['longitude'])
            Latitude.append(r['latitude'])
            LaunchSite.append(r['name'])

def getPayloadData(data):
    for load in data['payloads']:
        if load:
            r = requests.get("https://api.spacexdata.com/v4/payloads/" + str(load)).json()
            PayloadMass.append(r.get('mass_kg'))
            Orbit.append(r.get('orbit'))

def getCoreData(data):
    for core in data['cores']:
        if core['core'] is not None:
            r = requests.get("https://api.spacexdata.com/v4/cores/" + str(core['core'])).json()
            Block.append(r.get('block'))
            ReusedCount.append(r.get('reuse_count'))
            Serial.append(r.get('serial'))
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core['landing_success']) + ' ' + str(core['landing_type']))
        Flights.append(core['flight'])
        GridFins.append(core['gridfins'])
        Reused.append(core['reused'])
        Legs.append(core['legs'])
        LandingPad.append(core['landpad'])

print("\nFetching booster versions...")
getBoosterVersion(data)
print("Fetching launch sites...")
getLaunchSite(data)
print("Fetching payload data...")
getPayloadData(data)
print("Fetching core data...")
getCoreData(data)

# ---------------------------------------------------------------
# Step 3: Assemble the final dataframe
# ---------------------------------------------------------------
launch_dict = {
    'FlightNumber': list(data['flight_number']),
    'Date': list(data['date']),
    'BoosterVersion': BoosterVersion,
    'PayloadMass': PayloadMass,
    'Orbit': Orbit,
    'LaunchSite': LaunchSite,
    'Outcome': Outcome,
    'Flights': Flights,
    'GridFins': GridFins,
    'Reused': Reused,
    'Legs': Legs,
    'LandingPad': LandingPad,
    'Block': Block,
    'ReusedCount': ReusedCount,
    'Serial': Serial,
    'Longitude': Longitude,
    'Latitude': Latitude
}

df = pd.DataFrame(launch_dict)

# Keep only Falcon 9 (drop Falcon 1)
df = df[df['BoosterVersion'] != 'Falcon 1']
df['FlightNumber'] = list(range(1, df.shape[0] + 1))

print("\nFinal API dataframe shape:", df.shape)
print(df.head())

df.to_csv(f'{ROOT}/data/spacex_api_raw.csv', index=False)
print("\nSaved to data/spacex_api_raw.csv")
