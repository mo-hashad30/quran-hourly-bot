Note that this readme file and some parts of the script were made using AI, since I'm a doctor, not a programmer. However if you find any issues with the code, feel free to reach out or submit one!
# Telegram Qur'an Auto Bot

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python script that fetches a random verse from the Quran, the tafseer of this verse, its number and the chapter, sends it as a single message to a specified Telegram chat, channel, or user. Designed to be run periodically (e.g., hourly) using a scheduler like Render with UptimeRobot.

## Features

*   Fetches a random Quran verse number (1-6236).
*   Retrieves verse text and metadata (Surah name, Ayah number) from `api.alquran.cloud`.
*   Sends a **single message** to Telegram containing the verse text with tafseer.
*   Uses the asynchronous `python-telegram-bot` library (v20+).
*   Configured via environment variables for security (no hardcoded tokens).
*   Includes basic logging for monitoring and debugging.

## Output Example

When run, the script will send a message to your configured Telegram chat like this:

قَالُوا وَأَقْبَلُوا عَلَيْهِمْ مَاذَا تَفْقِدُونَ

📖 [سُورَةُ يُوسُفَ، الآية: 71] (السورة 12)

-- التفسير الميسر --
قال أولاد يعقوب مقبلين على المنادي: ما الذي تفقدونه؟

*(The specific verse will be random each time)*

## Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)
*   A Telegram Account
*   A Telegram Bot Token:
    *   Create a bot by talking to the `@BotFather` on Telegram.
    *   Follow the steps (`/newbot`) to get your unique API token.
*   A Telegram Chat ID:
    *   **Channel/Group:** Add your bot as an admin. Send a message in the channel/group, forward it to `@JsonDumpBot` or `@RawDataBot` on Telegram. The bot will reply with JSON data; find the `chat` -> `id` value (it usually starts with `-100...` for channels or `-` for groups).
    *   **Private Chat:** Send a message to `@JsonDumpBot` or `@RawDataBot`. It will show your user ID in the `chat` -> `id` field.
*   A hosting environment (like [Render](https://render.com/), Heroku, PythonAnywhere, VPS) or a local machine to run the script.

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(This installs `python-telegram-bot` and `requests`)*

## Configuration

The script requires two environment variables to be set:

*   `TELEGRAM_BOT_TOKEN`: Your Telegram bot's API token obtained from BotFather.
*   `TELEGRAM_CHAT_ID`: The ID of the chat, channel, or user where the messages should be sent (including the leading `-` if applicable).

**How to set environment variables:**

*   **On Render:** Go to your Service -> Environment settings and add the key-value pairs.
*   **On Linux/macOS (Terminal):**
    ```bash
    export TELEGRAM_BOT_TOKEN="YOUR_ACTUAL_BOT_TOKEN"
    export TELEGRAM_CHAT_ID="YOUR_ACTUAL_CHAT_ID"
    ```
*   **On Windows (Command Prompt):**
    ```cmd
    set TELEGRAM_BOT_TOKEN=YOUR_ACTUAL_BOT_TOKEN
    set TELEGRAM_CHAT_ID=YOUR_ACTUAL_CHAT_ID
    ```
*   **On Windows (PowerShell):**
    ```powershell
    $env:TELEGRAM_BOT_TOKEN="YOUR_ACTUAL_BOT_TOKEN"
    $env:TELEGRAM_CHAT_ID="YOUR_ACTUAL_CHAT_ID"
    ```
*   **Using a `.env` file (Recommended for local development):**
    1.  Install `python-dotenv`: `pip install python-dotenv`
    2.  Create a file named `.env` in the project root:
        ```dotenv
        TELEGRAM_BOT_TOKEN="YOUR_ACTUAL_BOT_TOKEN"
        TELEGRAM_CHAT_ID="YOUR_ACTUAL_CHAT_ID"
        ```
    3.  Ensure `.env` is listed in your `.gitignore` file to avoid committing secrets.
    4.  The provided script doesn't automatically load `.env`, you would need to add `from dotenv import load_dotenv; load_dotenv()` near the top of `send_quran_verse.py`.

**Important:** Never commit your API token or Chat ID directly into your code or public repositories.

## Usage

Once configured, you can run the script manually:

```bash
python send_quran_verse.py
