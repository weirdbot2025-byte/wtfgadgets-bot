import time
import random
import logging
from telegram import Bot

# 🔑 Inserisci qui il tuo TOKEN BOT TELEGRAM
TELEGRAM_TOKEN = "INSERISCI_IL_TUO_TOKEN"
CHAT_ID = "INSERISCI_CHAT_ID"

# Attiva logging per debug
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)

# Lista prodotti (i tuoi link con titoli e immagini)
PRODUCTS = [
    {
        "title": "Mini Proiettore Portatile 🎥 — cinema in tasca ovunque tu sia",
        "url": "https://amzn.to/47KBkFn",
        "image": "https://m.media-amazon.com/images/I/61cIvItG3VL._AC_SL1500_.jpg"
    },
    {
        "title": "Tazza autorimescolante ⚡ — addio cucchiaino!",
        "url": "https://amzn.to/3Iuis30",
        "image": "https://m.media-amazon.com/images/I/71xzYl5sXgL._AC_SL1500_.jpg"
    },
    {
        "title": "Lampada Luna 🌕 — illumina la stanza come un sogno",
        "url": "https://amzn.to/4ncyvBR",
        "image": "https://m.media-amazon.com/images/I/61hLeuGQX7L._AC_SL1500_.jpg"
    },
    {
        "title": "Piantina Bonsai Lego 🌱 — decoro zen che non muore mai",
        "url": "https://amzn.to/4nalicM",
        "image": "https://m.media-amazon.com/images/I/71nPg6o1FGL._AC_SL1500_.jpg"
    },
    {
        "title": "Allarme anti-smarrimento 🔔 — trova subito chiavi e oggetti",
        "url": "https://amzn.to/41YpqUE",
        "image": "https://m.media-amazon.com/images/I/61X6rRAI6-L._AC_SL1500_.jpg"
    },
    {
        "title": "Mini Frigo USB 🥤 — bibite fredde sempre a portata di mano",
        "url": "https://amzn.to/4nvWJGQ",
        "image": "https://m.media-amazon.com/images/I/71dZmcf5WVL._AC_SL1500_.jpg"
    },
    {
        "title": "Sveglia Volante 🚁 — ti fa alzare davvero dal letto!",
        "url": "https://amzn.to/4n5E8Bz",
        "image": "https://m.media-amazon.com/images/I/71hXwHFFZVL._AC_SL1500_.jpg"
    },
    {
        "title": "Scrivania pieghevole 💻 — smart working ovunque",
        "url": "https://amzn.to/48sHMRs",
        "image": "https://m.media-amazon.com/images/I/81+QjF7p4JL._AC_SL1500_.jpg"
    },
    {
        "title": "Lampadina con altoparlante Bluetooth 🔊 — luce + musica",
        "url": "https://amzn.to/46JowOk",
        "image": "https://m.media-amazon.com/images/I/71Fqlix3RFL._AC_SL1500_.jpg"
    },
    {
        "title": "Tappetino mouse RGB 🌈 — scrivania che si illumina",
        "url": "https://amzn.to/468RlDM",
        "image": "https://m.media-amazon.com/images/I/81HTjEAwLqL._AC_SL1500_.jpg"
    },
]

def main():
    while True:
        product = random.choice(PRODUCTS)  # sceglie un prodotto a caso
        text = f"{product['title']}\n👉 {product['url']}"
        
        try:
            bot.send_photo(chat_id=CHAT_ID, photo=product['image'], caption=text)
            logging.info(f"✅ Pubblicato: {product['title']}")
        except Exception as e:
            logging.error(f"Errore: {e}")

        time.sleep(3600)  # aspetta 1 ora prima di pubblicare di nuovo

if __name__ == "__main__":
    main()

