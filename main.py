from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import m3u8
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import FloodWait
from pyromod import listen
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from logger import logging
import time
import asyncio
import sys
import re
import os
import urllib.parse
import tgcrypto
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from helper import *
from pyrogram.enums import ParseMode
from vars import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

photo = "youtube.jpg"
start_ph = "image-optimisation-scaled.jpg"

api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
token_cp = "eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9"


@bot.on_message(filters.command("start"))
async def start_handler(bot: Client, m: Message):
    welcome_text = (
        "📦 **TXT File Downloader Bot**\n\n"
        "**📁 Bot Root**\n"
        "├── 👋 **Welcome!**\n"
        "│   └── 🤖 I’m your one and only TXT File Downloader Bot\n"
        "├── 📌 **What I Can Do:**\n"
        "│   ├── 🔸 Clean TXT file downloads\n"
        "│   ├── 🔸 Fast, smooth & user-friendly\n"
        "│   └── 🔸 Zero ads, zero BS 🚫\n"
        "├── 🚀 **How To Use:**\n"
        "│   ├── 👉 Send `/txt` to start\n"
        "│   └── 🛑 Send `/stop` to stop me\n"
        "├── 💡 **Pro Tip:**\n"
        "│   └── I'm getting better every day 😎\n"
        "└── 🔥 **Ready to go? Let's begin!**"
    )
    await m.reply_photo(photo=start_ph, caption=welcome_text)


@bot.on_message(filters.command("stop"))
async def stop_handler(_, m: Message):
    await m.reply_text("🚦STOPPED🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["txt"]))
async def txt_handler(bot: Client, m: Message):
    await m.reply_text("📄 **Please send me the TXT file URL or upload your TXT file.**")

@bot.on_message(filters.text & filters.incoming)
async def url_handler(bot: Client, m: Message):
    try:
        url = m.text.strip()
        name = "downloaded_file"

        if url.endswith(".txt"):
            await m.reply_text("📥 Downloading TXT file...")
            file_path = await helper.download_txt(url, name)
            await m.reply_document(document=file_path, caption="✅ TXT file downloaded successfully!")
            os.remove(file_path)

        elif ".pdf" in url:
            await m.reply_text("📚 Downloading PDF file...")
            pdf_path = await helper.download_pdf(url, f"{name}.pdf")
            await m.reply_document(document=pdf_path, caption="✅ PDF downloaded successfully!")
            os.remove(pdf_path)

        elif ".mp4" in url or "video" in url:
            await m.reply_text("🎬 Downloading video, please wait...")
            video_path = await helper.download_video(url, f"{name}.mp4")
            await m.reply_document(document=video_path, caption="✅ Video downloaded successfully!")
            os.remove(video_path)

        else:
            await m.reply_text("⚠️ Unsupported link or file type!")

    except Exception as e:
        await m.reply_text(f"❌ **Error:** `{e}`")

@bot.on_message(filters.document)
async def document_handler(bot: Client, m: Message):
    try:
        document = m.document
        file_name = document.file_name
        file_path = await bot.download_media(document)

        await m.reply_text(f"📂 File `{file_name}` received and saved successfully!")
        await asyncio.sleep(2)

        if file_name.endswith(".txt"):
            await m.reply_text("📤 Uploading your TXT file to process...")
            processed_file = await helper.process_txt(file_path)
            await m.reply_document(document=processed_file, caption="✅ Processed TXT file.")
            os.remove(processed_file)

        elif file_name.endswith(".pdf"):
            await m.reply_text("📤 Processing your PDF file...")
            processed_pdf = await helper.process_pdf(file_path)
            await m.reply_document(document=processed_pdf, caption="✅ Processed PDF file.")
            os.remove(processed_pdf)

        else:
            await m.reply_text("⚠️ Unsupported file type. Please send a TXT or PDF file.")

        os.remove(file_path)

    except Exception as e:
        await m.reply_text(f"❌ **Error while handling document:** `{e}`")
        
@bot.on_message(filters.command(["status"]))
async def status_handler(bot: Client, m: Message):
    try:
        await m.reply_text("🔍 Checking server status...")
        async with ClientSession() as session:
            async with session.get(f"{api_url}status", headers={"Authorization": f"Bearer {api_token}"}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await m.reply_text(f"✅ **Server Status:** {data.get('status', 'unknown')}")
                else:
                    await m.reply_text("⚠️ Unable to fetch status from server.")
    except Exception as e:
        await m.reply_text(f"❌ **Status Check Failed:** `{e}`")
            
