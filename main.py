import requests
import random
import os
import sys  # Import sys to check if running as a server
from http.server import BaseHTTPRequestHandler, HTTPServer  # Needed for web server part

# Get secrets securely from Replit's environment
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']


# --- Function to get Quran Data ---
def get_random_verse_and_tafsir():
    """Fetches a random Quran verse, its info, and Tafsir Al-Muyassar."""
    try:
        # Quran has 6236 verses (excluding Bismillahs counted separately)
        # api.alquran.cloud uses a global verse numbering system
        random_verse_number = random.randint(1, 6236)
        print(f"Fetching global verse number: {random_verse_number}")

        # API endpoint to get verse text (simple script) and Tafsir (Muyassar)
        # We request two 'editions': quran-simple and ar.muyassar
        api_url = f"https://api.alquran.cloud/v1/ayah/{random_verse_number}/editions/quran-simple,ar.muyassar"

        response = requests.get(api_url)
        response.raise_for_status(
        )  # Raises an error for bad status codes (like 404, 500)

        data = response.json()['data']

        # Extract information
        verse_text = ""
        tafsir_text = ""
        surah_number = 0
        surah_name = ""
        ayah_number_in_surah = 0

        # Find the simple Quran text
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

        # Find the Tafsir text
        if data[0]['edition']['identifier'] == 'ar.muyassar':
            tafsir_text = data[0]['text']
        elif data[1]['edition']['identifier'] == 'ar.muyassar':
            tafsir_text = data[1]['text']

        if not verse_text or not tafsir_text:
            print("Error: Couldn't extract verse or tafsir from API response.")
            return None  # Indicate failure

        # Format the message
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


# --- Function to send to Telegram ---
def send_message_to_telegram(message_text):
    """Sends the formatted message to the specified Telegram channel."""
    telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message_text,
        'parse_mode':
        'HTML'  # Allows basic formatting if needed, though we avoid it here
    }
    try:
        response = requests.post(telegram_api_url, data=payload)
        response.raise_for_status()  # Check for errors from Telegram API
        print("Message sent successfully to Telegram!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        # Print Telegram's response if available
        if e.response is not None:
            print(f"Telegram response: {e.response.text}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while sending: {e}")
        return False


# --- Function to handle the main task ---
def send_hourly_verse():
    print("Starting hourly task...")
    verse_message = get_random_verse_and_tafsir()
    if verse_message:
        send_message_to_telegram(verse_message)
    else:
        print("Failed to get verse or tafsir, skipping send.")
    print("Hourly task finished.")


# --- Web Server Part (To keep Replit running) ---
# This part makes the Repl act like a mini website.
# We will use an external service (UptimeRobot) to visit this website
# every hour, which will trigger our code to run.

# --- Web Server Part (To keep Replit running) ---
# This part makes the Repl act like a mini website.
# We will use an external service (UptimeRobot) to visit this website
# every hour, which will trigger our code to run.


class RequestHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        # Handle HEAD requests (often used by uptime monitors like UptimeRobot free tier)
        if self.path == '/run':
            self.send_response(200)  # Send 'OK' status
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            # --- Crucially, still trigger the task ---
            print("HEAD request received for /run, triggering task...")
            send_hourly_verse()
            # --- Do NOT send a body (no self.wfile.write) for HEAD ---
        else:
            # Respond successfully for other paths too, without a body
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            print(f"HEAD request received for {self.path}")

    def do_GET(self):
        # Handle regular GET requests (like from a browser or paid UptimeRobot)
        if self.path == '/run':
            self.send_response(200)  # Send 'OK' status
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(
                b"Task triggered successfully!")  # Send body for GET

            # --- Trigger the actual work ---
            print("GET request received for /run, triggering task...")
            send_hourly_verse()

        else:
            # Respond with a simple message for any other GET URL visits
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(
                b"Quran Bot Runner - Use /run endpoint to trigger.")
            print(f"GET request received for {self.path}")


# The rest of your code (get_random_verse_and_tafsir, send_message_to_telegram,
# send_hourly_verse, run_server, if __name__ == "__main__":...)
# should remain unchanged below this class definition.


def run_server(server_class=HTTPServer,
               handler_class=RequestHandler,
               port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()


# --- Main Execution ---
if __name__ == "__main__":
    # Check if 'server.py' or similar isn't being used to run this,
    # This is a simple check for Replit's typical run environment.
    # If run directly (like clicking 'Run' button), it starts the server.
    print("Script starting...")
    run_server()  # Start the web server to listen for UptimeRobot

    # If you wanted to test sending just ONCE without the server,
    # you could temporarily comment out `run_server()`
    # and uncomment the line below:
    # send_hourly_verse()
