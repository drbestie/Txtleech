# main.py
from pyrogram import Client, filters
from pyrogram.types import Message
from helpers.file_processor import process_txt_file
from helpers.downloader import download_all_links
from helpers.utils import ask_user_input, send_log

import os
import asyncio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))

app = Client("video_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_settings = {}

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply("Welcome! Send me a `.txt` file to begin downloading links.")

@app.on_message(filters.command("cookies"))
async def cookies_handler(client, message: Message):
    if message.reply_to_message and message.reply_to_message.document:
        path = await message.reply_to_message.download(file_name="cookies.txt")
        user_settings[message.from_user.id] = {"cookies": path}
        await message.reply("Cookies saved successfully.")
    else:
        await message.reply("Please reply to a cookies.txt file using /cookies")

@app.on_message(filters.document)
async def txt_file_handler(client, message: Message):
    if not message.document.file_name.endswith(".txt"):
        return await message.reply("Please send a `.txt` file.")
    
    file_path = await message.download()
    user_id = message.from_user.id

    # Ask for settings
    rename_prefix = await ask_user_input(client, message, "Enter rename prefix (or type 'no'):")
    caption_format = await ask_user_input(client, message, "Enter caption format (or type 'no'):")
    thumbnail_link = await ask_user_input(client, message, "Send thumbnail image link (or type 'no'):")
    quality = await ask_user_input(client, message, "Enter preferred video quality (e.g., 720p, 360p):")
    start_index = int(await ask_user_input(client, message, "Enter the starting link number (e.g., 11):"))

    user_data = {
        "rename_prefix": rename_prefix if rename_prefix.lower() != "no" else None,
        "caption_format": caption_format if caption_format.lower() != "no" else None,
        "thumbnail": thumbnail_link if thumbnail_link.lower() != "no" else None,
        "quality": quality,
        "start_index": start_index,
        "cookies": user_settings.get(user_id, {}).get("cookies", None)
    }

    # Process file
    processed_lines = process_txt_file(file_path)
    
    # Start downloading
    await download_all_links(client, message, processed_lines, user_data, LOG_CHANNEL)

app.run()
