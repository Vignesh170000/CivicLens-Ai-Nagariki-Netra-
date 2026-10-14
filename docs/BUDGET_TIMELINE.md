# Project Budget, Timeline & Team Roles
## CivicLens AI (NagrikNetra)

---

## 1. Estimated Project Budget (Student / Hackathon Tier)

| Item / Resource | Provider / Tool | Cost (INR) | Free-Tier Limitations & Notes |
| :--- | :--- | :--- | :--- |
| **Multimodal Vision API** | Google AI Studio (Gemini 1.5/2.0 Flash) | **₹0.00** | Free tier provides 15 Requests Per Minute (RPM), up to 1,500 Requests Per Day (RPD). More than sufficient for hackathons. |
| **Edge Vision Inference** | Embedded Python (PIL + NumPy) | **₹0.00** | Runs locally on CPU with zero network calls. |
| **Backend & Web Hosting** | Render / Railway / Localhost | **₹0.00** | Free tier spinning web service (512 MB RAM, free tier instance). |
| **Database Storage** | Embedded SQLite3 | **₹0.00** | Zero cloud database subscription costs; stored locally in project root. |
| **Mapping & GIS Tiles** | OpenStreetMap + Leaflet.js | **₹0.00** | 100% free open-source mapping without credit card requirement. |
| **Domain & SSL** | Localhost / ngrok / Render `.onrender.com` | **₹0.00** | Free development and demonstration URLs with auto-generated SSL. |
| **Total MVP Development Cost** | — | **₹0.00 (Free)** | **Accessible to any Indian student developer** |

### Optional Production Scale Enhancements
- Dedicated Cloud GPU Instance (AWS / GCP / RunPod for custom YOLOv8 fine-tuning): ₹2,500 / month
- Custom `.org` / `.in` Domain & Cloudflare SSL: ₹850 / year
- Twilio / Kaleyra WhatsApp Business API for grievance alerts: ₹1,500 / month

---

## 2. 7 to 14-Day Development Schedule

```
Day 1 - 2: Problem Research & Architectural Design
├── Conduct stakeholder analysis across PWD, SWM, and citizen forums
├── Define Software Requirements Specification (SRS) and SQLite schema
└── Design dual-mode AI fallback strategy

Day 3 - 5: AI Engine & Backend Core
├── Implement Gemini 1.5/2.0 Flash REST API integration
├── Build PIL & NumPy edge heuristic computer vision algorithms
├── Develop Haversine 50-meter proximity clustering logic
└── Build Before-and-After Resolution Verification scoring pipeline

Day 6 - 8: Interactive Frontend & Visualizations
├── Implement responsive Tailwind CSS interface (Citizen, Command, Verification, Analytics)
├── Build Leaflet.js GIS map with color-coded severity markers
├── Implement Chart.js analytics for hazard distribution and city stats
└── Integrate animated AI laser-scan preview feedback

Day 9 - 11: Testing, Refinement & Data Seeding
├── Seed realistic Indian metropolitan incident datasets (Bengaluru, Delhi, Mumbai, Hyderabad, Chennai)
├── Create sample before-and-after photo pairs (potholes, garbage, electric wires)
├── Run automated test suite (`test_engine.py`) verifying 100% pass rate
└── Calibrate Before-After surface clearance scoring thresholds

Day 12 - 14: Pitch Deck, Demo Rehearsal & Deployment
├── Finalize 10-slide competition pitch deck (`docs/PITCH_DECK.md`)
├── Rehearse 5-7 minute live demonstration script (`docs/DEMO_SCRIPT.md`)
├── Prepare judges FAQ responses (`docs/JUDGES_FAQ.md`)
└── Package one-click Windows launcher (`run.bat` & `run.ps1`)
```

---

## 3. Team Roles for 1 to 4 Students

### Solo Developer (Full-Stack AI Generalist)
- Executes full stack: Flask API, AI vision integration, database, frontend templates, test suite, and pitch deck.

### 2-Member Team
- **Member 1 (AI & Backend Specialist)**: Gemini API, edge CV heuristics, Haversine clustering, resolution verification, SQLite database, and automated tests.
- **Member 2 (Frontend & Design Lead)**: HTML5/Tailwind layout, Leaflet GIS integration, Chart.js analytics, sample scenarios, pitch presentation, and demo script.

### 3 to 4-Member Team
- **Member 1 (AI / Machine Learning Engineer)**: Vision classification, prompt engineering, surface restoration scoring, and anti-fraud clone checks.
- **Member 2 (Full-Stack Backend Architect)**: Flask REST API, SQLite models, geospatial clustering, SLA scheduling, and test suite.
- **Member 3 (Frontend & GIS Engineer)**: UI/UX design, Leaflet.js interactive maps, camera capture integration, Chart.js dashboards, and mobile responsiveness.
- **Member 4 (Civic Domain Analyst & Pitch Lead)**: Stakeholder research, civic health index algorithmic formula, pitch deck, video demo recording, and judges Q&A lead.

---

## 4. Minimum Viable Product (MVP) vs. Future Enhancements

### Mandatory Features in Working Prototype (MVP - Delivered)
- [x] Instant Multimodal Visual Triage (Hazard, Severity 1-10, Department, SLA).
- [x] Dual-Mode AI engine (Cloud Gemini + Resilient Offline Edge CV).
- [x] Geospatial 50m Haversine Clustering to prevent duplicate tickets.
- [x] Interactive Leaflet GIS Map with Indian city pins and severity styling.
- [x] Municipal Command Triage Queue with SLA countdown alerts.
- [x] Contractor Before-and-After Resolution Verification with quantitative scoring.
- [x] Ward Civic Health Index (CHI) scorecard and Chart.js analytics.
- [x] Pre-seeded realistic Indian metropolitan dataset and test imagery.
- [x] Conversational Nagrik AI Copilot chatbot.

### Optional Advanced Features (Future Roadmap)
- [ ] Direct WhatsApp Business API Bot for zero-app grievance submission.
- [ ] Dashcam continuous video stream processing on municipal buses/garbage trucks.
- [ ] Satellite SAR (Synthetic Aperture Radar) radar analysis for post-monsoon road erosion.
- [ ] Blockchain-backed contractor work order audit trail for municipal tendering transparency.
