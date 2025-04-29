import requests
import random
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']


#### --- Get Quran Verse --- ####
def get_random_verse_and_tafsir():
    """Fetches a random Quran verse, its info, and Tafsir Al-Muyassar."""
    try:
        random_verse_number = random.randint(1, 6236)
        print(f"Fetching global verse number: {random_verse_number}")
        # Tafsir (Muyassar)
        api_url = f"https://api.alquran.cloud/v1/ayah/{random_verse_number}/editions/quran-simple,ar.muyassar"
        response = requests.get(api_url)
        response.raise_for_status(
        )
        data = response.json()['data']
        # Extract information
        verse_text = ""
        tafsir_text = ""
        surah_number = 0
        surah_name = ""
        ayah_number_in_surah = 0
        if data[0]['edition']['identifier'] == 'quran-simple':
            verse_text = data[0]['text']
            surah_number = data[0]['surah']['number']
            surah_name = data[0]['surah']['name']
            ayah_number_in_surah = data[0]['numberInSurah']
        elif data[1]['edition']['identifier'] == 'quran-simple':
            verse_text = data[1]['text']
            surah_number = data[1]['surah']['number']
            surah_name = data[1]['surah']['name']
            ayah_number_in_surah = data[1]['numberInSurah']

        if data[0]['edition']['identifier'] == 'ar.muyassar':
            tafsir_text = data[0]['text']
        elif data[1]['edition']['identifier'] == 'ar.muyassar':
            tafsir_text = data[1]['text']

        if not verse_text or not tafsir_text:
            print("Error: Couldn't extract verse or tafsir from API response.")
            return None 

        #### --- Message Format --- ####
        message = f"""
{verse_text}

📖 [{surah_name}، الآية: {ayah_number_in_surah}] (السورة {surah_number})

-- التفسير الميسر --
{tafsir_text}
"""
        return message.strip()  # Remove leading/trailing whitespace

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


#### --- Send to Telegram --- ####
def send_message_to_telegram(message_text):
    """Sends the formatted message to the specified Telegram channel."""
    telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message_text,
        'parse_mode':
        'HTML'  
    }
    try:
        response = requests.post(telegram_api_url, data=payload)
        response.raise_for_status() 
        print("Message sent successfully to Telegram!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        if e.response is not None:
            print(f"Telegram response: {e.response.text}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while sending: {e}")
        return False


#### --- Main --- ####
def send_hourly_verse():
    print("Starting hourly task...")
    verse_message = get_random_verse_and_tafsir()
    if verse_message:
        send_message_to_telegram(verse_message)
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
