"""
Phase 3: Data Wrangling
========================
Goal: Turn the raw 'Outcome' string (e.g. "True ASDS", "False Ocean",
"None None") into a single binary target variable 'Class':
    1 = booster landed successfully (any method)
    0 = booster did not land / no landing attempted

This is the label our ML models will predict in Phase 7.
"""

import pandas as pd
import numpy as np

df = pd.read_csv('/home/claude/capstone/data/dataset_part_1.csv')
print("Loaded:", df.shape)

# ---------------------------------------------------------------
# Step 1: Missing value check
# ---------------------------------------------------------------
print("\nMissing values per column:")
print(df.isnull().sum() / len(df) * 100)

# PayloadMass has missing values -> fill with column mean (standard
# approach used in the IBM lab, since dropping rows loses launch records
# we still want for site/orbit analysis)
mean_payload = df['PayloadMass'].mean()
df['PayloadMass'] = df['PayloadMass'].fillna(mean_payload)

# ---------------------------------------------------------------
# Step 2: Landing outcomes breakdown
# ---------------------------------------------------------------
print("\nRaw Outcome value counts:")
print(df['Outcome'].value_counts())

# Outcomes where the first word is "True" or landing type is a real pad
# = a successful landing. "False ..." or "None None" = unsuccessful/no attempt.
bad_outcomes = {'False ASDS', 'None None', 'False Ocean', 'None ASDS', 'False RTLS'}

landing_class = []
for outcome in df['Outcome']:
    if outcome in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)

df['Class'] = landing_class

print("\nClass balance:")
print(df['Class'].value_counts())
print(f"Success rate: {df['Class'].mean()*100:.1f}%")

df.to_csv('/home/claude/capstone/data/dataset_part_2_wrangled.csv', index=False)
print("\nSaved to data/dataset_part_2_wrangled.csv")
