from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import m3u8
import json
import subprocess
import asyncio
import os
import sys
import threading
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import FloodWait
import helper


bot = Client(
    "bot",
    api_id=24324617,
    api_hash="8d97d6b260a67e0e9f6e5a0f8291d6f8",
    bot_token="YOUR_BOT_TOKEN_HERE"
)


@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text("👋 **Bot started successfully!**\n\nSend me a link to download.")


@bot.on_message(filters.command(["txt"]))
async def txt_handler(bot: Client, m: Message):
    try:
        if not m.reply_to_message or not m.reply_to_message.document:
            await m.reply_text("⚠️ Please reply to a TXT file containing links.")
            return

        txt_path = await m.reply_to_message.download()
        with open(txt_path, "r") as file:
            links = [line.strip() for line in file if line.strip()]

        await m.reply_text(f"✅ Total {len(links)} links found in TXT file.\nNow send name with '|'.")
        os.remove(txt_path)

    except Exception as e:
        await m.reply_text(f"❌ Error processing TXT file:\n\n`{e}`")


@bot.on_message(filters.text & ~filters.command(["start", "txt"]))
async def handle_message(bot: Client, m: Message):
    try:
        raw_text = m.text
        if "|" in raw_text:
            links = raw_text.split("|")[0].strip().split("\n")
            name = raw_text.split("|")[1].strip()
        else:
            await m.reply_text("❌ Invalid input format. Please send as:\n`url | filename`")
            return

        count = 1
        for url in links:
            url = url.strip()
            if not url:
                continue

            try:
                if "rwa-play-on.vercel.app/proxy" in url:
                    Show = (
                        f"📥 DOWNLOADING...\n\n"
                        f"┌──📦 Summary\n"
                        f"│   ├── 🔗 Total Links: {len(links)}\n"
                        f"│   └── ⏳ Current File: {str(count).zfill(3)}\n"
                        f"┌──📄 File Details\n"
                        f"│   ├── 📝 Name: {name}\n"
                        f"│   ├── 🔗 URL: Chill maar bhai 😎\n"
                        f"└── 🤖 Powered by: SAKSHAM\n\n"
                        f"✅ File is downloading... Please wait ⏳"
                    )
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_pdf_proxy(url, f"{name}.pdf")
                    await prog.delete(True)
                    await helper.send_vid(bot, m, "", res_file, "", name, prog)
                    count += 1
                    await asyncio.sleep(1)
                    continue

                elif ".pdf" in url:
                    Show = (
                        f"📥 DOWNLOADING...\n\n"
                        f"┌──📦 Summary\n"
                        f"│   ├── 🔗 Total Links: {len(links)}\n"
                        f"│   └── ⏳ Current File: {str(count).zfill(3)}\n"
                        f"┌──📄 File Details\n"
                        f"│   ├── 📝 Name: {name}\n"
                        f"│   ├── 🔗 URL: Chill maar bhai 😎\n"
                        f"└── 🤖 Powered by: SAKSHAM\n\n"
                        f"✅ File is downloading... Please wait ⏳"
                    )
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_pdf(url, f"{name}.pdf")
                    await prog.delete(True)
                    await helper.send_vid(bot, m, "", res_file, "", name, prog)
                    count += 1
                    await asyncio.sleep(1)
                    continue

                elif "m3u8" in url:
                    Show = (
                        f"📥 DOWNLOADING...\n\n"
                        f"┌──📦 Summary\n"
                        f"│   ├── 🔗 Total Links: {len(links)}\n"
                        f"│   └── ⏳ Current File: {str(count).zfill(3)}\n"
                        f"┌──📄 File Details\n"
                        f"│   ├── 📝 Name: {name}\n"
                        f"│   ├── 🔗 URL: Chill maar bhai 😎\n"
                        f"└── 🤖 Powered by: SAKSHAM\n\n"
                        f"✅ File is downloading... Please wait ⏳"
                    )
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_m3u8_video(url, name)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, "", res_file, "", name, prog)
                    count += 1
                    await asyncio.sleep(1)
                    continue
            
