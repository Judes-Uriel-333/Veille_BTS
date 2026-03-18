"""Test direct du service RSS et de la base SQLite — debug audit."""
from app.services.db import init_db, get_conn
from app.services.rss_service import fetch_and_store_articles, get_articles

print("=" * 60)
print("TEST DIRECT RSS SERVICE")
print("=" * 60)

# 1. Init DB
init_db()
print("[OK] Base initialisee")

# 2. Compter les articles existants
articles_avant = get_articles()
print(f"[INFO] Articles en base AVANT fetch : {len(articles_avant)}")

# 3. Tenter le fetch
print("[INFO] Lancement fetch_and_store_articles()...")
try:
    fetch_and_store_articles()
    print("[OK] fetch_and_store_articles() termine sans erreur")
except Exception as e:
    print(f"[ERREUR] fetch_and_store_articles() a leve : {type(e).__name__}: {e}")

# 4. Compter apres
articles_apres = get_articles()
print(f"[INFO] Articles en base APRES fetch : {len(articles_apres)}")

# 5. Afficher les 3 premiers
if articles_apres:
    print("[INFO] Premiers articles :")
    for a in articles_apres[:3]:
        d = dict(a)
        print(f"  - {d.get('title', '???')[:70]}")
        print(f"    source={d.get('source', '?')}  link={d.get('link', '?')[:50]}")
else:
    print("[ATTENTION] La base est VIDE meme apres le fetch.")

print("=" * 60)
print("FIN DU TEST")
