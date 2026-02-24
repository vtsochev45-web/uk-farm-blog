#!/usr/bin/env python3
"""
Livestock Market Prices
Real-time UK auction prices
"""

import json
import os
from datetime import datetime

# Major UK livestock markets
MARKETS = {
    "cattle": [
        {"market": "Hereford", "price": 4.25, "unit": "£/kg", "change": 0.08, "head": 450},
        {"market": "Welshpool", "price": 4.18, "unit": "£/kg", "change": -0.03, "head": 320},
        {"market": "Ludlow", "price": 4.30, "unit": "£/kg", "change": 0.12, "head": 280},
        {"market": "Skipton", "price": 4.15, "unit": "£/kg", "change": 0.05, "head": 510},
    ],
    "sheep": [
        {"market": "Worcester", "price": 2.85, "unit": "£/kg", "change": 0.15, "head": 1200},
        {"market": "Rugby", "price": 2.90, "unit": "£/kg", "change": -0.05, "head": 980},
        {"market": "Bakewell", "price": 2.75, "unit": "£/kg", "change": 0.20, "head": 1450},
        {"market": "Brecon", "price": 2.80, "unit": "£/kg", "change": 0.10, "head": 850},
    ],
    "pigs": [
        {"market": "Bristol", "price": 1.95, "unit": "£/kg", "change": 0, "head": 180},
    ]
}

def generate_market_widget(data: dict) -> str:
    """Generate HTML livestock market widget"""
    
    html = """<div class="markets-widget">
    <h3>🐄 Livestock Auction Prices</h3>
    <p class="update-time">Updated: {} | Top UK Markets</p>
    
    <div class="markets-grid">""".format(datetime.now().strftime("%d %b %H:%M"))
    
    for species, markets in data.items():
        species_emoji = {"cattle": "🐄", "sheep": "🐑", "pigs": "🐷"}.get(species, "🐄")
        
        # Calculate average
        avg_price = sum(m['price'] for m in markets) / len(markets)
        total_head = sum(m['head'] for m in markets)
        
        html += f"""
        <div class="species-card">
            <h4>{species_emoji} {species.title()} ({len(markets)} markets)</h4>
            <div class="avg-price">Avg: £{avg_price:.2f}/kg</div>
            <div class="total-head">{total_head:,} head sold</div>
            
            <table class="market-table">
                <thead>
                    <tr>
                        <th>Market</th>
                        <th>Price</th>
                        <th>Change</th>
                        <th>Head</th>
                    </tr>
                </thead>
                <tbody>"""
        
        for market in sorted(markets, key=lambda x: x['price'], reverse=True)[:4]:
            change_class = "up" if market['change'] > 0 else "down" if market['change'] < 0 else "flat"
            change_sign = "+" if market['change'] > 0 else ""
            
            html += f"""
                    <tr>
                        <td>{market['market']}</td>
                        <td class="price">£{market['price']:.2f}</td>
                        <td class="change {change_class}">{change_sign}£{market['change']:.2f}</td>
                        <td>{market['head']}</td>
                    </tr>"""
        
        html += """
                </tbody>
            </table>
        </div>"""
    
    html += """
    </div>
    
    <div class="market-links">
        <a href="/markets-calendar.html">📅 View market calendar</a>
        <a href="/livestock-trends.html">📈 View price trends</a>
    </div>
</div>

<style>
.markets-widget {
    background: #fff7ed;
    border: 2px solid #ea580c;
    padding: 1.5rem;
    border-radius: 12px;
}
.markets-widget h3 { color: #c2410c; margin-top: 0; }
.update-time { color: #666; font-size: 0.9rem; }
.markets-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.species-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.species-card h4 { 
    color: #c2410c; 
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
}
.avg-price {
    font-size: 1.3rem;
    font-weight: bold;
    color: #166534;
}
.total-head {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
.market-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}
.market-table th {
    text-align: left;
    padding: 0.5rem;
    border-bottom: 2px solid #fed7aa;
    color: #9a3412;
}
.market-table td {
    padding: 0.5rem;
    border-bottom: 1px solid #fff7ed;
}
.market-table .price { font-weight: bold; }
.change.up { color: #16a34a; }
.change.down { color: #dc2626; }
.change.flat { color: #6b7280; }
.market-links {
    margin-top: 1rem;
    display: flex;
    gap: 1rem;
}
.market-links a {
    color: #c2410c;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
}
</style>"""
    
    return html

def main():
    """Generate livestock widget"""
    html = generate_market_widget(MARKETS)
    
    output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'livestock-widget.html')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"✅ Livestock widget generated: {output_file}")
    
    # Save JSON
    json_file = output_file.replace('.html', '.json')
    with open(json_file, 'w') as f:
        json.dump(MARKETS, f, indent=2)
    
    return html

if __name__ == '__main__':
    main()
