import os, time, threading, requests
from flask import Flask, jsonify

# ========= CONFIG (tuoi valori già inseriti) =========
TOKEN   = "8342129776:AAEz_oC8m3WJedV0VLhE82arwmUuW_9uwXg"
CHAT_ID = "@wtfgadgets"         # se vuoi al 100% sicuro usa l'ID numerico -100...
INTERVAL = 14400                # 4 ore (soft). Cambia con POST_INTERVAL_SEC env var se vuoi.

# ========= PRODOTTI (10 link che mi hai dato) =========
# TIP: quando hai l'URL immagine da SiteStripe, incollalo nel campo "image".
PRODUCTS = [
    {"title": "Pocket Projector 🎥 — mini cinema anywhere",
     "url": "https://amzn.to/47KBkFn", "image": "https://m.media-amazon.com/images/I/61nZei8qXYL._AC_SY695_.jpg"},

    {"title": "Self-Stirring Mug ⚡ — stir at the push of a button",
     "url": "https://amzn.to/3Iuis30", "image": "https://m.media-amazon.com/images/I/81y2kuGAntL._AC_SX679_.jpg"},

    {"title": "Moon Lamp 🌕 — cozy ambient night light",
     "url": "https://amzn.to/4ncyvBR", "image": "https://m.media-amazon.com/images/I/61duHGPsujL._AC_SX679_.jpg"},

    {"title": "LEGO Bonsai Tree 🌱 — zen desk centerpiece",
     "url": "https://amzn.to/4nalicM", "image": "https://m.media-amazon.com/images/I/61duHGPsujL._AC_SL1500_.jpg"},

    {"title": "Smart Tracker 🔔 — find keys & bags in seconds",
     "url": "https://amzn.to/41YpqUE", "image": "https://m.media-amazon.com/images/I/71PYcIhduPL._AC_SL1500_.jpg"},

    {"title": "USB Mini Fridge 🥤 — keep one can icy cold",
     "url": "https://amzn.to/4nvWJGQ", "image": "https://m.media-amazon.com/images/I/51cCOq5+34L._AC_SX679_.jpg"},

    {"title": "Flying Alarm Clock 🚁 — get out of bed to stop it",
     "url": "https://amzn.to/4n5E8Bz", "image": "https://m.media-amazon.com/images/I/51Pzpb9ZQDL._AC_SY695_.jpg"},

    {"title": "Folding Laptop Desk 💻 — work anywhere",
     "url": "https://amzn.to/48sHMRs", "image": "https://m.media-amazon.com/images/I/71NMU2AJSnL._AC_SX679_.jpg"},

    {"title": "Bulb with Bluetooth Speaker 🔊 — light + music",
     "url": "https://amzn.to/46JowOk", "image": "https://m.media-amazon.com/images/I/61z6YsGdWuL._AC_SX679_.jpg"},

    {"title": "RGB Mouse Pad 🌈 — glow-up your setup",
     "url": "https://amzn.to/468RlDM", "image": ""},
]

current_index = 0

# ====== Invii Telegram via API HTTP ======
def send_text(text: str):
    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": False}
    r = requests.post(api, data=payload, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "error": r.text}

def send_photo(caption: str, photo_url: str):
    api = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {"chat_id": CHAT_ID, "photo": photo_url, "caption": caption}
    r = requests.post(api, data=payload, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "error": r.text}

def post_product(index: int):
    p = PRODUCTS[index % len(PRODUCTS)]
    caption = f"🌀 {p['title']}\n\n🛒 Buy here: {p['url']}\n#weird #gadgets #wtf"
    res = None
    if p.get("image"):
        res = send_photo(caption, p["image"])
        if not res.get("ok"):
            print("[WARN] photo failed, fallback to text:", res)
            res = send_text(caption)
    else:
        res = send_text(caption)
    print("[POST]", index, p["title"], res)
    return res

def bot_loop():
    global current_index
    # 👉 Post immediato del primo prodotto
    try:
        post_product(current_index)
    except Exception as e:
        print("[START ERROR]", e)
    current_index += 1

    # Poi prosegue ogni INTERVAL secondi (4h)
    while True:
        try:
            time.sleep(int(os.getenv("POST_INTERVAL_SEC", str(INTERVAL))))
            post_product(current_index)
            current_index += 1
        except Exception as e:
            print("[LOOP ERROR]", e)

# ====== mini web server (Render vuole una porta) ======
app = Flask(__name__)

@app.get("/")
def health():
    return "OK"

@app.get("/ping")
def ping():
    res = send_text("🔧 Ping test from Render (weirdgadgets2025_bot)")
    return jsonify(res), 200

@app.get("/post-now")
def post_now():
    global current_index
    res = post_product(current_index)
    current_index += 1
    return jsonify(res), 200

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
