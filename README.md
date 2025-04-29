## 📖 Quran Verse & Tafsir Notifier Bot

This Python script sends a **random Quran verse**, its **Tafsir Al-Muyassar**, and a **Quranic recitation (audio)** to a Telegram chat/channel **every hour**, using a webhook trigger (e.g. via UptimeRobot). The message is sent as a **single Telegram audio message** with the verse and tafsir as a caption — to avoid spamming users with multiple messages.

---

### 🔊 Example Output

A sample message received in Telegram:

```
Abdul Basit – An-Naml, Ayah 69 (27:69).mp3 *playable*
﴿قُلْ سِيرُوا فِي الْأَرْضِ فَانْظُرُوا كَيْفَ كَانَ عَاقِبَةُ الْمُجْرِمِينَ﴾

📖 [سُورَةُ النَّمۡلِ، الآية: 69] (السورة 27)

-- التفسير الميسر --
قل -أيها الرسول- لهؤلاء المكذبين: سيروا في الأرض، فانظروا إلى ديار مَن كان قبلكم من المجرمين، كيف كان عاقبة المكذبين للرسل؟ أهلكهم الله بتكذيبهم، والله فاعل بكم مثلهم إن لم تؤمنوا.

📘 أكمل القراءة / تفسير ابن كثير (https://quran.ksu.edu.sa/tafseer/katheer-saadi/sura27-aya69.html)
```

For more samples, check my telegram channel running on this bot: https://t.me/quraan_hourly_30

🎧 *With Abdul Basit recitation attached as audio.*

---

### ✨ Features

- ✅ Sends a **single audio message** with caption (verse + tafsir)
- ✅ Pulls **random ayah** every time (from any surah)
- ✅ Uses [alquran.cloud](https://alquran.cloud) API for Quran and Tafsir
- ✅ Audio from [Islamic.network CDN](https://cdn.islamic.network/quran/audio)
- ✅ Includes a **link to Ibn Kathir tafsir** for deeper reading
- ✅ Lightweight — works great with platforms like **UptimeRobot**

---

### ⚙️ How it Works

1. A random verse (1–6236) is picked.
2. Verse text and Tafsir Al-Muyassar are fetched via [alquran.cloud API](https://alquran.cloud).
3. A corresponding recitation audio is built using:
   ```
   https://cdn.islamic.network/quran/audio/192/ar.abdulbasitmurattal/{verse_number}.mp3
   ```
4. A message is built with the verse, tafsir, and a link to Ibn Kathir’s tafsir on [quran.ksu.edu.sa](https://quran.ksu.edu.sa).
5. The message is sent via Telegram **as a single audio post with caption**.

---

### 📦 Setup Instructions

1. **Clone this repo**:
   ```bash
   git clone https://github.com/your-username/quran-hourly-bot.git
   cd quran-hourly-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install requests
   ```

3. **Set your environment variables** (in `.env` or system env):
   ```
   BOT_TOKEN=your_telegram_bot_token
   CHAT_ID=@your_channel_or_user_id
   ```

4. **Run the script**:
   ```bash
   python main.py
   ```

5. **Trigger via webhook (e.g. UptimeRobot)**:
   - Deploy on a platform like **Render**, **Replit**, or **Glitch**
   - Set the UptimeRobot monitor to ping `https://yourdomain.com/run` every hour

---

### 🧪 Test Manually

You can test manually by visiting:

```
https://yourdomain.com/run
```

This will instantly trigger the sending of one verse and tafsir.

---

### 🛠 Technologies Used

- Python 3
- [AlQuran Cloud API](https://alquran.cloud)
- [Islamic Network Audio API](https://cdn.islamic.network)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- `requests`, `http.server`

---

### 📌 Customization

- You can **replace the reciter** by changing the audio URL to another supported reciter.
- The tafsir can be swapped to another translation if supported by [alquran.cloud](https://alquran.cloud/docs).
- Truncation is applied automatically if the caption gets too long (>1024 characters).

---

### 🤲 Contributing

Note that parts of this project as well as the readme you're currently reading is made by AI, since I'm a doctor, not a programmer.
However, pull requests and improvements are welcome!  
Feel free to fork and enhance — whether it's adding new features, fixing bugs, or supporting new languages/translations.

---

### 📜 License

This project is open-source and free to use under the *I don't know, probably MIT, I didn't create the license file in this project :'( .
