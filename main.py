import random
import telegram
import time
from datetime import datetime

# Qur'an verses (for simplicity, just a few sample verses)
quran_verses = [
    {"verse": "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "number": "1:1", "tafseer": "الآية الأولى من السورة المباركة، تعني أن الله هو الرحمان الرحيم."},
    {"verse": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "number": "1:2", "tafseer": "تعني أن الحمد كله لله سبحانه وتعالى."},
    # Add more verses here as needed
]

# Telegram bot setup
bot_token = '8191491312:AAFGT5qYiwens2MEcB9Em0gMlW-ERd1NMvE'  # Replace with your bot token
channel_username = '@quraan_hourly_30'  # Replace with your channel username

# Create the bot
bot = telegram.Bot(token=bot_token)

def send_random_verse():
    verse = random.choice(quran_verses)
    message = f"الآية: {verse['verse']}\nرقم الآية: {verse['number']}\nالتفسير: {verse['tafseer']}"
    bot.send_message(chat_id=channel_username, text=message)

# Send verse every hour
while True:
    send_random_verse()
    time.sleep(3600)  # Wait for one hour before sending the next verse
