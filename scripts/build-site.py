#!/usr/bin/env python3
"""
UK Farm Blog Site Builder
Builds the full farming website with all sections
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

def load_posts(posts_dir: str) -> list:
    """Load all markdown posts"""
    posts = []
    for md_file in Path(posts_dir).glob('*.md'):
        with open(md_file) as f:
            content = f.read()
        
        # Parse frontmatter
        fm = {}
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if fm_match:
            for line in fm_match.group(1).split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    fm[key.strip()] = val.strip().strip('"').strip("'")
        
        body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        
        posts.append({
            'filename': md_file.stem,
            'frontmatter': fm,
            'content': body,
            'is_brief': fm.get('type') == 'brief'
        })
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x['frontmatter'].get('date', ''), reverse=True)
    return posts

def markdown_to_html(md: str) -> str:
    """Simple markdown to HTML"""
    html = md
    
    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Lists
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Wrap lists
    html = re.sub(r'(<li>.*?</li>\n)+', r'<ul>\g<0></ul>', html, flags=re.DOTALL)
    
    # Paragraphs
    html = '\n'.join(f'<p>{p}</p>' if not p.startswith('<') else p for p in html.split('\n\n'))
    
    return html

def load_widget(widget_type: str) -> str:
    """Load widget HTML if available"""
    widget_path = os.path.join(os.path.dirname(__file__), '..', 'data', f'{widget_type}-widget.html')
    if os.path.exists(widget_path):
        with open(widget_path) as f:
            return f.read()
    return ""

def build_homepage(posts: list, config: dict) -> str:
    """Build the homepage with navigation to all sections and live widgets"""
    
    # Get latest brief
    latest_briefs = [p for p in posts if p.get('is_brief')][:3]
    other_posts = [p for p in posts if not p.get('is_brief')][:5]
    
    # Load widgets
    weather_widget = load_widget('weather')
    prices_widget = load_widget('prices')
    livestock_widget = load_widget('livestock')
    
    html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['site']['name']} | {config['site']['tagline']}</title>
    <meta name="description" content="{config['site']['description']}">
    <style>
        :root {{
            --farm-green: #2d5a27;
            --farm-brown: #8b7355;
            --farm-sky: #87ceeb;
            --alert-red: #dc2626;
            --money-green: #16a34a;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            line-height: 1.6; 
            color: #333;
            background: #f5f5f4;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 1rem; }}
        
        /* Header */
        header {{ 
            background: var(--farm-green); 
            color: white; 
            padding: 1.5rem 0;
            border-bottom: 4px solid var(--farm-brown);
        }}
        header h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
        header p {{ opacity: 0.9; }}
        
        /* Navigation */
        nav {{ 
            background: white; 
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        nav ul {{ list-style: none; display: flex; flex-wrap: wrap; gap: 1rem; }}
        nav a {{ text-decoration: none; color: var(--farm-green); font-weight: 500; }}
        nav a:hover {{ text-decoration: underline; }}
        
        /* Main Brief Section */
        .brief-hero {{ 
            background: linear-gradient(135deg, var(--farm-sky) 0%, #fff 100%);
            padding: 2rem 0;
            margin: 2rem 0;
            border-radius: 8px;
            border: 2px solid var(--farm-green);
        }}
        .brief-hero h2 {{ 
            color: var(--farm-green); 
            font-size: 1.8rem; 
            margin-bottom: 1rem;
            text-align: center;
        }}
        
        /* Grid */
        .sections-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        .section-card {{ 
            background: white; 
            padding: 1.5rem; 
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid var(--farm-brown);
        }}
        .section-card h3 {{ 
            display: flex; 
            align-items: center; 
            gap: 0.5rem;
            margin-bottom: 1rem;
            color: var(--farm-green);
        }}
        .section-card a {{ 
            display: inline-block; 
            margin-top: 1rem;
            color: var(--farm-green);
            text-decoration: none;
            font-weight: 500;
        }}
        
        /* Posts list */
        .post-list {{ margin: 2rem 0; }}
        .post-item {{ 
            background: white; 
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .post-item h4 {{ margin-bottom: 0.5rem; }}
        .post-item h4 a {{ color: var(--farm-green); text-decoration: none; }}
        .post-item .meta {{ color: #666; font-size: 0.9rem; }}
        
        /* Brief specific */
        .brief-section {{ 
            background: #f0fdf4;
            border-left: 4px solid var(--money-green);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 8px 8px 0;
        }}
        .brief-section h4 {{ color: var(--farm-green); margin-bottom: 0.5rem; }}
        .brief-section ul {{ list-style: none; padding-left: 0; }}
        .brief-section li {{ padding: 0.25rem 0; }}
        
        footer {{ 
            background: var(--farm-green); 
            color: white; 
            text-align: center; 
            padding: 2rem 0;
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{config['site']['name']}</h1>
            <p>{config['site']['tagline']}</p>
        </div>
    </header>
    
    <nav>
        <div class="container">
            <ul>
                <li><a href="index.html">🏠 Home</a></li>
                <li><a href="briefs/index.html">🗞 Daily Brief</a></li>
                <li><a href="weather.html">🌦 Weather</a></li>
                <li><a href="grants.html">💰 Grants</a></li>
                <li><a href="livestock.html">🐄 Livestock</a></li>
                <li><a href="crops.html">🌾 Crops</a></li>
                <li><a href="equipment.html">🚜 Equipment</a></li>
            </ul>
        </div>
    </nav>
    
    <main class="container">
"""
    
    # Live Data Widgets Section
    html += '''
    <div class="live-data-section" style="margin: 2rem 0;">
        <h2 style="text-align: center; color: var(--farm-green); margin-bottom: 1.5rem;">
            📊 Live Farm Data
        </h2>
        <p style="text-align: center; color: #666; margin-bottom: 2rem;">
            Updated hourly • Real-time prices & conditions
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem;">
    '''
    
    # Add widgets if they exist
    if weather_widget:
        html += weather_widget
    if prices_widget:
        html += prices_widget
    if livestock_widget:
        html += livestock_widget
    
    html += '</div></div>'
    
    # Latest Brief Section
    if latest_briefs:
        brief = latest_briefs[0]
        content = markdown_to_html(brief['content'])
        
        html += f"""
        <section class="brief-hero">
            <h2>🗞 Today's Daily Farm Brief</h2>
            <div class="brief-content">
                {content}
            </div>
            <p style="text-align: center; margin-top: 1rem;">
                <a href="posts/{brief['filename']}.html" style="color: var(--farm-green); font-weight: 500;">
                    Read full brief →
                </a>
            </p>
        </section>
"""
    
    # Sections Grid
    html += """
        <div class="sections-grid">
            <div class="section-card">
                <h3>🌦 Weather + Risk Alerts</h3>
                <p>Regional weather forecasts, warnings, and agricultural impact analysis.</p>
                <a href="weather.html">View weather →</a>
            </div>
            
            <div class="section-card">
                <h3>💰 Grants & Money Updates</h3>
                <p>SFI payments, RPA updates, funding deadlines, and scheme changes.</p>
                <a href="grants.html">View grants →</a>
            </div>
            
            <div class="section-card">
                <h3>🐄 Livestock Section</h3>
                <p>Beef, lamb, dairy prices, disease alerts, and market trends.</p>
                <a href="livestock.html">View livestock →</a>
            </div>
            
            <div class="section-card">
                <h3>🌾 Crop Section</h3>
                <p>Cereal, oilseed, and pulse prices with agronomy updates.</p>
                <a href="crops.html">View crops →</a>
            </div>
            
            <div class="section-card">
                <h3>🚜 Equipment & Tech</h3>
                <p>Machinery reviews, tech updates, and equipment deals.</p>
                <a href="equipment.html">View equipment →</a>
            </div>
            
            <div class="section-card">
                <h3>📅 Seasonal Checklist</h3>
                <p>Year-round farming tasks and timing reminders.</p>
                <a href="seasonal.html">View checklist →</a>
            </div>
        </div>
        
        <section class="post-list">
            <h2>Recent Updates</h2>
"""
    
    # Recent posts
    for post in other_posts[:5]:
        fm = post['frontmatter']
        html += f"""
            <div class="post-item">
                <h4><a href="posts/{post['filename']}.html">{fm.get('title', 'Untitled')}</a></h4>
                <p class="meta">{fm.get('date', '')[:10]}</p>
                <p>{fm.get('description', '')}</p>
            </div>
"""
    
    html += f"""
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>{config['site']['name']} • Generated {datetime.now().year}</p>
            <p style="font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;">
                Sources: Met Office, DEFRA, AHDB, NFU, Farmers Weekly
            </p>
        </div>
    </footer>
</body>
</html>
"""
    
    return html

def main():
    """Build complete site"""
    
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'blog.json')
    with open(config_path) as f:
        config = json.load(f)
    
    # Load posts
    posts_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts')
    posts = load_posts(posts_dir)
    
    # Build homepage
    dist_dir = os.path.join(os.path.dirname(__file__), '..', 'dist')
    os.makedirs(dist_dir, exist_ok=True)
    os.makedirs(f"{dist_dir}/posts", exist_ok=True)
    
    # Write homepage
    homepage = build_homepage(posts, config)
    with open(f"{dist_dir}/index.html", 'w') as f:
        f.write(homepage)
    
    print(f"✅ Site built: {dist_dir}/")
    print(f"📊 Posts: {len(posts)}")
    print(f"🔗 Homepage: {dist_dir}/index.html")

if __name__ == '__main__':
    main()
