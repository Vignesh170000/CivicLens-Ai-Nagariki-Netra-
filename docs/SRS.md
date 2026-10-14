# Software Requirements Specification (SRS)
## CivicLens AI (NagrikNetra): Autonomous Multimodal Civic Triage & Verification Engine

---

## 1. Introduction
CivicLens AI is an artificial intelligence platform designed to revolutionize civic issue reporting and municipal grievance redressal in Indian urban and semi-urban communities. It addresses broken roads, uncollected solid waste, open drains, and hazardous live wires by replacing error-prone manual complaint forms with real-time Multimodal Computer Vision, geospatial clustering, automated department dispatching, and AI-powered Before-and-After repair verification.

---

## 2. Functional Requirements

### 2.1 Citizen Portal ("Nagrik Triage")
- **FR-01 (Multimodal Input)**: Users must be able to upload images directly via file browser or mobile camera capture.
- **FR-02 (Instant AI Diagnosis)**: The system must extract visual signatures in real time (< 1.5 seconds) to classify the hazard type, assess severity (1–10), determine priority (Critical/High/Medium/Low), and estimate defect dimensions.
- **FR-03 (Location Geotagging)**: The application must support GPS coordinates and reverse-geocode to the corresponding municipal ward and administrative zone.
- **FR-04 (Multilingual Voice & Text Intake)**: The portal must accept grievance descriptions in English, Hindi, Tamil, Telugu, and other Indian languages.
- **FR-05 (Geospatial Deduplication & Upvoting)**: If an incident is reported within 50 meters of an existing active hazard, the system must link the report to the existing parent cluster and increment its public upvote count.

### 2.2 Municipal Command Center ("Ward Commander")
- **FR-06 (Automated Department Routing)**: The system must automatically map classified hazards to the appropriate municipal body (e.g., PWD, Municipal Solid Waste Management, Electricity Board, Water & Sewerage Board).
- **FR-07 (Priority Triage Queue)**: The municipal dashboard must dynamically rank work orders using an impact score: `Priority Score = Severity × log2(Upvotes + 1)`.
- **FR-08 (SLA Tracking & Alerts)**: Each incident must have a dynamic SLA deadline (4h for live wires, 12h for garbage dumps, 24h for arterial potholes, 48h for pedestrian walkways) with visual breach countdown warnings.
- **FR-09 (Status Lifecycle Management)**: Municipal engineers must be able to transition tickets through: `Reported` → `Investigating` → `Assigned` → `In Progress` → `Resolved` → `Rejected`.

### 2.3 Contractor Resolution & Verification Loop
- **FR-10 (Photographic Proof Mandatory)**: Work orders cannot be closed with an administrative checkbox alone; a post-repair photograph must be submitted.
- **FR-11 (AI Surface Clearance Audit)**: The system must compare the pre-repair and post-repair photos to evaluate defect elimination, surface leveling, and compute a quantitative clearance score (0–100%).
- **FR-12 (Anti-Fraud Protection)**: The verification engine must detect duplicate or cloned image submissions and reject attempts to submit the same photo as before and after.

### 2.4 Analytics & Citizen Copilot
- **FR-13 (Ward Civic Health Index - CHI)**: The system must calculate a real-time health score (0–100) and grade (A–D) for each municipal ward based on active critical issues and resolution velocity.
- **FR-14 (Conversational Civic Copilot)**: A virtual assistant must answer citizen inquiries regarding civic rights, reporting procedures, ward emergency numbers, and ticket status.

---

## 3. Non-Functional Requirements

### 3.1 Performance & Reliability
- **NFR-01 (Response Latency)**: Edge vision inference must complete in < 200 ms locally; cloud multimodal calls must complete in < 2.5 seconds.
- **NFR-02 (Availability & Failover)**: Dual-Mode AI architecture ensures 100% platform availability even when external cloud AI APIs are offline or unconfigured.

### 3.2 Security & Privacy
- **NFR-03 (Zero Secret Exposure)**: API keys must never be exposed to frontend code or client bundles. All external API transactions occur on the secure backend.
- **NFR-04 (EXIF Stripping & Anonymization)**: Sensitive citizen EXIF metadata (device serials, personal phone identifiers) is stripped prior to storage.
- **NFR-05 (Input Sanitization)**: All file uploads must pass MIME type and extension validation to prevent remote code execution.

### 3.3 Usability & Accessibility
- **NFR-06 (Mobile Responsiveness)**: The interface must render fluidly across smartphone screens (360px+), tablets, and desktop workstations.
- **NFR-07 (WCAG AA Compliance)**: High-contrast color palettes for status badges and large touch-friendly buttons ensure accessibility for elderly citizens and field workers.

---

## 4. Hardware Requirements

| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Processor** | Dual-Core 2.0 GHz (x86_64 / ARM) | Quad-Core 2.8 GHz+ (Intel i5/Ryzen 5/Apple M-series) |
| **RAM** | 2 GB Available RAM | 4 GB+ RAM |
| **Disk Storage** | 250 MB free disk space | 1 GB SSD storage |
| **Network** | 2G/3G connectivity (Offline Edge mode requires 0 KBps) | 4G/5G / Broadband |
| **Camera** | 2-megapixel smartphone camera | 8+ megapixel camera with geotagging |

---

## 5. Software Requirements

- **Operating System**: Windows 10/11, Ubuntu 20.04+, macOS 12+
- **Runtime Environment**: Python 3.10 to 3.13
- **Core Framework**: Flask 3.x, Werkzeug, Flask-CORS
- **AI Libraries**: Pillow (PIL), NumPy, Scikit-learn, Requests
- **Database**: SQLite3 (Embedded, zero-install)
- **Frontend Technologies**: HTML5, Modern CSS, Tailwind CSS (CDN), Vanilla JavaScript (ES6+)
- **Mapping & Charts**: Leaflet.js 1.9.4, Chart.js 4.x
- **Optional Cloud AI**: Google AI Studio Gemini 1.5/2.0 Flash API

---

## 6. Requirement Prioritization (MoSCoW Matrix)

- **Must Have (MVP)**: Image upload, instant hazard classification, severity scoring, SQLite storage, 50m proximity deduplication, GIS heatmap, municipal triage queue, and Before-After verification engine.
- **Should Have**: Ward Civic Health Index (CHI) calculation, Chart.js analytics dashboard, and Nagrik AI Copilot chatbot.
- **Could Have**: Native smartphone speech-to-text integration, automated SMS/WhatsApp alerts.
- **Won't Have (Future Scope)**: Satellite synthetic-aperture radar (SAR) integration, drone-based aerial thermal road inspections.
