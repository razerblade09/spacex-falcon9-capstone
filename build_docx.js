const { Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun, Table, TableRow, TableCell,
        WidthType, ShadingType, AlignmentType, BorderStyle, PageBreak, ExternalHyperlink } = require("docx");
const fs = require("fs");

const IMG = "/home/claude/capstone/images/";
const GITHUB_URL = "https://github.com/YOUR-USERNAME/spacex-falcon9-capstone"; // <-- replace after you push your repo
const NAVY = "0B1F3A";
const BLUE = "3B60E4";
const GREY = "444444";

function h1(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 160 } });
}
function h2(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 } });
}
function p(text, opts = {}) {
  return new Paragraph({ children: [new TextRun({ text, size: 22, ...opts })], spacing: { after: 160 } });
}
function bullet(text) {
  return new Paragraph({ text, bullet: { level: 0 }, spacing: { after: 80 } });
}
function githubLink(url) {
  return new Paragraph({
    spacing: { after: 200 },
    children: [
      new TextRun({ text: "GitHub repository: ", bold: true, size: 21 }),
      new ExternalHyperlink({
        link: url,
        children: [new TextRun({ text: url, style: "Hyperlink", size: 21 })]
      })
    ]
  });
}
function img(filename, width = 550) {
  const data = fs.readFileSync(IMG + filename);
  // maintain rough aspect ratio; charts are ~ 9x5.5 or similar
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [ new ImageRun({ data, transformation: { width: width, height: Math.round(width * 0.62) }, type: "png" }) ]
  });
}
function caption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 260 },
    children: [ new TextRun({ text, italics: true, size: 19, color: "666666" }) ]
  });
}
function simpleTable(headerRow, rows, colWidths) {
  const mkCell = (text, isHeader) => new TableCell({
    width: { size: 2000, type: WidthType.DXA },
    shading: isHeader ? { type: ShadingType.CLEAR, fill: BLUE } : undefined,
    children: [ new Paragraph({ children: [ new TextRun({ text: String(text), bold: isHeader, color: isHeader ? "FFFFFF" : "000000", size: 20 }) ] }) ]
  });
  const trs = [ new TableRow({ children: headerRow.map(t => mkCell(t, true)) }) ];
  rows.forEach(r => trs.push(new TableRow({ children: r.map(t => mkCell(t, false)) })));
  return new Table({ rows: trs, width: { size: 9000, type: WidthType.DXA }, columnWidths: colWidths });
}

const children = [];

// ---------------- TITLE PAGE ----------------
children.push(
  new Paragraph({ text: "", spacing: { after: 1600 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [ new TextRun({ text: "Data Science Capstone Project Report", bold: true, size: 44, color: NAVY }) ], spacing: { after: 200 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [ new TextRun({ text: "SpaceX Falcon 9 First-Stage Landing Prediction", size: 28, color: BLUE }) ], spacing: { after: 800 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [ new TextRun({ text: "Prepared by: [Your Name]", size: 22 }) ] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [ new TextRun({ text: "IBM Applied Data Science Capstone", size: 22 }) ] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [ new TextRun({ text: new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }), size: 22 }) ] }),
  new Paragraph({ children: [ new PageBreak() ] })
);

// ---------------- 1.1/1.2 LINKS ----------------
children.push(h1("Project Links"));
children.push(githubLink(GITHUB_URL));
children.push(p("Presentation slides (PDF): Data_Science_Capstone_Presentation.pdf (submitted alongside this report)."));

// ---------------- EXECUTIVE SUMMARY ----------------
children.push(h1("Executive Summary"));
children.push(p("This project follows the full data science methodology — data collection, wrangling, exploratory analysis, interactive visualization, and predictive modeling — to solve a real business problem: predicting whether a SpaceX Falcon 9 first-stage booster will land successfully after launch."));
children.push(p("Methods used: launch data was collected from the SpaceX REST API and by scraping Wikipedia's Falcon 9 launch history; the two sources were cross-checked and merged. The data was cleaned, missing values were imputed, and a binary landing-success label was engineered from raw outcome text. Exploratory analysis used both visualization (scatter plots, bar charts, a yearly trend line) and direct SQL querying. Two interactive tools — a Folium map and a Plotly Dash app — were built for stakeholder self-service exploration. Finally, four classifiers (Logistic Regression, SVM, Decision Tree, KNN) were trained and tuned with 10-fold GridSearchCV."));
children.push(p("Key results: across 90 Falcon 9 launches (2010–Nov 2020), the overall first-stage landing success rate was 66.7%. Logistic Regression, SVM, and KNN all reached 83.3% test accuracy; Logistic Regression was selected as the best model for its interpretability. Success rate correlates strongly with orbit type (light LEO/ISS missions land far more reliably than heavy GTO missions) and improved steadily year over year as SpaceX matured its recovery process."));

// ---------------- INTRODUCTION ----------------
children.push(h1("Introduction"));
children.push(p("Background: SpaceX advertises Falcon 9 launches at $62 million, versus $165 million or more from other providers, largely because SpaceX reuses the first stage instead of discarding it after every flight. If the first stage does not land successfully, the true cost of a launch changes substantially."));
children.push(p("Problem statement: this project assumes the role of a data scientist for a startup competing with SpaceX. The goal is to predict, from historical and publicly available launch parameters, whether the first stage will land successfully — enabling an accurate cost estimate for a competing bid."));
children.push(h2("Objectives"));
["Collect and clean historical Falcon 9 launch data from multiple sources",
 "Identify which launch parameters correlate with landing success",
 "Visualize patterns across launch sites, orbits, and time",
 "Build and evaluate a machine-learning classifier for landing outcome"].forEach(b => children.push(bullet(b)));

// ---------------- DATA COLLECTION - API ----------------
children.push(h1("Data Collection – SpaceX API"));
children.push(p("The SpaceX v4 REST API (api.spacexdata.com) was queried for all past launches. Each launch record was filtered to single-core, single-payload Falcon 9 flights, then enriched by calling the /rockets, /launchpads, /payloads, and /cores endpoints to resolve IDs into readable attributes (booster version, launch site name/coordinates, payload mass, orbit, landing outcome, grid fins, reused flag, legs, landing pad, booster block, and serial)."));
children.push(p("Result: 90 clean Falcon 9 launch records spanning 2010 through November 2020, one row per launch."));
children.push(githubLink(GITHUB_URL + "/blob/main/notebooks/01_data_collection_api.py"));

// ---------------- DATA COLLECTION - SCRAPING ----------------
children.push(h1("Data Collection – Web Scraping"));
children.push(p("As a second, independent source, the Wikipedia page \"List of Falcon 9 and Falcon Heavy launches\" was scraped using requests and BeautifulSoup. HTML tables were located, column headers extracted programmatically, and each table row parsed into flight number, date/time, booster version, launch site, payload, payload mass, orbit, customer, launch outcome, and booster landing outcome."));
children.push(p("This scraped dataset cross-validates the API data and was also loaded directly into a SQL database for the EDA-with-SQL phase below."));
children.push(githubLink(GITHUB_URL + "/blob/main/notebooks/02_web_scraping.py"));

// ---------------- DATA WRANGLING ----------------
children.push(h1("Data Wrangling Methodology"));
children.push(p("Missing values: PayloadMass was missing for 5.6% of records and was filled with the column mean. LandingPad was missing for 28.9% of records — this was left as-is, since a null landing pad legitimately indicates no ground/drone-ship landing occurred (e.g., an ocean landing or no landing attempt)."));
children.push(p("Label engineering: the raw Outcome field (free-text strings such as \"True ASDS\", \"False Ocean\", \"None None\") was converted into a single binary Class column: 1 if the booster landed successfully by any method (drone ship, ground pad, RTLS return, or ocean-controlled), 0 if it did not land or no attempt was made."));
children.push(p("Result: of 90 launches, 60 (66.7%) resulted in a successful first-stage landing and 30 (33.3%) did not — this is the target variable for the predictive model."));
children.push(githubLink(GITHUB_URL + "/blob/main/notebooks/03_data_wrangling.py"));

// ---------------- EDA WITH DATA VIZ ----------------
children.push(h1("EDA with Data Visualization"));
children.push(p("Flight number, payload mass, orbit type, and launch year were plotted against landing outcome to surface which factors correlate with success."));
children.push(img("eda_flightnum_site.png"));
children.push(caption("Figure 1. Flight number vs. launch site, colored by landing outcome."));
children.push(img("eda_payload_site.png"));
children.push(caption("Figure 2. Payload mass vs. launch site, colored by landing outcome."));
children.push(img("eda_orbit_success.png"));
children.push(caption("Figure 3. Landing success rate by orbit type."));
children.push(img("eda_flightnum_orbit.png"));
children.push(caption("Figure 4. Flight number vs. orbit type, colored by landing outcome."));
children.push(img("eda_payload_orbit.png"));
children.push(caption("Figure 5. Payload mass vs. orbit type, colored by landing outcome."));
children.push(img("eda_yearly_trend.png"));
children.push(caption("Figure 6. Landing success rate by year (2010–2020)."));
children.push(p("Summary: GTO and ISS-orbit missions (heavier, higher-energy trajectories) show lower success rates than LEO/SSO/GEO missions. Success rate climbed from near 0% in 2010–2013 to consistently near 100% by 2019–2020, reflecting SpaceX's iterative refinement of the recovery process rather than a static hardware property."));
children.push(githubLink(GITHUB_URL + "/blob/main/notebooks/04_07_eda_sql_ml.py"));

// ---------------- EDA WITH SQL ----------------
children.push(h1("EDA with SQL"));
children.push(p("The scraped launch table was loaded into a SQL database (SQLite for this report; IBM Db2 in the original lab environment) as SPACEXTABLE, then queried directly to answer specific business questions:"));
[
 "Distinct launch sites used",
 "Total payload mass carried for NASA (CRS) missions",
 "Average payload mass for F9 v1.1 boosters",
 "Date of the first successful ground-pad landing",
 "Boosters that succeeded on a drone ship carrying 4,000–6,000 kg",
 "Count of each mission outcome (success/failure)",
 "Booster(s) carrying the maximum payload mass",
 "Failed drone-ship landings in 2015",
 "Ranking of landing outcomes between 2010 and 2017"
].forEach(q => children.push(bullet(q)));

children.push(h2("Selected Results"));
children.push(simpleTable(
  ["Query", "Result"],
  [
    ["Distinct launch sites", "CCAFS LC-40, CCAFS SLC-40, KSC LC-39A, VAFB SLC-4E"],
    ["Total payload for NASA (CRS)", "45,596 kg"],
    ["Avg. payload, F9 v1.1 boosters", "2,534.7 kg"],
    ["First successful ground-pad landing", "1 May 2017"],
    ["Max payload carried", "15,600 kg (F9 B5)"],
    ["Failed drone-ship landings in 2015", "2 (F9 v1.1 B1012, B1015 — CCAFS LC-40)"],
  ],
  [3500, 5500]
));
children.push(new Paragraph({ text: "", spacing: { after: 200 } }));
children.push(h2("Landing Outcome Ranking, 2010–2017"));
children.push(simpleTable(
  ["Landing Outcome", "Count"],
  [
    ["Success", "20"], ["No attempt", "10"], ["Success (drone ship)", "8"],
    ["Success (ground pad)", "6"], ["Failure (drone ship)", "4"], ["Failure", "3"],
    ["Controlled (ocean)", "3"], ["Failure (parachute)", "2"]
  ],
  [6500, 2500]
));
children.push(new Paragraph({ text: "", spacing: { after: 200 } }));
children.push(githubLink(GITHUB_URL + "/blob/main/notebooks/04_07_eda_sql_ml.py"));

// ---------------- INTERACTIVE VISUAL ANALYTICS ----------------
children.push(h1("Interactive Visual Analytics"));
children.push(h2("Folium Map"));
children.push(p("An interactive Folium map plots all 4 launch sites and every individual launch (55 geocoded records), colored green for a successful landing and red for a failed/no-attempt landing. A proximity analysis was also computed: using the haversine formula, the distance from KSC LC-39A to the nearest coastline point is 7.43 km, and to the nearest city (Titusville area) is 20.50 km — consistent with real launch-site safety requirements (close to open water for downrange safety, a safe distance from population centers)."));
children.push(img("folium_static_view.png"));
children.push(caption("Figure 7. Static rendering of the interactive Folium map (launch sites and per-launch outcomes)."));
children.push(githubLink(GITHUB_URL + "/blob/main/notebooks/06_folium_map.py"));

children.push(h2("Plotly Dash App"));
children.push(p("A Plotly Dash dashboard (dashboard/app.py) provides a dropdown to filter by launch site, a live-updating pie chart of success rate, and a payload-vs-outcome scatter plot filterable by a payload-mass range slider."));
children.push(img("dash_pie_all_sites.png", 400));
children.push(caption("Figure 8. Share of total successful landings contributed by each launch site."));
children.push(img("dash_payload_scatter.png"));
children.push(caption("Figure 9. Payload mass vs. launch outcome, colored by booster version category."));
children.push(p("Newer booster generations (FT, B4, B5) succeed reliably across a much wider payload range than early versions (v1.0, v1.1) — visual confirmation that booster maturity, not just payload mass alone, drives landing success."));
children.push(githubLink(GITHUB_URL + "/blob/main/dashboard/app.py"));

// ---------------- PREDICTIVE ANALYSIS ----------------
children.push(h1("Predictive Analysis"));
children.push(h2("Methodology"));
children.push(p("Features: 80 one-hot-encoded columns (orbit, launch site, landing pad, booster serial) plus flight number, payload mass, flight count, grid fins, reused flag, legs, and booster block — standardized with StandardScaler. Data was split 80/20 into train (72 launches) and test (18 launches) sets."));
children.push(p("Four classifiers were trained and tuned via 10-fold GridSearchCV: Logistic Regression (C, penalty, solver), Support Vector Machine (kernel, C, gamma), Decision Tree (criterion, max_depth, min_samples_split), and K-Nearest Neighbors (n_neighbors, distance metric)."));

children.push(h2("Evaluation Results"));
children.push(simpleTable(
  ["Model", "CV Score", "Test Accuracy"],
  [
    ["Logistic Regression", "0.821", "0.833"],
    ["SVM", "0.834", "0.833"],
    ["KNN", "0.834", "0.833"],
    ["Decision Tree", "0.804", "0.778"],
  ],
  [4500, 2500, 2500]
));
children.push(new Paragraph({ text: "", spacing: { after: 200 } }));
children.push(img("model_comparison.png", 450));
children.push(caption("Figure 10. Test accuracy comparison across all four models."));
children.push(img("confusion_matrix_best.png", 350));
children.push(caption("Figure 11. Confusion matrix for the best model (Logistic Regression)."));
children.push(p("Reading the confusion matrix (18 test launches): 12 successful landings correctly predicted, 3 unsuccessful landings correctly predicted, 3 unsuccessful landings misclassified as successful, and 0 successful landings missed. The model never misses a true landing, which is the more conservative error direction for cost estimation."));

children.push(h2("Best Model"));
children.push(p("Logistic Regression (C=1, L2 penalty, lbfgs solver) was selected as the best model. It ties SVM and KNN on raw test accuracy (83.3%) but is far more interpretable — each feature's coefficient directly shows its effect on landing-success odds, which matters when explaining a cost bid to non-technical stakeholders. It is also the cheapest of the four to retrain as new launch data becomes available."));

children.push(h2("Conclusion"));
[
 "Landing success is highly learnable from launch parameters — 83.3% test accuracy from a simple, interpretable model.",
 "Orbit type and payload mass are the strongest predictors; heavier GTO missions land less reliably than light LEO/ISS missions.",
 "Success rate improved dramatically over time (2013 to 2020), reflecting SpaceX's iterative process improvements rather than a fixed hardware property.",
 "Recommendation: a competing launch provider can use this model as a first-pass cost-risk estimator for a Falcon-9-class bid, refining it further as more recent launch data becomes available and by incorporating weather and pad-specific factors in future work."
].forEach(c => children.push(bullet(c)));

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 } } },
    children
  }],
  styles: {
    default: {
      document: { run: { size: 22, font: "Calibri" } }
    }
  }
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/claude/capstone/Data_Science_Capstone_Project_Report.docx", buf);
  console.log("Report saved.");
});
