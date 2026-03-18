import feedparser
import requests
from app.services.db import get_conn

RSS_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch/",
    "https://www.theverge.com/rss/index.xml"
]

def fetch_and_store_articles():
    success_count = 0
    last_error = None

    with get_conn() as conn:
        for url in RSS_FEEDS:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                feed = feedparser.parse(response.content)
                
                for entry in feed.entries[:10]:
                    title = entry.get("title", "")
                    link = entry.get("link", "")
                    published = entry.get("published", "")
                    source = feed.feed.get("title", "Unknown")

                    existing = conn.execute(
                        "SELECT id FROM articles WHERE link = ?",
                        (link,)
                    ).fetchone()

                    if not existing:
                        conn.execute("""
                            INSERT INTO articles(title, link, source, published)
                            VALUES (?, ?, ?, ?)
                        """, (title, link, source, published))
                
                success_count += 1

            except Exception as e:
                print(f"[RSS] Erreur sur {url} : {e}")
                last_error = str(e)

        conn.commit()

    if success_count == 0 and len(RSS_FEEDS) > 0:
        raise Exception(f"Aucun flux RSS disponible. Derniere erreur : {last_error}")

def get_articles(limit=20):
    with get_conn() as conn:
        return conn.execute("""
            SELECT title, link, source, published
            FROM articles
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()
