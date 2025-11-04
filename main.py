from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import m3u8
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from logger import logging
import time
import asyncio
from pyrogram.types import User, Message
import sys
import re
import os
import urllib
import urllib.parse
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from helper import *
from pyrogram import Client, filters
from pyrogram.types import Message
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
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
token_cp = 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'


@bot.on_message(filters.command("start"))
async def account_login(bot: Client, m: Message):
    welcome_text = (
        f"📦 **TXT File Downloader Bot**\n\n"
        f"**📁 Bot Root**\n"
        f"├── **👋 WELCOME!**\n"
        f"│   └── 🤖 **I’m your one and only TXT File Downloader Bot**\n"
        f"├── **📌 What I Can Do:**\n"
        f"│   ├── 🔸 **Clean TXT file downloads**\n"
        f"│   ├── 🔸 **Fast, smooth & user-friendly**\n"
        f"│   └── 🔸 **Zero ads, zero BS 🚫**\n"
        f"├── **🚀 How To Use:**\n"
        f"│   ├── 👉 Send `/txt` to start\n"
        f"│   └── 🛑 Send `/stop` to stop me\n"
        f"├── **💡 Pro Tip:**\n"
        f"│   └── **I'm getting better every day 😎**\n"
        f"└── **🔥 Ready to go? Let's begin!**"
    )

    await m.reply_photo(photo=start_ph, caption=welcome_text)


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("🚦STOPPED🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["txt"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "📂✨ **Please Send Your TXT File for Download** ✨📂\n"
        "📌 Only `.txt` files are supported.\n"
        "⚡ Fast | 🔒 Secure | 💯 Hassle-Free"
    )
    input: Message = await bot.listen(editable.chat.id)
    y = await input.download()
    file_name, ext = os.path.splitext(os.path.basename(y))

    if file_name.startswith("encrypted_"):
        x = decrypt_file_txt(y)
        await input.delete(True)
    else:
        x = y

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Send Me Your Batch Name or send `df` for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    if raw_text0 == 'df':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution** `1080` , `720` , `480` , `360` , `240` , `144`")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080"
        else:
            res = "1280x720"
    except Exception:
        res = "UN"

    await editable.edit("**Now Enter A Caption to add caption on your uploaded file\n\n>>OR Send `df` for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text

    if raw_text3 == 'df':
        MR = " S A K S H A M "
    else:
        MR = raw_text3
    await input3.delete(True)

    await editable.edit("**If pw mpd links enter working token ! \n Send `no` **")
    input11: Message = await bot.listen(editable.chat.id)
    token = input11.text
    await input11.delete(True)

    await editable.edit("Now send the Thumb url For Custom Thumbnail.\nExample » `https://envs.sh/Hlb.jpg` \n Or if don't want Custom Thumbnail send = `no`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': '*/*'}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif "rwa-play-on.vercel.app/proxy" in url:
                vid_file = helper.download_m3u8_proxy(url, f"{name}.mp4")
                if vid_file:
                    await bot.send_video(chat_id=m.chat.id, video=vid_file, caption=cc)
                    count += 1
                    os.remove(vid_file)
                continue

            elif ".pdf" in url:
                try:
                    if "cwmediabkt99" in url:
                        time.sleep(2)
                        cmd = f'yt-dlp -o "{name}.pdf" "https://master-api-v3.vercel.app/cw-pdf?url={url}&authorization={api_token}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    else:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')

                except FloodWait as e:
                    await m.reply_text(str(e))
                    time.sleep(e.x)
                    continue

    except Exception as e:
        await m.reply_text(f"⚠️ Error: {str(e)}")

                 elif any(img in url.lower() for img in ['.jpeg', '.png', '.jpg']):
                        try:
                            subprocess.run(['wget', url, '-O', f'{name}.jpg'], check=True)  # Fixing this line
                            await bot.send_photo(
                                chat_id=m.chat.id,
                                caption = cc2,
                                photo= f'{name}.jpg',  )
                        except subprocess.CalledProcessError:
                            await message.reply("Failed to download the image. Please check the URL.")
                        except Exception as e:
                            await message.reply(f"An error occurred: {e}")
                        finally:
                            # Clean up the downloaded file
                            if os.path.exists(f'{name}.jpg'):
                                os.remove(f'{name}.jpg')


                elif "youtu" in url:
                    try:
                        await bot.send_photo(chat_id=m.chat.id, photo=photo, caption=ccyt)
                        count += 1
                    except Exception as e:
                        await m.reply_text(str(e))
                        await asyncio.sleep(1)
                        continue

                elif ".ws" in url and  url.endswith(".ws"):
                        try :
                            await helper.pdf_download(f"{api_url}utkash-ws?url={url}&authorization={api_token}",f"{name}.html")
                            time.sleep(1)
                            await bot.send_document(chat_id=m.chat.id, document=f"{name}.html", caption=cc1)
                            os.remove(f'{name}.html')
                            count += 1
                            time.sleep(5)
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                            await m.reply_text(str(e))
                            continue

                elif 'encrypted.m' in url:
                   Show = (
                            f"📥 DOWNLOADING...\n\n"
                            f"┌──📦 Summary\n"
                            f"│   ├── 🔗 Total Links: {len(links)}\n"
                            f"│   └── ⏳ Current File: {str(count).zfill(3)}\n" 
                            f"┌──📄 File Details\n"
                            f"│   ├── 📝 Name: {name}\n"
                            f"│   ├── 🎞️ Quality: {raw_text2}\n"
                            f"│   ├── 🔗 URL: Chill maar bhai 😎\n"
                            f"│   └── 🖼️ Thumbnail: {input6.text}\n"
                            f"└── 🤖 Powered by:SAKSHAM \n\n"
                            f"✅ File is downloading... Please wait ⏳"
                        )
                   prog = await m.reply_text(Show)
                   res_file = await helper.download_and_decrypt_video(url, cmd, name, appxkey)
                   filename = res_file

                   await prog.delete(True)
                   await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                   count += 1
                   await asyncio.sleep(1)
                   continue

                elif 'drmcdni' in url or 'drm/wv' in url:
                    Show = (
                            f"📥 DOWNLOADING...\n\n"
                            f"┌──📦 Summary\n"
                            f"│   ├── 🔗 Total Links: {len(links)}\n"
                            f"│   └── ⏳ Current File: {str(count).zfill(3)}\n"    
                            f"┌──📄 File Details\n"
                            f"│   ├── 📝 Name: {name}\n"
                            f"│   ├── 🎞️ Quality: {raw_text2}\n"
                            f"│   ├── 🔗 URL: Chill maar bhai 😎\n"
                            f"│   └── 🖼️ Thumbnail: {input6.text}\n"
                            f"└── 🤖 Powered by: SAKSHAM\n\n"
                            f"✅ File is downloading... Please wait ⏳"
                        )
                    prog = await m.reply_text(Show)

                    # Use the decrypt_and_merge_video function
                    res_file = await helper.decrypt_and_merge_video(mpd, keys_string, path, name, raw_text2)

                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    await asyncio.sleep(1)
                    continue


                else:
                    Show = (
                            f"📥 DOWNLOADING...\n\n"
                            f"┌──📦 Summary\n"
                            f"│   ├── 🔗 Total Links: {len(links)}\n"
                            f"│   └── ⏳ Current File: {str(count).zfill(3)}\n" 
                            f"┌──📄 File Details\n"
                            f"│   ├── 📝 Name: {name}\n"
                            f"│   ├── 🎞️ Quality: {raw_text2}\n"
                            f"│   ├── 🔗 URL: Chill maar bhai 😎\n"
                            f"│   └── 🖼️ Thumbnail: {input6.text}\n"
                            f"└── 🤖 Powered by: SAKSHAM\n\n"
                            f"✅ File is downloading... Please wait ⏳"
                        )
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"**downloading failed **\n\n{str(e)}\n\n**Name** - {name}\n"
                )
                count += 1
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("**🔥 Sᴜᴄᴄᴇsғᴜʟʟʏ Dᴏᴡɴʟᴏᴀᴅᴇᴅ Aʟʟ Lᴇᴄᴛᴜʀᴇs  SIR 🔥**")

import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"🌐 Web server running on port {port}")
    server.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

bot.run()


