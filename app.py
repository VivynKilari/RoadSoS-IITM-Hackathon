import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# --- LOGIC: Fetch Nearby Hospitals ---
def get_nearby_hospitals(lat, lon, radius=3000): # Lowered radius to 3km for speed
    """Fetches real-time hospital data from OpenStreetMap with error handling."""
    # Switched to the LZ4 mirror which is often faster and less congested
    overpass_url = "https://lz4.overpass-api.de/api/interpreter"
    
    # Added [timeout:10] to force the server to process it quickly
    overpass_query = f"""
    [out:json][timeout:10];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
    );
    out center;
    """
    
    headers = {
        'User-Agent': 'RoadSoS-IITM-Hackathon-Project/1.0'
    }
    
    try:
        response = requests.get(overpass_url, params={'data': overpass_query}, headers=headers)
        response.raise_for_status() 
        data = response.json()
        return data.get('elements', [])
    except Exception as e:
        st.error(f"API Error: Could not fetch live data. Server says: {e}")
        return []

# --- UI: Streamlit Webpage Setup ---
st.set_page_config(page_title="RoadSoS - Debug & Drive", layout="wide")
st.title("🚑 RoadSoS: Emergency Response System")
st.write("Live tracking of nearest medical centers for rapid SOS dispatch.")

# Set base coordinates (Nashik)
nashik_lat, nashik_lon = 19.9975, 73.7898
m = folium.Map(location=[nashik_lat, nashik_lon], zoom_start=13)

# Add a red marker for the User/Accident location
folium.Marker(
    [nashik_lat, nashik_lon], 
    popup="⚠️ ACCIDENT LOCATION", 
    icon=folium.Icon(color="red", icon="warning-sign")
).add_to(m)

# --- ACTION: Fetch and Plot Data ---
with st.spinner("Fetching live hospital data from OpenStreetMap..."):
    hospitals = get_nearby_hospitals(nashik_lat, nashik_lon)

# Loop through the results and add a blue marker for each hospital
if hospitals:
    for hospital in hospitals:
        name = hospital.get('tags', {}).get('name', 'Unknown Medical Center')
        h_lat = hospital['lat']
        h_lon = hospital['lon']
        
        folium.Marker(
            [h_lat, h_lon],
            popup=f"🏥 {name}",
            icon=folium.Icon(color="blue", icon="plus")
        ).add_to(m)
    st.success(f"Successfully located {len(hospitals)} medical centers within 5km!")
else:
    st.warning("No medical centers found or API is currently busy.")

# Display the map on the screen
st_folium(m, width=1200, height=600)