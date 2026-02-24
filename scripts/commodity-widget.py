#!/usr/bin/env python3
"""
Commodity Prices Widget
Live UK agricultural commodity prices
"""

import json
import os
from datetime import datetime

# Sample prices (replace with real API calls)
COMMODITIES = {
    "cereals": {
        "wheat_feed": {"price": 165.00, "unit": "£/t", "change": 2.50, "trend": "up"},
        "wheat_milling": {"price": 185.00, "unit": "£/t", "change": 2.00, "trend": "up"},
        "barley_feed": {"price": 155.00, "unit": "£/t", "change": -1.00, "trend": "down"},
        "oats": {"price": 145.00, "unit": "£/t", "change": 0, "trend": "flat"},
    },
    "oilseeds": {
        "rapeseed": {"price": 420.00, "unit": "£/t", "change": 5.00, "trend": "up"},
        "linseed": {"price": 380.00, "unit": "£/t", "change": 0, "trend": "flat"},
    },
    "pulses": {
        "beans": {"price": 220.00, "unit": "£/t", "change": -2.00, "trend": "down"},
        "peas": {"price": 210.00, "unit": "£/t", "change": 1.00, "trend": "up"},
    },
    "livestock": {
        "prime_cattle": {"price": 4.25, "unit": "£/kg", "change": 0.05, "trend": "up"},
        "cull_cows": {"price": 2.80, "unit": "£/kg", "change": -0.02, "trend": "down"},
        "lamb": {"price": 6.50, "unit": "£/kg", "change": 0.15, "trend": "up"},
        "pig": {"price": 1.95, "unit": "£/kg", "change": 0, "trend": "flat"},
    },
    "dairy": {
        "milk_avg": {"price": 0.38, "unit": "£/L", "change": 0.01, "trend": "up"},
        "butter": {"price": 5.20, "unit": "£/kg", "change": 0.10, "trend": "up"},
        "cheddar": {"price": 3.80, "unit": "£/kg", "change": 0.05, "trend": "up"},
    }
}

def fetch_ahdb_prices():
    """
    Fetch real prices from AHDB
    https://ahdb.org.uk/cereals-oilseeds/markets
    """
    # Real implementation would scrape or API call
    # For demo, return sample data
    return COMMODITIES

def generate_price_widget(prices: dict) -> str:
    """Generate HTML price widget"""
    
    html = """<div class="prices-widget">
    <h3>💰 Live Commodity Prices</h3>
    <p class="update-time">Updated: {} | Source: AHDB</p>
    
    <div class="prices-grid">""".format(datetime.now().strftime("%d %b %H:%M"))
    
    for category, items in prices.items():
        html += f"""
        <div class="price-category">
            <h4>{category.replace('_', ' ').title()}</h4>"""
        
        for commodity, data in items.items():
            trend_emoji = "📈" if data['trend'] == 'up' else "📉" if data['trend'] == 'down' else "➡️"
            change_sign = "+" if data['change'] > 0 else ""
            
            html += f"""
            <div class="price-item">
                <span class="name">{commodity.replace('_', ' ').title()}</span>
                <span class="price">£{data['price']:.2f}/{data['unit'].split('/')[-1]}</span>
                <span class="trend {data['trend']}">{trend_emoji} {change_sign}{data['change']:.2f}</span>
            </div>"""
        
        html += "</div>"
    
    html += """
    </div>
    
    <div class="price-chart-link">
        <a href="/prices-history.html">View price charts →</a>
    </div>
</div>

<style>
.prices-widget {
    background: #f0fdf4;
    border: 2px solid #16a34a;
    padding: 1.5rem;
    border-radius: 12px;
}
.prices-widget h3 { color: #166534; margin-top: 0; }
.update-time { color: #666; font-size: 0.9rem; }
.prices-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.price-category {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.price-category h4 {
    color: #166534;
    margin: 0 0 0.75rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #bbf7d0;
}
.price-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #eee;
}
.price-item:last-child { border-bottom: none; }
.price-item .name { flex: 1; }
.price-item .price {
    font-weight: bold;
    font-size: 1.1rem;
    margin-right: 1rem;
}
.price-item .trend { font-size: 0.9rem; }
.trend.up { color: #16a34a; }
.trend.down { color: #dc2626; }
.trend.flat { color: #6b7280; }
.price-chart-link {
    margin-top: 1rem;
    text-align: right;
}
.price-chart-link a {
    color: #166534;
    text-decoration: none;
    font-weight: 500;
}
</style>"""
    
    return html

def main():
    """Generate commodity widget"""
    prices = fetch_ahdb_prices()
    html = generate_price_widget(prices)
    
    output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'prices-widget.html')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"✅ Prices widget generated: {output_file}")
    
    # Save JSON
    json_file = output_file.replace('.html', '.json')
    with open(json_file, 'w') as f:
        json.dump(prices, f, indent=2)
    
    return html

if __name__ == '__main__':
    main()
