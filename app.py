"""
CivicLens AI (NagrikNetra) - Web Server & REST API
Flask backend connecting AI Engine, SQLite Database, and Frontend UI.
"""

import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

import models
import ai_engine
import states_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
CORS(app)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

import tempfile
IS_VERCEL = bool(os.environ.get("VERCEL"))
if IS_VERCEL:
    UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "uploads")
else:
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

SAMPLE_FOLDER = os.path.join(BASE_DIR, "static", "sample_images")

try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception:
    pass

try:
    os.makedirs(SAMPLE_FOLDER, exist_ok=True)
except Exception:
    pass

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database on startup
try:
    models.init_db(seed=True)
except Exception as e:
    print("Database initialization notice:", e)

# -------------------------------------------------------------
# FRONTEND ROUTE
# -------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/uploads/<path:filename>")
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# -------------------------------------------------------------
# REST API ENDPOINTS
# -------------------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "service": "CivicLens AI (NagrikNetra)",
        "version": "2.0.0",
        "ai_cloud_mode": bool(ai_engine.GEMINI_API_KEY),
        "ai_engine": "Google Gemini 1.5/2.0 Flash" if ai_engine.GEMINI_API_KEY else "Edge Vision Heuristics (Offline Guarantee)",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/sample-images", methods=["GET"])
def get_sample_images():
    """Returns sample test images for one-click testing in the UI."""
    samples = [
        {
            "id": "pothole",
            "name": "Crater Pothole (Road Hazard)",
            "before": "/static/sample_images/pothole_before.jpg",
            "after": "/static/sample_images/pothole_after.jpg",
            "suggested_title": "Severe crater pothole on major road",
            "city": "Bengaluru",
            "ward": "Ward 150 - Bellandur",
            "lat": 12.9260,
            "lng": 77.6762
        },
        {
            "id": "garbage",
            "name": "Open Solid Waste Dump (Sanitation Hazard)",
            "before": "/static/sample_images/garbage_before.jpg",
            "after": "/static/sample_images/garbage_after.jpg",
            "suggested_title": "Commercial garbage overflow on sidewalk",
            "city": "Bengaluru",
            "ward": "Ward 80 - Hoysala Nagar",
            "lat": 12.9719,
            "lng": 77.6412
        },
        {
            "id": "wire",
            "name": "Live Electric Wire (Pedestrian Hazard)",
            "before": "/static/sample_images/wire_hazard_before.jpg",
            "after": "/static/sample_images/wire_hazard_after.jpg",
            "suggested_title": "Snapped dangling electric line near school",
            "city": "Bengaluru",
            "ward": "Ward 151 - Koramangala",
            "lat": 12.9352,
            "lng": 77.6245
        }
    ]
    return jsonify({"samples": samples})

@app.route("/api/scan", methods=["POST"])
def scan_image():
    """
    Instant Pre-Submission AI Triage:
    Takes an image and description, runs multimodal analysis, and returns
    detected hazard type, severity (1-10), priority, confidence, and target municipal department.
    """
    description = request.form.get("description", "")
    sample_path = request.form.get("sample_image_path", "")
    image_file = request.files.get("image")
    
    saved_path = None
    web_url = None
    
    if image_file and allowed_file(image_file.filename):
        filename = f"scan_{uuid.uuid4().hex[:8]}_{secure_filename(image_file.filename)}"
        saved_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(saved_path)
        web_url = f"/static/uploads/{filename}"
    elif sample_path:
        rel_path = sample_path.lstrip("/").replace("/", os.sep)
        potential_path = os.path.join(os.path.dirname(__file__), rel_path)
        if os.path.exists(potential_path):
            saved_path = potential_path
            web_url = sample_path
            
    if not saved_path or not os.path.exists(saved_path):
        return jsonify({"error": "No valid image provided for AI scan"}), 400
        
    # Run AI Analysis (Gemini if key exists, otherwise Local CV Heuristics)
    ai_result = ai_engine.analyze_image_with_gemini(saved_path, description)
    ai_result["image_url"] = web_url
    return jsonify(ai_result)

@app.route("/api/states", methods=["GET"])
def get_states():
    """Returns all 28 States and 8 Union Territories with metadata."""
    return jsonify({
        "states": states_data.get_states_list(),
        "raw": states_data.ALL_INDIA_STATES
    })

@app.route("/api/reports", methods=["POST"])
def create_report():
    """
    Submit a citizen grievance report.
    Performs AI assessment, checks 50m geospatial clustering for deduplication,
    assigns department SLA, and stores incident in SQLite.
    """
    title = request.form.get("title", "")
    description = request.form.get("description", "")
    state = request.form.get("state", "Karnataka")
    city = request.form.get("city", "Bengaluru")
    ward = request.form.get("ward", "Ward 1 - Central")
    address = request.form.get("address", "")
    
    try:
        lat = float(request.form.get("latitude", 12.9716))
        lng = float(request.form.get("longitude", 77.5946))
    except (ValueError, TypeError):
        lat, lng = 12.9716, 77.5946
        
    image_file = request.files.get("image")
    sample_path = request.form.get("sample_image_path", "")
    
    before_img_path = None
    web_img_url = "/static/sample_images/pothole_before.jpg"
    
    if image_file and allowed_file(image_file.filename):
        filename = f"incident_{uuid.uuid4().hex[:8]}_{secure_filename(image_file.filename)}"
        before_img_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(before_img_path)
        web_img_url = f"/static/uploads/{filename}"
    elif sample_path:
        rel_path = sample_path.lstrip("/").replace("/", os.sep)
        potential_path = os.path.join(os.path.dirname(__file__), rel_path)
        if os.path.exists(potential_path):
            before_img_path = potential_path
            web_img_url = sample_path
            
    if not before_img_path:
        before_img_path = os.path.join(SAMPLE_FOLDER, "pothole_before.jpg")
        web_img_url = "/static/sample_images/pothole_before.jpg"
        
    # 1. Run AI analysis
    ai_result = ai_engine.analyze_image_with_gemini(before_img_path, description)
    
    # 2. Geospatial Clustering (50-meter proximity grouping)
    existing = models.list_incidents()
    cluster_id, duplicate_id, distance_m = ai_engine.find_or_create_cluster(lat, lng, existing, threshold_meters=50.0)
    
    # Determine effective hazard type, allowing citizen/user manual correction
    chosen_hazard = request.form.get("hazard_type")
    if chosen_hazard and chosen_hazard.strip():
        final_hazard = chosen_hazard.strip()
        dept_info = ai_engine.get_department_and_sla(final_hazard, ai_result["severity"])
        final_dept = dept_info["department"]
        final_sla = dept_info["sla_hours"]
        final_work_order = dept_info["work_order"]
    else:
        final_hazard = ai_result["hazard_type"]
        final_dept = ai_result["department"]
        final_sla = ai_result["sla_hours"]
        final_work_order = ai_result.get("work_order_summary", "Field dispatch queued.")

    # Auto-generate title if missing
    if not title:
        title = f"{final_hazard} near {address or ward}"
        
    incident_data = {
        "title": title,
        "description": description or f"Reported via CivicLens AI. Detected: {final_hazard}",
        "hazard_type": final_hazard,
        "severity": ai_result["severity"],
        "priority": ai_result["priority"],
        "latitude": lat,
        "longitude": lng,
        "address": address or f"{ward}, {city}",
        "ward": ward,
        "city": city,
        "state": state,
        "department": final_dept,
        "sla_hours": final_sla,
        "before_image": web_img_url,
        "cluster_id": cluster_id,
        "upvotes": 1,
        "ai_confidence": ai_result["confidence"],
        "ai_defect_details": ai_result.get("defect_details", {}),
        "work_order_summary": final_work_order
    }
    
    created = models.create_incident(incident_data)
    created["is_clustered"] = bool(duplicate_id)
    created["cluster_proximity_m"] = distance_m if duplicate_id else 0.0
    created["ai_engine_used"] = ai_result.get("ai_engine_used", "CivicLens AI")
    
    return jsonify({"success": True, "incident": created}), 201

@app.route("/api/reports", methods=["GET"])
def get_reports():
    hazard = request.args.get("hazard_type")
    status = request.args.get("status")
    state = request.args.get("state")
    city = request.args.get("city")
    ward = request.args.get("ward")
    search = request.args.get("search")
    
    incidents = models.list_incidents(
        hazard_type=hazard, status=status, state=state, city=city, ward=ward, search=search
    )
    return jsonify({"incidents": incidents, "count": len(incidents)})

@app.route("/api/reports/<int:incident_id>", methods=["GET"])
def get_single_report(incident_id):
    inc = models.get_incident(incident_id)
    if not inc:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify({"incident": inc})

@app.route("/api/reports/<int:incident_id>/upvote", methods=["POST"])
def upvote(incident_id):
    inc = models.upvote_incident(incident_id)
    if not inc:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify({"success": True, "upvotes": inc["upvotes"]})

@app.route("/api/reports/<int:incident_id>/status", methods=["POST"])
def update_status(incident_id):
    data = request.json or {}
    new_status = data.get("status")
    actor = data.get("actor", "Municipal Officer")
    
    if new_status not in ["Reported", "Investigating", "Assigned", "In Progress", "Resolved", "Rejected"]:
        return jsonify({"error": "Invalid status"}), 400
        
    inc = models.update_incident_status(incident_id, new_status, actor=actor)
    return jsonify({"success": True, "incident": inc})

@app.route("/api/verify-resolution", methods=["POST"])
def verify_resolution():
    """
    Contractor Before-and-After Resolution Verification Loop.
    Compares the original incident photo with the post-repair proof photo.
    Returns AI verification confidence score, remarks, and updates ticket status to 'Resolved' if passing.
    """
    incident_id = request.form.get("incident_id")
    after_file = request.files.get("after_image")
    sample_after_path = request.form.get("sample_after_path", "")
    
    if not incident_id:
        return jsonify({"error": "Missing incident_id"}), 400
        
    incident = models.get_incident(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
        
    before_url = incident.get("before_image")
    if not before_url:
        return jsonify({"error": "Incident has no original before image to verify against"}), 400
        
    # Map before_url to local path
    rel_before = before_url.lstrip("/").replace("/", os.sep)
    local_before = os.path.join(os.path.dirname(__file__), rel_before)
    if not os.path.exists(local_before):
        # Fallback to sample pothole before
        local_before = os.path.join(SAMPLE_FOLDER, "pothole_before.jpg")
        
    local_after = None
    web_after_url = None
    
    if after_file and allowed_file(after_file.filename):
        fname = f"resolution_{uuid.uuid4().hex[:8]}_{secure_filename(after_file.filename)}"
        local_after = os.path.join(UPLOAD_FOLDER, fname)
        after_file.save(local_after)
        web_after_url = f"/static/uploads/{fname}"
    elif sample_after_path:
        rel_after = sample_after_path.lstrip("/").replace("/", os.sep)
        potential = os.path.join(os.path.dirname(__file__), rel_after)
        if os.path.exists(potential):
            local_after = potential
            web_after_url = sample_after_path
            
    if not local_after or not os.path.exists(local_after):
        return jsonify({"error": "Valid post-repair proof photo is required"}), 400
        
    employee_id = request.form.get("employee_id", "BBMP-ENG-8492")
    employee_name = request.form.get("employee_name", "Er. Rajesh Kumar")
    employee_dept = request.form.get("employee_dept", "Public Works Department (Roads & Bridges)")
    
    # 1. Worker Arrival Selfie & Attendance Audit
    worker_selfie_file = request.files.get("worker_selfie")
    sample_selfie_path = request.form.get("sample_selfie_path", "")
    
    local_selfie = None
    web_selfie_url = None
    
    if worker_selfie_file and allowed_file(worker_selfie_file.filename):
        sname = f"selfie_{uuid.uuid4().hex[:8]}_{secure_filename(worker_selfie_file.filename)}"
        local_selfie = os.path.join(UPLOAD_FOLDER, sname)
        worker_selfie_file.save(local_selfie)
        web_selfie_url = f"/static/uploads/{sname}"
    elif sample_selfie_path:
        rel_s = sample_selfie_path.lstrip("/").replace("/", os.sep)
        pot_s = os.path.join(os.path.dirname(__file__), rel_s)
        if os.path.exists(pot_s):
            local_selfie = pot_s
            web_selfie_url = sample_selfie_path
            
    if not local_selfie:
        # Pick appropriate sample worker selfie based on hazard
        h_type = incident.get("hazard_type", "").lower()
        if "garbage" in h_type or "waste" in h_type:
            s_file = "worker_selfie_garbage.jpg"
        elif "wire" in h_type or "electric" in h_type:
            s_file = "worker_selfie_wire.jpg"
        else:
            s_file = "worker_selfie_pothole.jpg"
            
        local_selfie = os.path.join(SAMPLE_FOLDER, s_file)
        web_selfie_url = f"/static/sample_images/{s_file}"
        
    selfie_audit = ai_engine.verify_worker_selfie(local_selfie)
    
    # 2. Coordinates & Geofence Verification
    try:
        checkin_lat = float(request.form.get("checkin_lat", incident.get("latitude", 12.9716)))
        checkin_lng = float(request.form.get("checkin_lng", incident.get("longitude", 77.5946)))
    except (ValueError, TypeError):
        checkin_lat, checkin_lng = incident.get("latitude", 12.9716), incident.get("longitude", 77.5946)
        
    try:
        completion_lat = float(request.form.get("completion_lat", checkin_lat))
        completion_lng = float(request.form.get("completion_lng", checkin_lng))
    except (ValueError, TypeError):
        completion_lat, completion_lng = checkin_lat, checkin_lng
        
    geofence_dist_m = ai_engine.haversine_distance(
        checkin_lat, checkin_lng,
        incident.get("latitude", checkin_lat), incident.get("longitude", checkin_lng)
    )
    geofence_verified = (geofence_dist_m <= 150.0)
    geofence_status_label = f"Verified On-Site ({round(geofence_dist_m, 1)}m from hazard GPS)" if geofence_verified else f"Geofence Alert ({round(geofence_dist_m, 1)}m deviation)"
    
    # 3. Run AI Before-After Verification
    ver_result = ai_engine.verify_repair_resolution(local_before, local_after, incident.get("hazard_type", ""))
    
    # If verified, mark incident as Resolved
    if ver_result.get("verified", False):
        actor_label = f"{employee_name} [{employee_id}]" if employee_id else "CivicLens AI Verification Engine"
        updated = models.update_incident_status(
            incident_id,
            status="Resolved",
            after_image=web_after_url,
            verification_score=ver_result.get("verification_score"),
            verification_remarks=ver_result.get("remarks"),
            actor=actor_label,
            worker_selfie=web_selfie_url,
            checkin_lat=checkin_lat,
            checkin_lng=checkin_lng,
            completion_lat=completion_lat,
            completion_lng=completion_lng,
            worker_name=employee_name,
            worker_id=employee_id,
            geofence_status=geofence_status_label
        )
        return jsonify({
            "success": True,
            "verified": True,
            "verification_score": ver_result["verification_score"],
            "remarks": ver_result["remarks"],
            "geofence": {
                "status": geofence_status_label,
                "verified": geofence_verified,
                "distance_meters": round(geofence_dist_m, 1),
                "incident_coords": [incident.get("latitude"), incident.get("longitude")],
                "checkin_coords": [checkin_lat, checkin_lng],
                "completion_coords": [completion_lat, completion_lng]
            },
            "worker": {
                "name": employee_name,
                "id": employee_id,
                "dept": employee_dept,
                "selfie_url": web_selfie_url,
                "safety_gear": selfie_audit.get("safety_gear_detected", "Verified"),
                "attendance": selfie_audit.get("facial_attendance", "Authenticated")
            },
            "incident": updated
        })
    else:
        # Rejected verification (e.g. fraud or incomplete work)
        return jsonify({
            "success": False,
            "verified": False,
            "verification_score": ver_result.get("verification_score", 0),
            "remarks": ver_result.get("remarks", "Defect still detected on-site. Work order remains open.")
        }), 422

@app.route("/api/demo/reset", methods=["POST"])
def reset_demo_tickets():
    """Resets field tickets to active state for presentation/testing."""
    conn = models.get_db()
    c = conn.cursor()
    c.execute("UPDATE incidents SET status='Assigned', after_image=NULL, verification_score=NULL, verification_remarks=NULL, before_image='/static/sample_images/pothole_before.jpg' WHERE id IN (1, 8, 13, 20)")
    c.execute("UPDATE incidents SET status='In Progress', after_image=NULL, verification_score=NULL, verification_remarks=NULL, before_image='/static/sample_images/garbage_before.jpg' WHERE id IN (2, 5, 21)")
    c.execute("UPDATE incidents SET status='In Progress', after_image=NULL, verification_score=NULL, verification_remarks=NULL, before_image='/static/sample_images/wire_hazard_before.jpg' WHERE id IN (3, 9, 23)")
    c.execute("UPDATE incidents SET status='Reported', after_image=NULL, verification_score=NULL, verification_remarks=NULL WHERE id IN (6, 7, 10, 24)")
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Demo field tickets reset to active state."})

@app.route("/api/analytics", methods=["GET"])
def get_analytics():
    stats = models.get_analytics()
    return jsonify(stats)

@app.route("/api/chat", methods=["POST"])
def citizen_chat():
    data = request.json or {}
    message = data.get("message", "")
    if not message:
        return jsonify({"reply": "Please describe your question or issue."}), 400
        
    reply = ai_engine.chat_with_civic_bot(message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"============================================================")
    print(f" CivicLens AI (NagrikNetra) running at http://127.0.0.1:{port}")
    print(f" AI Cloud Mode: {'Active (Gemini)' if ai_engine.GEMINI_API_KEY else 'Edge Vision Mode (Offline Resilient)'}")
    print(f"============================================================")
    app.run(host="127.0.0.1", port=port, debug=False)
