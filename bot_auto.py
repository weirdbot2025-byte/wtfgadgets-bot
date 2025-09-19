import os, time, threading, requests
from flask import Flask, jsonify

# ========= CONFIG DIRETTO (i tuoi valori) =========
TOKEN   = "8342129776:AAEz_oC8m3WJedV0VLhE82arwmUuW_9uwXg"
CHAT_ID = "@wtfgadgets"          # usa @username del canale
INTERVAL = 14400                 # 4 ore = 14400 secondi

# ========= PRODUCTS =========
PRODUCTS = [
    {"title": "Pocket Projector 🎥 — mini cinema anywhere",                 "url": "https://amzn.to/47KBkFn"},
    {"title": "Self-Stirring Mug ⚡ — stir at the push of a button",        "url": "https://amzn.to/3Iuis30"},
    {"title": "Moon Lamp 🌕 — cozy ambient night light",                    "url": "https://amzn.to/4ncyvBR"},
    {"title": "LEGO Bonsai Tree 🌱 — zen desk centerpiece",                 "url": "https://amzn.to/4nalicM"},
    {"title": "Smart Tracker 🔔 — find keys & bags in seconds",             "url": "https://amzn.to/41YpqUE"},
    {"title": "USB Mini Fridge 🥤 — keep one can icy cold",                 "url": "https://amzn.to/4nvWJGQ"},
    {"title": "Flying Alarm Clock 🚁 — get out of bed to stop it",          "url": "https://amzn.to/4n5E8Bz"},
    {"title": "Folding Laptop Desk 💻 — work anywhere",                     "url": "https://amzn.to/48sHMRs"},
    {"title": "Bulb with Bluetooth Speaker 🔊 — light + music",             "url": "https://amzn.to/46JowOk"},
    {"title": "RGB Mouse Pad 🌈 — glow-up your setup",                      "url": "https://amzn.to/468RlDM"},
]

current_index = 0

def send_text(text: str):
    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": False}
    r = requests.post(api, data=payload, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "error": r.text}

def post_product(index: int):
    p = PRODUCTS[index % len(PRODUCTS)]
    caption = f"🌀 {p['title']}\n\n🛒 Buy here: {p['url']}\n#weird #gadgets #wtf"
    res = send_text(caption)
    print("[POST]", index, p["title"], res)
    return res

def bot_loop():
    global current_index
    # 👉 primo post immediato
    try:
        post_product(current_index)
    except Exception as e:
        print("[START ERROR]", e)
    current_index += 1

    while True:
        try:
            time.sleep(INTERVAL)
            post_product(current_index)
            current_index += 1
        except Exception as e:
            print("[LOOP ERROR]", e)

# ========= Flask server (per Render) =========
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
