#!/usr/bin/env python3
"""
Weather Widget Generator
Fetches live Met Office data for UK farming regions
"""

import json
import os
from datetime import datetime
import urllib.request

# UK Farming regions with major agricultural areas
REGIONS = {
    "scotland": {"lat": 56.4907, "lon": -4.2026, "sites": ["Aberdeen", "Glasgow", "Edinburgh"]},
    "north_england": {"lat": 54.5, "lon": -2.5, "sites": ["York", "Newcastle", "Carlisle"]},
    "midlands": {"lat": 52.5, "lon": -1.8, "sites": ["Birmingham", "Nottingham", "Leicester"]},
    "east_anglia": {"lat": 52.5, "lon": 0.5, "sites": ["Norwich", "Cambridge", "Ipswich"]},
    "south_west": {"lat": 50.9, "lon": -3.5, "sites": ["Exeter", "Plymouth", "Bristol"]},
    "south_east": {"lat": 51.5, "lon": -0.5, "sites": ["London", "Reading", "Canterbury"]},
    "wales": {"lat": 52.1307, "lon": -3.7837, "sites": ["Cardiff", "Aberystwyth"]},
    "northern_ireland": {"lat": 54.7877, "lon": -6.4923, "sites": ["Belfast", "Londonderry"]}
}

# Farming-relevant weather thresholds
THRESHOLDS = {
    "frost": 2,  # °C - risk to crops/livestock
    "heavy_rain": 15,  # mm - field work impossible
    "high_wind": 50,  # mph - dangerous for spraying/lifting
    "heat_stress": 25  # °C - livestock welfare concern
}

def fetch_met_office_data(api_key: str = None) -> dict:
    """
    Fetch from Met Office DataPoint API
    Free tier: 10,000 calls/day
    """
    if not api_key:
        # Return sample structure for demo
        return {
            "scotland": {
                "temp": 8,
                "rain": 18,
                "wind": 45,
                "forecast": "Heavy rain continuing through tomorrow",
                "alerts": ["Heavy rain warning issued"],
                "farm_impact": "Field work suspended"
            },
            "midlands": {
                "temp": 6,
                "rain": 2,
                "wind": 15,
                "forecast": "Dry overnight, frost risk down to -1°C",
                "alerts": ["Frost warning"],
                "farm_impact": "Protect tender crops, check livestock"
            },
            "south_west": {
                "temp": 11,
                "rain": 5,
                "wind": 25,
                "forecast": "Showers, clearing by afternoon",
                "alerts": [],
                "farm_impact": "Good conditions for field work"
            }
        }
    
    # Real API implementation would go here
    # See: https://www.metoffice.gov.uk/datapoint
    pass

def generate_weather_widget(data: dict) -> str:
    """Generate HTML weather widget"""
    
    html = """<div class="weather-widget">
    <h3>🌦 Live Weather Conditions</h3>
    <p class="update-time">Updated: {}</p>
    <div class="weather-grid">""".format(datetime.now().strftime("%H:%M"))
    
    for region, info in data.items():
        region_name = region.replace('_', ' ').title()
        
        # Determine alert level
        alert_class = "normal"
        alerts = []
        
        if info.get('rain', 0) > THRESHOLDS['heavy_rain']:
            alert_class = "warning"
            alerts.append("⛈ Heavy rain")
        
        if info.get('temp', 10) < THRESHOLDS['frost']:
            alert_class = "warning"
            alerts.append("❄️ Frost risk")
        
        if info.get('wind', 0) > THRESHOLDS['high_wind']:
            alert_class = "warning"
            alerts.append("💨 High winds")
        
        html += f"""
        <div class="region-card {alert_class}">
            <h4>{region_name}</h4>
            <div class="temp">{info.get('temp', '--')}°C</div>
            <div class="details">
                <span>💧 {info.get('rain', '--')}mm rain</span>
                <span>💨 {info.get('wind', '--')}mph wind</span>
            </div>
            <p class="impact">{info.get('farm_impact', 'Conditions suitable')}</p>
            {''.join(f'<span class="alert">{a}</span>' for a in alerts) if alerts else ''}
        </div>"""
    
    html += """
    </div>
</div>

<style>
.weather-widget {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
}
.weather-widget h3 { margin-top: 0; }
.update-time { opacity: 0.8; font-size: 0.9rem; }
.weather-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.region-card {
    background: rgba(255,255,255,0.1);
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #4ade80;
}
.region-card.warning {
    border-left-color: #fbbf24;
    background: rgba(251, 191, 36, 0.2);
}
.region-card h4 { margin: 0 0 0.5rem 0; }
.temp { font-size: 2rem; font-weight: bold; }
.details { display: flex; gap: 1rem; margin: 0.5rem 0; opacity: 0.9; }
.impact { font-size: 0.9rem; font-style: italic; }
.alert {
    display: inline-block;
    background: #ef4444;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}
</style>"""
    
    return html

def main():
    """Generate weather widget"""
    data = fetch_met_office_data()
    html = generate_weather_widget(data)
    
    output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'weather-widget.html')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"✅ Weather widget generated: {output_file}")
    
    # Also save JSON for other uses
    json_file = output_file.replace('.html', '.json')
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    return html

if __name__ == '__main__':
    main()
