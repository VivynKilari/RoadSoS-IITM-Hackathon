import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import math

# --- LOGIC: Distance Calculation ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- LOGIC: Fetch Nearby Hospitals ---
def get_nearby_hospitals(lat, lon, radius=3000):
    overpass_url = "https://lz4.overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:10];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
    );
    out center;
    """
    headers = {'User-Agent': 'RoadSoS-IITM-Hackathon-Project/1.0'}
    
    fallback_data = [
        {"lat": lat + 0.005, "lon": lon + 0.002, "tags": {"name": "Apollo City Hospital (Offline)"}},
        {"lat": lat - 0.003, "lon": lon - 0.004, "tags": {"name": "Sanjeevani Trauma Center (Offline)"}},
        {"lat": lat + 0.001, "lon": lon - 0.006, "tags": {"name": "Nashik General Clinic (Offline)"}}
    ]
    
    try:
        response = requests.get(overpass_url, params={'data': overpass_query}, headers=headers, timeout=5)
        response.raise_for_status() 
        data = response.json()
        if not data.get('elements'):
            raise ValueError("API returned empty data.")
        return data.get('elements', []), True 
    except Exception:
        return fallback_data, False 

# --- LOGIC: NLP Severity Analyzer ---
def analyze_severity(text):
    """Analyzes text to determine emergency severity."""
    text = text.lower()
    critical_keywords = ['unconscious', 'bleeding', 'severe', 'head', 'heart', 'trauma', 'unresponsive', 'heavy', 'critical']
    
    if any(word in text for word in critical_keywords):
        return "CRITICAL (Code Red)", "red", "🚑 Dispatching Advanced Life Support (ALS) Ambulance..."
    else:
        return "MODERATE (Code Yellow)", "orange", "🚐 Dispatching Basic Life Support (BLS) Ambulance..."

# --- UI: Streamlit Webpage Setup ---
st.set_page_config(page_title="RoadSoS - Debug & Drive", layout="wide")
st.title("🚑 RoadSoS: Emergency Response System")
st.write("Live tracking of nearest medical centers for rapid SOS dispatch.")

# Set base coordinates (Nashik)
nashik_lat, nashik_lon = 19.9975, 73.7898

# Add a two-column layout
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("🚨 Incident Report")
    
    # Text input for the AI Analyzer
    incident_text = st.text_area(
        "Enter caller description:", 
        value="Motorcycle skidded on Trimbak Road. The rider has a severe head injury and is unconscious."
    )
    
    # Run the NLP logic
    severity, color, action = analyze_severity(incident_text)
    
    # Display dynamic status based on text
    st.markdown(f"**STATUS: <span style='color:{color}'>{severity}</span>**", unsafe_allow_html=True)
    st.info(action)
    
    with st.spinner("Routing to nearest medical center..."):
        hospitals, is_live = get_nearby_hospitals(nashik_lat, nashik_lon)

    if not is_live:
        st.warning("Using Offline Emergency Mode.")

with col2:
    m = folium.Map(location=[nashik_lat, nashik_lon], zoom_start=14)

    folium.Marker(
        [nashik_lat, nashik_lon], 
        popup="⚠️ ACCIDENT LOCATION", 
        icon=folium.Icon(color="red", icon="warning-sign")
    ).add_to(m)

    closest_hospital = None
    min_distance = float('inf')

    for hospital in hospitals:
        h_lat = hospital['lat']
        h_lon = hospital['lon']
        
        dist = calculate_distance(nashik_lat, nashik_lon, h_lat, h_lon)
        
        if dist < min_distance:
            min_distance = dist
            closest_hospital = hospital

        name = hospital.get('tags', {}).get('name', 'Unknown Medical Center')
        folium.Marker(
            [h_lat, h_lon],
            popup=f"🏥 {name} ({dist:.2f} km)",
            icon=folium.Icon(color="blue", icon="plus")
        ).add_to(m)

    if closest_hospital:
        c_lat = closest_hospital['lat']
        c_lon = closest_hospital['lon']
        c_name = closest_hospital.get('tags', {}).get('name', 'Unknown Medical Center')
        
        folium.Marker(
            [c_lat, c_lon],
            popup=f"✅ NEAREST: {c_name} ({min_distance:.2f} km)",
            icon=folium.Icon(color="green", icon="ok-sign")
        ).add_to(m)
        
        folium.PolyLine(
            locations=[[nashik_lat, nashik_lon], [c_lat, c_lon]],
            color="red" if color == "red" else "orange", # Line color matches severity!
            weight=4,
            dash_array="10",
            tooltip=f"Emergency Route: {min_distance:.2f} km"
        ).add_to(m)
        
        with col1:
            st.success(f"**Nearest Hospital Found!**\n\n🏥 {c_name}\n\n📏 Distance: {min_distance:.2f} km")

    st_folium(m, width=800, height=500)