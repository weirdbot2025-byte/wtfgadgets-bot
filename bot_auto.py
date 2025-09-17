import os, time, random, threading, requests
from flask import Flask

# ====== ENV ======
TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN") or ""
CHAT_ID = os.getenv("CHAT_ID", "@wtfgadgets")
ASSOCIATE_TAG = os.getenv("ASSOCIATE_TAG", "weirdfindsdai-20")

# Intervallo (default 3 ore). Impongo minimo 30 min per sicurezza.
POST_EVERY_SECONDS = int(os.getenv("POST_INTERVAL_SEC", "10800"))
if POST_EVERY_SECONDS < 1800:
    POST_EVERY_SECONDS = 1800  # 30 minuti minimo

# ====== PRODOTTI DI ESEMPIO (sostituisci con i tuoi link reali .com) ======
PRODUCTS = [
    {"title":"OTOTO Nessie Soup Ladle — the standing ladle 🦕","url":"https://www.amazon.com/dp/B0114WKC46"},
    {"title":"Spaghetti Monster Colander 🍝","url":"https://www.amazon.com/dp/B076676PS9"},
    {"title":"The Screaming Goat (mini book + figure) 🐐","url":"https://www.amazon.com/dp/0762459816"},
]

def affiliate_link(url: str) -> str:
    if ASSOCIATE_TAG and "tag=" not in url:
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={ASSOCIATE_TAG}"
    return url

def send_text(text: str):
    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": False}
    r = requests.post(api, data=payload, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "error": r.text}

def post_random_product():
    p = random.choice(PRODUCTS)
    link = affiliate_link(p["url"])
    caption = f"🌀 {p['title']}\n\n🛒 Buy here: {link}\n#weird #gadgets #wtf"
    res = send_text(caption)
    print("[POST]", p["title"], res)

def bot_loop():
    # Post immediato all’avvio (se non lo vuoi, commenta la riga sotto)
    try:
        post_random_product()
    except Exception as e:
        print("[FATAL at start]", e)
    # Loop
    while True:
        try:
            time.sleep(POST_EVERY_SECONDS)
            post_random_product()
        except Exception as e:
            print("[ERROR loop]", e)

# ====== MINI WEB SERVER per Render ======
app = Flask(__name__)

@app.get("/")
def health():
    return "OK"

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
