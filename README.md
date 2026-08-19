# SpaceX Falcon 9 First-Stage Landing Prediction

IBM Applied Data Science Capstone — Aaron Vargas

Predicting whether a Falcon 9 first stage will land successfully, so a competing
launch provider can estimate SpaceX's true reusable-launch cost advantage.
Across 90 Falcon 9 launches (2010 – Nov 2020) the landing success rate was 66.7%;
Logistic Regression reached 83.3% test accuracy.

## Deliverables

| File | Description |
| --- | --- |
| [Data_Science_Capstone_Presentation.pdf](Data_Science_Capstone_Presentation.pdf) | 19-slide presentation (PDF submission) |
| [Data_Science_Capstone_Presentation.pptx](Data_Science_Capstone_Presentation.pptx) | Editable source of the presentation |
| [Data_Science_Capstone_Project_Report.pdf](Data_Science_Capstone_Project_Report.pdf) | Written project report (PDF submission) |
| [Data_Science_Capstone_Project_Report.docx](Data_Science_Capstone_Project_Report.docx) | Editable source of the report |

## Project stages

| Stage | Code |
| --- | --- |
| Data collection — SpaceX REST API | [notebooks/01_data_collection_api.py](notebooks/01_data_collection_api.py) |
| Data collection — Wikipedia web scraping | [notebooks/02_web_scraping.py](notebooks/02_web_scraping.py) |
| Data wrangling and label engineering | [notebooks/03_data_wrangling.py](notebooks/03_data_wrangling.py) |
| EDA with visualization, EDA with SQL, predictive analysis | [notebooks/04_07_eda_sql_ml.py](notebooks/04_07_eda_sql_ml.py) |
| Interactive Folium map and proximity analysis | [notebooks/06_folium_map.py](notebooks/06_folium_map.py) |
| Static launch-site map render (for the deck and report) | [notebooks/06b_static_map_fallback.py](notebooks/06b_static_map_fallback.py) |
| Static proximity-analysis map render | [notebooks/06c_proximity_map_render.py](notebooks/06c_proximity_map_render.py) |
| Shared OpenStreetMap tile helpers | [notebooks/mapping.py](notebooks/mapping.py) |
| Dash chart renders | [notebooks/07_dash_charts.py](notebooks/07_dash_charts.py) |
| Plotly Dash application | [dashboard/app.py](dashboard/app.py) |

## Repository layout

- `notebooks/` — analysis scripts, one per capstone stage
- `dashboard/` — Plotly Dash app (`python dashboard/app.py`, then open http://127.0.0.1:8050)
- `data/` — source and derived datasets, plus `ml_summary.json` with model results
- `images/` — chart, map, and dashboard renders used in the report and slides
- Map renders use OpenStreetMap tiles and require network access; basemaps © OpenStreetMap contributors
- `build_pptx.js` / `build_docx.js` — scripts that generate the presentation and report

## Results summary

| Model | CV score | Test accuracy |
| --- | --- | --- |
| Logistic Regression (best) | 0.821 | 0.833 |
| SVM | 0.834 | 0.833 |
| KNN | 0.834 | 0.833 |
| Decision Tree | 0.804 | 0.778 |

Logistic Regression was selected as the best model: it ties SVM and KNN on accuracy
while remaining the most interpretable and the cheapest to retrain.
