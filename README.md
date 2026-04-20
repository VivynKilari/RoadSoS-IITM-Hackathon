# 🚑 RoadSoS: AI-Powered Emergency Response System

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=leaflet&logoColor=white)
![Deployed](https://img.shields.io/badge/Deployed-Live-success?style=for-the-badge)

RoadSoS is an intelligent, real-time dispatch dashboard designed to optimize emergency medical response times. By combining Natural Language Processing (NLP) with dynamic geospatial routing, RoadSoS ensures the right resources reach the right locations—faster. 

Built for the **IITM Hackathon**.

---

## 🚀 Live Demo
**[Click here to view the live application!](YOUR_STREAMLIT_URL_HERE)** *(Note: If the public mapping API is congested, the app will automatically switch to an offline failsafe mode to ensure uninterrupted demonstrations).*

---

## ⚠️ The Problem
In medical emergencies, the "Golden Hour" dictates that rapid intervention drastically increases survival rates. However, traditional dispatch systems often suffer from:
1. Subjective human evaluation of emergency severity.
2. Delays in manually cross-referencing accident locations with the nearest available medical centers.
3. System failures when mapping servers go down.

## 💡 The Solution
RoadSoS automates and optimizes the dispatch workflow:
* **Instant Triage:** An AI engine reads the incident description and automatically classifies the severity (Code Red vs. Code Yellow).
* **Automated Dispatch:** Based on the severity, the system determines the appropriate vehicle (Advanced Life Support vs. Basic Life Support).
* **Smart Geospatial Routing:** Calculates the absolute shortest mathematical distance to the nearest verified medical center and maps the rescue vector.

---

## ✨ Core Features

### 🧠 1. AI Severity Analyzer (NLP)
* Uses a Rule-Based NLP engine to scan dispatcher text for critical trauma keywords.
* Dynamically updates UI statuses and map routing colors based on the assessed threat level.

### 🗺️ 2. Smart Routing Engine
* Utilizes the **Haversine formula** to calculate exact Earth-surface distances between the accident site and all surrounding hospitals.
* Visually draws a targeted rescue vector (dashed line) to the absolute closest facility.

### 📡 3. Live OpenStreetMap Integration
* Fetches real-time hospital and clinic coordinates within a specific radius using the **Overpass API**.

### 🛡️ 4. Failsafe Offline Mode
* Hackathon-proof architecture: If the public Overpass API times out or fails during high-traffic events, the system instantly catches the error and falls back to a locally cached JSON dataset of medical centers.

---

## 🛠️ Technical Architecture

* **Frontend / UI:** Streamlit (Python)
* **Map Rendering:** Folium, Streamlit-Folium
* **Data Fetching:** Python `requests`, Overpass API (OpenStreetMap JSON)
* **Mathematical Routing:** Python `math` module
* **Deployment:** Streamlit Community Cloud

---

## 💻 How to Run Locally

To run this project on your own machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/RoadSoS-IITM-Hackathon.git](https://github.com/YOUR_GITHUB_USERNAME/RoadSoS-IITM-Hackathon.git)
   cd RoadSoS-IITM-Hackathon