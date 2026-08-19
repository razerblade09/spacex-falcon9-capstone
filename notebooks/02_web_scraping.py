"""
Phase 2: Data Collection - Web Scraping
==========================================
Goal: Scrape the Wikipedia "List of Falcon 9 and Falcon Heavy launches"
page and parse the HTML table into a structured dataframe -- flight number,
date, booster version, launch site, payload, orbit, customer, outcome.

Note: run this on a machine with normal internet access (this sandbox's
network is restricted to package registries only, so BeautifulSoup can't
reach Wikipedia from here). The parsing logic below is the real,
working IBM-lab approach.
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import unicodedata

import os
# Repo root, resolved relative to this file so the script runs from any checkout.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"


def date_time(table_cells):
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out

def landing_status(table_cells):
    out = [i for i in table_cells.strings][0]
    return out

def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass

def extract_column_from_header(row):
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
    colunm_name = ' '.join(row.contents)
    if not colunm_name.strip().isdigit():
        colunm_name = colunm_name.strip()
        return colunm_name


# ---------------------------------------------------------------
# Step 1: Request the page and parse with BeautifulSoup
# ---------------------------------------------------------------
response = requests.get(static_url)
soup = BeautifulSoup(response.text, 'html.parser')
print("Page title:", soup.title.string)

# ---------------------------------------------------------------
# Step 2: Find all wikitable elements, extract column headers
# ---------------------------------------------------------------
html_tables = soup.find_all('table', class_='wikitable plainrowheaders collapsible')

column_names = []
first_launch_table = html_tables[2]
for th in first_launch_table.find_all('th'):
    name = extract_column_from_header(th)
    if name is not None and len(name) > 0:
        column_names.append(name)

print("Parsed columns:", column_names)

# ---------------------------------------------------------------
# Step 3: Build the launch_dict and fill it by walking each table row
# ---------------------------------------------------------------
launch_dict = dict.fromkeys(column_names)
del launch_dict['Date and time ( )']

launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
launch_dict['Version Booster'] = []
launch_dict['Booster landing'] = []
launch_dict['Date'] = []
launch_dict['Time'] = []

extracted_row = 0
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    for rows in table.find_all("tr"):
        if rows.th and rows.th.string:
            flight_number = rows.th.string.strip()
            flag = flight_number.isdigit()
        else:
            flag = False

        row = rows.find_all('td')
        if flag:
            extracted_row += 1
            launch_dict['Flight No.'].append(flight_number)

            datatimelist = date_time(row[0])
            launch_dict['Date'].append(datatimelist[0].strip(','))
            launch_dict['Time'].append(datatimelist[1])

            bv = booster_version(row[1])
            if not bv:
                bv = row[1].a.string if row[1].a else None
            launch_dict['Version Booster'].append(bv)

            launch_dict['Launch site'].append(row[2].a.string if row[2].a else None)
            launch_dict['Payload'].append(row[3].a.string if row[3].a else None)
            launch_dict['Payload mass'].append(get_mass(row[4]))
            launch_dict['Orbit'].append(row[5].a.string if row[5].a else None)
            launch_dict['Customer'].append(row[6].a.string if row[6].a else None)
            launch_dict['Launch outcome'].append(list(row[7].strings)[0])
            launch_dict['Booster landing'].append(landing_status(row[8]))

df = pd.DataFrame({k: pd.Series(v) for k, v in launch_dict.items()})
print("\nScraped shape:", df.shape)
df.to_csv(f'{ROOT}/data/spacex_web_scraped.csv', index=False)
print("Saved to data/spacex_web_scraped.csv")
