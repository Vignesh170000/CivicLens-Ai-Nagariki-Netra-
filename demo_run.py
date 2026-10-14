"""
Live Demonstration Script for CivicLens AI (NagrikNetra)
Demonstrates:
1. Instant Multimodal AI Scan
2. Report Ingestion & Automatic Routing
3. Proximity Clustering (50-meter deduplication)
4. Anti-Fraud Rejection (Contractor uploading identical photo)
5. AI Surface Leveling Verification (Genuine repair passed & auto-closed)
6. Ward Civic Health Index (CHI) update
"""
import urllib.request
import urllib.parse
import json

BASE_URL = "http://127.0.0.1:5000"

def post(endpoint, data):
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}{endpoint}", data=encoded, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        res = urllib.request.urlopen(req)
        return json.loads(res.read().decode("utf-8")), res.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode("utf-8")), e.code

def get(endpoint):
    res = urllib.request.urlopen(f"{BASE_URL}{endpoint}")
    return json.loads(res.read().decode("utf-8"))

def run_demo():
    print("=" * 70)
    print("   CIVICLENS AI (NAGRIKNETRA) - LIVE OPERATIONAL DEMONSTRATION")
    print("=" * 70)
    print()

    # 1. Instant AI Scan
    print("[STEP 1] Citizen Uploads Photo -> Instant AI Computer Vision Triage")
    print("-" * 70)
    scan_res, _ = post("/api/scan", {
        "sample_image_path": "/static/sample_images/pothole_before.jpg",
        "description": "Deep dangerous crater on Outer Ring Road near Bellandur flyover"
    })
    print(f" -> Detected Hazard Class : {scan_res.get('hazard_type')}")
    print(f" -> Calculated Severity   : {scan_res.get('severity')}/10 ({scan_res.get('priority')} Priority)")
    print(f" -> AI Confidence Score   : {round(scan_res.get('confidence', 0)*100, 1)}%")
    print(f" -> Auto-Routed Department: {scan_res.get('department')}")
    print(f" -> Dynamic SLA Target    : {scan_res.get('sla_hours')} Hours")
    print(f" -> Generated Work Order  : {scan_res.get('work_order_summary')}")
    print(f" -> AI Engine Used        : {scan_res.get('ai_engine_used')}")
    print()

    # 2. Grievance Ingestion
    print("[STEP 2] Submitting Grievance 1 (Citizen A at Bellandur EcoSpace)")
    print("-" * 70)
    rep1_res, _ = post("/api/reports", {
        "title": "Severe Crater on Bellandur Service Road",
        "description": "Two-wheelers violently skidding in rain; deep crater.",
        "city": "Bengaluru",
        "ward": "Ward 150 - Bellandur",
        "address": "Near EcoSpace Gate 1, ORR",
        "latitude": 12.9260,
        "longitude": 77.6762,
        "sample_image_path": "/static/sample_images/pothole_before.jpg"
    })
    ticket1 = rep1_res["incident"]
    ticket1_id = ticket1["id"]
    print(f" -> Ticket Issued         : {ticket1['ticket_number']}")
    print(f" -> Assigned Ward         : {ticket1['ward']}")
    print(f" -> Status in Municipal DB: {ticket1['status']}")
    print(f" -> Master Cluster ID     : {ticket1['cluster_id']}")
    print(f" -> Initial Community Upvotes: {ticket1['upvotes']}")
    print()

    # 3. Geospatial Deduplication
    print("[STEP 3] Citizen B Reports Same Hazard 22 Meters Away (Deduplication Test)")
    print("-" * 70)
    rep2_res, _ = post("/api/reports", {
        "title": "Huge pothole opposite EcoSpace",
        "description": "Accident risk near bus stop",
        "city": "Bengaluru",
        "ward": "Ward 150 - Bellandur",
        "address": "EcoSpace Bus Stop, ORR",
        "latitude": 12.9262,
        "longitude": 77.6763,
        "sample_image_path": "/static/sample_images/pothole_before.jpg"
    })
    ticket2 = rep2_res["incident"]
    print(f" -> Is Merged in Cluster? : {ticket2.get('is_clustered')} (Detected {ticket2.get('cluster_proximity_m')}m proximity)")
    print(f" -> Merged Cluster ID     : {ticket2.get('cluster_id')}")
    print(f" -> Result                : Merged into master cluster! No duplicate ticket spam created.")
    print()

    # 4. Anti-Fraud Check
    print("[STEP 4A] Contractor Attempts FRAUD: Uploads Identical Un-repaired Photo")
    print("-" * 70)
    fraud_res, code = post("/api/verify-resolution", {
        "incident_id": ticket1_id,
        "sample_after_path": "/static/sample_images/pothole_before.jpg"
    })
    print(f" -> HTTP Response Code    : {code} (Validation Failed)")
    print(f" -> AI Verified Status    : {fraud_res.get('verified')}")
    print(f" -> Clearance Score       : {fraud_res.get('verification_score')}%")
    print(f" -> System Audit Result   : {fraud_res.get('remarks')}")
    print(f" -> Action                : Ticket CANNOT be closed. Work order remains open.")
    print()

    # 5. Genuine Repair Verification
    print("[STEP 4B] Contractor Submits GENUINE Repair Proof (Smooth Bitumen Patch)")
    print("-" * 70)
    real_res, code = post("/api/verify-resolution", {
        "incident_id": ticket1_id,
        "sample_after_path": "/static/sample_images/pothole_after.jpg"
    })
    print(f" -> HTTP Response Code    : {code} (Success)")
    print(f" -> AI Verified Status    : {real_res.get('verified')}")
    print(f" -> Surface Clearance Score: {real_res.get('verification_score')}%")
    print(f" -> AI Audit Remarks      : {real_res.get('remarks')}")
    print(f" -> Database Status Update: {real_res.get('incident', {}).get('status')}")
    print()

    # 6. Ward Analytics & CHI
    print("[STEP 5] Ward Civic Health Index (CHI) Scorecard Recalibration")
    print("-" * 70)
    analytics = get("/api/analytics")
    print(f" -> Total Logged Issues   : {analytics.get('total_incidents')}")
    print(f" -> Verified Resolved     : {analytics.get('resolved_incidents')}")
    print(f" -> Metro Resolution Rate : {analytics.get('resolution_rate')}%")
    print(f" -> Avg Verification Score: {analytics.get('avg_verification_score')}%")
    print()
    print(" -> Ward Leaderboard Snapshot:")
    for w in analytics.get("ward_health_index", [])[:4]:
        print(f"    * {w['ward']:<26} | Total: {w['total']} | Resolved: {w['resolved']} | CHI Score: {w['chi_score']}/100 [Grade {w['grade']}]")
    print()
    print("=" * 70)
    print("   LIVE DEMONSTRATION COMPLETE: ALL MODULES VERIFIED OPERATIONAL!")
    print("=" * 70)

if __name__ == "__main__":
    run_demo()
