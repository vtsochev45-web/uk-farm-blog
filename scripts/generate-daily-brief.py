#!/usr/bin/env python3
"""
UK Farm Daily Brief Generator
Creates the flagship 'Daily 3-Minute Farm Brief'
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List

def load_sources() -> Dict:
    """Load RSS sources and API keys"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'blog.json')
    with open(config_path) as f:
        return json.load(f)

def fetch_weather_risk() -> List[Dict]:
    """Fetch weather warnings for UK regions"""
    # TODO: Integrate Met Office API
    # For now, return placeholder structure
    return [
        {"region": "Scotland", "risk": "Heavy rain expected", "severity": "medium", "emoji": "🌧"},
        {"region": "England", "risk": "Frost overnight", "severity": "low", "emoji": "❄️"}
    ]

def fetch_grant_updates() -> List[Dict]:
    """Check for new grant announcements"""
    # TODO: Scrape gov.uk/DEFRA
    return [
        {"scheme": "SFI", "update": "Payment schedule changes announced", "deadline": None, "emoji": "💰"}
    ]

def fetch_livestock_alerts() -> List[Dict]:
    """Check livestock disease alerts, market prices"""
    # TODO: AHDB beef/sheep prices + DEFRA disease alerts
    return [
        {"type": "disease", "alert": "New foot-and-mouth monitoring notice", "region": "UK-wide", "emoji": "🐄"}
    ]

def fetch_crop_updates() -> List[Dict]:
    """Check crop disease, markets"""
    # TODO: AHDB cereal/oilseed prices
    return [
        {"crop": "Wheat", "price": "£XXX/t", "trend": "up", "emoji": "🌾"}
    ]

def fetch_equipment_deals() -> List[Dict]:
    """Check equipment deals"""
    # TODO: Pull from farming press
    return [
        {"item": "Fencing tools", "deal": "20% discount", "source": "Equipment supplier", "emoji": "🚜"}
    ]

def fetch_policy_updates() -> List[Dict]:
    """Check policy/regulatory changes"""
    # TODO: NFU/defra feeds
    return []

def fetch_market_prices() -> List[Dict]:
    """Key market price movements"""
    # TODO: AHDB prices
    return []

def generate_brief(date: datetime = None) -> Dict:
    """Generate the full daily brief"""
    
    if date is None:
        date = datetime.now()
    
    sources = load_sources()
    config = sources.get('brief', {})
    emoji = config.get('emoji', {})
    
    # Collect all updates
    weather = fetch_weather_risk()
    grants = fetch_grant_updates()
    livestock = fetch_livestock_alerts()
    crops = fetch_crop_updates()
    equipment = fetch_equipment_deals()
    policy = fetch_policy_updates()
    prices = fetch_market_prices()
    
    # Build brief sections
    sections = []
    
    # Weather Section
    if weather:
        weather_items = []
        for w in weather[:3]:  # Max 3
            weather_items.append(f"{w['emoji']} **{w['region']}**: {w['risk']}")
        sections.append({
            "title": "Weather Risk",
            "items": weather_items,
            "emoji": emoji.get('weather', '🌧')
        })
    
    # Grants Section
    if grants:
        grant_items = []
        for g in grants[:3]:
            deadline_text = f" (Deadline: {g['deadline']})" if g.get('deadline') else ""
            grant_items.append(f"{g['emoji']} **{g['scheme']}**: {g['update']}{deadline_text}")
        sections.append({
            "title": "Grant Update",
            "items": grant_items,
            "emoji": emoji.get('grants', '💰')
        })
    
    # Livestock Section
    if livestock:
        livestock_items = []
        for l in livestock[:3]:
            livestock_items.append(f"{l['emoji']} **{l['type'].title()} Alert**: {l['alert']}")
        sections.append({
            "title": "Livestock Alert",
            "items": livestock_items,
            "emoji": emoji.get('livestock', '🐄')
        })
    
    # Equipment Deals
    if equipment:
        equip_items = []
        for e in equipment[:3]:
            equip_items.append(f"{e['emoji']} **{e['item']}**: {e['deal']}")
        sections.append({
            "title": "Equipment Deal",
            "items": equip_items,
            "emoji": emoji.get('equipment', '🚜')
        })
    
    # Policy
    if policy:
        policy_items = [f"{p['emoji']} {p['update']}" for p in policy[:3]]
        sections.append({
            "title": "Policy Update",
            "items": policy_items,
            "emoji": emoji.get('policy', '📋')
        })
    
    # Prices
    if prices:
        price_items = [f"{p['emoji']} **{p['item']}**: {p['price']}" for p in prices[:3]]
        sections.append({
            "title": "Market Prices",
            "items": price_items,
            "emoji": emoji.get('prices', '💹')
        })
    
    return {
        "date": date.strftime("%A, %-d %B %Y"),
        "title": f"Daily Farm Brief – {date.strftime('%d %B %Y')}",
        "sections": sections,
        "count": len(sections)
    }

def format_markdown(brief: Dict) -> str:
    """Format brief as clean markdown"""
    
    lines = [
        f"---",
        f"title: \"{brief['title']}\"",
        f"date: {datetime.now().isoformat()}",
        f"description: \"Daily farming updates: weather, grants, livestock, crops, and equipment\"",
        f"tags: [\"daily-brief\", \"uk-farming\", \"agriculture-news\"]",
        f"type: brief",
        f"---",
        f"",
        f"# 📰 Daily Farm Brief – {brief['date']}",
        f"",
        f"> Your 3-minute roundup of today's important farming updates.",
        f"",
        f"---",
        f""
    ]
    
    for section in brief['sections']:
        lines.append(f"## {section['emoji']} {section['title']}")
        lines.append("")
        for item in section['items']:
            lines.append(f"- {item}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*Generated by AI • Sources: Met Office, DEFRA, AHDB, NFU, Farmers Weekly*")
    
    return "\n".join(lines)

def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate UK Farm Daily Brief')
    parser.add_argument('--output', default='../content/posts', help='Output directory')
    parser.add_argument('--date', help='Specific date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # Parse date if provided
    date = None
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    
    # Generate brief
    brief = generate_brief(date)
    
    # Format as markdown
    md_content = format_markdown(brief)
    
    # Save file
    output_dir = os.path.join(os.path.dirname(__file__), args.output)
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{datetime.now().strftime('%Y-%m-%d')}-daily-brief.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(md_content)
    
    print(f"✅ Daily Brief generated: {filepath}")
    print(f"📊 Sections: {brief['count']}")
    print(f"\n📝 Preview:\n")
    print(md_content[:500] + "...")

if __name__ == '__main__':
    main()
