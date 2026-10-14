# CivicLens AI (NagrikNetra)
### Autonomous Multimodal Civic Grievance Triage, Geospatial Hotspots & Resolution Verification

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 3.x](https://img.shields.io/badge/Framework-Flask_3.x-green.svg)](https://flask.palletsprojects.com/)
[![AI-Mode](https://img.shields.io/badge/AI--Engine-Gemini_Flash_%2B_Edge_CV-orange.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Overview
**CivicLens AI (NagrikNetra)** is an end-to-end civic intelligence platform built specifically for Indian municipal corporations (e.g., BBMP, MCD, BMC, GHMC) and citizens. It addresses the dangerous reality of cratered roads, overflowing solid waste dumps, open drains, and dangling electric wires by replacing manual, slow, duplicate-heavy complaint portals with real-time **Multimodal Computer Vision**, **50m geospatial clustering**, **automated department dispatching**, and **AI-powered Before-and-After repair verification**.

---

## 🚀 Key Features

1. **Multimodal Vision AI Triage**:
   - Citizens snap or upload an image of a civic hazard.
   - The AI identifies the defect (potholes, solid waste, hanging live wires, sewage), assigns a severity score (1–10), and calculates an urgent SLA (4h to 48h).
2. **Dual-Mode AI Resiliency**:
   - **Cloud Mode**: Harnesses Google Gemini 1.5/2.0 Flash for reasoning, dimension estimation, and work order generation.
   - **Edge Mode**: Automatically falls back to an embedded deterministic computer vision heuristic engine if offline or if no API key is provided—**guaranteeing 100% demo reliability**.
3. **50-Meter Geospatial Deduplication (Haversine Clustering)**:
   - Eliminates duplicate tickets by aggregating reports within 50 meters into a single master ticket and boosting community upvotes.
4. **Autonomous Department Routing**:
   - Automatically directs grievances to the responsible municipal body (PWD, Municipal Solid Waste Management, Electricity Board, Water & Sewerage Board).
5. **3-Stage Municipal Field Worker SOP & Anti-Ghost Verification**:
   - **Stage 1 (Arrival Selfie & GPS Check-in)**: Field workers submit an arrival selfie with their employee badge. AI detects face, safety helmet, and high-visibility uniform while verifying geofence proximity ($\le 150$m) against hazard coordinates.
   - **Stage 2 (Before & After Work Evidence)**: Confirms pre-work defect photo with coordinates and captures post-work completion photo with coordinates.
   - **Stage 3 (Tri-Factor AI Audit & Certificate)**: Executes surface leveling analysis, duplicate fraud detection, and mints an official digital **Municipal Work Completion Certificate** with quad-photo evidence and cryptographic audit hash.
6. **Pan-India Coverage (All 28 States & 8 Union Territories)**:
   - Full GIS coordinate registry and municipal department mapping across every Indian state and UT (e.g. BBMP Karnataka, BMC Maharashtra, MCD Delhi, GHMC Telangana, etc.).
7. **Authentic Street Photography & Landmarks**:
   - Realistic street-level documentary photography featuring Indian landmarks (Bengaluru Silk Board flyover, Mumbai Dadar market, Delhi Chandni Chowk) and uniformed municipal workers (PWD, BMC, BSES DISCOM).
8. **Ward Civic Health Index (CHI) & Interactive GIS Map**:
   - Live Leaflet.js heatmap with severity-coded pins across Indian metropolitan wards.
   - Algorithmic Ward Civic Health Index (grades A to D) with Chart.js analytics.
9. **Multilingual Vernacular Support & Nagrik AI Copilot**:
   - Handles text descriptions in Hindi, Tamil, Telugu, Kannada, Bengali, and English.
   - Built-in conversational AI chatbot with instant database grievance ticket lookup by ticket ID, house number, or locality.

---

## 📂 Project Directory Structure

```
d:\civiclens-ai/
├── app.py                      # Flask backend controller & REST API
├── ai_engine.py                # Dual-mode AI pipeline (Gemini + Edge CV + Haversine + Verification)
├── models.py                   # SQLite database models, DAL, and seed data generator
├── generate_sample_images.py   # PIL script generating high-detail test before/after photos
├── test_engine.py              # Automated test suite (8 tests covering full stack)
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows Batch single-click launcher
├── run.ps1                     # Windows PowerShell launcher
├── .env.example                # Example environment variables
├── templates/
│   └── index.html              # Modern, responsive single-page application UI
├── static/
│   ├── css/
│   │   └── style.css           # Custom styling, radar laser scan animation, pin styling
│   ├── js/
│   │   └── app.js              # Interactive client application logic
│   ├── sample_images/          # Pre-packaged before/after test imagery
│   └── uploads/                # User uploaded incident images
└── docs/
    ├── SRS.md                  # Software Requirements Specification
    ├── AI_ARCHITECTURE.md      # Detailed AI architecture, prompts, and heuristics
    ├── PITCH_DECK.md           # 10-Slide Hackathon Pitch Deck & Presentation Guide
    ├── DEMO_SCRIPT.md          # 5-to-7 Minute Live Demonstration Script
    ├── JUDGES_FAQ.md           # Judges Frequently Asked Questions & Winning Answers
    └── BUDGET_TIMELINE.md      # Estimated budget, 7-14 day schedule, and team roles
```

---

## 🛠️ Quickstart Guide (Local Setup)

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13 installed.
- Modern web browser (Chrome, Edge, Firefox, Safari).

### 2. Installation
Open PowerShell or Command Prompt in `d:\civiclens-ai`:

```bash
cd d:\civiclens-ai
python -m pip install -r requirements.txt
```

*(Note: If `pip install` gives a permission warning, you can run `python -m pip install --user -r requirements.txt`)*

### 3. (Optional) Configure Gemini API Key
If you have a Google AI Studio Gemini API key, copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Open `.env` in any text editor and paste your key:
```ini
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
> **Note**: If you don't have an API key, **no problem!** CivicLens AI will automatically activate its built-in Edge Vision Heuristics and run 100% locally with zero configuration.

### 4. Run the Automated Test Suite
Verify that all 8 unit and integration tests pass:

```bash
python test_engine.py
```

Expected Output:
```
Ran 8 tests in 0.08s
OK
[PASS] Health endpoint verified: Edge Vision Heuristics (Offline Guarantee)
[PASS] Found 3 sample test scenarios
[PASS] Local CV Pothole Classification: Pothole & Road Damage (Severity 7/10)
[PASS] Local CV Garbage Classification: Garbage & Solid Waste (Severity 8/10)
[PASS] Haversine Distance Calculated: 24.7m (near), 6358.9m (far)
[PASS] Proximity Clustering Grouped nearby report into CLUSTER-IND-01
[PASS] Resolution Verification Passed: Score 86.3%
[PASS] Anti-Fraud Protection Verified: Re-uploading identical photo rejected
[PASS] Created incident via API: CIVIC-BEN-xxxx
[PASS] Analytics verified: 12 total issues, 9 wards scored
```

### 5. Launch the Web Application
Simply double-click `run.bat` or run:

```bash
python app.py
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🎯 How to Demonstrate the Project in 3 Minutes

1. **Test Live AI Diagnosis**:
   - On the homepage (**Nagrik Report**), click any of the preset scenario cards (e.g., *Bengaluru ORR Crater* or *Indiranagar Solid Waste*).
   - Observe the **animated laser scanner** and instant AI triage card showing detected hazard class, severity score (1-10), SLA target, and auto-routed department.
   - Click **Submit Grievance** to register the issue.
2. **Inspect the Live GIS Heatmap**:
   - Click the **GIS Heatmap** tab.
   - View interactive color-coded cluster pins across Indian metropolitan wards (Red = Critical, Orange = High, Green = Resolved).
3. **Review the Municipal Triage Queue**:
   - Click the **Command Triage** tab.
   - See how incidents are dynamically ordered by severity and upvotes, complete with live SLA countdown timers.
4. **Demonstrate AI Before-and-After Resolution Verification**:
   - Click the **AI Verification** tab.
   - Select an open ticket from the dropdown.
   - Observe the original damage photo (Before) on the left and the contractor repair photo (After) on the right.
   - Click **Run AI Resolution Audit**.
   - Watch the AI compute surface leveling, defect clearance score (e.g., 94.5%), and automatically transition the ticket status to **RESOLVED**!
5. **View Civic Health Index (CHI)**:
   - Click **Civic Health (CHI)** to view real-time ward leaderboard grades and Chart.js analytics.
6. **Chat with Nagrik AI**:
   - Click the **Nagrik AI** button in the top navigation bar to ask civic questions in natural language.

---

## 🌐 Online Deployment Instructions

### Option A: Render.com (Recommended Free Cloud Hosting)
1. Push this repository to GitHub.
2. Log in to [Render.com](https://render.com) and click **New + > Web Service**.
3. Connect your GitHub repository.
4. Set:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (or `python app.py`)
5. In Environment Variables, optionally add:
   - `GEMINI_API_KEY`: *(Your key)*
   - `PORT`: `10000`
6. Click **Deploy Web Service**. Render provides a free `https://your-app.onrender.com` public URL.

### Option B: Railway.app
1. Install Railway CLI or connect GitHub.
2. Run `railway up`.
3. Railway automatically detects `requirements.txt` and provisions the Flask service.

---

## ⚖️ Ethics, Privacy & Safety Safeguards
- **EXIF Stripping**: Image geolocation coordinates are recorded into the database while personal device serial numbers are permanently purged.
- **Fair SLA Prioritization**: Emergency live wire electrocution hazards (4-hour SLA) take absolute precedence over non-fatal road cosmetic repairs.
- **Anti-Fraud Guard**: Post-repair photos with identical pixel hashes or sub-threshold variance are rejected with a fraud alert to stop ghost billing.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
Developed for the Community AI Innovation Challenge.
