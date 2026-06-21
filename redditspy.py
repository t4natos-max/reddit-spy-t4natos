#  Reddit Spy Bot - Multi-Channel Edition
#  Copyright (c) 2026 t4natos-max
#  This project is licensed under the MIT License.

import requests
import time
import xml.etree.ElementTree as ET

VERSION = "1.0.0"

print(f"🌌 REDDIT SPY BOT v{VERSION} (Official Release)")
print("-----------------------------------------------")

# 1. Configuración interactiva por consola
subreddit = input("➡️ Enter Subreddit to spy (e.g., gaming): ").strip().lower()
keywords_input = input("➡️ Enter keywords separated by commas: ")
keywords = [k.strip().lower() for k in keywords_input.split(",") if k.strip()]

# Configuración de Telegram
telegram_token = input("🤖 Enter Telegram Bot Token (Leave empty to skip): ").strip()
chat_id = input("🆔 Enter your Telegram Chat ID (Leave empty to skip): ").strip()

print("\n[+] Spy active... Monitoring Reddit via RSS syndication layer.\n")

# Base de datos local para no repetir alertas
history_file = "spy_history.txt"

def load_history():
    try:
        with open(history_file, "r") as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def save_to_history(post_id):
    with open(history_file, "a") as f:
        f.write(f"{post_id}\n")

def send_telegram_alert(title, link):
    if not telegram_token or not chat_id:
        return
    message = f"🚨 *MATCH FOUND IN r/{subreddit}* 🚨\n\n📌 *Title:* {title}\n🔗 [View Post]({link})"
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[!] Telegram send error: {e}")

already_notified = load_history()
url = f"https://www.reddit.com/r/{subreddit}/new/.rss"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Linux/Termux/v1.0.0"}

while True:
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            # El namespace estándar de los feeds RSS/Atom de Reddit
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                post_id = entry.find('atom:id', ns).text if entry.find('atom:id', ns) is not None else ""
                title = entry.find('atom:title', ns).text if entry.find('atom:title', ns) is not None else ""
                link_node = entry.find('atom:link', ns)
                link = link_node.attrib['href'] if link_node is not None else ""

                if post_id and post_id not in already_notified:
                    # Comprobar si alguna palabra clave está en el título
                    if any(kw in title.lower() for kw in keywords):
                        print(f"🎯 Match found: {title}")
                        send_telegram_alert(title, link)
                        already_notified.add(post_id)
                        save_to_history(post_id)
                        
        elif response.status_code == 429:
            print("[!] Rate limited (429). Backing off...")
            time.sleep(30)
        else:
            print(f"[!] Error {response.status_code} reaching Reddit RSS.")
            
    except Exception as e:
        print(f"[!] Connection error: {e}")
        
    time.sleep(15)  # Delay para no saturar

