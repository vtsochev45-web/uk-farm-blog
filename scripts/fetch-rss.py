#!/usr/bin/env python3
"""
RSS Feed Aggregator for UK Farming News
Fetches and stores latest articles from farming sources
"""

import json
import os
import sys
from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET

RSS_SOURCES = {
    "farmers_weekly": {
        "url": "https://www.fwi.co.uk/rss",
        "category": "news"
    },
    "ahdb_cereals": {
        "url": "https://ahdb.org.uk/cereals-oilseeds/news/rss", 
        "category": "crops"
    },
    "ahdb_beef": {
        "url": "https://ahdb.org.uk/beef-lamb/news/rss",
        "category": "livestock"
    },
    "ahdb_dairy": {
        "url": "https://ahdb.org.uk/dairy/news/rss",
        "category": "livestock"
    },
    "nfu": {
        "url": "https://nfuonline.com/news/latest",
        "category": "policy"
    }
}

def fetch_feed(source_id: str, source_config: dict) -> list:
    """Fetch and parse RSS feed"""
    try:
        req = urllib.request.Request(
            source_config['url'],
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        
        # Handle RSS 2.0 and Atom
        items = []
        for item in root.findall('.//item')[:5]:  # Top 5
            title = item.find('title')
            link = item.find('link')
            pubDate = item.find('pubDate') or item.find('.//published')
            
            if title is not None:
                items.append({
                    'title': title.text,
                    'link': link.text if link is not None else '',
                    'date': pubDate.text if pubDate is not None else '',
                    'source': source_id,
                    'category': source_config['category']
                })
        
        return items
    except Exception as e:
        print(f"⚠️ Failed to fetch {source_id}: {e}", file=sys.stderr)
        return []

def main():
    """Fetch all feeds and save"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    all_items = []
    for source_id, config in RSS_SOURCES.items():
        items = fetch_feed(source_id, config)
        all_items.extend(items)
        print(f"✅ {source_id}: {len(items)} items")
    
    # Save to file
    data_file = os.path.join(data_dir, 'rss-news.json')
    with open(data_file, 'w') as f:
        json.dump({
            'fetched_at': datetime.now().isoformat(),
            'total': len(all_items),
            'items': all_items
        }, f, indent=2)
    
    print(f"\n📊 Total items: {len(all_items)}")
    print(f"💾 Saved: {data_file}")

if __name__ == '__main__':
    main()
