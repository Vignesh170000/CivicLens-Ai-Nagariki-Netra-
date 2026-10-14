"""
CivicLens AI (NagrikNetra) - Automated Test Suite
Tests:
1. Local Computer Vision & Multimodal Heuristics
2. Geospatial Haversine Clustering & 50m Deduplication
3. Before-After Resolution Verification Engine
4. Database Integrity & Ward Civic Health Index (CHI)
5. Flask REST API Integration Endpoints
"""

import os
import unittest
import json
from app import app
import models
import ai_engine

class CivicLensTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        models.init_db(seed=True)
        cls.sample_pothole = os.path.join(os.path.dirname(__file__), "static", "sample_images", "pothole_before.jpg")
        cls.sample_pothole_after = os.path.join(os.path.dirname(__file__), "static", "sample_images", "pothole_after.jpg")
        cls.sample_garbage = os.path.join(os.path.dirname(__file__), "static", "sample_images", "garbage_before.jpg")
        cls.sample_garbage_after = os.path.join(os.path.dirname(__file__), "static", "sample_images", "garbage_after.jpg")

    def test_01_health_endpoint(self):
        """Test GET /api/health endpoint"""
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "online")
        self.assertIn("ai_engine", data)
        print("[PASS] Health endpoint verified:", data["ai_engine"])

    def test_02_sample_images_endpoint(self):
        """Test GET /api/sample-images endpoint"""
        res = self.client.get("/api/sample-images")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(len(data.get("samples", [])) >= 3)
        print(f"[PASS] Found {len(data['samples'])} sample test scenarios")

    def test_03_local_heuristic_vision_triage(self):
        """Test Local Computer Vision Triage on Pothole and Garbage images"""
        pothole_result = ai_engine.analyze_image_heuristics(self.sample_pothole, "Deep crater on road")
        self.assertEqual(pothole_result["hazard_type"], "Pothole & Road Damage")
        self.assertGreaterEqual(pothole_result["severity"], 7)
        self.assertEqual(pothole_result["department"], "Public Works Department (Roads & Bridges)")
        print(f"[PASS] Local CV Pothole Classification: {pothole_result['hazard_type']} (Severity {pothole_result['severity']}/10)")

        garbage_result = ai_engine.analyze_image_heuristics(self.sample_garbage, "Overflowing trash and garbage on footpath")
        self.assertEqual(garbage_result["hazard_type"], "Garbage & Solid Waste")
        self.assertEqual(garbage_result["department"], "Municipal Solid Waste Management")
        print(f"[PASS] Local CV Garbage Classification: {garbage_result['hazard_type']} (Severity {garbage_result['severity']}/10)")

    def test_04_geospatial_haversine_clustering(self):
        """Test Geospatial Haversine calculation and 50m proximity deduplication"""
        # Indiranagar 12th Main junction coords
        lat1, lon1 = 12.9719, 77.6412
        # Point 25 meters away
        lat2, lon2 = 12.9721, 77.6413
        # Point 5 kilometers away
        lat3, lon3 = 12.9260, 77.6762

        dist_near = ai_engine.haversine_distance(lat1, lon1, lat2, lon2)
        dist_far = ai_engine.haversine_distance(lat1, lon1, lat3, lon3)

        self.assertLess(dist_near, 50.0)
        self.assertGreater(dist_far, 3000.0)
        print(f"[PASS] Haversine Distance Calculated: {dist_near:.1f}m (near), {dist_far:.1f}m (far)")

        # Verify cluster grouping
        existing = [{"id": 101, "latitude": lat1, "longitude": lon1, "cluster_id": "CLUSTER-IND-01", "status": "Reported"}]
        c_id, dup_id, d = ai_engine.find_or_create_cluster(lat2, lon2, existing, threshold_meters=50.0)
        self.assertEqual(c_id, "CLUSTER-IND-01")
        self.assertEqual(dup_id, 101)
        print(f"[PASS] Proximity Clustering Grouped nearby report into {c_id}")

    def test_05_resolution_verification_engine(self):
        """Test AI Before-and-After Resolution Verification Engine"""
        # Test Genuine Repair (Before pothole vs After asphalt patch)
        ver_pass = ai_engine.verify_repair_resolution(self.sample_pothole, self.sample_pothole_after, "Pothole & Road Damage")
        self.assertTrue(ver_pass["verified"])
        self.assertGreaterEqual(ver_pass["verification_score"], 75.0)
        print(f"[PASS] Resolution Verification Passed: Score {ver_pass['verification_score']}% - {ver_pass['remarks']}")

        # Test Fraud Detection (Same image uploaded as before and after)
        ver_fraud = ai_engine.verify_repair_resolution(self.sample_pothole, self.sample_pothole, "Pothole & Road Damage")
        self.assertFalse(ver_fraud["verified"])
        self.assertLess(ver_fraud["verification_score"], 50.0)
        self.assertIn("Fraud Alert", ver_fraud["remarks"])
        print(f"[PASS] Anti-Fraud Protection Verified: Re-uploading identical photo rejected ({ver_fraud['remarks']})")

    def test_06_incident_creation_and_api(self):
        """Test POST /api/reports and GET /api/reports"""
        payload = {
            "title": "Severe Pothole Test on MG Road",
            "description": "Hazardous road crater near metro pillar",
            "city": "Bengaluru",
            "ward": "Ward 80 - Hoysala Nagar",
            "address": "MG Road near Pillar 45",
            "latitude": "12.9750",
            "longitude": "77.6050",
            "sample_image_path": "/static/sample_images/pothole_before.jpg"
        }
        res = self.client.post("/api/reports", data=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data["success"])
        inc = data["incident"]
        self.assertEqual(inc["hazard_type"], "Pothole & Road Damage")
        self.assertIn("CIVIC-KA-", inc["ticket_number"])
        print("[PASS] Created incident via API:", inc["ticket_number"])

        # Test Upvoting
        res_upvote = self.client.post(f"/api/reports/{inc['id']}/upvote")
        self.assertEqual(res_upvote.status_code, 200)
        self.assertEqual(res_upvote.get_json()["upvotes"], 2)
        print("[PASS] Incident upvote verified (Upvotes: 2)")

    def test_07_analytics_and_chi(self):
        """Test GET /api/analytics and Ward Civic Health Index calculation"""
        res = self.client.get("/api/analytics")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("total_incidents", data)
        self.assertIn("ward_health_index", data)
        self.assertTrue(len(data["ward_health_index"]) > 0)
        print(f"[PASS] Analytics verified: {data['total_incidents']} total issues, {len(data['ward_health_index'])} wards scored")

    def test_08_chatbot_api(self):
        """Test POST /api/chat civic copilot queries"""
        res = self.client.post("/api/chat", json={"message": "How do I report a pothole on the road?"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("pothole", data["reply"].lower())
        print("[PASS] Chatbot reply verified:", data["reply"][:80], "...")

    def test_09_all_indian_states_endpoint(self):
        """Test GET /api/states returns all 28 States and 8 Union Territories"""
        res = self.client.get("/api/states")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("states", data)
        self.assertEqual(len(data["states"]), 36)
        # Verify sample states from different regions of India
        state_names = [s["name"] for s in data["states"]]
        self.assertIn("Karnataka", state_names)
        self.assertIn("Maharashtra", state_names)
        self.assertIn("Assam", state_names)
        self.assertIn("Delhi", state_names)
        self.assertIn("Tamil Nadu", state_names)
        self.assertIn("Jammu and Kashmir", state_names)
        print(f"[PASS] All-India Coverage Verified: {len(data['states'])} States & Union Territories loaded.")

if __name__ == "__main__":
    unittest.main()
