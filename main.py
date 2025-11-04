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
    
