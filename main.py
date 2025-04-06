from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import os

# Replace these with your credentials
API_ID = "28996064"
API_HASH = "e09920a63e5f157b85a64ddba66596c6"
BOT_TOKEN = "7547790773:AAEcERYFEe4CQBLqkWWj6BZrKfrF2oxzops"

app = Client("drm_button_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply("Send me a .txt file with video names and DRM links.")

@app.on_message(filters.document & filters.private)
async def txt_file_handler(client, message: Message):
    if not message.document.file_name.endswith(".txt"):
        await message.reply("Please send a valid .txt file.")
        return

    # Download the file
    file_path = await message.download()
    
    buttons = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    for i in range(0, len(lines), 2):  # Assuming format: name, then link
        if i + 1 < len(lines):
            name = lines[i]
            original_link = lines[i + 1]
            playable_link = f"https://dragoapi.vercel.app/video/{original_link}"
            buttons.append([InlineKeyboardButton(name, url=playable_link)])

    # Send the buttons
    if buttons:
        await message.reply("Here are your video links:", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply("No valid links found in the file.")

    # Optional: cleanup
    os.remove(file_path)

app.run()
