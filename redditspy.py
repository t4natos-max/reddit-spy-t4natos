import requests
import random
import time
import xml.etree.ElementTree as ET

# ==========================================
# 🛡️ OFFICIAL AUTHOR SIGNATURE
# ==========================================
AUTHOR = "t4natos"
VERSION = "1.0.0 (First Edition)"

def print_banner():
    print(f"""
    #################################################
    #      REDDIT SPY BOT v{VERSION}                  #
    #      Created by: {AUTHOR}                     #
    #      Feel free to modify this code!           #
    #################################################
    """)

# Lista de agentes RSS legítimos para rotar y evitar el rastreo de firmas
RSS_AGENTS = [
    f"Feedly/1.0 (+http://feedly.com/fetcher.html; info@feedly.com) t4spy_{AUTHOR}",
    f"Mozilla/5.0 (compatible; Google-News; +http://support.google.com/news/answer/40411) Reader_{AUTHOR}",
    f"Inoreader/1.5 (+http://www.inoreader.com/feed_fetcher) spybot_{AUTHOR}",
    f"NewsBlur Feed Fetcher (+http://www.newsblur.com) engine_{AUTHOR}"
]

def fetch_rss_with_retry(url, max_retries=3):
    """Realiza la petición con reintentos si detecta el código 429"""
    base_delay = 5  # Segundos a esperar inicialmente en caso de 429
    
    for attempt in range(max_retries):
        headers = {
            "User-Agent": random.choice(RSS_AGENTS),
            "Accept": "application/rss+xml, application/atom+xml, text/xml, */*"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response
            
        if response.status_code == 429:
            # Multiplicador exponencial de tiempo para enfriar la IP (5s, 10s, 15s...)
            sleep_time = base_delay * (attempt + 1) + random.uniform(1, 3)
            print(f"⚠️ [429 Too Many Requests] Reddit rate-limit hit. Cooling down IP for {sleep_time:.1f} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(sleep_time)
        else:
            # Si es otro error (como 403 o 500), salimos del bucle
            return response
            
    return response

def main():
    print_banner()
    
    print("⚙️  [SETUP] Configure your spying target:")
    subreddit_input = input(" 👤 Enter Subreddit to monitor (e.g., gaming, startup): ").strip()
    if not subreddit_input:
        subreddit_input = "gaming"
        
    keywords_input = input(" 🔑 Enter keywords to find (separated by commas): ")
    if not keywords_input:
        print("❌ You must enter at least one keyword!")
        return
        
    keywords = [kw.strip().lower() for kw in keywords_input.split(",") if kw.strip()]
    
    print("\n" + "-"*50)
    print(f"[-] Launching {AUTHOR} Resilient RSS Engine...")
    print(f"[-] Target Subreddit: r/{subreddit_input}")
    print(f"[-] Keywords to match: {keywords}")
    print("-"*50 + "\n")
    
    url = f"https://www.reddit.com/r/{subreddit_input}/new/.rss"
    
    try:
        # Ejecutamos la petición protegida contra el bloqueo 429
        response = fetch_rss_with_retry(url)
        
        if response.status_code != 200:
            print(f"❌ Reddit Connection Failed: Code {response.status_code}")
            print("💡 [Tip] Si el 429 persiste, apaga tu Wi-Fi en el cel y usa datos móviles para forzar un cambio de IP.")
            return
            
        root = ET.fromstring(response.content)
        namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', namespaces)
        
        mentions_found = 0
        
        for entry in entries:
            title_node = entry.find('atom:title', namespaces)
            content_node = entry.find('atom:content', namespaces)
            link_node = entry.find('atom:link', namespaces)
            
            title = title_node.text if title_node is not None else ""
            content = content_node.text if content_node is not None else ""
            link = link_node.attrib.get('href', '') if link_node is not None else ""
            
            full_text = f"{title} {content}".lower()
            matches = [kw for kw in keywords if kw in full_text]
            
            if matches:
                mentions_found += 1
                print(f"🔥 [DETECTED BY {AUTHOR.upper()}] [{', '.join(matches)}] -> {title[:50]}...")
                print(f"   🔗 Link: {link}")
                
        print("\n" + "="*50)
        print(f"📊 {AUTHOR.upper()} INTELLIGENCE REPORT - r/{subreddit_input}")
        print(f"Total posts parsed: {len(entries)}")
        print(f"Mentions found successfully: {mentions_found}")
        print(f"Core Engine: {AUTHOR}")
        print("="*50)

    except Exception as e:
        print(f"❌ Critical error parsing RSS: {e}")

if __name__ == "__main__":
    main()

