import requests
import random
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']


#### --- Get Quran Verse --- ####
def get_random_verse_and_tafsir():
    try:
        random_verse_number = random.randint(1, 6236)
        print(f"Fetching global verse number: {random_verse_number}")
        
        # API request
        api_url = f"https://api.alquran.cloud/v1/ayah/{random_verse_number}/editions/quran-simple,ar.muyassar"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()['data']
        
        # Extract values
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

        # Base message format
        link = f'<a href="https://quran.ksu.edu.sa/tafseer/katheer-saadi/sura{surah_number}-aya{ayah_number_in_surah}.html">📘 أكمل القراءة / تفسير ابن كثير</a>'
        base = f"""﴿{verse_text}﴾

📖 [{surah_name}، الآية: {ayah_number_in_surah}] (السورة {surah_number})

-- التفسير الميسر --
"""

        # Calculate remaining space for tafsir
        max_length = 1024
        remaining = max_length - len(base + link)

        if len(tafsir_text) > remaining:
            tafsir_text = tafsir_text[:remaining - 3] + "..."

        message = base + tafsir_text + "\n\n" + link
        return message.strip(), random_verse_number

    except Exception as e:
        print(f"Error: {e}")
        return None

def send_audio_with_caption_to_telegram(verse_number, caption_text):
    """Sends the audio verse with the tafsir as a caption."""
    audio_url = f"https://cdn.islamic.network/quran/audio/192/ar.abdulbasitmurattal/{verse_number}.mp3"
    telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio"
    payload = {
        'chat_id': CHAT_ID,
        'audio': audio_url,
        'caption': caption_text[:1024],  # Telegram caption limit
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(telegram_api_url, data=payload)
        response.raise_for_status()
        print("Audio with caption sent successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending audio with caption: {e}")
        if e.response is not None:
            print(f"Telegram response: {e.response.text}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while sending audio: {e}")
        return False

#### --- Send to Telegram --- ####
def send_message_to_telegram(message_text, verse_number):
    """Sends the verse and tafsir as a caption along with audio to Telegram."""
    telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio"
    audio_url = f"https://cdn.islamic.network/quran/audio/192/ar.abdulbasitmurattal/{verse_number}.mp3"

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
def send_hourly_verse():
    print("Starting hourly task...")
    result = get_random_verse_and_tafsir()
    if result:
        verse_message, verse_number = result
        send_message_to_telegram(verse_message, verse_number)
    else:
        print("Failed to get verse or tafsir, skipping send.")
    print("Hourly task finished.")

#### --- Web Server --- ####
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

if __name__ == "__main__":
    print("Script starting...")
    run_server()
