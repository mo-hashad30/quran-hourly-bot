import requests
import random
import os
import sys
import threading
import time
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

#### --- Get Quran Verse --- ####
def get_random_verse_and_tafsir():
    try:
        AUDIO_LINKS = [
            ("https://cdn.islamic.network/quran/audio/192/ar.abdullahbasfar/{verse_number}.mp3", "عبدالله بصفر"),
            ("https://cdn.islamic.network/quran/audio/192/ar.abdulbasitmurattal/{verse_number}.mp3", "عبدالباسط عبدالصمد"),
            ("https://cdn.islamic.network/quran/audio/64/ar.alafasy/{verse_number}.mp3", "مشاري العفاسي"),
            ("https://cdn.islamic.network/quran/audio/128/ar.husary/{verse_number}.mp3", "محمود الحصري"),
            ("https://cdn.islamic.network/quran/audio/128/ar.hudhaify/{verse_number}.mp3", "علي الحذيفي"),
            ("https://cdn.islamic.network/quran/audio/32/ar.ibrahimakhbar/{verse_number}.mp3", "إبراهيم الأخضر"),
            ("https://cdn.islamic.network/quran/audio/128/ar.muhammadayyoub/{verse_number}.mp3", "محمد أيوب"),
            ("https://cdn.islamic.network/quran/audio/64/ar.aymanswoaid/{verse_number}.mp3", "أيمن سويد")
        ]
        
        # Choose reciter
        audio_url_template, reciter_name = random.choice(AUDIO_LINKS)
        
        # Pick a verse
        random_verse_number = random.randint(1, 6236)
        print(f"Fetching verse #{random_verse_number} ({reciter_name})")

        # Fetch text and tafsir
        api_url = f"https://api.alquran.cloud/v1/ayah/{random_verse_number}/editions/quran-simple,ar.muyassar"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()['data']
        
        verse_text, tafsir_text = "", ""
        surah_number = surah_name = ayah_number_in_surah = None

        for item in data:
            if item['edition']['identifier'] == 'quran-simple':
                verse_text = item['text']
                surah_number = item['surah']['number']
                surah_name = item['surah']['name']
                ayah_number_in_surah = item['numberInSurah']
            elif item['edition']['identifier'] == 'ar.muyassar':
                tafsir_text = item['text']

        if not verse_text or not tafsir_text:
            print("Error: Missing verse or tafsir.")
            return None

        link = f'<a href="https://quran.ksu.edu.sa/tafseer/katheer-saadi/sura{surah_number}-aya{ayah_number_in_surah}.html">📘 أكمل القراءة / تفسير ابن كثير</a>'
        
        base = f"""﴿{verse_text}﴾

📖 [{surah_name}، الآية: {ayah_number_in_surah}] (السورة {surah_number}) — 🎙️ {reciter_name}

-- التفسير الميسر --
"""

        max_length = 1024
        remaining = max_length - len(base + link)

        if len(tafsir_text) > remaining:
            tafsir_text = tafsir_text[:remaining - 3] + "..."

        message = base + tafsir_text + "\n\n" + link
        audio_url = audio_url_template.format(verse_number=random_verse_number)
        return message.strip(), random_verse_number, audio_url

    except Exception as e:
        print(f"Error: {e}")
        return None

#### --- Send to Telegram --- ####
def send_message_to_telegram(message_text, verse_number, audio_url):
    telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio"
    payload = {
        'chat_id': CHAT_ID,
        'audio': audio_url,
        'caption': message_text,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(telegram_api_url, data=payload)
        response.raise_for_status()
        print("Audio + caption sent successfully to Telegram!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending audio to Telegram: {e}")
        if e.response is not None:
            print(f"Telegram response: {e.response.text}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while sending: {e}")
        return False

#### --- Main --- ####
class RequestHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        if self.path == '/run':
            self.send_response(200) 
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            print("/run Request received, triggering task...")
            send_hourly_verse()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            print(f"HEAD request received for {self.path}")

    def do_GET(self):
        if self.path == '/run':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(
                b"Task triggered successfully!")
            print("/run Request received, triggering task...")
            send_hourly_verse()

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(
                b"Use /run to trigger.")
            print(f"GET request received for {self.path}")

def run_server(server_class=HTTPServer,
               handler_class=RequestHandler,
               port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()
                   
def send_hourly_verse():
    print("Starting hourly task...")
    result = get_random_verse_and_tafsir()
    if result:
        verse_message, verse_number, audio_url = result
        send_message_to_telegram(verse_message, verse_number, audio_url)
    else:
        print("Failed to get verse or tafsir, skipping send.")
    print("Hourly task finished.")


#### --- Web Server --- ####
def wait_and_send_forever():
    while True:
        now = datetime.datetime.now()
        next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        wait_seconds = (next_hour - now).total_seconds()
        print(f"[Scheduler] Waiting {int(wait_seconds)} seconds until next hour...")
        time.sleep(wait_seconds)
        send_hourly_verse()

if __name__ == "__main__":
    # If RUN_ONCE is set, just send one verse and exit (for GitHub Actions)
    if os.environ.get("RUN_ONCE") == "1":
        send_hourly_verse()
    else:
        print("Web service starting...")
        thread = threading.Thread(target=wait_and_send_forever, daemon=True)
        thread.start()
        run_server()
