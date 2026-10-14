"""
CivicLens AI Database Models & Data Access Layer
Zero-dependency SQLite storage supporting all 28 States & 8 Union Territories of India.
"""
import sqlite3
import os
import json
import uuid
from datetime import datetime, timedelta

import shutil

import tempfile

IS_VERCEL = bool(os.environ.get("VERCEL"))

if IS_VERCEL:
    TMP_DIR = tempfile.gettempdir()
    DB_PATH = os.path.join(TMP_DIR, "civiclens.db")
    ORIG_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "civiclens.db")
    if not os.path.exists(DB_PATH) and os.path.exists(ORIG_DB):
        try:
            shutil.copy2(ORIG_DB, DB_PATH)
        except Exception as e:
            print("Failed to copy seed db to temp dir:", e)
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "civiclens.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    try:
        if not IS_VERCEL:
            conn.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        pass
    try:
        conn.execute("PRAGMA busy_timeout=30000;")
    except Exception:
        pass
    conn.row_factory = sqlite3.Row
    return conn

def init_db(seed=True):
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Incidents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_number TEXT UNIQUE,
        title TEXT NOT NULL,
        description TEXT,
        hazard_type TEXT NOT NULL,
        severity INTEGER NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Reported',
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        address TEXT NOT NULL,
        ward TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL DEFAULT 'Karnataka',
        department TEXT NOT NULL,
        assigned_engineer TEXT,
        sla_hours INTEGER NOT NULL DEFAULT 48,
        before_image TEXT,
        after_image TEXT,
        cluster_id TEXT,
        upvotes INTEGER DEFAULT 1,
        created_at TEXT NOT NULL,
        resolved_at TEXT,
        ai_confidence REAL DEFAULT 0.85,
        ai_defect_details TEXT,
        work_order_summary TEXT,
        verification_score REAL,
        verification_remarks TEXT
    )
    """)
    
    # Migration: check if 'state' and worker tracking columns exist
    cursor.execute("PRAGMA table_info(incidents)")
    cols = [col[1] for col in cursor.fetchall()]
    new_cols = [
        ("state", "TEXT DEFAULT 'Karnataka'"),
        ("worker_selfie", "TEXT"),
        ("checkin_lat", "REAL"),
        ("checkin_lng", "REAL"),
        ("completion_lat", "REAL"),
        ("completion_lng", "REAL"),
        ("worker_name", "TEXT"),
        ("worker_id", "TEXT"),
        ("geofence_status", "TEXT")
    ]
    for col_name, col_def in new_cols:
        if col_name not in cols:
            cursor.execute(f"ALTER TABLE incidents ADD COLUMN {col_name} {col_def}")
    
    # 2. Departments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        head_officer TEXT,
        emergency_contact TEXT,
        sla_standard_hours INTEGER
    )
    """)
    
    # 3. Audit Log Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id INTEGER,
        action TEXT NOT NULL,
        actor TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        details TEXT,
        FOREIGN KEY (incident_id) REFERENCES incidents(id)
    )
    """)
    
    conn.commit()
    
    # Check if we need to seed
    cursor.execute("SELECT COUNT(*) FROM incidents")
    count = cursor.fetchone()[0]
    if count == 0 and seed:
        seed_database(conn)
        
    conn.close()

def seed_database(conn):
    cursor = conn.cursor()
    
    departments = [
        ("PWD", "Public Works Department (Roads & Bridges)", "All India", "Er. R. K. Sharma", "1800-425-5000", 24),
        ("SWM", "Municipal Solid Waste Management", "All India", "Dr. Geeta Narayanan", "1969", 12),
        ("POWER", "State Electricity Board / Discom", "All India", "Er. M. Praveen", "1912", 4),
        ("WATER", "Water Supply and Sewerage Board", "All India", "Er. K. Sreenivas", "1800-425-1000", 18),
        ("TRAFFIC", "City Traffic Police (Hazard Management)", "All India", "DCP Anand Rao", "103 / 112", 6),
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO departments (code, name, city, head_officer, emergency_contact, sla_standard_hours)
    VALUES (?, ?, ?, ?, ?, ?)
    """, departments)
    
    now = datetime.now()
    
    # Realistic Seed Incidents across Indian States (North, South, East, West, Central, Northeast)
    seed_incidents = [
        # Karnataka
        (
            "CIVIC-KA-2026-1001",
            "Severe 1.2m Deep Crater Pothole on Outer Ring Road",
            "Dangerous crater near Bellandur flyover causing severe bike skids and evening traffic jams during rain.",
            "Pothole & Road Damage",
            9,
            "Critical",
            "Assigned",
            12.9260,
            77.6762,
            "Service Road near Bellandur EcoSpace, ORR",
            "Ward 150 - Bellandur",
            "Bengaluru",
            "Karnataka",
            "Public Works Department (Roads & Bridges)",
            "Junior Engineer K. Ramesh",
            24,
            "/static/sample_images/pothole_before.jpg",
            None,
            "CLUSTER-BLR-ORR-01",
            14,
            (now - timedelta(hours=6)).isoformat(),
            None,
            0.94,
            json.dumps({"depth_cm": 18, "width_cm": 120, "hazard": "High risk of 2-wheeler fatalities"}),
            "Emergency bituminous cold-mix patch required. Barricading deployed.",
            None,
            None
        ),
        (
            "CIVIC-KA-2026-1002",
            "Illegal Commercial Garbage Dumping at 12th Main Indiranagar",
            "Mixed plastic waste, wet commercial food waste from local restaurants overflowing onto sidewalk, foul stench.",
            "Garbage & Solid Waste",
            8,
            "High",
            "In Progress",
            12.9719,
            77.6412,
            "Corner of 12th Main & 100ft Road, Indiranagar",
            "Ward 80 - Hoysala Nagar",
            "Bengaluru",
            "Karnataka",
            "Municipal Solid Waste Management",
            "Ward Inspector S. Ananth",
            12,
            "/static/sample_images/garbage_before.jpg",
            None,
            "CLUSTER-BLR-IND-01",
            8,
            (now - timedelta(hours=4)).isoformat(),
            None,
            0.91,
            json.dumps({"volume_m3": 2.5, "waste_types": ["Single-use plastic", "Food waste"]}),
            "Dispatch compacting tipper truck & penalize non-segregating establishments.",
            None,
            None
        ),
        (
            "CIVIC-KA-2026-1003",
            "Dangling Live High-Tension Electric Wire at 5th Block Koramangala",
            "Tree branch broke overhead electric supply wire, dangling 1.8 meters above walking trail near park.",
            "Electrical & Live Wire",
            10,
            "Critical",
            "In Progress",
            12.9352,
            77.6245,
            "17th Cross, 5th Block Koramangala",
            "Ward 151 - Koramangala",
            "Bengaluru",
            "Karnataka",
            "Electricity Supply Company (Power & Safety)",
            "Lineman Supervisor R. Das",
            4,
            "/static/sample_images/wire_hazard_before.jpg",
            None,
            "CLUSTER-BLR-KOR-01",
            22,
            (now - timedelta(hours=2)).isoformat(),
            None,
            0.98,
            json.dumps({"clearance_height_m": 1.8, "voltage": "11kV feeder"}),
            "Feeder substation isolated. Emergency lineman crew dispatched on-site.",
            None,
            None
        ),
        (
            "CIVIC-KA-2026-1004",
            "Successfully Repaired Pothole on CMH Road Indiranagar",
            "Deep pothole repaired with asphalt mastic patch and roller compaction.",
            "Pothole & Road Damage",
            7,
            "Medium",
            "Resolved",
            12.9784,
            77.6389,
            "Near Indiranagar Metro Station Pillar 128",
            "Ward 80 - Hoysala Nagar",
            "Bengaluru",
            "Karnataka",
            "Public Works Department (Roads & Bridges)",
            "Contractor Premier Infra Ltd",
            24,
            "/static/sample_images/pothole_before.jpg",
            "/static/sample_images/pothole_after.jpg",
            "CLUSTER-BLR-IND-02",
            5,
            (now - timedelta(days=2)).isoformat(),
            (now - timedelta(hours=18)).isoformat(),
            0.96,
            json.dumps({"repair_type": "Hot-mix asphalt patch"}),
            "Work completed. Smooth leveling verified.",
            94.5,
            "AI Verification Passed: Defect cleared with complete bituminous flush patch."
        ),
        
        # Maharashtra
        (
            "CIVIC-MH-2026-2001",
            "Submerged Pothole Cluster on Andheri-Kurla Road",
            "Four consecutive wheel-bending potholes submerged under puddle water causing auto-rickshaws to topple.",
            "Pothole & Road Damage",
            9,
            "Critical",
            "Reported",
            19.1136,
            72.8697,
            "Near Chakala Metro Station, Andheri-Kurla Road",
            "Ward K/East - Andheri",
            "Mumbai",
            "Maharashtra",
            "Public Works Department (Roads & Bridges)",
            "Er. Sachin Kadam",
            24,
            "/static/sample_images/pothole_before.jpg",
            None,
            "CLUSTER-MUM-AND-01",
            31,
            (now - timedelta(hours=1)).isoformat(),
            None,
            0.95,
            json.dumps({"pothole_count": 4, "max_depth_cm": 22}),
            "Rapid cold-asphalt hardening mix required immediately.",
            None,
            None
        ),
        (
            "CIVIC-MH-2026-2002",
            "Open Garbage Overflow near Kothrud Depot",
            "Overflowing public waste bin scattering on footpath near bus terminus.",
            "Garbage & Solid Waste",
            7,
            "High",
            "Assigned",
            18.5074,
            73.8077,
            "Paud Road, near Kothrud Bus Stand",
            "Ward 16 - Kothrud",
            "Pune",
            "Maharashtra",
            "Municipal Solid Waste Management",
            "Er. Nitin Shinde",
            12,
            "/static/sample_images/garbage_before.jpg",
            None,
            "CLUSTER-PUN-KOT-01",
            9,
            (now - timedelta(hours=5)).isoformat(),
            None,
            0.89,
            json.dumps({"estimated_kg": 300}),
            "Deploy secondary collection van.",
            None,
            None
        ),

        # Delhi (UT)
        (
            "CIVIC-DL-2026-3001",
            "Open Drain Overflow & Waterlogging at Lajpat Nagar Central Market",
            "Monsoon stormwater drain blocked by silt and single-use plastics, creating 2 feet deep stagnation.",
            "Waterlogging & Sewage",
            9,
            "Critical",
            "Investigating",
            28.5684,
            77.2435,
            "Block 4, Central Market, Lajpat Nagar",
            "Ward 58S - Lajpat Nagar",
            "Delhi",
            "Delhi",
            "Water Supply and Sewerage Board",
            "Er. Vipin Singhal",
            18,
            "/static/sample_images/pothole_before.jpg",
            None,
            "CLUSTER-DEL-LP-01",
            19,
            (now - timedelta(hours=8)).isoformat(),
            None,
            0.92,
            json.dumps({"water_depth_cm": 35}),
            "High-capacity dewatering pump deployed. Super sucker en route.",
            None,
            None
        ),
        (
            "CIVIC-DL-2026-3002",
            "Broken Footpath Slabs and Exposed Rebar near Connaught Place",
            "Pedestrian walkway tiles collapsed with rusty iron rods jutting out, severe tripping hazard.",
            "Broken Footpath / Utility",
            7,
            "High",
            "Assigned",
            28.6315,
            77.2167,
            "Outer Circle, Block E, Connaught Place",
            "Ward NDMC-01 - Connaught Place",
            "Delhi",
            "Delhi",
            "Public Works Department (Roads & Bridges)",
            "JE Amit Verma",
            48,
            "/static/sample_images/pothole_before.jpg",
            None,
            "CLUSTER-DEL-CP-01",
            6,
            (now - timedelta(hours=14)).isoformat(),
            None,
            0.88,
            json.dumps({"damaged_length_m": 8}),
            "Replace precast paver blocks and grind down exposed iron rebar.",
            None,
            None
        ),

        # Tamil Nadu
        (
            "CIVIC-TN-2026-4001",
            "Stagnant Sewage Spill & Clogged Storm Canal in T. Nagar",
            "Overflowing manhole flooding North Usman Road commercial precinct.",
            "Waterlogging & Sewage",
            8,
            "High",
            "Reported",
            13.0418,
            80.2341,
            "North Usman Road, T. Nagar",
            "Ward 136 - T. Nagar",
            "Chennai",
            "Tamil Nadu",
            "Water Supply and Sewerage Board",
            "Er. S. Murugan",
            18,
            "/static/sample_images/garbage_before.jpg",
            None,
            "CLUSTER-CHE-TN-01",
            11,
            (now - timedelta(hours=3)).isoformat(),
            None,
            0.90,
            json.dumps({"spill_radius_m": 15}),
            "Desilting suction vehicle dispatched to unblock trunk sewer line.",
            None,
            None
        ),

        # Telangana
        (
            "CIVIC-TG-2026-5001",
            "Overturned Transformer and Exposed Cables at Hitec City Cyber Towers",
            "Construction vehicle brushed against feeder box, sparking overhead cables.",
            "Electrical & Live Wire",
            10,
            "Critical",
            "Resolved",
            17.4504,
            78.3808,
            "Junction Pillar 44, Cyber Towers Road, Madhapur",
            "Ward 107 - Madhapur Hitec City",
            "Hyderabad",
            "Telangana",
            "Electricity Supply Company (Power & Safety)",
            "TSSPDCL Quick Response Unit",
            4,
            "/static/sample_images/wire_hazard_before.jpg",
            "/static/sample_images/wire_hazard_after.jpg",
            "CLUSTER-HYD-MAD-01",
            18,
            (now - timedelta(days=1)).isoformat(),
            (now - timedelta(hours=12)).isoformat(),
            0.97,
            json.dumps({"clearance_height_m": 5.8}),
            "Hazard cleared. Overhead cables secured in PVC conduit at 6m elevation.",
            96.8,
            "AI Verification Passed: Overhead power lines re-secured with approved clearance."
        ),

        # West Bengal
        (
            "CIVIC-WB-2026-6001",
            "Road Surface Crater at Park Circus 7-Point Crossing",
            "Deep asphalt fracture causing bus diversions and severe morning bottlenecks.",
            "Pothole & Road Damage",
            8,
            "High",
            "Assigned",
            22.5448,
            88.3697,
            "Near Park Circus Tram Depot, 7-Point Crossing",
            "Ward 64 - Park Circus",
            "Kolkata",
            "West Bengal",
            "Public Works Department (Roads & Bridges)",
            "Er. Subhashish Roy",
            24,
            "/static/sample_images/pothole_before.jpg",
            None,
            "CLUSTER-KOL-PC-01",
            16,
            (now - timedelta(hours=7)).isoformat(),
            None,
            0.91,
            json.dumps({"crater_width_m": 1.5}),
            "Resurface section with dense bituminous macadam.",
            None,
            None
        ),

        # Uttar Pradesh
        (
            "CIVIC-UP-2026-7001",
            "Open Waste Accumulation on Dashashwamedh Ghat Road",
            "Commercial temple flower and packaging waste piling up near heritage pathway.",
            "Garbage & Solid Waste",
            8,
            "High",
            "Reported",
            25.3076,
            83.0107,
            "Dashashwamedh Road, Near Godowlia Chowk",
            "Ward 8 - Dashashwamedh Ghat",
            "Varanasi",
            "Uttar Pradesh",
            "Municipal Solid Waste Management",
            "Inspector Arvind Shukla",
            12,
            "/static/sample_images/garbage_before.jpg",
            None,
            "CLUSTER-VAR-DS-01",
            24,
            (now - timedelta(hours=2)).isoformat(),
            None,
            0.93,
            json.dumps({"waste_volume_kg": 600}),
            "Deploy e-rickshaw waste collection squad.",
            None,
            None
        ),

        # Gujarat
        (
            "CIVIC-GJ-2026-8001",
            "Cracked Bitumen & Joint Failure on SG Highway Service Road",
            "Sharp pavement drop-off causing two-wheeler destabilization near flyover entry.",
            "Pothole & Road Damage",
            7,
            "Medium",
            "Reported",
            23.0525,
            72.5120,
            "SG Highway, Opposite Iscon Mega Mall",
            "Ward 14 - SG Highway",
            "Ahmedabad",
            "Gujarat",
            "Public Works Department (Roads & Bridges)",
            "Er. Paresh Patel",
            48,
            "/static/sample_images/pothole_before.jpg",
            None,
            "CLUSTER-AHM-SG-01",
            7,
            (now - timedelta(hours=10)).isoformat(),
            None,
            0.89,
            json.dumps({"fault_type": "Joint expansion failure"}),
            "Saw-cut defect boundaries and refill with hot-mix bitumen.",
            None,
            None
        ),

        # Assam
        (
            "CIVIC-AS-2026-9001",
            "Flash Flood Silt & Drain Blockage on GS Road Dispur",
            "Hill runoff mud blocking stormwater channel, causing knee-deep water near Janata Bhawan.",
            "Waterlogging & Sewage",
            9,
            "Critical",
            "Assigned",
            26.1408,
            91.7907,
            "GS Road, Dispur Capital Complex Junction",
            "Ward 14 - GS Road",
            "Guwahati",
            "Assam",
            "Water Supply and Sewerage Board",
            "Er. Hemanta Kalita",
            18,
            "/static/sample_images/pothole_before.jpg",
            None,
            "CLUSTER-GUW-DIS-01",
            15,
            (now - timedelta(hours=5)).isoformat(),
            None,
            0.94,
            json.dumps({"silt_depth_cm": 40}),
            "Deploy excavator for emergency drain desilting.",
            None,
            None
        ),

        # Rajasthan
        (
            "CIVIC-RJ-2026-10001",
            "Dangling Overhead Utility Cable Cluster in Johari Bazaar",
            "Tangled low-hanging cables obstructing double-decker e-buses in heritage market.",
            "Electrical & Live Wire",
            8,
            "High",
            "In Progress",
            26.9208,
            75.8267,
            "Johari Bazaar, Near Badi Chaupar",
            "Ward 18 - Walled City Johari Bazaar",
            "Jaipur",
            "Rajasthan",
            "Electricity Supply Company (Power & Safety)",
            "JVVNL Quick Response Team",
            6,
            "/static/sample_images/wire_hazard_before.jpg",
            None,
            "CLUSTER-JAI-JB-01",
            12,
            (now - timedelta(hours=3)).isoformat(),
            None,
            0.92,
            json.dumps({"clearance_m": 2.2}),
            "Bundle lines into subterranean or wall-mounted ducting.",
            None,
            None
        ),

        # Kerala
        (
            "CIVIC-KL-2026-11001",
            "Monsoon Overflow Drain Collapse on Marine Drive",
            "Broken stone slab over seaside storm drain posing danger to evening walkers.",
            "Broken Footpath / Utility",
            7,
            "Medium",
            "Resolved",
            9.9816,
            76.2753,
            "Marine Drive Walkway, Near Rainbow Bridge",
            "Ward 12 - Marine Drive",
            "Kochi",
            "Kerala",
            "Public Works Department (Roads & Bridges)",
            "Er. K. V. Biju",
            24,
            "/static/sample_images/pothole_before.jpg",
            "/static/sample_images/pothole_after.jpg",
            "CLUSTER-KOC-MD-01",
            8,
            (now - timedelta(days=2)).isoformat(),
            (now - timedelta(hours=14)).isoformat(),
            0.95,
            json.dumps({"slab_replaced": True}),
            "Pre-cast reinforced concrete slab installed with non-slip texture.",
            95.2,
            "AI Verification Passed: Walkway slab replacement verified flush and secure."
        ),

        # Goa
        (
            "CIVIC-GA-2026-12001",
            "Plastic Waste Mound along Miramar Beach Promenade",
            "Tourist litter accumulated near public shower facilities.",
            "Garbage & Solid Waste",
            6,
            "Medium",
            "Resolved",
            15.4820,
            73.8070,
            "Miramar Beach Road, Opposite Youth Hostel",
            "Ward 1 - Miramar Beach Road",
            "Panaji",
            "Goa",
            "Municipal Solid Waste Management",
            "Corporation of City of Panaji (CCP)",
            12,
            "/static/sample_images/garbage_before.jpg",
            "/static/sample_images/garbage_after.jpg",
            "CLUSTER-GOA-MIR-01",
            10,
            (now - timedelta(days=1)).isoformat(),
            (now - timedelta(hours=6)).isoformat(),
            0.96,
            json.dumps({"bins_installed": 2}),
            "Litter cleared, twin segregation bins placed.",
            97.8,
            "AI Verification Passed: Waste mound cleared. Beachside pavement sanitized."
        )
    ]
    
    cursor.executemany("""
    INSERT INTO incidents (
        ticket_number, title, description, hazard_type, severity, priority,
        status, latitude, longitude, address, ward, city, state, department,
        assigned_engineer, sla_hours, before_image, after_image,
        cluster_id, upvotes, created_at, resolved_at, ai_confidence,
        ai_defect_details, work_order_summary, verification_score, verification_remarks
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, seed_incidents)
    
    # Audit logs
    for i in range(1, len(seed_incidents) + 1):
        cursor.execute("""
        INSERT INTO audit_logs (incident_id, action, actor, timestamp, details)
        VALUES (?, 'CREATED', 'CivicLens AI System', ?, 'Auto-triaged from citizen image analysis')
        """, (i, (now - timedelta(hours=8)).isoformat()))
        
    conn.commit()

def list_incidents(hazard_type=None, status=None, city=None, ward=None, state=None, search=None):
    conn = get_db()
    query = "SELECT * FROM incidents WHERE 1=1"
    params = []
    
    if hazard_type:
        query += " AND hazard_type = ?"
        params.append(hazard_type)
    if status:
        query += " AND status = ?"
        params.append(status)
    if state:
        query += " AND state = ?"
        params.append(state)
    if city:
        query += " AND city = ?"
        params.append(city)
    if ward:
        query += " AND ward = ?"
        params.append(ward)
    if search:
        query += " AND (title LIKE ? OR description LIKE ? OR address LIKE ? OR ticket_number LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term, term])
        
    query += " ORDER BY severity DESC, upvotes DESC, id DESC"
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_incident(incident_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE id = ? OR ticket_number = ?", (incident_id, incident_id))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_incident(data):
    conn = get_db()
    cursor = conn.cursor()
    
    # Generate unique ticket number with State Code
    state_name = data.get("state", "Karnataka")
    from states_data import ALL_INDIA_STATES
    state_code = ALL_INDIA_STATES.get(state_name, {}).get("code", "IND")
    timestamp_suffix = f"{datetime.now().strftime('%y%m%d-%H%M%S')}-{uuid.uuid4().hex[:4].upper()}"
    ticket_number = f"CIVIC-{state_code}-{timestamp_suffix}"
    
    cursor.execute("""
    INSERT INTO incidents (
        ticket_number, title, description, hazard_type, severity, priority,
        status, latitude, longitude, address, ward, city, state, department,
        assigned_engineer, sla_hours, before_image, cluster_id, upvotes,
        created_at, ai_confidence, ai_defect_details, work_order_summary
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_number,
        data.get("title", "Reported Civic Hazard"),
        data.get("description", ""),
        data.get("hazard_type", "Pothole & Road Damage"),
        data.get("severity", 5),
        data.get("priority", "Medium"),
        "Reported",
        data.get("latitude", 12.9716),
        data.get("longitude", 77.5946),
        data.get("address", "Municipal Road"),
        data.get("ward", "Ward 1 - Central"),
        data.get("city", "Bengaluru"),
        state_name,
        data.get("department", "Public Works Department (Roads & Bridges)"),
        data.get("assigned_engineer", "Unassigned (Auto-Queue)"),
        data.get("sla_hours", 24),
        data.get("before_image", "/static/sample_images/pothole_before.jpg"),
        data.get("cluster_id"),
        data.get("upvotes", 1),
        datetime.now().isoformat(),
        data.get("ai_confidence", 0.88),
        json.dumps(data.get("ai_defect_details", {})),
        data.get("work_order_summary", "Field inspection scheduled.")
    ))
    
    new_id = cursor.lastrowid
    
    cursor.execute("""
    INSERT INTO audit_logs (incident_id, action, actor, timestamp, details)
    VALUES (?, 'CREATED', 'Citizen / CivicLens AI', ?, 'Citizen complaint ingested and classified')
    """, (new_id, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    return get_incident(new_id)

def update_incident_status(incident_id, status, after_image=None, verification_score=None, verification_remarks=None, actor="System", worker_selfie=None, checkin_lat=None, checkin_lng=None, completion_lat=None, completion_lng=None, worker_name=None, worker_id=None, geofence_status=None):
    conn = get_db()
    cursor = conn.cursor()
    
    resolved_at = datetime.now().isoformat() if status == "Resolved" else None
    
    cursor.execute("""
    UPDATE incidents SET
        status = ?,
        after_image = COALESCE(?, after_image),
        verification_score = COALESCE(?, verification_score),
        verification_remarks = COALESCE(?, verification_remarks),
        resolved_at = COALESCE(?, resolved_at),
        worker_selfie = COALESCE(?, worker_selfie),
        checkin_lat = COALESCE(?, checkin_lat),
        checkin_lng = COALESCE(?, checkin_lng),
        completion_lat = COALESCE(?, completion_lat),
        completion_lng = COALESCE(?, completion_lng),
        worker_name = COALESCE(?, worker_name),
        worker_id = COALESCE(?, worker_id),
        geofence_status = COALESCE(?, geofence_status)
    WHERE id = ? OR ticket_number = ?
    """, (
        status, after_image, verification_score, verification_remarks, resolved_at,
        worker_selfie, checkin_lat, checkin_lng, completion_lat, completion_lng,
        worker_name, worker_id, geofence_status,
        incident_id, incident_id
    ))
    
    cursor.execute("""
    INSERT INTO audit_logs (incident_id, action, actor, timestamp, details)
    VALUES (?, ?, ?, ?, ?)
    """, (incident_id, f"STATUS_CHANGE_{status}", actor, datetime.now().isoformat(), f"Status updated to {status}. Geofence: {geofence_status or 'Verified'}. Worker ID: {worker_id or 'N/A'}"))
    
    conn.commit()
    conn.close()
    return get_incident(incident_id)

def upvote_incident(incident_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE incidents SET upvotes = upvotes + 1 WHERE id = ? OR ticket_number = ?", (incident_id, incident_id))
    conn.commit()
    conn.close()
    return get_incident(incident_id)

def get_analytics():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM incidents")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE status = 'Resolved'")
    resolved = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE priority = 'Critical' AND status != 'Resolved'")
    critical_active = cursor.fetchone()[0]
    
    cursor.execute("SELECT hazard_type, COUNT(*) as count FROM incidents GROUP BY hazard_type")
    hazard_counts = dict(cursor.fetchall())
    
    cursor.execute("SELECT state, COUNT(*) as count FROM incidents GROUP BY state")
    state_counts = dict(cursor.fetchall())
    
    cursor.execute("SELECT city, COUNT(*) as count FROM incidents GROUP BY city")
    city_counts = dict(cursor.fetchall())
    
    cursor.execute("SELECT AVG(verification_score) FROM incidents WHERE verification_score IS NOT NULL")
    avg_verification = round(cursor.fetchone()[0] or 0.0, 1)
    
    # Ward Civic Health Index (CHI) calculation
    cursor.execute("""
    SELECT ward, city, state,
           COUNT(*) as total_reports,
           SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) as resolved_reports,
           SUM(CASE WHEN priority = 'Critical' AND status != 'Resolved' THEN 1 ELSE 0 END) as active_critical,
           SUM(CASE WHEN priority = 'High' AND status != 'Resolved' THEN 1 ELSE 0 END) as active_high
    FROM incidents GROUP BY ward, city, state
    ORDER BY total_reports DESC
    """)
    wards_data = []
    for row in cursor.fetchall():
        w_name = row["ward"]
        w_city = row["city"]
        w_state = row["state"]
        w_total = row["total_reports"]
        w_resolved = row["resolved_reports"]
        w_crit = row["active_critical"]
        w_high = row["active_high"]
        
        penalty = (w_crit * 15) + (w_high * 8)
        bonus = int((w_resolved / max(w_total, 1)) * 25)
        chi_score = max(35, min(98, 85 - penalty + bonus))
        
        wards_data.append({
            "ward": w_name,
            "city": w_city,
            "state": w_state,
            "total": w_total,
            "resolved": w_resolved,
            "active_critical": w_crit,
            "chi_score": chi_score,
            "grade": "A" if chi_score >= 85 else ("B" if chi_score >= 70 else ("C" if chi_score >= 50 else "D"))
        })
        
    conn.close()
    
    return {
        "total_incidents": total,
        "resolved_incidents": resolved,
        "active_critical": critical_active,
        "resolution_rate": round((resolved / max(total, 1)) * 100, 1),
        "avg_verification_score": avg_verification,
        "hazard_counts": hazard_counts,
        "state_counts": state_counts,
        "city_counts": city_counts,
        "ward_health_index": wards_data
    }

if __name__ == "__main__":
    init_db(seed=True)
    print("Database initialized and verified for all Indian States.")
