const pptxgen = require("pptxgenjs");
const path = require("path");

// Repo root, so the build runs from any checkout.
const ROOT = __dirname;

const IMG = path.join(ROOT, "images") + path.sep;
const GITHUB_URL = "https://github.com/razerblade09/spacex-falcon9-capstone";

const NAVY = "0B1F3A";
const BLUE = "3B60E4";
const TEAL = "17BEBB";
const ORANGE = "E4572E";
const LIGHT = "F4F7FC";
const GREY = "5B6472";

let pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5

function titleBar(slide, kicker, title) {
  slide.addText(kicker.toUpperCase(), {
    x: 0.5, y: 0.35, w: 8, h: 0.3, fontSize: 12, color: BLUE, bold: true, charSpacing: 2
  });
  slide.addText(title, {
    x: 0.5, y: 0.62, w: 12.3, h: 0.7, fontSize: 26, color: NAVY, bold: true
  });
}

function githubFooter(slide, url) {
  slide.addText([{ text: "GitHub: ", options: { color: GREY, bold: true } }, { text: url, options: { color: BLUE, hyperlink: { url: url } } }], {
    x: 0.5, y: 7.1, w: 12.3, h: 0.3, fontSize: 10.5
  });
}

function pageNum(slide, n) {
  slide.addText(String(n), { x: 12.85, y: 7.1, w: 0.4, h: 0.3, fontSize: 10, color: GREY, align: "right" });
}

// ================= SLIDE 1: TITLE =================
let s1 = pres.addSlide();
s1.background = { color: NAVY };
s1.addText("SpaceX Falcon 9\nFirst-Stage Landing Prediction", {
  x: 0.8, y: 2.3, w: 11.7, h: 2.0, fontSize: 40, bold: true, color: "FFFFFF", align: "left"
});
s1.addText("Data Science Capstone Project Report", {
  x: 0.8, y: 4.1, w: 11, h: 0.5, fontSize: 20, color: TEAL
});
s1.addText([
  { text: "GitHub repository (all notebooks and Python files): ", options: { color: "AAB4C8" } },
  { text: GITHUB_URL, options: { color: TEAL, hyperlink: { url: GITHUB_URL } } }
], { x: 0.8, y: 5.15, w: 11.7, h: 0.4, fontSize: 14 });
s1.addText("Presented by: Aaron Vargas   |   " + new Date().toISOString().slice(0,10), {
  x: 0.8, y: 6.6, w: 11, h: 0.4, fontSize: 13, color: "AAB4C8"
});
s1.addShape(pres.ShapeType.rect, { x: 0.8, y: 4.75, w: 2.2, h: 0.06, fill: { color: BLUE } });

// ================= SLIDE 2: EXECUTIVE SUMMARY =================
let s2 = pres.addSlide();
titleBar(s2, "Overview", "Executive Summary");
s2.addText([
  { text: "Methods used: ", options: { bold: true, color: NAVY } },
  { text: "Data was collected via the SpaceX REST API and Wikipedia web scraping, cleaned and labeled, explored with visualization and SQL, mapped geospatially with Folium, and modeled with four classifiers (Logistic Regression, SVM, Decision Tree, KNN) tuned via GridSearchCV.", options: { color: GREY } }
], { x: 0.5, y: 1.6, w: 6.1, h: 2.1, fontSize: 14, lineSpacing: 22 });

s2.addText([
  { text: "Key results: ", options: { bold: true, color: NAVY } },
  { text: `Across ${90} Falcon 9 launches, the overall first-stage landing success rate was ${Math.round(0.667*100)}%. The best-performing model, Logistic Regression, reached ${Math.round(0.833*100)}% test accuracy in predicting landing outcome.`, options: { color: GREY } }
], { x: 6.8, y: 1.6, w: 6.0, h: 2.1, fontSize: 14, lineSpacing: 22 });

const kpis = [
  ["90", "Launches analyzed"],
  ["67%", "Overall landing success rate"],
  ["83.3%", "Best model test accuracy"],
  ["4", "ML models compared"]
];
kpis.forEach((k, i) => {
  const x = 0.5 + i * 3.1;
  s2.addShape(pres.ShapeType.roundRect, { x: x, y: 4.0, w: 2.85, h: 1.5, fill: { color: LIGHT }, line: { color: "E2E8F5" }, rectRadius: 0.1 });
  s2.addText(k[0], { x: x, y: 4.15, w: 2.85, h: 0.7, fontSize: 28, bold: true, color: BLUE, align: "center" });
  s2.addText(k[1], { x: x, y: 4.85, w: 2.85, h: 0.5, fontSize: 11.5, color: GREY, align: "center" });
});
s2.addText("Conclusion: Landing success is highly predictable from launch parameters, meaning a competing launch provider could reliably estimate SpaceX's true reusable-launch cost advantage.", {
  x: 0.5, y: 5.85, w: 12.3, h: 0.9, fontSize: 13, italic: true, color: NAVY
});
pageNum(s2, 2);

// ================= SLIDE 3: INTRODUCTION =================
let s3 = pres.addSlide();
titleBar(s3, "Background", "Introduction");
s3.addText([
  { text: "SpaceX advertises Falcon 9 launches at $62 million, versus $165M+ from other providers — largely because SpaceX reuses the rocket's first stage instead of discarding it.\n\n", options: {} },
  { text: "Problem statement: ", options: { bold: true, color: NAVY } },
  { text: "If the first stage does not land successfully, that launch's cost estimate changes substantially. This project builds a model to predict whether the first stage will land, using historical launch data — enabling accurate cost estimation for a competing bid.\n\n", options: {} },
  { text: "Objectives:", options: { bold: true, color: NAVY } },
], { x: 0.5, y: 1.6, w: 7.3, h: 3.2, fontSize: 14.5, color: GREY, lineSpacing: 24 });

const objectives = ["Collect and clean historical Falcon 9 launch data", "Identify factors correlated with landing success", "Visualize patterns across sites, orbits, and time", "Build and evaluate a landing-outcome classifier"];
objectives.forEach((o, i) => {
  s3.addText(o, { x: 0.8, y: 4.75 + i*0.42, w: 6.8, h: 0.4, fontSize: 13, color: NAVY, bullet: { code: "2022" } });
});

s3.addImage({ path: IMG + "eda_yearly_trend.png", x: 8.1, y: 1.6, w: 4.7, h: 3.1 });
s3.addText("Falcon 9 landing success climbed steadily as SpaceX matured its recovery process.", { x: 8.1, y: 4.75, w: 4.7, h: 1.3, fontSize: 11.5, italic: true, color: GREY });
pageNum(s3, 3);

// ================= SLIDE 4: DATA COLLECTION - API =================
let s4 = pres.addSlide();
titleBar(s4, "Data Collection · Part 1", "Data Collection – SpaceX API");
s4.addText("Pipeline:", { x: 0.5, y: 1.6, w: 5.9, h: 0.35, fontSize: 14, bold: true, color: NAVY });
const apiSteps = [
  "GET /v4/launches/past → all historical launches",
  "Filter to single-core, single-payload Falcon 9 flights",
  "For each launch, call /rockets, /launchpads, /payloads, /cores endpoints",
  "Assemble into one row per launch: booster, orbit, site, outcome, mass"
];
apiSteps.forEach((step, i) => {
  s4.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 2.05 + i*0.78, w: 0.45, h: 0.45, fill: { color: BLUE }, rectRadius: 0.5 });
  s4.addText(String(i+1), { x: 0.5, y: 2.05 + i*0.78, w: 0.45, h: 0.45, fontSize: 14, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
  s4.addText(step, { x: 1.1, y: 2.05 + i*0.78, w: 5.3, h: 0.7, fontSize: 12.5, color: GREY, valign: "middle" });
});

s4.addShape(pres.ShapeType.roundRect, { x: 6.9, y: 1.6, w: 5.9, h: 3.9, fill: { color: LIGHT }, line: { color: "E2E8F5" }, rectRadius: 0.08 });
s4.addText("api.spacexdata.com/v4/launches/past", { x: 7.15, y: 1.8, w: 5.4, h: 0.4, fontSize: 12, fontFace: "Courier New", color: BLUE, bold: true });
s4.addText("Result: 90 clean Falcon 9 launch records (2010–Nov 2020), each with booster version, payload mass, orbit, launch site, flight count, grid fins, reused flag, legs, landing pad, and outcome.", {
  x: 7.15, y: 2.35, w: 5.4, h: 1.8, fontSize: 12.5, color: NAVY, lineSpacing: 20
});
s4.addText("Falcon 1 launches were excluded — this project focuses only on the Falcon 9 landing-prediction problem.", { x: 7.15, y: 4.5, w: 5.4, h: 0.9, fontSize: 11, italic: true, color: GREY });
githubFooter(s4, GITHUB_URL + "/blob/main/notebooks/01_data_collection_api.py");
pageNum(s4, 4);

// ================= SLIDE 5: DATA COLLECTION - WEB SCRAPING =================
let s5 = pres.addSlide();
titleBar(s5, "Data Collection · Part 2", "Data Collection – Web Scraping");
s5.addText("Pipeline:", { x: 0.5, y: 1.6, w: 5.9, h: 0.35, fontSize: 14, bold: true, color: NAVY });
const scrapeSteps = [
  "Request the Wikipedia \"List of Falcon 9 and Falcon Heavy launches\" page",
  "Parse HTML tables with BeautifulSoup, locate the wikitable elements",
  "Extract column headers, then walk each row of launch data",
  "Clean text (dates, booster serials, payload mass) into a dataframe"
];
scrapeSteps.forEach((step, i) => {
  s5.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 2.05 + i*0.78, w: 0.45, h: 0.45, fill: { color: TEAL }, rectRadius: 0.5 });
  s5.addText(String(i+1), { x: 0.5, y: 2.05 + i*0.78, w: 0.45, h: 0.45, fontSize: 14, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
  s5.addText(step, { x: 1.1, y: 2.05 + i*0.78, w: 5.3, h: 0.7, fontSize: 12.5, color: GREY, valign: "middle" });
});
s5.addShape(pres.ShapeType.roundRect, { x: 6.9, y: 1.6, w: 5.9, h: 3.9, fill: { color: LIGHT }, line: { color: "E2E8F5" }, rectRadius: 0.08 });
s5.addText("BeautifulSoup(response.text, 'html.parser')", { x: 7.15, y: 1.8, w: 5.4, h: 0.4, fontSize: 12, fontFace: "Courier New", color: TEAL, bold: true });
s5.addText("This gives an independent, cross-checked source for launch records — used to validate the API dataset and fill in fields (like precise payload customer) the API doesn't expose.", {
  x: 7.15, y: 2.35, w: 5.4, h: 1.8, fontSize: 12.5, color: NAVY, lineSpacing: 20
});
s5.addText("Key techniques: regex/Unicode cleanup for payload mass strings, and helper functions to pull booster version and landing status out of merged table cells.", { x: 7.15, y: 4.5, w: 5.4, h: 1.0, fontSize: 11, italic: true, color: GREY });
githubFooter(s5, GITHUB_URL + "/blob/main/notebooks/02_web_scraping.py");
pageNum(s5, 5);

// ================= SLIDE 6: DATA WRANGLING =================
let s6 = pres.addSlide();
titleBar(s6, "Preparation", "Data Wrangling Methodology");
s6.addText([
  { text: "Missing values: ", options: { bold: true, color: NAVY } },
  { text: "PayloadMass (5.6% missing) filled with column mean; LandingPad (28.9% missing) kept as-is since a null pad legitimately means \"no ground/drone-ship landing occurred.\"\n\n", options: { color: GREY } },
  { text: "Label engineering: ", options: { bold: true, color: NAVY } },
  { text: "The raw Outcome field (e.g. \"True ASDS\", \"False Ocean\", \"None None\") was converted into a binary Class label — 1 if the booster landed successfully by any method, 0 otherwise.", options: { color: GREY } },
], { x: 0.5, y: 1.6, w: 7.2, h: 3.0, fontSize: 14, lineSpacing: 23 });

s6.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 4.5, w: 7.2, h: 1.4, fill: { color: LIGHT }, rectRadius: 0.08 });
s6.addText("Result: 90 launches → 60 successful landings (66.7%), 30 unsuccessful (33.3%)", { x: 0.7, y: 4.5, w: 6.8, h: 1.4, fontSize: 13, bold: true, color: NAVY, valign: "middle" });

s6.addImage({ path: IMG + "eda_orbit_success.png", x: 8.0, y: 1.5, w: 4.8, h: 3.6 });
githubFooter(s6, GITHUB_URL + "/blob/main/notebooks/03_data_wrangling.py");
pageNum(s6, 6);

// ================= SLIDE 7: EDA WITH DATA VIZ (overview) =================
let s7 = pres.addSlide();
titleBar(s7, "Exploratory Analysis · Part 1", "EDA with Data Visualization");
s7.addText("We plotted flight number, payload mass, orbit type, and launch year against landing outcome to surface which factors correlate with success.", {
  x: 0.5, y: 1.55, w: 12.3, h: 0.6, fontSize: 14, color: GREY
});
const charts7 = [
  ["eda_flightnum_site.png", "Flight # vs Launch Site"],
  ["eda_payload_site.png", "Payload vs Launch Site"],
  ["eda_orbit_success.png", "Success Rate by Orbit"],
];
charts7.forEach((c, i) => {
  s7.addImage({ path: IMG + c[0], x: 0.5 + i*4.25, y: 2.3, w: 4.0, h: 2.7 });
  s7.addText(c[1], { x: 0.5 + i*4.25, y: 5.0, w: 4.0, h: 0.35, fontSize: 11.5, bold: true, color: NAVY, align: "center" });
});
s7.addText("Chart types used: scatter plots (flight #/payload vs site or orbit), bar charts (success rate by orbit), and a line chart (yearly trend, see Introduction slide).", {
  x: 0.5, y: 5.55, w: 12.3, h: 0.9, fontSize: 12, italic: true, color: GREY
});
githubFooter(s7, GITHUB_URL + "/blob/main/notebooks/04_07_eda_sql_ml.py");
pageNum(s7, 7);

// ================= SLIDE 8: EDA VIZ RESULTS 2 =================
let s8 = pres.addSlide();
titleBar(s8, "Exploratory Analysis · Part 1 (cont.)", "EDA Visualization — Orbit & Trend Detail");
const charts8 = [
  ["eda_flightnum_orbit.png", "Flight # vs Orbit Type"],
  ["eda_payload_orbit.png", "Payload vs Orbit Type"],
  ["eda_yearly_trend.png", "Success Rate by Year"],
];
charts8.forEach((c, i) => {
  s8.addImage({ path: IMG + c[0], x: 0.5 + i*4.25, y: 1.7, w: 4.0, h: 2.9 });
  s8.addText(c[1], { x: 0.5 + i*4.25, y: 4.65, w: 4.0, h: 0.35, fontSize: 11.5, bold: true, color: NAVY, align: "center" });
});
s8.addText("Takeaway: GTO and ISS-orbit missions (heavier, higher-energy) show lower success rates; success climbed year-over-year as SpaceX refined the recovery process, from ~0% in 2010–2013 to consistently near 100% by 2019–2020.", {
  x: 0.5, y: 5.15, w: 12.3, h: 1.4, fontSize: 13, color: NAVY, lineSpacing: 20
});
pageNum(s8, 8);

// ================= SLIDE 9: EDA WITH SQL (overview) =================
let s9 = pres.addSlide();
titleBar(s9, "Exploratory Analysis · Part 2", "EDA with SQL");
s9.addText("The scraped launch table was loaded into a SQL database (SQLite / IBM Db2) as SPACEXTABLE, then queried directly to answer specific business questions.", {
  x: 0.5, y: 1.55, w: 12.3, h: 0.6, fontSize: 14, color: GREY
});
const sqlQueries = [
  "Distinct launch sites used",
  "Total payload mass carried for NASA (CRS)",
  "Average payload mass for F9 v1.1 boosters",
  "Date of the first successful ground-pad landing",
  "Boosters that succeeded on a drone ship with 4,000–6,000 kg payload",
  "Count of each mission outcome (success/failure)",
  "Booster(s) carrying the maximum payload mass",
  "Failed drone-ship landings in 2015",
  "Ranking of landing outcomes between 2010–2017"
];
const half = Math.ceil(sqlQueries.length/2);
sqlQueries.slice(0, half).forEach((q, i) => s9.addText(q, { x: 0.5, y: 2.35 + i*0.55, w: 5.9, h: 0.5, fontSize: 12.5, color: NAVY, bullet: { code: "2713" } }));
sqlQueries.slice(half).forEach((q, i) => s9.addText(q, { x: 6.7, y: 2.35 + i*0.55, w: 5.9, h: 0.5, fontSize: 12.5, color: NAVY, bullet: { code: "2713" } }));
githubFooter(s9, GITHUB_URL + "/blob/main/notebooks/04_07_eda_sql_ml.py");
pageNum(s9, 9);

// ================= SLIDE 10: EDA SQL RESULTS - sites/payload =================
let s10 = pres.addSlide();
titleBar(s10, "Exploratory Analysis · Part 2 (cont.)", "EDA SQL Results — Sites & Payload");
s10.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 1.6, w: 5.9, h: 2.4, fill: { color: LIGHT }, rectRadius: 0.08 });
s10.addText("Launch Sites (4 distinct)", { x: 0.7, y: 1.75, w: 5.5, h: 0.4, fontSize: 13, bold: true, color: NAVY });
s10.addText("CCAFS LC-40 · CCAFS SLC-40 · KSC LC-39A · VAFB SLC-4E", { x: 0.7, y: 2.2, w: 5.5, h: 0.5, fontSize: 12.5, color: GREY });
s10.addText("Total payload for NASA (CRS): 45,596 kg", { x: 0.7, y: 2.85, w: 5.5, h: 0.4, fontSize: 12.5, color: NAVY });
s10.addText("Avg. payload, F9 v1.1 boosters: 2,534.7 kg", { x: 0.7, y: 3.25, w: 5.5, h: 0.4, fontSize: 12.5, color: NAVY });
s10.addText("Max payload carried: 15,600 kg (F9 B5)", { x: 0.7, y: 3.65, w: 5.5, h: 0.4, fontSize: 12.5, color: NAVY });

s10.addShape(pres.ShapeType.roundRect, { x: 6.9, y: 1.6, w: 5.9, h: 2.4, fill: { color: LIGHT }, rectRadius: 0.08 });
s10.addText("Milestones", { x: 7.1, y: 1.75, w: 5.5, h: 0.4, fontSize: 13, bold: true, color: NAVY });
s10.addText("First successful ground-pad landing: 1 May 2017", { x: 7.1, y: 2.2, w: 5.5, h: 0.5, fontSize: 12.5, color: GREY });
s10.addText("2015 drone-ship landing failures: 2 (F9 v1.1 B1012, B1015 — CCAFS LC-40)", { x: 7.1, y: 2.7, w: 5.5, h: 0.9, fontSize: 12.5, color: GREY });
s10.addText("4,000–6,000 kg drone-ship successes: F9 FT B1021.2, B1022, B1026, B1031.2", { x: 7.1, y: 3.6, w: 5.5, h: 0.9, fontSize: 12.5, color: GREY });

s10.addText("These figures ground the EDA charts in exact, query-verified numbers rather than visual estimates.", { x: 0.5, y: 4.35, w: 12.3, h: 0.5, fontSize: 12, italic: true, color: GREY });
githubFooter(s10, GITHUB_URL + "/blob/main/notebooks/04_07_eda_sql_ml.py");
pageNum(s10, 10);

// ================= SLIDE 11: EDA SQL RESULTS - success/rankings/time =================
let s11 = pres.addSlide();
titleBar(s11, "Exploratory Analysis · Part 2 (cont.)", "EDA SQL Results — Success Rates & Rankings");
s11.addText("Landing outcome ranking, 2010–2017 (by count):", { x: 0.5, y: 1.6, w: 12, h: 0.4, fontSize: 14, bold: true, color: NAVY });
const rankRows = [
  ["Success", "20"], ["No attempt", "10"], ["Success (drone ship)", "8"],
  ["Success (ground pad)", "6"], ["Failure (drone ship)", "4"], ["Failure", "3"],
  ["Controlled (ocean)", "3"], ["Failure (parachute)", "2"]
];
let tableRows = [[{text:"Landing Outcome", options:{bold:true, color:"FFFFFF", fill:{color:BLUE}}}, {text:"Count", options:{bold:true, color:"FFFFFF", fill:{color:BLUE}}}]];
rankRows.forEach(r => tableRows.push([{text:r[0], options:{color:NAVY}}, {text:r[1], options:{color:NAVY, align:"center"}}]));
s11.addTable(tableRows, { x: 0.5, y: 2.1, w: 6.0, h: 4.4, fontSize: 11.5, border: { type: "solid", color: "E2E8F5", pt: 1 }, autoPage: false, colW: [4.4, 1.6] });

s11.addText("Mission outcome (2010–2020): 98 of 101 recorded outcomes were successful missions — first-stage recovery success is the harder, separate problem this model targets.", {
  x: 6.9, y: 2.1, w: 5.9, h: 1.3, fontSize: 12.5, color: GREY, lineSpacing: 19
});
s11.addImage({ path: IMG + "eda_orbit_success.png", x: 6.9, y: 3.5, w: 5.9, h: 3.0 });
githubFooter(s11, GITHUB_URL + "/blob/main/notebooks/04_07_eda_sql_ml.py");
pageNum(s11, 11);

// ================= SLIDE 12: INTERACTIVE VISUAL ANALYTICS (overview) =================
let s12 = pres.addSlide();
titleBar(s12, "Exploratory Analysis · Part 3", "Interactive Visual Analytics");
s12.addText("Two interactive tools let stakeholders explore the data themselves rather than reading static charts:", { x: 0.5, y: 1.6, w: 12.3, h: 0.5, fontSize: 14, color: GREY });

s12.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 2.3, w: 5.9, h: 3.6, fill: { color: LIGHT }, rectRadius: 0.1 });
s12.addText("Folium Map", { x: 0.8, y: 2.5, w: 5.3, h: 0.5, fontSize: 17, bold: true, color: BLUE });
s12.addText("Launch-site markers, per-launch outcome markers (color-coded), and proximity distance lines (coastline, city, railway, highway).", { x: 0.8, y: 3.05, w: 5.3, h: 1.0, fontSize: 12.5, color: GREY, lineSpacing: 18 });
s12.addImage({ path: IMG + "folium_static_view.png", x: 1.38, y: 4.1, w: 4.15, h: 1.8 });

s12.addShape(pres.ShapeType.roundRect, { x: 6.9, y: 2.3, w: 5.9, h: 3.6, fill: { color: LIGHT }, rectRadius: 0.1 });
s12.addText("Plotly Dash App", { x: 7.2, y: 2.5, w: 5.3, h: 0.5, fontSize: 17, bold: true, color: TEAL });
s12.addText("Dropdown to filter by launch site; live-updating success-rate pie chart and payload-vs-outcome scatter plot.", { x: 7.2, y: 3.05, w: 5.3, h: 1.0, fontSize: 12.5, color: GREY, lineSpacing: 18 });
s12.addImage({ path: IMG + "dash_pie_all_sites.png", x: 7.35, y: 4.1, w: 1.75, h: 1.6 });
s12.addImage({ path: IMG + "dash_payload_scatter.png", x: 9.25, y: 4.1, w: 3.35, h: 1.6 });
githubFooter(s12, GITHUB_URL + "/blob/main/dashboard/app.py");
pageNum(s12, 12);

// ================= SLIDE 13: FOLIUM MAP - site markers/records =================
let s13 = pres.addSlide();
titleBar(s13, "Interactive Visual Analytics · Folium", "Launch Site Markers & Launch Records");
s13.addImage({ path: IMG + "folium_static_view.png", x: 0.5, y: 2.3, w: 8.6, h: 3.73 });
s13.addText([
  { text: "All 4 launch sites plotted with markers.\n", options: { bold: true, color: NAVY } },
  { text: "Every individual launch (56 records) plotted as a marker cluster, colored green for a successful landing and red for a failed/no-attempt landing — letting you see which sites cluster more successes.\n\n", options: { color: GREY } },
  { text: "Observation: ", options: { bold: true, color: NAVY } },
  { text: "KSC LC-39A shows the densest green cluster — 10 landings from 13 launches (77%). CCAFS LC-40, the earliest and highest-volume pad, landed only 7 of 26 (27%): most of its records predate a working recovery process.", options: { color: GREY } },
], { x: 9.3, y: 1.7, w: 3.5, h: 4.9, fontSize: 12, lineSpacing: 18 });
githubFooter(s13, GITHUB_URL + "/blob/main/notebooks/06_folium_map.py");
pageNum(s13, 13);

// ================= SLIDE 14: FOLIUM MAP - proximity analysis =================
let s14 = pres.addSlide();
titleBar(s14, "Interactive Visual Analytics · Folium", "Proximity Analysis");
s14.addText("Using the haversine formula, we measured distance from KSC LC-39A to nearby geographic features:", { x: 0.5, y: 1.6, w: 12.3, h: 0.5, fontSize: 14, color: GREY });

const proxRows = [
  ["Nearest coastline point", "7.43 km"],
  ["Nearest city (Titusville)", "16.33 km"],
  ["Nearest railway (NASA Railroad)", "0.69 km"],
  ["Nearest highway (Kennedy Pkwy N)", "0.85 km"],
];
let proxTable = [[{text:"Feature", options:{bold:true, color:"FFFFFF", fill:{color:ORANGE}}}, {text:"Distance from Launch Site", options:{bold:true, color:"FFFFFF", fill:{color:ORANGE}}}]];
proxRows.forEach(r => proxTable.push([{text:r[0], options:{color:NAVY}}, {text:r[1], options:{color:NAVY, align:"center"}}]));
s14.addTable(proxTable, { x: 0.5, y: 2.25, w: 6.0, h: 1.9, fontSize: 12.5, border: { type: "solid", color: "E2E8F5", pt: 1 }, colW: [4.2, 1.8] });

s14.addText([
  { text: "Why this matters: ", options: { bold: true, color: NAVY } },
  { text: "Launch sites are deliberately sited close to coastlines (for downrange safety over open water) and to rail and road links (boosters and stages arrive overland), but a safe distance from population centers — real siting constraints any competing launch provider would need to replicate.", options: { color: GREY } }
], { x: 0.5, y: 4.35, w: 6.0, h: 2.2, fontSize: 12.5, lineSpacing: 19 });

s14.addImage({ path: IMG + "folium_map_screenshot.png", x: 7.25, y: 2.2, w: 5.2, h: 4.5 });
s14.addText("City, railway and highway coordinates sourced from OpenStreetMap.", { x: 0.5, y: 6.15, w: 6.0, h: 0.4, fontSize: 10.5, color: GREY, italic: true });
githubFooter(s14, GITHUB_URL + "/blob/main/notebooks/06_folium_map.py");
pageNum(s14, 14);

// ================= SLIDE 15: PLOTLY DASH - pie charts =================
let s15 = pres.addSlide();
titleBar(s15, "Interactive Visual Analytics · Dash", "Success Rate — Pie Charts");
s15.addImage({ path: IMG + "dash_pie_all_sites.png", x: 0.5, y: 1.6, w: 5.9, h: 5.0 });
s15.addImage({ path: IMG + "dash_pie_top_site.png", x: 6.9, y: 1.9, w: 5.5, h: 4.4 });
s15.addText("Left: share of total successful landings contributed by each site. Right: success-vs-failure split at the top-volume site (CCAFS LC-40) — filterable live via the dashboard dropdown.", {
  x: 6.9, y: 6.35, w: 5.9, h: 0.7, fontSize: 11.5, italic: true, color: GREY
});
githubFooter(s15, GITHUB_URL + "/blob/main/dashboard/app.py");
pageNum(s15, 15);

// ================= SLIDE 16: PLOTLY DASH - payload scatter =================
let s16 = pres.addSlide();
titleBar(s16, "Interactive Visual Analytics · Dash", "Payload Mass vs. Launch Outcome");
s16.addImage({ path: IMG + "dash_payload_scatter.png", x: 0.9, y: 1.7, w: 11.4, h: 4.9 });
s16.addText("A RangeSlider (0–10,000 kg) lets users narrow the payload window; the scatter plot recolors by booster version category (v1.0 / v1.1 / FT / B4 / B5), revealing that newer booster generations succeed reliably across a much wider payload range than early versions.", {
  x: 0.5, y: 6.5, w: 12.3, h: 0.7, fontSize: 12, italic: true, color: GREY
});
githubFooter(s16, GITHUB_URL + "/blob/main/dashboard/app.py");
pageNum(s16, 16);

// ================= SLIDE 17: PREDICTIVE ANALYSIS - models/methodology =================
let s17 = pres.addSlide();
titleBar(s17, "Predictive Analysis · Part 1", "Model Development");
s17.addText([
  { text: "Features: ", options: { bold: true, color: NAVY } },
  { text: "80 one-hot-encoded columns (orbit, launch site, landing pad, booster serial) plus flight number, payload mass, flights, grid fins, reused, legs, and block — standardized with StandardScaler.\n\n", options: { color: GREY } },
  { text: "Split: ", options: { bold: true, color: NAVY } },
  { text: "80% train / 20% test (72 / 18 launches), stratified via random_state=2.\n\n", options: { color: GREY } },
  { text: "Models compared (each tuned via 10-fold GridSearchCV):", options: { bold: true, color: NAVY } },
], { x: 0.5, y: 1.6, w: 6.3, h: 3.0, fontSize: 13.5, lineSpacing: 21 });

const models = ["Logistic Regression — C, penalty, solver", "Support Vector Machine — kernel, C, gamma", "Decision Tree — criterion, max_depth, min_samples_split", "K-Nearest Neighbors — n_neighbors, distance metric (p)"];
models.forEach((m, i) => s17.addText(m, { x: 0.8, y: 4.55 + i*0.42, w: 6.0, h: 0.4, fontSize: 12, color: NAVY, bullet: { code: "2022" } }));

s17.addImage({ path: IMG + "model_comparison.png", x: 7.1, y: 1.6, w: 5.7, h: 4.0 });
s17.addText("All four models converged near 83% test accuracy, with Decision Tree slightly behind — signal that the engineered features are strong and model choice matters less than feature quality here.", {
  x: 7.1, y: 5.7, w: 5.7, h: 1.0, fontSize: 11.5, italic: true, color: GREY
});
githubFooter(s17, GITHUB_URL + "/blob/main/notebooks/04_07_eda_sql_ml.py");
pageNum(s17, 17);

// ================= SLIDE 18: PREDICTIVE ANALYSIS - evaluation/confusion matrix =================
let s18 = pres.addSlide();
titleBar(s18, "Predictive Analysis · Part 2", "Evaluation Results & Confusion Matrix");
s18.addImage({ path: IMG + "confusion_matrix_best.png", x: 0.6, y: 1.6, w: 5.5, h: 4.9 });

let evalTable = [[{text:"Model", options:{bold:true, color:"FFFFFF", fill:{color:BLUE}}}, {text:"CV Score", options:{bold:true, color:"FFFFFF", fill:{color:BLUE}}}, {text:"Test Accuracy", options:{bold:true, color:"FFFFFF", fill:{color:BLUE}}}]];
const evalRows = [
  ["Logistic Regression", "0.821", "0.833"],
  ["SVM", "0.834", "0.833"],
  ["KNN", "0.834", "0.833"],
  ["Decision Tree", "0.804", "0.778"],
];
evalRows.forEach(r => evalTable.push([{text:r[0], options:{color:NAVY, bold:r[0]==="Logistic Regression"}}, {text:r[1], options:{color:NAVY, align:"center"}}, {text:r[2], options:{color:NAVY, align:"center"}}]));
s18.addTable(evalTable, { x: 6.5, y: 1.7, w: 6.3, h: 2.2, fontSize: 12.5, border: { type: "solid", color: "E2E8F5", pt: 1 }, colW: [3.0, 1.65, 1.65] });

s18.addText([
  { text: "Reading the confusion matrix (18 test launches): ", options: { bold: true, color: NAVY } },
  { text: "12 successful landings correctly predicted, 3 unsuccessful landings correctly predicted, 3 unsuccessful landings misclassified as successful, 0 successful landings missed. The model never misses a true landing — it's conservative in the safer direction for cost bidding.", options: { color: GREY } }
], { x: 6.5, y: 4.2, w: 6.3, h: 2.6, fontSize: 13, lineSpacing: 20 });
githubFooter(s18, GITHUB_URL + "/blob/main/notebooks/04_07_eda_sql_ml.py");
pageNum(s18, 18);

// ================= SLIDE 19: BEST MODEL EXPLANATION + CONCLUSION =================
let s19 = pres.addSlide();
titleBar(s19, "Predictive Analysis · Part 3", "Best Model & Conclusion");
s19.addShape(pres.ShapeType.roundRect, { x: 0.5, y: 1.6, w: 5.9, h: 4.9, fill: { color: LIGHT }, rectRadius: 0.1 });
s19.addText("Best Model: Logistic Regression", { x: 0.8, y: 1.8, w: 5.3, h: 0.5, fontSize: 17, bold: true, color: BLUE });
s19.addText([
  { text: "Best params: C=1, L2 penalty, lbfgs solver\n\n", options: { color: GREY } },
  { text: "Why it wins: ", options: { bold: true, color: NAVY } },
  { text: "Ties SVM and KNN on raw accuracy (83.3%) but is far more interpretable — each feature's coefficient directly shows its effect on landing-success odds, which matters for explaining a cost bid to stakeholders. It's also the cheapest to retrain as new launches arrive.", options: { color: GREY } },
], { x: 0.8, y: 2.4, w: 5.3, h: 3.9, fontSize: 12.5, lineSpacing: 20 });

s19.addText("Conclusion & Insights", { x: 6.9, y: 1.6, w: 5.9, h: 0.4, fontSize: 17, bold: true, color: NAVY });
const conclusions = [
  "Landing success is highly learnable from launch parameters — 83% test accuracy from a simple, interpretable model.",
  "Orbit type and payload mass are the strongest visual predictors; heavier GTO missions land less reliably than light LEO/ISS missions.",
  "Success rate improved dramatically over time (2013 → 2020), reflecting SpaceX's iterative process improvements — not a static property of the hardware.",
  "Recommendation: a competing bidder can use this model as a first-pass cost-risk estimator, refining it further with more recent launches and continuous re-training.",
];
conclusions.forEach((c, i) => s19.addText(c, { x: 6.9, y: 2.1 + i*1.1, w: 5.9, h: 1.0, fontSize: 12, color: GREY, bullet: { code: "2022" }, lineSpacing: 16 }));
githubFooter(s19, GITHUB_URL);
pageNum(s19, 19);

pres.writeFile({ fileName: path.join(ROOT, "Data_Science_Capstone_Presentation.pptx") }).then(() => {
  console.log("Presentation saved.");
});
