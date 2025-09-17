# bot_auto.py — post automatici affidabili (solo testo + link verificati)
import time, random, requests

TOKEN = "8342129776:AAEz_oC8m3WJedV0VLhE82arwmUuW_9uwXg"
CHAT_ID = "@wtfgadgets"

# per test: 60 sec; poi rimetti 3*60*60
POST_EVERY_SECONDS = 60

# aggiungeremo il tuo tracking ID quando attivi Amazon Associates
AMAZON_TAG = "YOURTAG-21"  # es: weirdbot-21

PRODUCTS = [
    {"title": "OTOTO Nessie Soup Ladle — the standing ladle 🦕",
     "url": "https://www.amazon.com/OTOTO-Vegetable-Strainer-Strainers-Dishwasher/dp/B0114WKC46"},
    {"title": "OTOTO Spaghetti Monster Colander 🍝",
     "url": "https://www.amazon.com/Spaghetti-Monster-Colander-Strainer-OTOTO/dp/B076676PS9"},
    {"title": "OTOTO Crabby Clip-On Strainer 🦀",
     "url": "https://www.amazon.com/OTOTO-OT063-Crabby-Clip-Strainer/dp/B0CJCPFMRZ"},
    {"title": "The Screaming Goat (book + screaming figure) 🐐",
     "url": "https://www.amazon.com/The-Screaming-Goat-Book-Figure/dp/0762459816"},
    {"title": "Mini Wacky Waving Inflatable Tube Guy (desktop) 🕺",
     "url": "https://www.amazon.com/Mealivos-Wacky-Waving-Inflatable-Blower/dp/B0DQNK98M7"},
    {"title": "Rubber Chicken Purse — The Hen Bag 🐔👜",
     "url": "https://www.amazon.com/Rubber-Chicken-Purse-Hen-Handbag/dp/B001G8N95I"},
    {"title": "Banana Duck Statue — whimsical yard art 🍌🦆",
     "url": "https://www.amazon.com/Banana-Sculpture-Whimsical-Creative-Outdoor/dp/B092QP28M3"},
    {"title": "Frozen Magic Squeeze Slushy Cup 🧊",
     "url": "https://www.amazon.com/Color-Land-Trending-Homemade-350ML/dp/B09NQ7P4CV"},
    {"title": "AMERFIST Flying Orb Ball — boomerang hover ball ✨",
     "url": "https://www.amazon.com/AMERFIST-Boomerang-Galactic-Spinner-Outdoor/dp/B08QTP3MLT"},
    {"title": "Paladone Henry Hoover Desk Mini Vacuum 🧹",
     "url": "https://www.amazon.com/Henry-Hetty-Desktop-Vacuum-Cleaner/dp/B00KRG8BPS"},
    {"title": "Ladybug Mini Desktop Vacuum 🐞",
     "url": "https://www.amazon.com/Honbay-Ladybug-Portable-Cleaner-Sweeper/dp/B01MU3HSK2"},
    {"title": "OTOTO Pinot — Parrot Corkscrew 🦜🍷",
     "url": "https://www.amazon.com/OTOTO-OT955-Pinot/dp/B09VPLLFS2"},
]

def affiliate_link(url: str) -> str:
    if AMAZON_TAG and "tag=" not in url:
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={AMAZON_TAG}"
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
    if not res.get("ok"):
        print("[ERROR]", res)
    else:
        print("[OK] Posted:", p["title"])

if __name__ == "__main__":
    while True:
        try:
            post_random_product()
        except Exception as e:
            print("[FATAL]", e)
        time.sleep(POST_EVERY_SECONDS)
