import os
import sys
import platform
import hashlib
import base64
import urllib.parse
import random
import string
import uuid
import subprocess
import requests
import json
import time
import psutil
import shutil

# ====== Load Config ======
CONFIG_FILE = "config.json"
VT_API_KEY = ""
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            VT_API_KEY = config.get("VT_API_KEY", "")
    except Exception as e:
        print(f"[!] Gagal baca config.json: {e}")

# ====== Util ======
def color(txt, c):
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "reset": "\033[0m"
    }
    return f"{colors.get(c, '')}{txt}{colors['reset']}"

def banner():
    print("""
\033[92m
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
╚██████╗   ██║   ██████╔╝███████╗██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝\033[0m
\033[94m 
 ███████╗██████╗ ██╗   ██╗
 ██╔════╝██╔══██╗██║   ██║
 █████╗  ██║  ██║██║   ██║
 ██╔══╝  ██║  ██║██║   ██║
 ███████╗██████╔╝╚██████╔╝
 ╚══════╝╚═════╝  ╚═════╝ \033[0m
\033[95m          By Wildan Sec\033[0m
""")



# ====== Features ======
def system_info():
   import psutil
import shutil

def os_banner():
    os_name = platform.system().lower()

    if "windows" in os_name:
        return color(r"""
██████╗ ██╗   ██╗██████╗ ██╗     ██╗██╗  ██╗
██╔══██╗██║   ██║██╔══██╗██║     ██║██║ ██╔╝
██████╔╝██║   ██║██████╔╝██║     ██║█████╔╝ 
██╔═══╝ ██║   ██║██╔══██╗██║     ██║██╔═██╗ 
██║     ╚██████╔╝██████╔╝███████╗██║██║  ██╗
╚═╝      ╚═════╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝
        """, "cyan")

    elif "linux" in os_name:
        # cek distro
        try:
            import distro
            dist = distro.id().lower()
        except:
            dist = "linux"

        if "kali" in dist:
            return color(r"""
███╗   ███╗██╗███████╗
████╗ ████║██║██╔════╝
██╔████╔██║██║█████╗  
██║╚██╔╝██║██║██╔══╝  
██║ ╚═╝ ██║██║███████╗
╚═╝     ╚═╝╚═╝╚══════╝

        """, "blue")

        elif "ubuntu" in dist:
            return color(r"""
██╗  ██╗ █████╗ ██╗     ██╗
██║ ██╔╝██╔══██╗██║     ██║
█████╔╝ ███████║██║     ██║
██╔═██╗ ██╔══██║██║     ██║
██║  ██╗██║  ██║███████╗██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝
        """, "white")
        else:
            return color(r"""
██████╗ ███████╗██╗  ██╗
██╔══██╗██╔════╝╚██╗██╔╝
██████╔╝█████╗   ╚███╔╝ 
██╔══██╗██╔══╝   ██╔██╗ 
██║  ██╗███████╗██╔╝ ██╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """, "green")

    else:
        return color("[?] OS Tidak dikenali", "red")


def system_info():
    print(color("\n[+] Info Sistem", "yellow"))
    print(os_banner())  # tampilkan banner sesuai OS

    # info dasar
    print("OS :", platform.system(), platform.release())
    print("Versi Python:", platform.python_version())
    print("User:", os.getenv("USER") or os.getenv("USERNAME"))

    # RAM info
    ram = psutil.virtual_memory()
    print(f"RAM Total   : {ram.total // (1024**3)} GB")
    print(f"RAM Tersisa : {ram.available // (1024**3)} GB")

    # Storage info
    total, used, free = shutil.disk_usage("/")
    print(f"Storage Total: {total // (1024**3)} GB")
    print(f"Storage Free : {free // (1024**3)} GB")



def hashing_tools():
    text = input("Masukkan teks: ")
    print("MD5   :", hashlib.md5(text.encode()).hexdigest())
    print("SHA1  :", hashlib.sha1(text.encode()).hexdigest())
    print("SHA256:", hashlib.sha256(text.encode()).hexdigest())

def checksum_file():
    path = input("Path file: ")
    if not os.path.exists(path):
        print(color("File tidak ditemukan!", "red"))
        return
    with open(path, "rb") as f:
        data = f.read()
    print("MD5   :", hashlib.md5(data).hexdigest())
    print("SHA1  :", hashlib.sha1(data).hexdigest())
    print("SHA256:", hashlib.sha256(data).hexdigest())

def base64_tools():
    pilih = input("[1] Encode [2] Decode : ")
    teks = input("Masukkan teks: ")
    if pilih == "1":
        print("Encode:", base64.b64encode(teks.encode()).decode())
    else:
        try:
            print("Decode:", base64.b64decode(teks).decode())
        except:
            print(color("Input bukan Base64 valid!", "red"))

def url_tools():
    pilih = input("[1] Encode [2] Decode : ")
    teks = input("Masukkan teks/url: ")
    if pilih == "1":
        print("Encode:", urllib.parse.quote(teks))
    else:
        print("Decode:", urllib.parse.unquote(teks))

def password_gen():
    panjang = int(input("Panjang password: "))
    chars = string.ascii_letters + string.digits + string.punctuation
    pwd = ''.join(random.choice(chars) for _ in range(panjang))
    print("Password:", pwd)

def password_strength():
    pwd = input("Masukkan password: ")
    score = 0
    if any(c.islower() for c in pwd): score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in string.punctuation for c in pwd): score += 1
    if len(pwd) >= 12: score += 1
    levels = ["Lemah", "Sedang", "Kuat", "Sangat Kuat", "Super Aman"]
    print("Kekuatan password:", levels[min(score, len(levels)-1)])

def uuid_gen():
    print("UUID v4:", str(uuid.uuid4()))

def ping_host():
    host = input("Masukkan host/IP: ")
    os.system(f"ping -c 4 {host}" if platform.system() != "Windows" else f"ping {host}")

def geoip_lookup():
    ip = input("Masukkan IP/domain: ")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        if r["status"] == "success":
            print("Negara :", r["country"])
            print("Kota    :", r["city"])
            print("ISP     :", r["isp"])
        else:
            print(color("Gagal lookup!", "red"))
    except Exception as e:
        print(color(f"Error: {e}", "red"))

def http_headers():
    url = input("Masukkan URL: ")
    try:
        r = requests.get(url)
        for k, v in r.headers.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(color(f"Error: {e}", "red"))

def virus_total():
    if not VT_API_KEY:
        print(color("API Key VirusTotal tidak ditemukan di config.json!", "red"))
        return
    pilih = input("[1] Scan URL [2] Scan File Hash : ")
    if pilih == "1":
        url = input("Masukkan URL: ")
        params = {"apikey": VT_API_KEY, "resource": url}
    else:
        h = input("Masukkan Hash (MD5/SHA256): ")
        params = {"apikey": VT_API_KEY, "resource": h}
    try:
        r = requests.get("https://www.virustotal.com/vtapi/v2/url/report", params=params)
        data = r.json()
        if data.get("positives") is not None:
            print("Deteksi:", data["positives"], "/", data["total"])
            print("Link laporan:", data.get("permalink"))
        else:
            print("Tidak ada hasil.")
    except Exception as e:
        print(color(f"Error: {e}", "red"))

def caesar_cipher():
    teks = input("Masukkan teks: ")
    shift = int(input("Shift (angka): "))
    mode = input("[E]ncrypt / [D]ecrypt : ").lower()
    hasil = ""
    for c in teks:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            if mode == "e":
                hasil += chr((ord(c) - base + shift) % 26 + base)
            else:
                hasil += chr((ord(c) - base - shift) % 26 + base)
        else:
            hasil += c
    print("Hasil:", hasil)

def list_files():
    path = input("Folder path: ")
    if not os.path.exists(path):
        print(color("Folder tidak ditemukan!", "red"))
        return
    for f in os.listdir(path):
        fp = os.path.join(path, f)
        if os.path.isfile(fp):
            size = os.path.getsize(fp)
            print(f"{f} - {size} bytes")

def matrix_rain():
    try:
        while True:
            print("".join(random.choice("01") for _ in range(80)))
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

# ====== Menu ======
def menu():
    opsi = {
        "1": system_info,
        "2": hashing_tools,
        "3": checksum_file,
        "4": base64_tools,
        "5": url_tools,
        "6": password_gen,
        "7": password_strength,
        "8": uuid_gen,
        "9": ping_host,
        "10": geoip_lookup,
        "11": http_headers,
        "12": virus_total,
        "13": caesar_cipher,
        "14": list_files,
        "15": matrix_rain
    }
    while True:
        banner()
        print(color("""
[1] Info Sistem        [9]  Ping Host
[2] Hashing            [10] GeoIP Lookup
[3] Checksum File      [11] HTTP Header Viewer
[4] Base64 Tools       [12] VirusTotal Scanner
[5] URL Tools          [13] Caesar Cipher
[6] Password Gen       [14] List Files
[7] Password Strength  [15] Matrix Rain
[8] UUID Generator     [16] Keluar
""", "cyan"))
        pilih = input("Pilih menu: ")
        if pilih == "16":
            sys.exit()
        func = opsi.get(pilih)
        if func:
            func()
        else:
            print(color("Menu tidak valid!", "red"))
        input("\nEnter untuk lanjut...")

if __name__ == "__main__":
    menu()
