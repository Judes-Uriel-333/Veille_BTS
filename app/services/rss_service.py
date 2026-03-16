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
                # 1. Requête sécurisée avec Timeout strict de 10 secondes
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                # 3. On donne le contenu pur au parser pour éviter qu'il gère le réseau lui-même
                feed = feedparser.parse(response.content)
                
                for entry in feed.entries[:10]:
                    title = entry.get("title", "")
                    link = entry.get("link", "")
                    published = entry.get("published", "")
                    source = feed.feed.get("title", "Unknown")

                    # 5. éviter doublons basique
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
                # 4. Le try/except dans la boucle isole les pannes d'un flux par rapport aux autres
                print(f"Information: Erreur ignorée sur le flux {url} : {e}")
                last_error = str(e)

        conn.commit()

    # 8. Si aucun flux n'a fonctionné, on lève une exception globale pour le QThread
    if success_count == 0 and len(RSS_FEEDS) > 0:
        raise Exception(f"Aucun serveur RSS consultable. Erreur type : {last_error}")

def get_articles(limit=20):
    # 5. On renvoie proprement les articles du cache
    with get_conn() as conn:
        return conn.execute("""
            SELECT title, link, source, published
            FROM articles
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()
