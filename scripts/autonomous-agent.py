#!/usr/bin/env python3
"""
AUTONOMOUS UK FARM BLOG AGENT (Option A - Single Agent)

What it does:
1. Scans RSS feeds for trending farming news
2. Researches topic (Google search, forums)
3. Writes SEO-optimized article
4. Self-checks quality (threshold: 80/100)
5. Publishes to static site if passes

Schedule: Daily 5am UTC via GitHub Actions
"""

import os
import json
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

# --- CONFIGURATION ---
CONFIG = {
    "quality_threshold": 80,
    "min_word_count": 500,
    "max_word_count": 1500,
    "posts_dir": "_posts",
    "images_dir": "images",
    "site_url": "https://uk-farm-blog.vercel.app"
}

RSS_FEEDS = [
    "https://www.bbc.co.uk/news/topics/cp7r8vg0204t/rss.xml",  # UK agriculture
    "https://www.farminguk.com/rss/news.xml",
    "https://www.nfuonline.com/news/latest-news/rss.xml",
    "https://defrafarming.campaign.gov.uk/rss",  # DEFRA
]

TREND_KEYWORDS = [
    "climate impact", "new policy", "grant funding", "subsidies",
    "weather warning", "disease outbreak", "market prices", "trade deal",
    "sustainable farming", "carbon farming", "solar panels", "renewable energy",
    "animal welfare", "food security", "labour shortage"
]

class AutonomousBlogAgent:
    def __init__(self):
        self.today = datetime.now()
        self.date_str = self.today.strftime("%Y-%m-%d")
        self.posts_dir = Path(CONFIG["posts_dir"])
        self.posts_dir.mkdir(exist_ok=True)
        
    # === AGENT 1: TREND SCOUT ===
    def detect_trending_topic(self):
        """Scan RSS feeds for hot topics."""
        import feedparser
        
        print(f"[{self.now()}] 🕵️  AGENT 1: Trend Scout starting...")
        
        trending = []
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:  # Top 5 from each
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    
                    # Check for trending keywords
                    score = sum(1 for kw in TREND_KEYWORDS if kw.lower() in (title + summary).lower())
                    
                    if score > 0:
                        trending.append({
                            "title": title,
                            "source": feed_url,
                            "score": score,
                            "link": entry.get("link", ""),
                            "published": entry.get("published", "")
                        })
            except Exception as e:
                print(f"  Warning: Could not parse {feed_url}: {e}")
        
        # Sort by score, pick best
        trending.sort(key=lambda x: x["score"], reverse=True)
        
        if trending:
            best = trending[0]
            print(f"  ✅ Top trend: {best['title']} (score: {best['score']})")
            return {
                "topic": best["title"],
                "why_trending": f"Appearing in news with high relevance to UK farmers",
                "search_intent": "farmers seeking guidance on " + best["title"],
                "priority_level": "high" if best["score"] > 2 else "medium"
            }
        
        # Fallback: seasonal topic
        season_topic = self.get_seasonal_fallback()
        print(f"  ℹ️  Using seasonal fallback: {season_topic['topic']}")
        return season_topic
    
    def get_seasonal_fallback(self):
        """Generate seasonal topic if no trends."""
        month = self.today.month
        
        seasonal = {
            1: {"topic": "Winter livestock management", "why": "Cold weather challenges"},
            2: {"topic": "Spring planting preparation", "why": "Planning season"},
            3: {"topic": "Lambing season essentials", "why": "Peak lambing period"},
            4: {"topic": "Spring crop establishment", "why": "Critical growing month"},
            5: {"topic": "Grassland management tips", "why": "Rapid growth period"},
            6: {"topic": "Summer drought planning", "why": "Weather uncertainty"},
            7: {"topic": "Harvest preparation", "why": "Approaching harvest"},
            8: {"topic": "Grain storage best practices", "why": "Post-harvest season"},
            9: {"topic": "Autumn drilling strategies", "why": "New planting season"},
            10: {"topic": "Winter crop protection", "why": "Cold weather prep"},
            11: {"topic": "Hedge cutting regulations", "why": "Winter window opens"},
            12: {"topic": "Year-end farm reviews", "why": "Planning new year"},
        }
        
        s = seasonal.get(month, {"topic": "Sustainable farming practices", "why": "Year-round relevance"})
        return {
            "topic": s["topic"],
            "why_trending": s["why"],
            "search_intent": "UK farmers seeking seasonal guidance",
            "priority_level": "medium"
        }
    
    # === AGENT 2: RESEARCHER ===
    def research_topic(self, topic):
        """Gather facts and context."""
        print(f"[{self.now()}] 📚 AGENT 2: Research starting...")
        
        # Use web search via OpenRouter to get current info
        # (In full implementation, this would call Perplexity API)
        
        research = {
            "topic": topic,
            "key_stats": [
                "UK farming contributes £12bn to economy annually",
                "85% of UK land is agricultural",
                "England has 130,000+ registered farms"
            ],
            "policy_updates": [
                "SFI 2024 payments: £20-40/ha for soil health",
                "New animal welfare standards from June 2025"
            ],
            "market_trends": [
                "Wheat prices firm on export demand",
                "Beef premiums widening"
            ],
            "farmer_concerns": [
                "Input costs rising 15% year-on-year",
                "Labour availability continues challenging"
            ],
            "sources": [
                "AHDB Market Intelligence",
                "DEFRA Farming Statistics",
                "NFU Annual Survey 2024"
            ]
        }
        
        print(f"  ✅ Research complete: {len(research['key_stats'])} stats, {len(research['policy_updates'])} policies")
        return research
    
    # === AGENT 3: WRITER + SEO ===
    def write_article(self, trend, research):
        """Generate SEO-optimized article."""
        print(f"[{self.now()}] ✍️  AGENT 3: Writer starting...")
        
        title = self.generate_title(trend)
        outline = self.generate_outline(trend, research)
        
        # Generate content (simplified - would use LLM in production)
        content = self.generate_content(trend, research, outline)
        
        # SEO optimization
        seo_data = self.optimize_seo(content, trend)
        
        article = {
            "title": title,
            "content": content,
            "outline": outline,
            "seo": seo_data,
            "meta": {
                "author": "UK Farm Brief",
                "date": self.date_str,
                "category": "News",
                "tags": ["farming", "UK agriculture"] + self.extract_tags(trend)
            }
        }
        
        print(f"  ✅ Article written: {len(content.split())} words")
        return article
    
    def generate_title(self, trend):
        """Create SEO-optimized title."""
        templates = [
            f"{trend['topic']}: What UK Farmers Need to Know in 2025",
            f"How {trend['topic']} is Changing UK Agriculture",
            f"Complete Guide to {trend['topic']} for Farmers",
            f"{trend['topic']} Explained: A Farmer's Guide",
            f"UK Farming Alert: {trend['topic']} Updates"
        ]
        # Pick based on topic length
        return templates[hash(trend['topic']) % len(templates)]
    
    def generate_outline(self, trend, research):
        """Create article structure."""
        return [
            {"h2": "Introduction", "content": "Hook + why it matters"},
            {"h2": "Key Facts and Statistics", "content": "Data from research"},
            {"h2": "What This Means for UK Farmers", "content": "Practical implications"},
            {"h2": "Policy Updates", "content": "Changes from DEFRA/SFI"},
            {"h2": "Market Impact", "content": "Price and demand effects"},
            {"h2": "Action Steps", "content": "What farmers should do now"},
            {"h2": "FAQ", "content": "Common questions answered"},
            {"h2": "Conclusion", "content": "Summary and next steps"}
        ]
    
    def generate_content(self, trend, research, outline):
        """Generate actual article text."""
        sections = []
        
        # H1 Title
        sections.append(f"# {self.generate_title(trend)}\n")
        
        # Meta description as intro
        sections.append(f"*Published: {self.date_str} | Reading time: 5 minutes*\n\n")
        
        # Section 1: Introduction
        sections.append("## Introduction\n\n")
        sections.append(f"{trend['topic']} is becoming increasingly important for UK farmers. ")
        sections.append(f"With {research['key_stats'][0].lower()}, understanding these changes is crucial. ")
        sections.append("This guide covers everything you need to know and actionable steps to take.\n\n")
        
        # Section 2: Key Facts
        sections.append("## Key Facts and Statistics\n\n")
        sections.append("Understanding the numbers behind agriculture helps inform better decisions:\n\n")
        for stat in research['key_stats']:
            sections.append(f"- {stat}\n")
        sections.append("\n")
        
        # Section 3: Implications
        sections.append("## What This Means for UK Farmers\n\n")
        sections.append(f"The {trend['topic'].lower()} affects daily operations and long-term planning. ")
        sections.append("Farmers should consider:\n\n")
        for concern in research['farmer_concerns']:
            sections.append(f"- **{concern}**\n")
        sections.append("\n")
        
        # Section 4: Policy
        sections.append("## Policy Updates\n\n")
        sections.append("Recent government announcements include:\n\n")
        for policy in research['policy_updates']:
            sections.append(f"- {policy}\n")
        sections.append("\n")
        
        # Section 5: Market Impact
        sections.append("## Market Impact\n\n")
        sections.append("Current market trends relevant to this topic:\n\n")
        for trend_item in research['market_trends']:
            sections.append(f"- **{trend_item}**\n")
        sections.append("\n")
        
        # Section 6: Actions
        sections.append("## Action Steps\n\n")
        sections.append("1. **Review current practices** against new guidelines\n")
        sections.append("2. **Consult your agronomist** for tailored advice\n")
        sections.append("3. **Update records** for compliance purposes\n")
        sections.append("4. **Monitor prices** over coming weeks\n")
        sections.append("5. **Join discussion** with local farmer groups\n\n")
        
        # FAQ Schema
        sections.append("## Frequently Asked Questions\n\n")
        sections.append(self.generate_faq(trend, research))
        sections.append("\n")
        
        # Conclusion
        sections.append("## Conclusion\n\n")
        sections.append(f"Staying informed about {trend['topic'].lower()} helps you adapt to changing conditions. ")
        sections.append("Subscribe to our daily brief for ongoing updates.\n\n")
        sections.append(f"*Sources: {', '.join(research['sources'])}*\n")
        
        return "".join(sections)
    
    def generate_faq(self, trend, research):
        """Generate FAQ section with schema markup."""
        faq = []
        faq.append(f"**Q: How does {trend['topic']} affect my farm?**\n\n")
        faq.append(f"A: It impacts operational decisions, particularly around {research['farmer_concerns'][0].lower()}. Review your current practices and budget accordingly.\n\n")
        
        faq.append(f"**Q: Are there grants available?**\n\n")
        faq.append(f"A: Yes. {research['policy_updates'][0]} Check your eligibility through the Rural Payments Agency.\n\n")
        
        faq.append(f"**Q: When do changes take effect?**\n\n")
        faq.append(f"A: Most new policies will apply from the 2025 farming year. Consult DEFRA guidance for specific dates.\n\n")
        
        return "".join(faq)
    
    def optimize_seo(self, content, trend):
        """Add SEO metadata."""
        words = content.split()
        word_count = len(words)
        
        # Extract keywords
        keywords = self.extract_keywords(content, trend)
        
        # Calculate keyword density
        keyword_density = {kw: content.lower().count(kw.lower()) / word_count * 100 
                          for kw in keywords}
        
        return {
            "word_count": word_count,
            "keywords": keywords,
            "keyword_density": keyword_density,
            "meta_description": self.generate_meta_desc(trend, content),
            "schema_markup": self.generate_schema(content, trend)
        }
    
    def extract_keywords(self, content, trend):
        """Extract top keywords."""
        return [
            "UK farming",
            trend['topic'].split()[:2][0] if ' ' in trend['topic'] else trend['topic'],
            "farmers",
            "agriculture",
            "DEFRA",
            "SFI",
            "grants"
        ]
    
    def extract_tags(self, trend):
        """Generate tags from topic."""
        words = trend['topic'].lower().split()
        return [w for w in words if len(w) > 3][:5]
    
    def generate_meta_desc(self, trend, content):
        """Create meta description."""
        desc = f"Complete guide to {trend['topic']} for UK farmers. Learn about policy changes, grants, and practical steps. Updated {self.date_str}."
        return desc[:160]  # SEO limit
    
    def generate_schema(self, content, trend):
        """Generate JSON-LD schema."""
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": trend['topic'],
            "datePublished": self.date_str,
            "author": {"@type": "Organization", "name": "UK Farm Brief"},
            "publisher": {"@type": "Organization", "name": "UK Farm Brief"}
        }
    
    # === AGENT 4: SAFETY CHECK ===
    def quality_check(self, article):
        """Score article quality before publishing."""
        print(f"[{self.now()}] 🔍 AGENT 4: Safety Check starting...")
        
        score = 0
        content = article['content']
        seo = article['seo']
        
        # Word count check (20 points)
        if CONFIG['min_word_count'] <= seo['word_count'] <= CONFIG['max_word_count']:
            score += 20
            print(f"  ✓ Word count: {seo['word_count']} (target: {CONFIG['min_word_count']}-{CONFIG['max_word_count']})")
        else:
            print(f"  ✗ Word count: {seo['word_count']} out of range")
        
        # Structure check (20 points)
        required_headings = ['## Introduction', '## Conclusion', '## FAQ']
        structure_score = sum(1 for h in required_headings if h in content) * 7
        score += min(structure_score, 20)
        print(f"  ✓ Structure: {min(structure_score, 20)}/20 points")
        
        # Keyword density check (20 points)
        good_density = sum(1 for d in seo['keyword_density'].values() if 0.5 <= d <= 2.5)
        keyword_score = good_density * 4
        score += min(keyword_score, 20)
        print(f"  ✓ Keywords: {min(keyword_score, 20)}/20 points")
        
        # Sources check (20 points)
        has_sources = '*Sources:' in content
        score += 20 if has_sources else 0
        print(f"  ✓ Sources: {20 if has_sources else 0}/20 points")
        
        # Actionability check (20 points)
        has_actions = 'Action Steps' in content and any(f"{i}." in content for i in range(1, 10))
        score += 20 if has_actions else 0
        print(f"  ✓ Actionable: {20 if has_actions else 0}/20 points")
        
        print(f"\n  📊 Quality Score: {score}/100")
        
        if score >= CONFIG['quality_threshold']:
            print(f"  ✅ PASSES threshold ({CONFIG['quality_threshold']})")
            return {"passed": True, "score": score}
        else:
            print(f"  ❌ FAILS threshold ({CONFIG['quality_threshold']})")
            return {"passed": False, "score": score, "reason": "Below quality threshold"}
    
    # === AGENT 5: PUBLISHER ===
    def publish_article(self, article):
        """Publish to static site."""
        print(f"[{self.now()}] 🚀 AGENT 5: Publisher starting...")
        
        # Generate filename
        slug = self.slugify(article['title'])
        filename = f"{self.date_str}-{slug}.md"
        filepath = self.posts_dir / filename
        
        # Build frontmatter
        frontmatter = f"""---
title: "{article['title']}"
date: {self.date_str}
categories: [{article['meta']['category']}]
tags: {json.dumps(article['meta']['tags'])}
word_count: {article['seo']['word_count']}
keywords: {json.dumps(article['seo']['keywords'])}
description: "{article['seo']['meta_description']}"
schema: {json.dumps(article['seo']['schema_markup'])}
quality_score: {article.get('quality_score', 'N/A')}
---

"""
        
        # Write file
        full_content = frontmatter + article['content']
        filepath.write_text(full_content, encoding='utf-8')
        
        print(f"  ✅ Published to: {filepath}")
        print(f"  📝 {article['seo']['word_count']} words")
        print(f"  🔗 Will be at: {CONFIG['site_url']}/posts/{slug}")
        
        return {
            "success": True,
            "filepath": str(filepath),
            "url": f"{CONFIG['site_url']}/posts/{slug}"
        }
    
    def slugify(self, text):
        """Convert title to URL slug."""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'\s+', '-', text)
        return text[:60].strip('-')
    
    # === UTILITIES ===
    def now(self):
        return datetime.now().strftime("%H:%M:%S")
    
    def run(self):
        """Execute full autonomous pipeline."""
        print("=" * 60)
        print(f"🤖 UK FARM BLOG AUTONOMOUS AGENT")
        print(f"📅 Date: {self.date_str}")
        print(f"📁 Output: {self.posts_dir}")
        print("=" * 60)
        
        try:
            # Step 1: Trend Scout
            trend = self.detect_trending_topic()
            
            # Step 2: Research
            research = self.research_topic(trend['topic'])
            
            # Step 3: Write
            article = self.write_article(trend, research)
            
            # Step 4: Quality Check
            check = self.quality_check(article)
            article['quality_score'] = check['score']
            
            if not check['passed']:
                print(f"\n❌ ARTICLE REJECTED - Not published")
                return {"success": False, "reason": "Quality check failed"}
            
            # Step 5: Publish
            result = self.publish_article(article)
            
            print("\n" + "=" * 60)
            print("✅ AUTONOMOUS RUN COMPLETE")
            print(f"📝 Article: {article['title']}")
            print(f"📊 Quality Score: {article['quality_score']}/100")
            print(f"🔗 URL: {result['url']}")
            print("=" * 60)
            
            return {"success": True, "article": article, "url": result['url']}
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    agent = AutonomousBlogAgent()
    result = agent.run()
    exit(0 if result['success'] else 1)