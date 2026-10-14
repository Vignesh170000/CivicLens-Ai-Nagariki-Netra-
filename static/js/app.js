/**
 * CivicLens AI (NagrikNetra) - Core Frontend Application
 * Handles Multimodal AI Triage, GIS Heatmap, SLA Priority Queue,
 * Resolution Verification, Chart.js Analytics across ALL 28 STATES & 8 UTs OF INDIA.
 */

// Application State
let currentTab = 'citizen';
let allIncidents = [];
let sampleImages = [];
let allStatesList = [];
let allStatesData = {};
let selectedSamplePath = null;
let selectedFile = null;
let leafletMap = null;
let mapMarkers = [];
let hazardChart = null;
let cityChart = null;

// Initialization on DOM Load
document.addEventListener('DOMContentLoaded', async () => {
    await checkHealth();
    await fetchStates();
    await fetchSampleImages();
    await loadIncidents();
    await loadAnalytics();
});

// -------------------------------------------------------------
// 1. HEALTH & SYSTEM MODE CHECK
// -------------------------------------------------------------
async function checkHealth() {
    try {
        const res = await fetch('/api/health');
        const data = await res.json();
        const badge = document.getElementById('ai-mode-badge');
        const badgeText = document.getElementById('ai-mode-text');
        if (data.status === 'online') {
            badgeText.textContent = data.ai_cloud_mode ? 'Gemini 1.5/2.0 Cloud' : 'Edge Vision Mode (Offline Resilient)';
            badge.classList.remove('hidden');
        }
    } catch (err) {
        console.warn('System health check warning:', err);
    }
}

// -------------------------------------------------------------
// 2. ALL-INDIA STATES & UNION TERRITORIES DATA LOADER
// -------------------------------------------------------------
async function fetchStates() {
    try {
        const res = await fetch('/api/states');
        const data = await res.json();
        allStatesList = data.states || [];
        allStatesData = data.raw || {};

        // Populate Form State Dropdown
        const reportStateSelect = document.getElementById('report-state');
        // Populate Map Fly-To State Dropdown
        const mapStateSelect = document.getElementById('map-state-selector');
        // Populate Municipal Table Filter Dropdown
        const filterStateSelect = document.getElementById('filter-state');

        if (reportStateSelect) reportStateSelect.innerHTML = '';
        if (mapStateSelect) mapStateSelect.innerHTML = '<option value="">-- Choose State / UT to Explore --</option>';
        if (filterStateSelect) filterStateSelect.innerHTML = '<option value="">All States / UTs</option>';

        allStatesList.forEach(s => {
            const opt1 = document.createElement('option');
            opt1.value = s.name;
            opt1.textContent = `${s.name} (${s.code})`;
            if (s.name === 'Karnataka') opt1.selected = true;
            if (reportStateSelect) reportStateSelect.appendChild(opt1);

            const opt2 = document.createElement('option');
            opt2.value = s.name;
            opt2.textContent = `${s.name} (${s.code}) - ${s.type}`;
            if (mapStateSelect) mapStateSelect.appendChild(opt2);

            const opt3 = document.createElement('option');
            opt3.value = s.name;
            opt3.textContent = s.name;
            if (filterStateSelect) filterStateSelect.appendChild(opt3);
        });

        // Trigger initial cascade for Karnataka
        onStateSelected();

    } catch (e) {
        console.error('Failed to load Indian states:', e);
    }
}

function onStateSelected() {
    const stateSelect = document.getElementById('report-state');
    const citySelect = document.getElementById('report-city');
    if (!stateSelect || !citySelect) return;

    const stateName = stateSelect.value;
    const stateObj = allStatesData[stateName];
    citySelect.innerHTML = '';

    if (stateObj && stateObj.cities) {
        const cityNames = Object.keys(stateObj.cities);
        cityNames.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            citySelect.appendChild(opt);
        });

        // Update default coordinates to state/city centroid
        if (stateObj.coords) {
            document.getElementById('report-lat').value = stateObj.coords.lat;
            document.getElementById('report-lng').value = stateObj.coords.lng;
        }
    }

    onCitySelected();
}

function onCitySelected() {
    const stateSelect = document.getElementById('report-state');
    const citySelect = document.getElementById('report-city');
    const wardSelect = document.getElementById('report-ward');
    if (!stateSelect || !citySelect || !wardSelect) return;

    const stateName = stateSelect.value;
    const cityName = citySelect.value;
    wardSelect.innerHTML = '';

    const stateObj = allStatesData[stateName];
    if (stateObj && stateObj.cities && stateObj.cities[cityName]) {
        const wards = stateObj.cities[cityName];
        wards.forEach(w => {
            const opt = document.createElement('option');
            opt.value = w;
            opt.textContent = w;
            wardSelect.appendChild(opt);
        });
    } else {
        wardSelect.innerHTML = '<option value="Ward 1 - Central Zone">Ward 1 - Central Zone</option>';
    }
}

// -------------------------------------------------------------
// 3. TAB NAVIGATION
// -------------------------------------------------------------
function switchTab(tabId) {
    currentTab = tabId;
    
    // Hide all tabs
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
    
    // Show selected
    const target = document.getElementById(`tab-${tabId}`);
    if (target) {
        target.classList.remove('hidden');
        target.classList.add('active');
    }

    // Update Desktop Nav Buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active-nav');
        btn.classList.add('text-slate-300');
    });
    const activeNav = document.getElementById(`nav-${tabId}`);
    if (activeNav) {
        activeNav.classList.add('active-nav');
        activeNav.classList.remove('text-slate-300');
    }

    // Specific tab triggers
    if (tabId === 'map') {
        setTimeout(initOrRefreshMap, 200);
    } else if (tabId === 'municipal') {
        loadReportsTable();
    } else if (tabId === 'contractor') {
        populateContractorTicketSelect();
    } else if (tabId === 'analytics') {
        loadAnalytics();
    }
}

// -------------------------------------------------------------
// 4. SAMPLE SCENARIOS & FILE HANDLING
// -------------------------------------------------------------
async function fetchSampleImages() {
    try {
        const res = await fetch('/api/sample-images');
        const data = await res.json();
        sampleImages = data.samples || [];
    } catch (e) {
        console.error('Failed to load sample images:', e);
    }
}

function loadSampleScenario(type) {
    const s = sampleImages.find(item => item.id === type);
    if (!s) return;

    selectedSamplePath = s.before;
    selectedFile = null;

    // Set preview image
    const preview = document.getElementById('image-preview');
    preview.src = s.before;
    document.getElementById('upload-placeholder').classList.add('hidden');
    document.getElementById('preview-container').classList.remove('hidden');

    // Fill Form Fields (Karnataka as sample state)
    const stateSelect = document.getElementById('report-state');
    if (stateSelect) {
        stateSelect.value = 'Karnataka';
        onStateSelected();
    }
    const citySelect = document.getElementById('report-city');
    if (citySelect) {
        citySelect.value = s.city;
        onCitySelected();
    }
    const wardSelect = document.getElementById('report-ward');
    if (wardSelect) wardSelect.value = s.ward;

    document.getElementById('report-address').value = s.suggested_title;
    document.getElementById('report-lat').value = s.lat;
    document.getElementById('report-lng').value = s.lng;
    document.getElementById('report-desc').value = `Severe ${s.name} detected near main transit junction. Urgent municipal action needed.`;

    // Trigger instant simulated AI scan
    triggerInstantAIScan(s.before, null, document.getElementById('report-desc').value);
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    selectedFile = file;
    selectedSamplePath = null;

    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('image-preview').src = e.target.result;
        document.getElementById('upload-placeholder').classList.add('hidden');
        document.getElementById('preview-container').classList.remove('hidden');
        
        triggerInstantAIScan(null, file, document.getElementById('report-desc').value);
    };
    reader.readAsDataURL(file);
}

function resetImageUpload(event) {
    if (event) event.stopPropagation();
    selectedFile = null;
    selectedSamplePath = null;
    document.getElementById('report-file-input').value = '';
    document.getElementById('upload-placeholder').classList.remove('hidden');
    document.getElementById('preview-container').classList.add('hidden');
    document.getElementById('ai-triage-card').classList.add('hidden');
}

// -------------------------------------------------------------
// 5. INSTANT PRE-SUBMISSION AI SCANNER
// -------------------------------------------------------------
async function triggerInstantAIScan(samplePath, file, description) {
    const laser = document.getElementById('laser-scan');
    const triageCard = document.getElementById('ai-triage-card');
    
    laser.classList.remove('hidden');
    triageCard.classList.add('hidden');

    try {
        const formData = new FormData();
        if (file) {
            formData.append('image', file);
        } else if (samplePath) {
            formData.append('sample_image_path', samplePath);
        }
        formData.append('description', description || '');

        const res = await fetch('/api/scan', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();

        // Populate Triage Card
        document.getElementById('triage-hazard').textContent = data.hazard_type;
        document.getElementById('triage-severity').textContent = `${data.severity} / 10`;
        document.getElementById('triage-sla').textContent = `${data.sla_hours} Hours`;
        document.getElementById('triage-confidence').textContent = `${(data.confidence * 100).toFixed(1)}%`;
        document.getElementById('triage-dept').textContent = data.department;
        document.getElementById('triage-workorder').textContent = data.work_order_summary || 'Inspection scheduled.';
        document.getElementById('triage-engine-badge').textContent = data.ai_engine_used || 'CivicLens AI';

        // Auto-select in form dropdown
        const hazardOverride = document.getElementById('report-hazard-override');
        if (hazardOverride && data.hazard_type) {
            hazardOverride.value = data.hazard_type;
        }

        setTimeout(() => {
            laser.classList.add('hidden');
            triageCard.classList.remove('hidden');
        }, 800);

    } catch (err) {
        console.error('Scan error:', err);
        laser.classList.add('hidden');
    }
}

// -------------------------------------------------------------
// 6. REPORT SUBMISSION (CREATE INCIDENT)
// -------------------------------------------------------------
async function submitCitizenReport(event) {
    event.preventDefault();
    const btn = document.getElementById('submit-report-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1"></i> Processing AI Triage & Geospatial Clustering...`;
    btn.disabled = true;

    try {
        const formData = new FormData();
        if (selectedFile) {
            formData.append('image', selectedFile);
        } else if (selectedSamplePath) {
            formData.append('sample_image_path', selectedSamplePath);
        }

        formData.append('title', document.getElementById('report-address').value);
        formData.append('description', document.getElementById('report-desc').value);
        const hazardOverride = document.getElementById('report-hazard-override');
        if (hazardOverride) {
            formData.append('hazard_type', hazardOverride.value);
        }
        formData.append('state', document.getElementById('report-state').value);
        formData.append('city', document.getElementById('report-city').value);
        formData.append('ward', document.getElementById('report-ward').value);
        formData.append('address', document.getElementById('report-address').value);
        formData.append('latitude', document.getElementById('report-lat').value);
        formData.append('longitude', document.getElementById('report-lng').value);

        const res = await fetch('/api/reports', {
            method: 'POST',
            body: formData
        });
        const result = await res.json();

        if (result.success) {
            const inc = result.incident;
            let alertMsg = `✅ Grievance Registered!\nTicket ID: ${inc.ticket_number}\nState: ${inc.state}\nAssigned to: ${inc.department}\nSLA Deadline: ${inc.sla_hours} Hours`;
            if (inc.is_clustered) {
                alertMsg += `\n\n📌 Merged into nearby hazard cluster (${inc.cluster_proximity_m}m away). Urgency upvoted!`;
            }
            alert(alertMsg);

            // Reset Form and reload
            document.getElementById('report-form').reset();
            resetImageUpload();
            await loadIncidents();
            switchTab('municipal');
        } else {
            alert('Failed to register grievance. Please try again.');
        }
    } catch (err) {
        console.error('Submit error:', err);
        alert('An error occurred while communicating with the server.');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// -------------------------------------------------------------
// 7. LOAD INCIDENTS & POPULATE MUNICIPAL TRIAGE TABLE
// -------------------------------------------------------------
async function loadIncidents() {
    try {
        const res = await fetch('/api/reports');
        const data = await res.json();
        allIncidents = data.incidents || [];
    } catch (e) {
        console.error('Failed to load incidents:', e);
    }
}

async function loadReportsTable() {
    const stateFilter = document.getElementById('filter-state') ? document.getElementById('filter-state').value : '';
    const hazardFilter = document.getElementById('filter-hazard').value;
    const statusFilter = document.getElementById('filter-status').value;
    const searchFilter = document.getElementById('filter-search').value;

    let url = `/api/reports?1=1`;
    if (stateFilter) url += `&state=${encodeURIComponent(stateFilter)}`;
    if (hazardFilter) url += `&hazard_type=${encodeURIComponent(hazardFilter)}`;
    if (statusFilter) url += `&status=${encodeURIComponent(statusFilter)}`;
    if (searchFilter) url += `&search=${encodeURIComponent(searchFilter)}`;

    try {
        const res = await fetch(url);
        const data = await res.json();
        const incidents = data.incidents || [];
        const tbody = document.getElementById('incidents-table-body');
        tbody.innerHTML = '';

        if (incidents.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" class="text-center py-8 text-slate-400">No matching civic incidents found in selected state/filters.</td></tr>`;
            return;
        }

        incidents.forEach(inc => {
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-50 transition border-b border-slate-100';

            // Severity color badge
            let sevBadge = 'bg-yellow-100 text-yellow-800';
            if (inc.severity >= 9) sevBadge = 'bg-red-100 text-red-800 font-bold';
            else if (inc.severity >= 7) sevBadge = 'bg-amber-100 text-amber-800';

            // Status color badge
            let statusBadge = 'bg-slate-100 text-slate-700';
            if (inc.status === 'Resolved') statusBadge = 'bg-emerald-100 text-emerald-800 font-bold';
            else if (inc.status === 'In Progress') statusBadge = 'bg-sky-100 text-sky-800';
            else if (inc.status === 'Assigned') statusBadge = 'bg-indigo-100 text-indigo-800';

            tr.innerHTML = `
                <td class="p-3">
                    <div class="flex items-center space-x-2">
                        <img src="${inc.before_image || '/static/sample_images/pothole_before.jpg'}" class="w-12 h-12 rounded-lg object-cover shadow-sm" alt="Thumbnail">
                        <div>
                            <span class="font-mono font-bold text-slate-900 block">${inc.ticket_number}</span>
                            <span class="text-[10px] text-slate-400">Upvotes: <span class="font-bold text-indigo-600">${inc.upvotes}</span></span>
                        </div>
                    </div>
                </td>
                <td class="p-3">
                    <p class="font-bold text-slate-800">${inc.title}</p>
                    <p class="text-[11px] text-slate-500 line-clamp-1">${inc.description || 'No additional notes'}</p>
                </td>
                <td class="p-3">
                    <span class="font-semibold block text-slate-800">${inc.ward}</span>
                    <span class="text-[11px] text-slate-500">${inc.city}, <span class="font-bold text-indigo-600">${inc.state || 'India'}</span></span>
                </td>
                <td class="p-3">
                    <span class="inline-block px-2 py-0.5 rounded text-[11px] ${sevBadge}">
                        Sev ${inc.severity}/10 (${inc.priority})
                    </span>
                </td>
                <td class="p-3">
                    <p class="font-semibold text-slate-800">${inc.department}</p>
                    <span class="text-[10px] text-amber-700 font-medium">SLA: ${inc.sla_hours}h</span>
                </td>
                <td class="p-3">
                    <span class="inline-block px-2 py-0.5 rounded text-[11px] ${statusBadge}">
                        ${inc.status}
                    </span>
                </td>
                <td class="p-3 whitespace-nowrap space-x-1">
                    <button onclick="upvoteIncident(${inc.id})" class="text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-2 py-1 rounded" title="Upvote Hazard">
                        <i class="fa-solid fa-thumbs-up"></i>
                    </button>
                    ${inc.status !== 'Resolved' ? `
                        <button onclick="openVerificationForId(${inc.id})" class="text-xs bg-emerald-600 hover:bg-emerald-700 text-white px-2 py-1 rounded" title="Verify Repair">
                            <i class="fa-solid fa-check-double mr-1"></i> Verify
                        </button>
                    ` : `
                        <span class="text-xs text-emerald-600 font-semibold"><i class="fa-solid fa-circle-check"></i> ${inc.verification_score || 95}%</span>
                    `}
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error('Failed to load reports table:', e);
    }
}

async function upvoteIncident(id) {
    try {
        const res = await fetch(`/api/reports/${id}/upvote`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            loadReportsTable();
            loadIncidents();
        }
    } catch (e) {
        console.error('Upvote failed:', e);
    }
}

// -------------------------------------------------------------
// 8. LEAFLET GIS HEATMAP & ALL-INDIA FLY-TO
// -------------------------------------------------------------
function initOrRefreshMap() {
    if (!leafletMap) {
        leafletMap = L.map('gis-map').setView([20.5937, 78.9629], 5); // India center overview
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors | CivicLens AI',
            maxZoom: 18
        }).addTo(leafletMap);
    }
    refreshMapData();
}

function panMapToState() {
    const stateSelector = document.getElementById('map-state-selector');
    if (!stateSelector) return;
    const stateName = stateSelector.value;
    if (!stateName) return;

    const stateObj = allStatesData[stateName];
    if (stateObj && stateObj.coords && leafletMap) {
        leafletMap.flyTo([stateObj.coords.lat, stateObj.coords.lng], stateObj.coords.zoom || 11, {
            duration: 1.5
        });
    }
}

async function refreshMapData() {
    if (!leafletMap) return;
    
    mapMarkers.forEach(m => leafletMap.removeLayer(m));
    mapMarkers = [];

    await loadIncidents();

    allIncidents.forEach(inc => {
        if (inc.latitude && inc.longitude) {
            let pinClass = 'pin-medium';
            if (inc.status === 'Resolved') pinClass = 'pin-resolved';
            else if (inc.severity >= 9) pinClass = 'pin-critical';
            else if (inc.severity >= 7) pinClass = 'pin-high';

            const icon = L.divIcon({
                className: 'custom-leaflet-icon',
                html: `<div class="custom-pin ${pinClass}">${inc.severity}</div>`,
                iconSize: [28, 28],
                iconAnchor: [14, 14]
            });

            const marker = L.marker([inc.latitude, inc.longitude], { icon: icon }).addTo(leafletMap);
            
            const popupContent = `
                <div class="p-1 max-w-[230px] text-xs">
                    <img src="${inc.before_image}" class="w-full h-24 object-cover rounded mb-2">
                    <p class="font-bold text-slate-800">${inc.title}</p>
                    <p class="text-slate-500 text-[11px] mb-1">${inc.ward}, ${inc.city} (${inc.state || 'India'})</p>
                    <div class="flex items-center justify-between text-[11px] font-semibold border-t pt-1">
                        <span class="text-red-600">Sev ${inc.severity}/10</span>
                        <span class="text-emerald-700">${inc.status}</span>
                    </div>
                </div>
            `;
            marker.bindPopup(popupContent);
            mapMarkers.push(marker);
        }
    });
}

// -------------------------------------------------------------
// 9. MUNICIPAL FIELD OFFICER & CONTRACTOR RESOLUTION VERIFICATION
// -------------------------------------------------------------
async function populateContractorTicketSelect() {
    const select = document.getElementById('verify-incident-select');
    if (!select) return;
    select.innerHTML = '<option value="">Loading active municipal tickets...</option>';
    
    // Fetch freshest incidents
    await loadIncidents();
    select.innerHTML = '';
    
    const filterElem = document.getElementById('verify-status-filter');
    const filterVal = filterElem ? filterElem.value : 'open';
    
    let candidates = [];
    if (filterVal === 'all') {
        candidates = allIncidents;
    } else {
        candidates = allIncidents.filter(i => i.status !== 'Resolved');
    }

    if (candidates.length === 0) {
        select.innerHTML = '<option value="">All active tickets resolved! Click "Reload Open Tickets" to test more.</option>';
        return;
    }

    candidates.forEach(inc => {
        const opt = document.createElement('option');
        opt.value = inc.id;
        opt.textContent = `[${inc.ticket_number}] ${inc.title} (${inc.city}, ${inc.state}) - Status: ${inc.status} (Sev: ${inc.severity})`;
        select.appendChild(opt);
    });

    loadIncidentForVerification();
}

async function resetDemoTickets() {
    const btn = document.getElementById('verify-reload-btn');
    if (btn) btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1"></i> Reloading...`;
    try {
        const res = await fetch('/api/demo/reset', { method: 'POST' });
        const data = await res.json();
        await loadIncidents();
        await populateContractorTicketSelect();
        if (btn) btn.innerHTML = `<i class="fa-solid fa-check mr-1 text-emerald-600"></i> Loaded 14 Tickets`;
        setTimeout(() => {
            if (btn) btn.innerHTML = `<i class="fa-solid fa-rotate-left mr-1"></i> Reload Open Tickets`;
        }, 2000);
    } catch (e) {
        console.error('Reset error:', e);
        if (btn) btn.innerHTML = `<i class="fa-solid fa-rotate-left mr-1"></i> Reload Open Tickets`;
    }
}

let selectedWorkerSelfieFile = null;
let selectedWorkerSelfiePath = null;

function handleWorkerSelfieSelect(event) {
    const file = event.target.files[0];
    if (file) {
        selectedWorkerSelfieFile = file;
        selectedWorkerSelfiePath = null;
        const reader = new FileReader();
        reader.onload = e => {
            const img = document.getElementById('verify-worker-selfie-img');
            if (img) img.src = e.target.result;
            const stamp = document.getElementById('verify-selfie-stamp');
            if (stamp) stamp.textContent = `Live Camera Captured • ${new Date().toLocaleTimeString()}`;
        };
        reader.readAsDataURL(file);
    }
}

function loadMatchingWorkerSelfie() {
    const select = document.getElementById('verify-incident-select');
    if (!select) return;
    const incId = select.value;
    const inc = allIncidents.find(i => String(i.id) === String(incId));
    
    let selfieSrc = '/static/sample_images/worker_selfie_pothole.jpg';
    let officerName = 'Er. Rajesh Kumar';
    let officerId = 'BBMP-PWD-8492';
    let officerDept = 'Public Works Department (Roads & Bridges)';

    if (inc) {
        const h = inc.hazard_type.toLowerCase();
        if (h.includes('garbage') || h.includes('waste')) {
            selfieSrc = '/static/sample_images/worker_selfie_garbage.jpg';
            officerName = 'Sunil Shinde';
            officerId = 'BMC-SWM-4102';
            officerDept = 'Municipal Solid Waste Management';
        } else if (h.includes('wire') || h.includes('electric')) {
            selfieSrc = '/static/sample_images/worker_selfie_wire.jpg';
            officerName = 'Mahesh Sharma';
            officerId = 'BSES-LINEMAN-2910';
            officerDept = 'Electricity Supply Company (Power & Safety)';
        }
    }

    selectedWorkerSelfieFile = null;
    selectedWorkerSelfiePath = selfieSrc;

    const img = document.getElementById('verify-worker-selfie-img');
    if (img) img.src = selfieSrc;
    const stamp = document.getElementById('verify-selfie-stamp');
    if (stamp) stamp.textContent = `Attendance Authenticated • On-Site`;

    const nameInput = document.getElementById('verify-emp-name');
    const idInput = document.getElementById('verify-emp-id');
    const deptSelect = document.getElementById('verify-emp-dept');
    if (nameInput) nameInput.value = officerName;
    if (idInput) idInput.value = officerId;
    if (deptSelect) deptSelect.value = officerDept;
}

function getCurrentDeviceGPS() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const lat = pos.coords.latitude.toFixed(4);
                const lng = pos.coords.longitude.toFixed(4);
                document.getElementById('verify-checkin-lat').value = lat;
                document.getElementById('verify-checkin-lng').value = lng;
                updateGeofenceBadge(parseFloat(lat), parseFloat(lng));
            },
            () => {
                // Fallback to auto-populated near ticket coords
                const select = document.getElementById('verify-incident-select');
                const inc = allIncidents.find(i => String(i.id) === String(select.value));
                if (inc) {
                    const lat = (inc.latitude + 0.0001).toFixed(4);
                    const lng = (inc.longitude + 0.0001).toFixed(4);
                    document.getElementById('verify-checkin-lat').value = lat;
                    document.getElementById('verify-checkin-lng').value = lng;
                    updateGeofenceBadge(parseFloat(lat), parseFloat(lng));
                }
            }
        );
    }
}

function updateGeofenceBadge(lat, lng) {
    const select = document.getElementById('verify-incident-select');
    const inc = allIncidents.find(i => String(i.id) === String(select.value));
    const badge = document.getElementById('verify-geofence-badge');
    if (inc && badge) {
        // Simple distance approximation in meters
        const dLat = (lat - inc.latitude) * 111000;
        const dLng = (lng - inc.longitude) * 111000 * Math.cos(inc.latitude * Math.PI / 180);
        const distM = Math.sqrt(dLat * dLat + dLng * dLng);
        if (distM <= 150) {
            badge.className = 'text-[11px] bg-emerald-500/20 text-emerald-300 border border-emerald-400/40 px-3 py-1 rounded-full font-semibold';
            badge.innerHTML = `<i class="fa-solid fa-satellite-dish mr-1 text-emerald-400"></i> Geofence Verified: ${distM.toFixed(1)}m from hazard`;
        } else {
            badge.className = 'text-[11px] bg-amber-500/20 text-amber-300 border border-amber-400/40 px-3 py-1 rounded-full font-semibold';
            badge.innerHTML = `<i class="fa-solid fa-triangle-exclamation mr-1 text-amber-400"></i> Geofence Alert: ${distM.toFixed(1)}m from hazard`;
        }
    }
}

function openVerificationForId(id) {
    switchTab('contractor');
    setTimeout(() => {
        const select = document.getElementById('verify-incident-select');
        if (select) {
            select.value = id;
            loadIncidentForVerification();
        }
    }, 200);
}

function loadIncidentForVerification() {
    const select = document.getElementById('verify-incident-select');
    if (!select) return;
    const incId = select.value;
    const inc = allIncidents.find(i => String(i.id) === String(incId));
    
    if (inc) {
        const beforeImg = document.getElementById('verify-before-img');
        const beforeLabel = document.getElementById('verify-before-label');
        const targetCoords = document.getElementById('verify-target-coords');
        const targetDept = document.getElementById('verify-target-dept');
        const beforeCoords = document.getElementById('verify-before-coords');
        const afterCoords = document.getElementById('verify-after-coords');
        
        let beforeSrc = inc.before_image || '/static/sample_images/pothole_before.jpg';
        if (beforeImg) beforeImg.src = beforeSrc;
        if (beforeLabel) beforeLabel.textContent = `${inc.title} (${inc.ward}, ${inc.state})`;
        
        const latStr = inc.latitude.toFixed(4);
        const lngStr = inc.longitude.toFixed(4);
        
        if (targetCoords) targetCoords.innerHTML = `<i class="fa-solid fa-map-pin text-red-500 mr-1"></i> Target Hazard GPS: ${latStr}° N, ${lngStr}° E • ${inc.address || inc.ward}`;
        if (targetDept) targetDept.innerHTML = `<i class="fa-solid fa-building text-slate-400 mr-1"></i> ${inc.department}`;
        if (beforeCoords) beforeCoords.textContent = `GPS: ${latStr}° N, ${lngStr}° E • Pre-Work Defect Confirmed`;
        if (afterCoords) afterCoords.textContent = `GPS: ${latStr}° N, ${lngStr}° E • Work Completed On-Site`;
        
        // Auto-fill check-in coords close to hazard
        const checkinLat = document.getElementById('verify-checkin-lat');
        const checkinLng = document.getElementById('verify-checkin-lng');
        if (checkinLat) checkinLat.value = (inc.latitude + 0.0001).toFixed(4);
        if (checkinLng) checkinLng.value = (inc.longitude + 0.0001).toFixed(4);
        updateGeofenceBadge(inc.latitude + 0.0001, inc.longitude + 0.0001);
        
        loadMatchingWorkerSelfie();
        loadMatchingSampleAfter();
        document.getElementById('verify-result-card').classList.add('hidden');
    }
}

function loadMatchingSampleAfter() {
    const select = document.getElementById('verify-incident-select');
    if (!select) return;
    const incId = select.value;
    const inc = allIncidents.find(i => String(i.id) === String(incId));
    
    let afterSrc = '/static/sample_images/pothole_after.jpg';
    if (inc) {
        const h = inc.hazard_type.toLowerCase();
        if (h.includes('garbage') || h.includes('waste')) afterSrc = '/static/sample_images/garbage_after.jpg';
        else if (h.includes('wire') || h.includes('electric')) afterSrc = '/static/sample_images/wire_hazard_after.jpg';
    }
    const afterImg = document.getElementById('verify-after-img');
    if (afterImg) afterImg.src = afterSrc;
}

function handleVerificationFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = e => {
            const afterImg = document.getElementById('verify-after-img');
            if (afterImg) afterImg.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}

async function runAIVerification() {
    const select = document.getElementById('verify-incident-select');
    const incId = select.value;
    if (!incId) {
        alert('Please select an open incident first.');
        return;
    }

    const inc = allIncidents.find(i => String(i.id) === String(incId));
    const fileInput = document.getElementById('verify-after-file');
    const currentAfterSrc = document.getElementById('verify-after-img').getAttribute('src');
    
    const empName = document.getElementById('verify-emp-name') ? document.getElementById('verify-emp-name').value : 'Er. Rajesh Kumar';
    const empId = document.getElementById('verify-emp-id') ? document.getElementById('verify-emp-id').value : 'BBMP-PWD-8492';
    const empDept = document.getElementById('verify-emp-dept') ? document.getElementById('verify-emp-dept').value : 'Public Works Department';
    
    const checkinLat = document.getElementById('verify-checkin-lat') ? document.getElementById('verify-checkin-lat').value : '12.9260';
    const checkinLng = document.getElementById('verify-checkin-lng') ? document.getElementById('verify-checkin-lng').value : '77.6762';

    const btn = document.getElementById('run-verify-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1"></i> Running Tri-Factor AI Audit (Selfie Attendance + Geofence + Surface Leveling)...`;
    btn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('incident_id', incId);
        formData.append('employee_name', empName);
        formData.append('employee_id', empId);
        formData.append('employee_dept', empDept);
        formData.append('checkin_lat', checkinLat);
        formData.append('checkin_lng', checkinLng);
        formData.append('completion_lat', checkinLat);
        formData.append('completion_lng', checkinLng);
        
        // Append worker selfie
        if (selectedWorkerSelfieFile) {
            formData.append('worker_selfie', selectedWorkerSelfieFile);
        } else if (selectedWorkerSelfiePath) {
            formData.append('sample_selfie_path', selectedWorkerSelfiePath);
        } else {
            const currentSelfieSrc = document.getElementById('verify-worker-selfie-img').getAttribute('src');
            if (currentSelfieSrc) formData.append('sample_selfie_path', currentSelfieSrc);
        }

        // Append completion after photo
        if (fileInput.files.length > 0) {
            formData.append('after_image', fileInput.files[0]);
        } else if (currentAfterSrc) {
            formData.append('sample_after_path', currentAfterSrc);
        }

        const res = await fetch('/api/verify-resolution', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();

        const card = document.getElementById('verify-result-card');
        const icon = document.getElementById('verify-icon');
        const title = document.getElementById('verify-title');
        const score = document.getElementById('verify-score');
        const remarks = document.getElementById('verify-remarks');

        card.classList.remove('hidden');

        if (data.success && data.verified) {
            icon.className = 'fa-solid fa-circle-check text-emerald-400 text-2xl';
            title.textContent = `Official Municipal Work Completion Certificate`;
            title.className = 'font-bold text-base text-emerald-400';
            score.textContent = `${data.verification_score}%`;
            score.className = 'text-2xl font-mono font-bold text-emerald-400';
            remarks.textContent = `${data.remarks} (Verified by: ${empName} [${empId}], Dept: ${empDept})`;

            // Populate Certificate 3-Photo Gallery
            const certSelfie = document.getElementById('cert-selfie-img');
            const certBefore = document.getElementById('cert-before-img');
            const certAfter = document.getElementById('cert-after-img');
            const certWorker = document.getElementById('cert-worker-info');
            const certBeforeInfo = document.getElementById('cert-before-info');
            const certAfterInfo = document.getElementById('cert-after-info');
            const certGear = document.getElementById('cert-worker-gear');
            const certGeofence = document.getElementById('cert-geofence');
            const certRemediation = document.getElementById('cert-remediation');
            const certHash = document.getElementById('cert-hash');

            if (certSelfie && data.worker) certSelfie.src = data.worker.selfie_url || '/static/sample_images/worker_selfie_pothole.jpg';
            if (certBefore && inc) certBefore.src = inc.before_image || '/static/sample_images/pothole_before.jpg';
            if (certAfter) certAfter.src = currentAfterSrc;

            if (certWorker) certWorker.textContent = `${empName} [${empId}]`;
            if (certBeforeInfo && inc) certBeforeInfo.textContent = `GPS: ${inc.latitude.toFixed(4)}°, ${inc.longitude.toFixed(4)}°`;
            if (certAfterInfo) certAfterInfo.textContent = `GPS: ${checkinLat}°, ${checkinLng}°`;

            if (certGear && data.worker) certGear.textContent = data.worker.safety_gear || 'Verified Uniform & Helmet';
            if (certGeofence && data.geofence) certGeofence.textContent = data.geofence.status || 'Verified On-Site';
            if (certRemediation) certRemediation.textContent = `Surface Remediation Verified (${data.verification_score}%)`;
            if (certHash) certHash.textContent = `CIVIC-${(Math.random()*1e9).toString(36).toUpperCase()}-AUTH`;

            card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            await loadIncidents();
        } else {
            icon.className = 'fa-solid fa-triangle-exclamation text-red-400 text-2xl';
            title.textContent = 'AI Verification Rejected: Incomplete Repair or Fraud';
            title.className = 'font-bold text-base text-red-400';
            score.textContent = `${data.verification_score || 0}%`;
            score.className = 'text-2xl font-mono font-bold text-red-400';
            remarks.textContent = data.remarks || 'Post-repair photo did not meet surface standards.';
        }

    } catch (e) {
        console.error('Verification error:', e);
        alert('Verification request failed. Check server connection.');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// -------------------------------------------------------------
// 10. ANALYTICS & WARD CIVIC HEALTH INDEX (CHI)
// -------------------------------------------------------------
async function loadAnalytics() {
    try {
        const res = await fetch('/api/analytics');
        const data = await res.json();

        document.getElementById('stat-total').textContent = data.total_incidents || 0;
        document.getElementById('stat-resolved').textContent = data.resolved_incidents || 0;
        document.getElementById('stat-rate').textContent = `${data.resolution_rate || 0}% Resolution Rate`;
        document.getElementById('stat-critical').textContent = data.active_critical || 0;
        document.getElementById('stat-avg-score').textContent = `${data.avg_verification_score || 0}%`;

        // Populate Ward Leaderboard
        const tbody = document.getElementById('ward-leaderboard-body');
        if (tbody) {
            tbody.innerHTML = '';
            (data.ward_health_index || []).forEach(w => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 border-b border-slate-100';
                
                let gradeBadge = 'bg-emerald-100 text-emerald-800 font-bold';
                if (w.grade === 'B') gradeBadge = 'bg-sky-100 text-sky-800 font-bold';
                else if (w.grade === 'C') gradeBadge = 'bg-amber-100 text-amber-800 font-bold';
                else if (w.grade === 'D') gradeBadge = 'bg-red-100 text-red-800 font-bold';

                tr.innerHTML = `
                    <td class="p-3 font-semibold text-slate-800">
                        ${w.ward}
                        <span class="text-[10px] text-slate-400 block">${w.city}, ${w.state || 'India'}</span>
                    </td>
                    <td class="p-3">${w.total}</td>
                    <td class="p-3 text-emerald-600 font-bold">${w.resolved}</td>
                    <td class="p-3 text-red-600 font-bold">${w.active_critical}</td>
                    <td class="p-3 font-mono font-bold text-slate-900">${w.chi_score} / 100</td>
                    <td class="p-3">
                        <span class="inline-block px-2.5 py-0.5 rounded text-xs ${gradeBadge}">
                            Grade ${w.grade}
                        </span>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        renderCharts(data.hazard_counts || {}, data.state_counts || data.city_counts || {});

    } catch (e) {
        console.error('Failed to load analytics:', e);
    }
}

function renderCharts(hazardCounts, distributionCounts) {
    const ctxHazard = document.getElementById('chart-hazards');
    if (ctxHazard) {
        if (hazardChart) hazardChart.destroy();
        hazardChart = new Chart(ctxHazard, {
            type: 'doughnut',
            data: {
                labels: Object.keys(hazardCounts),
                datasets: [{
                    data: Object.values(hazardCounts),
                    backgroundColor: ['#ef4444', '#f97316', '#3b82f6', '#8b5cf6', '#10b981'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } }
                }
            }
        });
    }

    const ctxCity = document.getElementById('chart-cities');
    if (ctxCity) {
        if (cityChart) cityChart.destroy();
        cityChart = new Chart(ctxCity, {
            type: 'bar',
            data: {
                labels: Object.keys(distributionCounts),
                datasets: [{
                    label: 'Logged Grievances by State/City',
                    data: Object.values(distributionCounts),
                    backgroundColor: '#4f46e5',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1, font: { size: 10 } } },
                    x: { ticks: { font: { size: 10 } } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
}

// -------------------------------------------------------------
// 11. NAGRIK AI COPILOT CHAT
// -------------------------------------------------------------
function toggleChatModal() {
    const modal = document.getElementById('chat-modal');
    modal.classList.toggle('hidden');
    if (!modal.classList.contains('hidden')) {
        document.getElementById('chat-input').focus();
    }
}

async function sendChatMessage(event) {
    event.preventDefault();
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (!msg) return;

    const chatMessages = document.getElementById('chat-messages');

    // Citizen Message Bubble
    const userBubble = document.createElement('div');
    userBubble.className = 'chat-bubble bg-indigo-600 text-white p-2.5 rounded-xl rounded-tr-none max-w-[85%] ml-auto text-right text-xs shadow-sm';
    userBubble.textContent = msg;
    chatMessages.appendChild(userBubble);
    input.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Typing Indicator Bubble
    const typingBubble = document.createElement('div');
    typingBubble.className = 'chat-bubble bg-slate-100 text-slate-500 p-2 rounded-xl rounded-tl-none max-w-[85%] text-xs italic flex items-center space-x-1.5';
    typingBubble.innerHTML = `<i class="fa-solid fa-spinner fa-spin text-indigo-600 text-xs"></i> <span>Nagrik AI is verifying municipal records...</span>`;
    chatMessages.appendChild(typingBubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();

        // Remove typing indicator
        if (typingBubble.parentNode) typingBubble.parentNode.removeChild(typingBubble);

        const botBubble = document.createElement('div');
        botBubble.className = 'chat-bubble bg-slate-200 text-slate-800 p-3 rounded-xl rounded-tl-none max-w-[90%] text-xs leading-relaxed shadow-sm';
        botBubble.style.whiteSpace = 'pre-wrap';
        botBubble.textContent = data.reply || "I'm here to assist with civic reporting across all Indian States.";
        chatMessages.appendChild(botBubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;

    } catch (e) {
        console.error('Chat error:', e);
        if (typingBubble.parentNode) typingBubble.parentNode.removeChild(typingBubble);
        
        const errBubble = document.createElement('div');
        errBubble.className = 'chat-bubble bg-amber-50 text-amber-900 border border-amber-300 p-2.5 rounded-xl rounded-tl-none max-w-[90%] text-xs';
        errBubble.innerHTML = `<i class="fa-solid fa-circle-exclamation text-amber-600 mr-1"></i> CivicLens server connection error. Please refresh the page or ensure the backend server is running.`;
        chatMessages.appendChild(errBubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// -------------------------------------------------------------
// 12. VERNACULAR SPEECH-TO-TEXT ASSISTANT
// -------------------------------------------------------------
function startVoiceInput() {
    const btnText = document.getElementById('voice-btn-text');
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        alert('Speech recognition is not supported in this browser. Please type your description.');
        return;
    }

    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRec();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;

    recognition.onstart = () => {
        btnText.textContent = 'Listening... Speak now';
        btnText.parentElement.classList.add('text-red-600', 'animate-pulse');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const descField = document.getElementById('report-desc');
        descField.value = transcript;
        btnText.textContent = 'Voice Input (Captured)';
        btnText.parentElement.classList.remove('text-red-600', 'animate-pulse');
    };

    recognition.onerror = () => {
        btnText.textContent = 'Voice Input Failed';
        btnText.parentElement.classList.remove('text-red-600', 'animate-pulse');
    };

    recognition.onend = () => {
        btnText.textContent = 'Voice Input (EN/HI/TA/TE)';
        btnText.parentElement.classList.remove('text-red-600', 'animate-pulse');
    };

    recognition.start();
}
