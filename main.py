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
#from p_bar import progress_bar
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
#from down1 import *
from vars import API_ID, API_HASH, BOT_TOKEN

# watermark_text = ""

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)



photo = "youtube.jpg"

start_ph = "image-optimisation-scaled.jpg"

api_url = "http://master-api-v3.vercel.app/"

api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
token_cp ='eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'

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
    file_name, ext = os.path.splitext(os.path.basename(y))  # Extract filename & extension

    if file_name.startswith("encrypted_"):  # ✅ Check if filename ends with "_helper"
        x = decrypt_file_txt(y)  # Decrypt the file
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
            # print(len(links)
    except:
           await m.reply_text("Invalid file input.")
           os.remove(x)
           return


    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Send Me Your Batch Name or send `df` for grabing from text filename.**")
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

    # await editable.edit("**Now Enter A text to add watermark on your uploaded pdf\n\n>>OR Send `no` for use default**")
    # input_w: Message = await bot.listen(editable.chat.id)
    # raw_textw = input_w.text
    # await input_w.delete(True)
    # if raw_textw == 'no':
    #     watermark_text = '\n'
    # else:
    #     watermark_text = raw_textw + '\n'


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

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
            elif "https://cpvod.testbook.com/" in url:
                url = url.replace("https://cpvod.testbook.com/","https://media-cdn.classplusapp.com/drm/")
                url = 'https://dragoapi.vercel.app/classplus?link=' + url
                mpd, keys = helper.get_mps_and_keys(url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])

            elif "classplusapp.com/drm/" in url:
                url = 'https://dragoapi.vercel.app/classplus?link=' + url
                mpd, keys = helper.get_mps_and_keys(url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])

            elif "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3Mjg3MDIyMDYsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiT0dweFpuWktabVl3WVdwRlExSXJhV013WVdvMlp6MDkiLCJmaXJzdF9uYW1lIjoiU0hCWVJFc3ZkbVJ0TVVSR1JqSk5WamN3VEdoYVp6MDkiLCJlbWFpbCI6ImNXbE5NRTVoTUd4NloxbFFORmx4UkhkWVV6bFhjelJTWWtwSlVVcHNSM0JDVTFKSWVGQXpRM2hsT0QwPSIsInBob25lIjoiYVhReWJ6TTJkWEJhYzNRM01uQjZibEZ4ZGxWR1p6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJla3RHYjJoYWRtcENXSFo0YTFsV2FEVlBaM042ZHowOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoidXBwZXIgdGhhbiAzMSIsImRldmljZV9tb2RlbCI6IlhpYW9NaSBNMjAwN0oxN0MiLCJyZW1vdGVfYWRkciI6IjQ0LjIyMi4yNTMuODUifX0.k_419KObeIVpLO6BqHcg8MpnvEwDgm54UxPnY7rTUEu_SIjOaE7FOzez5NL9LS7LdI_GawTeibig3ILv5kWuHhDqAvXiM8sQpTkhQoGEYybx8JRFmPw_fyNsiwNxTZQ4P4RSF9DgN_yiQ61aFtYpcfldT0xG1AfamXK4JlneJpVOJ8aG_vOLm6WkiY-XG4PCj5u4C3iyur0VM1-j-EhwHmNXVCiCz5weXDsv6ccV6SqNW2j_Cbjia16ghgX61XeIyyEkp07Nyrp7GN4eXuxxHeKcoBJB-YsQ0OopSWKzOQNEjlGgx7b54BkmU8PbiwElYgMGpjRT9bLTf3EYnTJ_wA'
                url = url.split("bcov_auth")[0]+bcov

            elif "tencdn.classplusapp" in url:
                headers = {'Host': 'api.classplusapp.com', 'x-access-token': f'{token_cp}', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
                params = (('url', f'{url}'))
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url = response.json()['url']

            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': f'{token_cp}'}).json()['url']

            elif 'media-cdn.classplusapp.com' in url or 'media-cdn-alisg.classplusapp.com' in url or 'media-cdn-a.classplusapp.com' in url:
                headers = { 'x-access-token': f'{token_cp}',"X-CDN-Tag": "empty"}
                response = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers=headers)
                url   = response.json()['url']

            elif 'encrypted.m' in url:
                appxkey = url.split('*')[1]
                url = url.split('*')[0]


            elif "allenplus" in url or "player.vimeo" in url :
             if "controller/videoplay" in url :
              url0 = "https://player.vimeo.com/video/" + url.split("videocode=")[1].split("&videohash=")[0]
              url = f"https://master-api-v3.vercel.app/allenplus-vimeo?url={url0}&authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
             else:
               url = f"https://master-api-v3.vercel.app/allenplus-vimeo?url={url}&authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"

            elif url.startswith("https://videotest.adda247.com/"):
                if url.split("/")[3] != "demo":
                    url = f'https://videotest.adda247.com/demo/{url.split("https://videotest.adda247.com/")[1]}'

            elif 'master.mpd' in url:
              #vid_id =  url.split('/')[-2]
              url =  f"{api_url}pw-dl?url={url}&token={token}&authorization={api_token}&q={raw_text2}"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                

                cc = (
                    f"🎬 VIDEO ID: {str(count).zfill(3)}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🖼️ Title: {name1}\n\n"
                    f"📁 Batch: {b_name}\n\n"
                    f"👤 Extracted By: {MR}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                )
                
                cc1 = (
                    f"🎬 VIDEO ID: {str(count).zfill(3)}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🖼️ Title: {name1}\n\n"
                    f"📁 Batch: {b_name}\n\n"
                    f"👤 Extracted By: {MR}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                )
                
                cc2 = (
                    f"🎬 VIDEO ID: {str(count).zfill(3)}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🖼️ Title: {name1}\n\n"
                    f"📁 Batch: {b_name}\n\n"
                    f"👤 Extracted By: {MR}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                )
                
                ccyt = (
                    f"🎬 VIDEO ID: {str(count).zfill(3)}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🖼️ Title: {name1}\n\n"
                    f"📁 Batch: {b_name}\n\n"
                    f"🔗 Video Link: {url}\n\n"
                    f"👤 Extracted By: {MR}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                )



                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
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


