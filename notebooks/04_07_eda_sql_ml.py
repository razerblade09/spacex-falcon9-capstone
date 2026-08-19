"""
Phases 4-7 combined (fast track): EDA Visualization, EDA SQL, Folium map,
and Predictive Analysis (ML models).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
IMG = f'{ROOT}/images/'
DATA = f'{ROOT}/data/'

df = pd.read_csv(DATA + 'dataset_part_2.csv')
print("Loaded dataset_part_2:", df.shape)

# =================================================================
# PHASE 4: EDA WITH VISUALIZATION
# =================================================================

# --- Chart 1: Flight Number vs Launch Site, colored by outcome
plt.figure(figsize=(9, 5))
sns.scatterplot(data=df, x='FlightNumber', y='LaunchSite', hue='Class', palette=['#E4572E', '#17BEBB'], s=80)
plt.title('Launch Site vs Flight Number (by Landing Outcome)', fontsize=13, fontweight='bold')
plt.xlabel('Flight Number'); plt.ylabel('Launch Site')
plt.legend(title='Class', labels=['Failure', 'Success'])
plt.tight_layout(); plt.savefig(IMG + 'eda_flightnum_site.png', dpi=150); plt.close()

# --- Chart 2: Payload Mass vs Launch Site, colored by outcome
plt.figure(figsize=(9, 5))
sns.scatterplot(data=df, x='PayloadMass', y='LaunchSite', hue='Class', palette=['#E4572E', '#17BEBB'], s=80)
plt.title('Payload Mass vs Launch Site (by Landing Outcome)', fontsize=13, fontweight='bold')
plt.xlabel('Payload Mass (kg)'); plt.ylabel('Launch Site')
plt.legend(title='Class', labels=['Failure', 'Success'])
plt.tight_layout(); plt.savefig(IMG + 'eda_payload_site.png', dpi=150); plt.close()

# --- Chart 3: Success rate by Orbit type (bar chart)
orbit_success = df.groupby('Orbit')['Class'].mean().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
orbit_success.plot(kind='bar', color='#3B60E4')
plt.title('Landing Success Rate by Orbit Type', fontsize=13, fontweight='bold')
plt.ylabel('Success Rate'); plt.xlabel('Orbit')
plt.xticks(rotation=45)
plt.tight_layout(); plt.savefig(IMG + 'eda_orbit_success.png', dpi=150); plt.close()

# --- Chart 4: Flight Number vs Orbit, colored by outcome
plt.figure(figsize=(9, 5))
sns.scatterplot(data=df, x='FlightNumber', y='Orbit', hue='Class', palette=['#E4572E', '#17BEBB'], s=80)
plt.title('Flight Number vs Orbit Type (by Landing Outcome)', fontsize=13, fontweight='bold')
plt.legend(title='Class', labels=['Failure', 'Success'])
plt.tight_layout(); plt.savefig(IMG + 'eda_flightnum_orbit.png', dpi=150); plt.close()

# --- Chart 5: Payload vs Orbit
plt.figure(figsize=(9, 5))
sns.scatterplot(data=df, x='PayloadMass', y='Orbit', hue='Class', palette=['#E4572E', '#17BEBB'], s=80)
plt.title('Payload Mass vs Orbit Type (by Landing Outcome)', fontsize=13, fontweight='bold')
plt.legend(title='Class', labels=['Failure', 'Success'])
plt.tight_layout(); plt.savefig(IMG + 'eda_payload_orbit.png', dpi=150); plt.close()

# --- Chart 6: Yearly success trend
df['Year'] = pd.to_datetime(df['Date']).dt.year
yearly = df.groupby('Year')['Class'].mean()
plt.figure(figsize=(9, 5))
plt.plot(yearly.index, yearly.values, marker='o', linewidth=2.5, color='#3B60E4')
plt.title('Launch Success Rate by Year', fontsize=13, fontweight='bold')
plt.xlabel('Year'); plt.ylabel('Success Rate'); plt.ylim(0, 1.05)
plt.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig(IMG + 'eda_yearly_trend.png', dpi=150); plt.close()

print("EDA visualization charts saved (6 charts)")

# =================================================================
# PHASE 5: EDA WITH SQL
# =================================================================
spacex_raw = pd.read_csv(DATA + 'Spacex.csv')
conn = sqlite3.connect(':memory:')
spacex_raw.to_sql('SPACEXTABLE', conn, index=False, if_exists='replace')

queries = {}

queries['distinct_launch_sites'] = pd.read_sql(
    "SELECT DISTINCT Launch_Site FROM SPACEXTABLE;", conn)

queries['ksc_sites_sample'] = pd.read_sql(
    "SELECT * FROM SPACEXTABLE WHERE Launch_Site LIKE 'KSC%' LIMIT 5;", conn)

queries['total_nasa_crs_payload'] = pd.read_sql(
    "SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass FROM SPACEXTABLE WHERE Customer = 'NASA (CRS)';", conn)

queries['avg_payload_f9v1_1'] = pd.read_sql(
    "SELECT AVG(PAYLOAD_MASS__KG_) AS Avg_Payload_Mass FROM SPACEXTABLE WHERE Booster_Version LIKE 'F9 v1.1%';", conn)

queries['first_success_ground_pad'] = pd.read_sql(
    "SELECT MIN(Date) AS First_Success_Ground_Pad FROM SPACEXTABLE WHERE \"Landing _Outcome\" = 'Success (ground pad)';", conn)

queries['boosters_4000_6000_success_drone'] = pd.read_sql(
    """SELECT DISTINCT Booster_Version FROM SPACEXTABLE
       WHERE \"Landing _Outcome\" = 'Success (drone ship)'
       AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000;""", conn)

queries['mission_outcome_counts'] = pd.read_sql(
    "SELECT Mission_Outcome, COUNT(*) AS Count FROM SPACEXTABLE GROUP BY Mission_Outcome;", conn)

queries['max_payload_booster'] = pd.read_sql(
    """SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTABLE
       WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE);""", conn)

queries['failure_landings_2015'] = pd.read_sql(
    """SELECT Booster_Version, Launch_Site, \"Landing _Outcome\" FROM SPACEXTABLE
       WHERE \"Landing _Outcome\" LIKE 'Failure%' AND substr(Date,7,4) = '2015';""", conn)

queries['landing_outcome_ranking_2010_2017'] = pd.read_sql(
    """SELECT \"Landing _Outcome\", COUNT(*) AS Count FROM SPACEXTABLE
       WHERE Date BETWEEN '04-06-2010' AND '20-03-2017'
       GROUP BY \"Landing _Outcome\" ORDER BY Count DESC;""", conn)

for name, result in queries.items():
    print(f"\n--- {name} ---")
    print(result)

conn.close()
print("\nSQL analysis complete (10 queries)")

# =================================================================
# PHASE 7: PREDICTIVE ANALYSIS (ML MODELS)
# =================================================================
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

df3 = pd.read_csv(DATA + 'dataset_part_3.csv')
Y = pd.read_csv(DATA + 'dataset_part_2.csv')['Class']
X = df3.copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)
print(f"\nTrain shape: {X_train.shape}, Test shape: {X_test.shape}")

results = {}

# --- Logistic Regression
lr = LogisticRegression(max_iter=1000)
params_lr = {'C': [0.01, 0.1, 1, 10, 100], 'penalty': ['l2'], 'solver': ['lbfgs']}
gs_lr = GridSearchCV(lr, params_lr, cv=10)
gs_lr.fit(X_train, Y_train)
results['Logistic Regression'] = (gs_lr, gs_lr.score(X_test, Y_test))

# --- SVM
svm = SVC()
params_svm = {'kernel': ['linear', 'rbf', 'poly'], 'C': [0.01, 1, 10], 'gamma': [0.01, 1]}
gs_svm = GridSearchCV(svm, params_svm, cv=10)
gs_svm.fit(X_train, Y_train)
results['SVM'] = (gs_svm, gs_svm.score(X_test, Y_test))

# --- Decision Tree
dt = DecisionTreeClassifier(random_state=2)
params_dt = {'criterion': ['gini', 'entropy'], 'max_depth': [2, 4, 6, 8, 10], 'min_samples_split': [2, 5, 10]}
gs_dt = GridSearchCV(dt, params_dt, cv=10)
gs_dt.fit(X_train, Y_train)
results['Decision Tree'] = (gs_dt, gs_dt.score(X_test, Y_test))

# --- KNN
knn = KNeighborsClassifier()
params_knn = {'n_neighbors': list(range(1, 11)), 'p': [1, 2]}
gs_knn = GridSearchCV(knn, params_knn, cv=10)
gs_knn.fit(X_train, Y_train)
results['KNN'] = (gs_knn, gs_knn.score(X_test, Y_test))

print("\n=== MODEL COMPARISON ===")
for name, (model, acc) in results.items():
    print(f"{name}: best params={model.best_params_}, CV score={model.best_score_:.3f}, Test accuracy={acc:.3f}")

best_name = max(results, key=lambda k: results[k][1])
best_model, best_acc = results[best_name]
print(f"\nBEST MODEL: {best_name} (test accuracy = {best_acc:.3f})")

# Confusion matrix for best model
yhat = best_model.predict(X_test)
cm = confusion_matrix(Y_test, yhat)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['Did not land', 'Landed'], yticklabels=['Did not land', 'Landed'])
plt.title(f'Confusion Matrix - {best_name}', fontsize=13, fontweight='bold')
plt.xlabel('Predicted'); plt.ylabel('Actual')
plt.tight_layout(); plt.savefig(IMG + 'confusion_matrix_best.png', dpi=150); plt.close()

# Bar chart comparing all 4 model accuracies
plt.figure(figsize=(8, 5))
names = list(results.keys())
accs = [results[n][1] for n in names]
colors = ['#17BEBB' if n == best_name else '#3B60E4' for n in names]
plt.bar(names, accs, color=colors)
plt.title('Model Comparison - Test Accuracy', fontsize=13, fontweight='bold')
plt.ylabel('Accuracy'); plt.ylim(0, 1)
for i, v in enumerate(accs):
    plt.text(i, v + 0.02, f'{v:.2f}', ha='center', fontweight='bold')
plt.tight_layout(); plt.savefig(IMG + 'model_comparison.png', dpi=150); plt.close()

print("\nML charts saved: confusion_matrix_best.png, model_comparison.png")

# Save summary for report generation
import json

import os
# Repo root, resolved relative to this file so the script runs from any checkout.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
summary = {
    'best_model': best_name,
    'best_accuracy': round(best_acc, 3),
    'best_params': str(best_model.best_params_),
    'all_results': {n: round(a, 3) for n, (m, a) in results.items()},
    'confusion_matrix': cm.tolist(),
    'success_rate_overall': round(df['Class'].mean(), 3),
    'orbit_success': orbit_success.round(3).to_dict(),
    'total_launches': len(df)
}
with open(f'{ROOT}/data/ml_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
print("\nSaved ml_summary.json")
