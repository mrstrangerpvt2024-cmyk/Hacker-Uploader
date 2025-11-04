import os 
import subprocess
import mmap
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import logging
import subprocess
import datetime
import asyncio
import os
import requests
import time
from p_bar import progress_bar
import aiohttp
import aiofiles
import tgcrypto
import concurrent.futures
from pyrogram.types import Message
from pyrogram import Client, filters
from pathlib import Path
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from pyrogram.enums import ParseMode

KEY = b'^#^#&@*HDU@&@*()'
IV = b'^@%#&*NSHUE&$*#)'

def dec_url(enc_url):
    enc_url = enc_url.replace("helper://", "")
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = unpad(cipher.decrypt(b64decode(enc_url)), AES.block_size)
    return decrypted.decode('utf-8')

def split_name_enc_url(line):
    match = re.search(r"(helper://\S+)", line)
    if match:
        name = line[:match.start()].strip().rstrip(":")
        enc_url = match.group(1).strip()
        return name, enc_url
    return line.strip(), None

def decrypt_file_txt(input_file):
    output_file = "decrypted_" + input_file
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(input_file, "r", encoding="utf-8") as f, open(output_file, "w", encoding="utf-8") as out:
        for line in f:
            name, enc_url = split_name_enc_url(line)
            if enc_url:
                dec = dec_url(enc_url)
                out.write(f"{name}: {dec}\n")
            else:
                out.write(line.strip() + "\n")
    return output_file

def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def get_mps_and_keys(api_url):
    response = requests.get(api_url)
    response_json = response.json()
    mpd = response_json.get('MPD')
    keys = response_json.get('KEYS')
    return mpd, keys

def exec(cmd):
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout.decode()
    print(output)
    return output

def pull_run(work, cmds):
    with concurrent.futures.ThreadPoolExecutor(max_workers=work) as executor:
        print("Waiting for tasks to complete")
        fut = executor.map(exec, cmds)

async def aio(url, name):
    k = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(k, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return k

async def download(url, name):
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka

async def pdf_download(url, file_name, chunk_size=1024 * 10):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name

def parse_vid_info(info):
    info = info.strip().split("\n")
    new_info, temp = [], []
    for i in info:
        if "[" not in i and '---' not in i:
            i = " ".join(i.split())
            i = i.split("|")[0].split(" ", 2)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.append((i[0], i[2]))
            except:
                pass
    return new_info

def vid_info(info):
    info = info.strip().split("\n")
    new_info, temp = dict(), []
    for i in info:
        if "[" not in i and '---' not in i:
            i = " ".join(i.split())
            i = i.split("|")[0].split(" ", 3)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.update({f'{i[2]}': f'{i[0]}'})
            except:
                pass
    return new_info

# 🔹 RWA-PLAY-ON handlers
import requests
from urllib.parse import unquote

def download_pdf_proxy(url, name="Downloaded_File.pdf"):
    try:
        decoded = unquote(url)
        if "rwa-play-on.vercel.app/pdf" not in decoded:
            print("❌ Not a supported PDF link:", decoded)
            return None
        print(f"🔽 Downloading PDF from {decoded}")
        r = requests.get(decoded, allow_redirects=True, timeout=120)
        if r.status_code == 200:
            with open(name, "wb") as f:
                f.write(r.content)
            print(f"✅ Saved as {name}")
            return name
        else:
            print("❌ PDF download failed:", r.status_code)
            return None
    except Exception as e:
        print("⚠️ Error downloading PDF:", e)
        return None

def download_m3u8_proxy(url, name="Downloaded_Video.mp4"):
    try:
        decoded = unquote(url)
        if "rwa-play-on.vercel.app/proxy" not in decoded:
            print("❌ Not a supported m3u8 proxy:", decoded)
            return None
        print(f"🎥 Downloading video from {decoded}")
        cmd = f'ffmpeg -y -i "{decoded}" -c copy -bsf:a aac_adtstoasc "{name}"'
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Video saved as {name}")
        return name
    except Exception as e:
        print("⚠️ Video proxy download error:", e)
        return None
