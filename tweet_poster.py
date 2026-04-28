import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

def clean_text(text):
    if not text: return ""
    text = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', text, flags=re.DOTALL)
    return text.strip()

def strip_html(html_content):
    if not html_content: return ""
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup(["script", "style", "a"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return " ".join(text.split())

def run_filter():
    rss_url = "https://nitter.net/mementomori_boi/rss"
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    
    if not webhook_url:
        print("Error: Missing DISCORD_WEBHOOK.")
        return

    try:
        print(f"--- Fetching from Nitter ---")
        response = requests.get(rss_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')

        if not items:
            print("No items found. Nitter instance might be rate-limited.")
            return

        now = datetime.now(timezone.utc)
        time_threshold = now - timedelta(minutes=1250)
        print(f"Checking for posts after: {time_threshold}")

        found_count = 0

        for item in reversed(items):
            pub_date_tag = item.find('pubDate')
            if not pub_date_tag: continue
            
            pub_date = parsedate_to_datetime(pub_date_tag.text)
            
            if pub_date < time_threshold:
                continue
            
            link = item.find('link').text if item.find('link') else ""

            # Convert to vxtwitter for Discord
            clean_link = re.sub(r'https?://[^/]+', 'https://vxtwitter.com', link)
            
            payload = {
                "username": "MementoMori Official",
                "content": clean_link
            }
            
            resp = requests.post(webhook_url, json=payload)
            if resp.status_code in [200, 204]:
                print(f"SUCCESS: {clean_link}")
                found_count += 1
            else:
                print(f"FAILED: {resp.status_code}")

        if found_count == 0:
            print("No new tweets found in this time window.")

    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    run_filter()
