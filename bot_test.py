import os, time, random, requests

# ====== CONFIG ======
TOKEN = "8342129776:AAEz_oC8m3WJedV0VLhE82arwmUuW_9uwXg"   # tuo token
CHAT_ID = "@wtfgadgets"                                     # canale pubblico
POST_EVERY_SECONDS = 3 * 60 * 60                            # ogni 3 ore
AMAZON_TAG = "YOURTAG-21"                                   # <-- metti il tuo tag Affiliati quando pronto

# Lista iniziale di prodotti (cambiali/aggiungine a piacere)
# title: testo breve; img: URL immagine; url: link Amazon (aggiungeremo ?tag=…)
PRODUCTS = [
    {
        "title": "Mini aspirapolvere da scrivania a forma di maialino 🐷",
        "img": "https://m.media-amazon.com/images/I/61VwD0EJ4fL._AC_SL1500_.jpg",
        "url": "https://www.amazon.it/dp/B07P9QF3J2"
    },
    {
        "title": "Macchina spara bolle portatile (versione turbo) 🫧",
        "img": "https://m.media-amazon.com/images/I/71oY3QWQ34L._AC_SL1500_.jpg",
        "url": "https://www.amazon.it/dp/B0B6LZ9K5M"
    },
    {
        "title": "Lampada luna 3D con supporto in legno 🌕",
        "img": "https://m.media-amazon.com/images/I/71yq8p2hV3L._AC_SL1500_.jpg",
        "url": "https://www.amazon.it/dp/B07H7H7P7B"
    },
    {
        "title": "Tazza autorimescolante (per pigri professionisti) ☕️",
        "img": "https://m.media-amazon.com/images/I/61n3Q0p1NfL._AC_SL1500_.jpg",
        "url": "https://www.amazon.it/dp/B07KQJQ5JQ"
    },
    {
        "title": "Mini frigo USB per una lattina (why not) 🧊",
        "img": "https://m.media-amazon.com/images/I/61Qd2S3wB2L._AC_SL1500_.jpg",
        "url": "https://www.amazon.it/dp/B00KDN2Z4Q"
    }
]

def affiliate_link(url: str) -> str:
    # Aggiunge il tag affiliato se disponibile (senza duplicarlo)
    if AMAZON_TAG and "tag=" not in url:
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={AMAZON_TAG}"
    return url

def send_photo_with_caption(token: str, chat_id: str, photo_url: str, caption: str):
    api = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption
    }
    r = requests.post(api, data=payload, timeout=30)
    try:
        data = r.json()
    except Exception:
        data = {"ok": False, "error": r.text}
    return data

def post_random_product():
    p = random.choice(PRODUCTS)
    link = affiliate_link(p["url"])
    caption = (
        f"🌀 {p['title']}\n\n"
        f"🛒 Buy here: {link}\n"
        f"#weird #gadgets #wtf"
    )
    res = send_photo_with_caption(TOKEN, CHAT_ID, p["img"], caption)
    ok = res.get("ok", False)
    if not ok:
        print("[ERROR]", res)
    else:
        print("[OK] Posted:", p["title"])

if __name__ == "__main__":
    # Post immediato all’avvio, poi ogni X ore
    while True:
        try:
            post_random_product()
        except Exception as e:
            print("[FATAL]", e)
        time.sleep(POST_EVERY_SECONDS)
