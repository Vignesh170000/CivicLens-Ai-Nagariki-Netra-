"""
All 28 States and 8 Union Territories of India
Complete dataset with state codes, capitals, major cities, GIS centroids, and sample administrative wards.
"""

ALL_INDIA_STATES = {
    # 28 States
    "Andhra Pradesh": {
        "code": "AP",
        "type": "State",
        "capital": "Amaravati",
        "coords": {"lat": 16.5062, "lng": 80.6480, "zoom": 11},
        "cities": {
            "Visakhapatnam": ["Ward 1 - Gajuwaka", "Ward 15 - MVP Colony", "Ward 22 - Jagadamba", "Ward 35 - Madhurawada"],
            "Vijayawada": ["Ward 5 - Benz Circle", "Ward 12 - Governorpet", "Ward 20 - Patamata"],
            "Guntur": ["Ward 3 - Brodipet", "Ward 8 - Arundelpet", "Ward 14 - Nagarampalem"],
            "Tirupati": ["Ward 4 - Alipiri", "Ward 9 - Korlagunta", "Ward 18 - Air Bypass Road"]
        }
    },
    "Arunachal Pradesh": {
        "code": "AR",
        "type": "State",
        "capital": "Itanagar",
        "coords": {"lat": 27.0844, "lng": 93.6053, "zoom": 12},
        "cities": {
            "Itanagar": ["Ward 1 - Ganga Market", "Ward 4 - Bank Tinali", "Ward 8 - Niti Vihar"],
            "Naharlagun": ["Ward 2 - Model Village", "Ward 5 - Helipad Road", "Ward 9 - Barapani"],
            "Pasighat": ["Ward 1 - Market Area", "Ward 3 - Hill Top", "Ward 6 - Mirsam"]
        }
    },
    "Assam": {
        "code": "AS",
        "type": "State",
        "capital": "Dispur / Guwahati",
        "coords": {"lat": 26.1445, "lng": 91.7362, "zoom": 12},
        "cities": {
            "Guwahati": ["Ward 14 - GS Road", "Ward 22 - Dispur Capital Zone", "Ward 31 - Paltan Bazaar", "Ward 45 - Jalukbari"],
            "Dibrugarh": ["Ward 3 - Thana Chariali", "Ward 7 - Graham Bazar", "Ward 12 - Boiragimoth"],
            "Silchar": ["Ward 5 - Rangirkhari", "Ward 10 - Premtala", "Ward 15 - Tarapur"],
            "Jorhat": ["Ward 4 - Gar-Ali", "Ward 8 - AT Road", "Ward 11 - Choladhara"]
        }
    },
    "Bihar": {
        "code": "BR",
        "type": "State",
        "capital": "Patna",
        "coords": {"lat": 25.5941, "lng": 85.1376, "zoom": 12},
        "cities": {
            "Patna": ["Ward 18 - Bailey Road", "Ward 22 - Fraser Road", "Ward 35 - Kankarbagh", "Ward 44 - Boring Road"],
            "Gaya": ["Ward 7 - Civil Lines", "Ward 14 - Bodhgaya Road", "Ward 21 - Station Road"],
            "Bhagalpur": ["Ward 4 - Tilkamanjhi", "Ward 9 - Sujaganj", "Ward 16 - Zero Mile"],
            "Muzaffarpur": ["Ward 5 - Motijheel", "Ward 11 - Mithanpura", "Ward 18 - Club Road"]
        }
    },
    "Chhattisgarh": {
        "code": "CG",
        "type": "State",
        "capital": "Raipur",
        "coords": {"lat": 21.2514, "lng": 81.6296, "zoom": 12},
        "cities": {
            "Raipur": ["Ward 12 - Telibandha", "Ward 25 - Pandri", "Ward 38 - Shankar Nagar", "Ward 52 - Tatibandh"],
            "Bilaspur": ["Ward 6 - Vyapar Vihar", "Ward 15 - Link Road", "Ward 24 - Torwa"],
            "Durg-Bhilai": ["Ward 8 - Sector 6 Bhilai", "Ward 19 - Civic Center", "Ward 31 - Durg Station Road"]
        }
    },
    "Goa": {
        "code": "GA",
        "type": "State",
        "capital": "Panaji",
        "coords": {"lat": 15.4909, "lng": 73.8278, "zoom": 13},
        "cities": {
            "Panaji": ["Ward 1 - Miramar Beach Road", "Ward 5 - Fontainhas Latin Quarter", "Ward 9 - Campal", "Ward 12 - Patto Plaza"],
            "Margao": ["Ward 3 - Comba", "Ward 8 - Aquem", "Ward 14 - Fatorda Stadium Road"],
            "Vasco da Gama": ["Ward 2 - Swatantra Path", "Ward 6 - Baina", "Ward 11 - Mangor Hill"]
        }
    },
    "Gujarat": {
        "code": "GJ",
        "type": "State",
        "capital": "Gandhinagar",
        "coords": {"lat": 23.0225, "lng": 72.5714, "zoom": 12},
        "cities": {
            "Ahmedabad": ["Ward 14 - SG Highway", "Ward 28 - Bodakdev", "Ward 42 - Navrangpura", "Ward 56 - Maninagar"],
            "Surat": ["Ward 8 - Adajan", "Ward 19 - Ring Road", "Ward 32 - Vesu", "Ward 45 - Varachha"],
            "Vadodara": ["Ward 5 - Alkapuri", "Ward 14 - Sayajigunj", "Ward 22 - Gotri"],
            "Rajkot": ["Ward 3 - Kalawad Road", "Ward 9 - Yagnik Road", "Ward 15 - University Road"]
        }
    },
    "Haryana": {
        "code": "HR",
        "type": "State",
        "capital": "Chandigarh",
        "coords": {"lat": 28.4595, "lng": 77.0266, "zoom": 12},
        "cities": {
            "Gurugram": ["Ward 12 - Cyber City DLF", "Ward 24 - Golf Course Road", "Ward 35 - Sohna Road", "Ward 42 - Sector 29"],
            "Faridabad": ["Ward 8 - Sector 15", "Ward 17 - NIT Faridabad", "Ward 26 - Mathura Road"],
            "Panipat": ["Ward 4 - Model Town", "Ward 9 - GT Road", "Ward 15 - Industrial Area"],
            "Ambala": ["Ward 3 - Cantt Station Road", "Ward 7 - Model Town", "Ward 12 - Cloth Market"]
        }
    },
    "Himachal Pradesh": {
        "code": "HP",
        "type": "State",
        "capital": "Shimla",
        "coords": {"lat": 31.1048, "lng": 77.1734, "zoom": 12},
        "cities": {
            "Shimla": ["Ward 2 - The Mall Road", "Ward 6 - Chotta Shimla", "Ward 11 - Sanjauli", "Ward 17 - Tutu"],
            "Dharamshala": ["Ward 1 - McLeodGanj Square", "Ward 4 - Kotwali Bazaar", "Ward 8 - Kachehri"],
            "Manali": ["Ward 2 - Circuit House Road", "Ward 5 - Old Manali", "Ward 7 - Model Town"]
        }
    },
    "Jharkhand": {
        "code": "JH",
        "type": "State",
        "capital": "Ranchi",
        "coords": {"lat": 23.3441, "lng": 85.3096, "zoom": 12},
        "cities": {
            "Ranchi": ["Ward 14 - Main Road", "Ward 22 - Lalpur", "Ward 31 - Doranda", "Ward 45 - Harmu Housing"],
            "Jamshedpur": ["Ward 5 - Bistupur", "Ward 12 - Sakchi Market", "Ward 19 - Telco Colony"],
            "Dhanbad": ["Ward 4 - Bank More", "Ward 11 - Steel Gate", "Ward 18 - Hirapur"]
        }
    },
    "Karnataka": {
        "code": "KA",
        "type": "State",
        "capital": "Bengaluru",
        "coords": {"lat": 12.9716, "lng": 77.5946, "zoom": 12},
        "cities": {
            "Bengaluru": ["Ward 150 - Bellandur", "Ward 80 - Hoysala Nagar", "Ward 151 - Koramangala", "Ward 112 - Domlur", "Ward 174 - HSR Layout", "Ward 198 - Hemmigepura"],
            "Mysuru": ["Ward 8 - Jayalakshmipuram", "Ward 19 - Kuvempunagar", "Ward 25 - Devaraja Mohalla"],
            "Hubballi-Dharwad": ["Ward 12 - Vidyanagar", "Ward 24 - Station Road", "Ward 35 - Dharwad Court Circle"],
            "Mangaluru": ["Ward 5 - Kadri", "Ward 14 - Hampankatta", "Ward 22 - Bejai"]
        }
    },
    "Kerala": {
        "code": "KL",
        "type": "State",
        "capital": "Thiruvananthapuram",
        "coords": {"lat": 8.5241, "lng": 76.9366, "zoom": 12},
        "cities": {
            "Thiruvananthapuram": ["Ward 15 - Kowdiar", "Ward 28 - Palayam", "Ward 42 - Thampanoor", "Ward 65 - Kazhakkoottam Techpark"],
            "Kochi": ["Ward 12 - Marine Drive", "Ward 26 - MG Road Ernakulam", "Ward 38 - Fort Kochi", "Ward 55 - Kakkanad Infopark"],
            "Kozhikode": ["Ward 8 - Mavoor Road", "Ward 19 - SM Street", "Ward 31 - Calicut Beach Road"],
            "Thrissur": ["Ward 5 - Swaraj Round", "Ward 14 - East Fort", "Ward 22 - Ayyanthole"]
        }
    },
    "Madhya Pradesh": {
        "code": "MP",
        "type": "State",
        "capital": "Bhopal",
        "coords": {"lat": 23.2599, "lng": 77.4126, "zoom": 12},
        "cities": {
            "Bhopal": ["Ward 18 - MP Nagar", "Ward 29 - Arera Colony", "Ward 44 - New Market", "Ward 62 - Bairagarh"],
            "Indore": ["Ward 14 - Vijay Nagar", "Ward 28 - Rajwada", "Ward 45 - Palasia", "Ward 68 - Chhappan Dukan"],
            "Gwalior": ["Ward 8 - Lashkar", "Ward 17 - City Centre", "Ward 29 - Morar"],
            "Jabalpur": ["Ward 5 - Wright Town", "Ward 14 - Civil Lines", "Ward 22 - Napier Town"]
        }
    },
    "Maharashtra": {
        "code": "MH",
        "type": "State",
        "capital": "Mumbai",
        "coords": {"lat": 19.0760, "lng": 72.8777, "zoom": 12},
        "cities": {
            "Mumbai": ["Ward K/East - Andheri", "Ward H/West - Bandra", "Ward D - Malabar Hill", "Ward F/North - Matunga", "Ward G/South - Worli"],
            "Pune": ["Ward 8 - Shivajinagar", "Ward 16 - Kothrud", "Ward 24 - Viman Nagar", "Ward 32 - Hinjawadi IT Zone"],
            "Nagpur": ["Ward 5 - Dharampeth", "Ward 14 - Sitabuldi", "Ward 23 - Wardha Road"],
            "Nashik": ["Ward 4 - College Road", "Ward 11 - Panchavati", "Ward 19 - Gangapur Road"],
            "Thane": ["Ward 6 - Ghodbunder Road", "Ward 15 - Naupada", "Ward 28 - Majiwada"]
        }
    },
    "Manipur": {
        "code": "MN",
        "type": "State",
        "capital": "Imphal",
        "coords": {"lat": 24.8170, "lng": 93.9368, "zoom": 12},
        "cities": {
            "Imphal": ["Ward 3 - Paona Bazaar", "Ward 7 - Thangal Bazaar", "Ward 12 - Kangla West", "Ward 19 - Lamphelpat"],
            "Churachandpur": ["Ward 2 - Tuibong", "Ward 5 - Rengkai", "Ward 9 - New Lamka"],
            "Thoubal": ["Ward 1 - Thoubal Bazaar", "Ward 4 - Wangbal", "Ward 8 - Athokpam"]
        }
    },
    "Meghalaya": {
        "code": "ML",
        "type": "State",
        "capital": "Shillong",
        "coords": {"lat": 25.5788, "lng": 91.8933, "zoom": 12},
        "cities": {
            "Shillong": ["Ward 2 - Police Bazar", "Ward 6 - Laitumkhrah", "Ward 11 - Laban", "Ward 15 - Polo Grounds"],
            "Tura": ["Ward 1 - Hawakhana", "Ward 4 - Araimile", "Ward 8 - Dobasipara"],
            "Cherrapunji": ["Ward 1 - Sohra Market", "Ward 3 - Nohkalikai Road", "Ward 5 - Khasi Heritage"]
        }
    },
    "Mizoram": {
        "code": "MZ",
        "type": "State",
        "capital": "Aizawl",
        "coords": {"lat": 23.7271, "lng": 92.7176, "zoom": 12},
        "cities": {
            "Aizawl": ["Ward 3 - Zarkawt", "Ward 7 - Dawrpui", "Ward 12 - Khatla", "Ward 18 - Mission Veng"],
            "Lunglei": ["Ward 2 - Venglai", "Ward 5 - Chanmari", "Ward 8 - Bazar Veng"],
            "Champhai": ["Ward 1 - Vengthlang", "Ward 4 - Kahrawt", "Ward 7 - Bethel"]
        }
    },
    "Nagaland": {
        "code": "NL",
        "type": "State",
        "capital": "Kohima",
        "coords": {"lat": 25.6751, "lng": 94.1086, "zoom": 12},
        "cities": {
            "Kohima": ["Ward 2 - Main Town", "Ward 6 - High School Colony", "Ward 11 - PR Hill", "Ward 16 - Ministers Hill"],
            "Dimapur": ["Ward 3 - Clock Tower Road", "Ward 8 - Circular Road", "Ward 14 - Purana Bazaar"],
            "Mokokchung": ["Ward 2 - Arkong", "Ward 5 - Penli", "Ward 9 - Dilong"]
        }
    },
    "Odisha": {
        "code": "OD",
        "type": "State",
        "capital": "Bhubaneswar",
        "coords": {"lat": 20.2961, "lng": 85.8245, "zoom": 12},
        "cities": {
            "Bhubaneswar": ["Ward 14 - Janpath Road", "Ward 25 - Saheed Nagar", "Ward 38 - Jayadev Vihar", "Ward 51 - Patia Infocity"],
            "Cuttack": ["Ward 6 - Badambadi", "Ward 15 - Ranihat", "Ward 28 - College Square"],
            "Rourkela": ["Ward 4 - Civil Township", "Ward 11 - Sector 19", "Ward 18 - Panposh Road"],
            "Puri": ["Ward 2 - Grand Road (Bada Danda)", "Ward 8 - VIP Road", "Ward 14 - Chakratirtha"]
        }
    },
    "Punjab": {
        "code": "PB",
        "type": "State",
        "capital": "Chandigarh",
        "coords": {"lat": 31.6340, "lng": 74.8723, "zoom": 12},
        "cities": {
            "Ludhiana": ["Ward 14 - Ferozepur Road", "Ward 29 - Sarabha Nagar", "Ward 45 - Model Town", "Ward 62 - Industrial Area A"],
            "Amritsar": ["Ward 8 - Golden Temple Heritage Street", "Ward 17 - Mall Road", "Ward 31 - Lawrence Road"],
            "Jalandhar": ["Ward 6 - Model Town", "Ward 18 - GT Road", "Ward 27 - BMC Chowk"],
            "Patiala": ["Ward 4 - Mall Road", "Ward 11 - Leela Bhawan", "Ward 19 - Tripuri"]
        }
    },
    "Rajasthan": {
        "code": "RJ",
        "type": "State",
        "capital": "Jaipur",
        "coords": {"lat": 26.9124, "lng": 75.7873, "zoom": 12},
        "cities": {
            "Jaipur": ["Ward 18 - Walled City Johari Bazaar", "Ward 32 - MI Road", "Ward 45 - Malviya Nagar", "Ward 61 - Vaishali Nagar"],
            "Jodhpur": ["Ward 7 - Sardarpura", "Ward 16 - Ratanada", "Ward 25 - Paota"],
            "Udaipur": ["Ward 4 - Fatehsagar Lake Road", "Ward 12 - Sukhadia Circle", "Ward 21 - Hiran Magri"],
            "Kota": ["Ward 6 - Vigyan Nagar", "Ward 15 - Talwandi", "Ward 28 - Chawani"]
        }
    },
    "Sikkim": {
        "code": "SK",
        "type": "State",
        "capital": "Gangtok",
        "coords": {"lat": 27.3389, "lng": 88.6065, "zoom": 12},
        "cities": {
            "Gangtok": ["Ward 2 - MG Marg Promenade", "Ward 5 - Deorali", "Ward 9 - Tadong", "Ward 14 - Development Area"],
            "Namchi": ["Ward 1 - Central Park", "Ward 4 - Assangthang", "Ward 7 - Boomtar"],
            "Geyzing": ["Ward 2 - Main Bazaar", "Ward 5 - Pelling Road", "Ward 8 - Kyongsa"]
        }
    },
    "Tamil Nadu": {
        "code": "TN",
        "type": "State",
        "capital": "Chennai",
        "coords": {"lat": 13.0827, "lng": 80.2707, "zoom": 12},
        "cities": {
            "Chennai": ["Ward 136 - T. Nagar", "Ward 114 - Mylapore", "Ward 175 - Adyar", "Ward 80 - Anna Nagar", "Ward 190 - OMR Sholinganallur"],
            "Coimbatore": ["Ward 12 - RS Puram", "Ward 24 - Gandhipuram", "Ward 36 - Peelamedu", "Ward 48 - Race Course"],
            "Madurai": ["Ward 8 - Meenakshi Amman Temple Zone", "Ward 21 - KK Nagar", "Ward 35 - Anna Nagar"],
            "Tiruchirappalli": ["Ward 6 - Thillai Nagar", "Ward 15 - Cantonment", "Ward 28 - Srirangam"]
        }
    },
    "Telangana": {
        "code": "TG",
        "type": "State",
        "capital": "Hyderabad",
        "coords": {"lat": 17.3850, "lng": 78.4867, "zoom": 12},
        "cities": {
            "Hyderabad": ["Ward 107 - Madhapur Hitec City", "Ward 98 - Jubilee Hills", "Ward 72 - Secunderabad", "Ward 54 - Gachibowli", "Ward 82 - Banjara Hills"],
            "Warangal": ["Ward 8 - Hanamkonda", "Ward 19 - Kazipet", "Ward 28 - Naimnagar"],
            "Nizamabad": ["Ward 4 - Khaleelwadi", "Ward 12 - Bodhan Road", "Ward 21 - Subhashnagar"],
            "Karimnagar": ["Ward 5 - Collectorate Road", "Ward 14 - Kothirampur", "Ward 22 - Mankammathota"]
        }
    },
    "Tripura": {
        "code": "TR",
        "type": "State",
        "capital": "Agartala",
        "coords": {"lat": 23.8315, "lng": 91.2868, "zoom": 12},
        "cities": {
            "Agartala": ["Ward 3 - Ujjayanta Palace Zone", "Ward 8 - Banamalipur", "Ward 14 - Kaman Chowmuhani", "Ward 21 - Ramnagar"],
            "Udaipur": ["Ward 2 - Matabari Road", "Ward 6 - Central Market", "Ward 9 - Rajarbagh"],
            "Dharmanagar": ["Ward 1 - Station Road", "Ward 4 - Thana Road", "Ward 7 - Nayapara"]
        }
    },
    "Uttar Pradesh": {
        "code": "UP",
        "type": "State",
        "capital": "Lucknow",
        "coords": {"lat": 26.8467, "lng": 80.9462, "zoom": 12},
        "cities": {
            "Lucknow": ["Ward 14 - Hazratganj", "Ward 28 - Gomti Nagar", "Ward 45 - Alambagh", "Ward 62 - Indira Nagar"],
            "Varanasi": ["Ward 8 - Dashashwamedh Ghat", "Ward 19 - Cantt Station Road", "Ward 32 - Lanka BHU Zone"],
            "Noida": ["Ward 5 - Sector 18 Commercial", "Ward 14 - Sector 62 IT Hub", "Ward 28 - Sector 137 Expressway"],
            "Kanpur": ["Ward 9 - Mall Road", "Ward 22 - Civil Lines", "Ward 38 - Swaroop Nagar"],
            "Agra": ["Ward 4 - Tajganj", "Ward 12 - Sanjay Place", "Ward 26 - Dayalbagh"]
        }
    },
    "Uttarakhand": {
        "code": "UK",
        "type": "State",
        "capital": "Dehradun",
        "coords": {"lat": 30.3165, "lng": 78.0322, "zoom": 12},
        "cities": {
            "Dehradun": ["Ward 8 - Rajpur Road", "Ward 19 - Clock Tower Paltan Bazaar", "Ward 31 - Ballupur", "Ward 44 - Clement Town"],
            "Haridwar": ["Ward 3 - Har Ki Pauri Ghat", "Ward 11 - Ranipur More", "Ward 18 - Jwalapur"],
            "Rishikesh": ["Ward 2 - Laxman Jhula Road", "Ward 7 - Triveni Ghat", "Ward 12 - Muni Ki Reti"],
            "Haldwani": ["Ward 5 - Nainital Road", "Ward 14 - Tikonia", "Ward 22 - Kathgodam"]
        }
    },
    "West Bengal": {
        "code": "WB",
        "type": "State",
        "capital": "Kolkata",
        "coords": {"lat": 22.5726, "lng": 88.3639, "zoom": 12},
        "cities": {
            "Kolkata": ["Ward 64 - Park Circus", "Ward 45 - Esplanade BBD Bagh", "Ward 85 - Ballygunge", "Ward 32 - Salt Lake Sector V", "Ward 92 - Jadavpur"],
            "Howrah": ["Ward 8 - Howrah Station Foreshore", "Ward 21 - Shibpur", "Ward 35 - Kadamtala"],
            "Siliguri": ["Ward 4 - Hill Cart Road", "Ward 12 - Sevoke Road", "Ward 26 - Pradhan Nagar"],
            "Durgapur": ["Ward 6 - City Centre", "Ward 15 - Benachity", "Ward 24 - Bidhannagar"]
        }
    },

    # 8 Union Territories
    "Andaman and Nicobar Islands": {
        "code": "AN",
        "type": "Union Territory",
        "capital": "Port Blair",
        "coords": {"lat": 11.6234, "lng": 92.7265, "zoom": 12},
        "cities": {
            "Port Blair": ["Ward 1 - Aberdeen Bazaar", "Ward 5 - Cellular Jail Marina", "Ward 9 - Dollygunj", "Ward 14 - Haddo"]
        }
    },
    "Chandigarh": {
        "code": "CH",
        "type": "Union Territory",
        "capital": "Chandigarh",
        "coords": {"lat": 30.7333, "lng": 76.7794, "zoom": 12},
        "cities": {
            "Chandigarh": ["Ward 3 - Sector 17 Plaza", "Ward 8 - Sector 35 Market", "Ward 14 - Sector 22", "Ward 22 - Manimajra"]
        }
    },
    "Dadra and Nagar Haveli and Daman and Diu": {
        "code": "DN",
        "type": "Union Territory",
        "capital": "Daman",
        "coords": {"lat": 20.3974, "lng": 72.8328, "zoom": 12},
        "cities": {
            "Daman": ["Ward 1 - Nani Daman Fort Road", "Ward 4 - Devka Beach", "Ward 8 - Moti Daman"],
            "Silvassa": ["Ward 2 - Kilwani Naka", "Ward 5 - Naroli Road", "Ward 9 - Tokarkhada"],
            "Diu": ["Ward 1 - Bunder Chowk", "Ward 3 - Ghoghla Beach", "Ward 6 - Fort Road"]
        }
    },
    "Delhi": {
        "code": "DL",
        "type": "Union Territory",
        "capital": "New Delhi",
        "coords": {"lat": 28.6139, "lng": 77.2090, "zoom": 12},
        "cities": {
            "Delhi": ["Ward 58S - Lajpat Nagar", "Ward NDMC-01 - Connaught Place", "Ward 12 - Karol Bagh", "Ward 45 - Rohini Sector 9", "Ward 82 - Dwarka Sector 10", "Ward 31 - Chandni Chowk"]
        }
    },
    "Jammu and Kashmir": {
        "code": "JK",
        "type": "Union Territory",
        "capital": "Srinagar / Jammu",
        "coords": {"lat": 34.0837, "lng": 74.7973, "zoom": 12},
        "cities": {
            "Srinagar": ["Ward 2 - Lal Chowk", "Ward 7 - Dal Gate Boulevard", "Ward 14 - Rajbagh", "Ward 22 - Hazratbal"],
            "Jammu": ["Ward 4 - Raghunath Bazaar", "Ward 11 - Gandhi Nagar", "Ward 19 - Bahu Fort Road", "Ward 27 - Trikuta Nagar"],
            "Anantnag": ["Ward 3 - KP Road", "Ward 8 - Mattan Chowk", "Ward 12 - Janglat Mandi"]
        }
    },
    "Ladakh": {
        "code": "LA",
        "type": "Union Territory",
        "capital": "Leh",
        "coords": {"lat": 34.1526, "lng": 77.5771, "zoom": 12},
        "cities": {
            "Leh": ["Ward 1 - Leh Main Market", "Ward 4 - Changspa Road", "Ward 8 - Skara", "Ward 11 - Choglamsar"],
            "Kargil": ["Ward 2 - Main Bazaar", "Ward 5 - Baroo Colony", "Ward 7 - Biamathang"]
        }
    },
    "Lakshadweep": {
        "code": "LD",
        "type": "Union Territory",
        "capital": "Kavaratti",
        "coords": {"lat": 10.5667, "lng": 72.6417, "zoom": 13},
        "cities": {
            "Kavaratti": ["Ward 1 - Jetty Area", "Ward 3 - Ujra Mosque Zone", "Ward 5 - Beach Road"]
        }
    },
    "Puducherry": {
        "code": "PY",
        "type": "Union Territory",
        "capital": "Puducherry",
        "coords": {"lat": 11.9416, "lng": 79.8083, "zoom": 12},
        "cities": {
            "Puducherry": ["Ward 1 - White Town Promenade", "Ward 5 - Goubert Market", "Ward 9 - Mission Street", "Ward 16 - Lawspet"],
            "Karaikal": ["Ward 2 - Beach Road", "Ward 6 - Bharathiar Road", "Ward 11 - Nehru Nagar"]
        }
    }
}

def get_states_list():
    """Returns sorted list of all 36 Indian States and Union Territories with metadata."""
    result = []
    for state_name, data in sorted(ALL_INDIA_STATES.items()):
        result.append({
            "name": state_name,
            "code": data["code"],
            "type": data["type"],
            "capital": data["capital"],
            "coords": data["coords"],
            "cities": list(data["cities"].keys())
        })
    return result

def get_cities_for_state(state_name):
    """Returns cities for given state."""
    state = ALL_INDIA_STATES.get(state_name)
    if not state:
        return []
    return list(state["cities"].keys())

def get_wards_for_city(state_name, city_name):
    """Returns wards for given city in state."""
    state = ALL_INDIA_STATES.get(state_name)
    if not state:
        return ["Ward 1 - Central"]
    cities = state["cities"]
    return cities.get(city_name, ["Ward 1 - Central"])
