import os, time, random, threading, requests
from flask import Flask

# === ENV ===
TOKEN = os.getenv("T8342129776:AAEz_oC8m3WJedV0VLhE82arwmUuW_9uwXg") or os.getenv("BOT_TOKEN") or ""
CHAT_ID = os.getenv("@wtfgadgets")
POST_EVERY_SECONDS = int(os.getenv("POST_INTERVAL_SEC", "14400"))  # default 4h
if POST_EVERY_SECONDS < 1800:
    POST_EVERY_SECONDS = 1800  # safety: min 30 min

# === PRODUCTS (your 10 amzn.to links) ===
PRODUCTS = [
    {"title": "Pocket Projector 🎥 — mini cinema anywhere", "url": "https://amzn.to/47KBkFn"},
    {"title": "Self-Stirring Mug ⚡ — stir at the push of a button", "url": "https://amzn.to/3Iuis30"},
    {"title": "Moon Lamp 🌕 — cozy ambient night light", "url": "https://amzn.to/4ncyvBR"},
    {"title": "LEGO Bonsai Tree 🌱 — zen desk centerpiece", "url": "https://amzn.to/4nalicM"},
    {"title": "Smart Tracker 🔔 — find keys & bags in seconds", "url": "https://amzn.to/41YpqUE"},
    {"title": "USB Mini Fridge 🥤 — keep one can icy cold", "url": "https://amzn.to/4nvWJGQ"},
    {"title": "Flying Alarm Clock 🚁 — get out of bed to stop it", "url": "https://amzn.to/4n5E8Bz"},
    {"title": "Folding Laptop Desk 💻 — work anywhere", "url": "https://amzn.to/48sHMRs"},
    {"title": "Bulb with Bluetooth Speaker 🔊 — light + music", "url": "https://amzn.to/46JowOk"},
    {"title": "RGB Mouse Pad 🌈 — glow-up your setup", "url": "https://amzn.to/468RlDM"},
]

def send_text(text: str):
    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": False}
    r = requests.post(api, data=payload, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "error": r.text}

def post_one():
    p = random.choice(PRODUCTS)
    caption = f"🌀 {p['title']}\n\n🛒 Buy here: {p['url']}\n#weird #gadgets #wtf"
    res = send_text(caption)
    print("[POST]", p["title"], res)

def bot_loop():
    # immediate post at startup (comment this if you don't want it)
    try:
        post_one()
    except Exception as e:
        print("[START ERROR]", e)
    # loop
    while True:
        try:
            time.sleep(POST_EVERY_SECONDS)
            post_one()
        except Exception as e:
            print("[LOOP ERROR]", e)

# === tiny web server so Render sees an open port ===
app = Flask(__name__)

@app.get("/")
def health():
    return "OK"

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
