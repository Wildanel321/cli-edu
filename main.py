import os
import sys
import platform
import hashlib
import base64
import urllib.parse
import random
import string
import uuid
import requests
import json
import time
import socket
import ipaddress
import re
import math
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

# Set UTF-8 encoding for stdout/stdin on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stdin, 'reconfigure'):
    try:
        sys.stdin.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Optional sound module for Windows
try:
    import winsound
except ImportError:
    winsound = None

# Optional packages
try:
    import psutil
except ImportError:
    psutil = None

try:
    import shutil
except ImportError:
    shutil = None

# ====== Paths & Config ======
CONFIG_FILE = "config.json"
PROFILE_FILE = "user_profile.json"
VT_API_KEY = ""

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            VT_API_KEY = config.get("VT_API_KEY", "")
    except Exception as e:
        print(f"[!] Gagal membaca config.json: {e}")

# ====== Utilities ======
def color(txt, c):
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "blue": "\033[94m",
        "white": "\033[97m",
        "gray": "\033[90m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "reset": "\033[0m"
    }
    return f"{colors.get(c, '')}{txt}{colors['reset']}"

def play_beep(freq=1200, duration=80):
    profile = load_profile()
    if profile.get("sound_enabled", False):
        if winsound and platform.system() == "Windows":
            try:
                winsound.Beep(freq, duration)
            except Exception:
                pass
        else:
            try:
                sys.stdout.write("\a")
                sys.stdout.flush()
            except Exception:
                pass

# ====== User Profile & Gamification ======
DEFAULT_PROFILE = {
    "username": "CyberAgent",
    "xp": 0,
    "level": 1,
    "sound_enabled": False,
    "quizzes_completed": 0,
    "quiz_high_score": 0,
    "tools_used": 0,
    "badges": [],
    "docs_read": []
}

ALL_BADGES = {
    "first_blood": {"name": "🎯 First Blood", "desc": "Menjalankan tool pertama di Cyber Edu"},
    "quiz_cadet": {"name": "🎓 Quiz Cadet", "desc": "Menyelesaikan kuis keamanan siber pertamamu"},
    "quiz_master": {"name": "🧠 Quiz Master", "desc": "Mendapatkan skor sempurna (100%) pada Cyber Quiz"},
    "password_sentinel": {"name": "🛡️ Password Sentinel", "desc": "Menganalisis kekuatan kata sandi dengan health checker"},
    "port_hunter": {"name": "🔍 Port Hunter", "desc": "Melakukan port scan jaringan"},
    "crypto_adept": {"name": "🔐 Crypto Adept", "desc": "Menggunakan tools enkripsi/dekripsi/hashing"},
    "subnet_guru": {"name": "🌐 Subnet Guru", "desc": "Melakukan kalkulasi subnetting CIDR"},
    "cyber_scholar": {"name": "📚 Cyber Scholar", "desc": "Membaca dokumentasi di Terminal Wiki"},
    "hokage_sec": {"name": "🌀 Hokage Sec", "desc": "Mencapai Level 5+ dalam perjalanan cybersecurity"}
}

def get_level_info(xp):
    levels = [
        (0, 1, "Script Kiddie"),
        (100, 2, "Cyber Cadet"),
        (300, 3, "Junior SecOps"),
        (600, 4, "Cyber Defender"),
        (1000, 5, "Penetration Tester"),
        (1600, 6, "Incident Commander"),
        (2500, 7, "Elite Hokage Sec")
    ]
    curr_lvl, title = 1, "Script Kiddie"
    next_xp = 100
    for min_xp, lvl, t in levels:
        if xp >= min_xp:
            curr_lvl = lvl
            title = t
        else:
            next_xp = min_xp
            break
    else:
        next_xp = xp + 1000
    return curr_lvl, title, next_xp

def load_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in DEFAULT_PROFILE.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            pass
    return DEFAULT_PROFILE.copy()

def save_profile(p):
    try:
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2)
    except Exception as e:
        print(f"[!] Gagal menyimpan profil: {e}")

def add_xp(amount, reason="Aktivitas Belajar"):
    p = load_profile()
    old_lvl, _, _ = get_level_info(p["xp"])
    p["xp"] += amount
    p["tools_used"] = p.get("tools_used", 0) + 1
    new_lvl, title, _ = get_level_info(p["xp"])
    p["level"] = new_lvl

    print(f"\n{color('[XP GAINED]', 'green')} +{amount} XP ({reason}) | Total XP: {p['xp']}")
    play_beep(1500, 60)

    if new_lvl > old_lvl:
        print(color(f"\n🎉 LEVEL UP! Kamu sekarang Level {new_lvl}: {title}! 🎉", "yellow"))
        play_beep(2000, 120)
        if new_lvl >= 5:
            unlock_badge("hokage_sec")

    save_profile(p)

def unlock_badge(badge_id):
    p = load_profile()
    badges = p.get("badges", [])
    if badge_id in ALL_BADGES and badge_id not in badges:
        badges.append(badge_id)
        p["badges"] = badges
        b_info = ALL_BADGES[badge_id]
        print(color(f"\n🏆 BADGE UNLOCKED: {b_info['name']} - {b_info['desc']}", "yellow"))
        play_beep(1800, 100)
        save_profile(p)

# ====== Cyber Quotes ======
CYBER_QUOTES = [
    ("Security is not a product, but a process.", "Bruce Schneier"),
    ("The only truly secure system is one that is powered off, cast in a block of concrete and sealed in a lead-lined room.", "Gene Spafford"),
    ("If you think technology can solve your security problems, then you don't understand the problems and you don't understand the technology.", "Bruce Schneier"),
    ("Amateurs hack systems, professionals hack people.", "Bruce Schneier"),
    ("There is no patch for human stupidity.", "Kevin Mitnick"),
    ("Passwords are like underwear: you don't let people see it, you should change it very often, and you shouldn't share it with strangers.", "Chris Pirillo"),
    ("It takes 20 years to build a reputation and few minutes of cyber-incident to ruin it.", "Stephane Nappo"),
    ("Hardware is easy to protect: lock it in a room, chain it to a desk, or buy a spare. Information poses more of a problem.", "Clifford Stoll"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("The quieter you become, the more you are able to hear.", "Kali Linux / Ram Dass")
]

def cyber_quote_generator():
    q, author = random.choice(CYBER_QUOTES)
    print(color("\n╭─────────────────────────────────────────────────────────────────────────────╮", "cyan"))
    print(f"│ {color('💬 CYBER WISDOM OF THE DAY', 'yellow'):<83}│")
    print(f"│ {color('"' + q + '"', 'white'):<83}│")
    print(f"│ {color('— ' + author, 'green'):>83}│")
    print(color("╰─────────────────────────────────────────────────────────────────────────────╯", "cyan"))

# ====== Boot Sequence Animation ======
def cyber_boot_animation():
    print(color("\033[2J\033[H", "reset"), end="") # Clear terminal
    steps = [
        ("INITIALIZING CYBER-EDU KERNEL v2.5", 0.08),
        ("CHECKING CRYPTOGRAPHIC ACCELERATORS (AES-NI / SHA-EXT)", 0.06),
        ("INITIALIZING SOCKET LAYER & PACKET FILTERS", 0.06),
        ("LOADING THREAT INTELLIGENCE SIGNATURES", 0.07),
        ("SECURING TERMINAL STREAMS & PROFILES", 0.05),
        ("MOUNTING SANDBOX VIRTUAL ENVIRONMENT", 0.06)
    ]
    
    print(color("┌──────────────────────────────────────────────────────────┐", "green"))
    print(color("│               CYBER EDU SYSTEM BOOT v2.5                 │", "green"))
    print(color("└──────────────────────────────────────────────────────────┘", "green"))

    for text, delay in steps:
        time.sleep(delay)
        print(f" {color('[ OK ]', 'green')} {text}")
        play_beep(1000 + int(delay * 5000), 20)

    # Progress bar effect
    print("\n " + color("Loading Modules: [", "cyan"), end="", flush=True)
    for _ in range(25):
        time.sleep(0.015)
        print(color("█", "green"), end="", flush=True)
    print(color("] 100% READY\n", "cyan"))
    time.sleep(0.2)

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
\033[95m       Interactive Cyber Security Suite v2.5\033[0m
""")

def os_banner():
    os_name = platform.system().lower()

    if "windows" in os_name:
        return color(r"""
██╗    ██╗██╗███╗   ██╗██████╗  ██████╗ ██╗    ██╗███████╗
██║    ██║██║████╗  ██║██╔══██╗██╔═══██╗██║    ██║██╔════╝
██║ █╗ ██║██║██╔██╗ ██║██║  ██║██║   ██║██║ █╗ ██║███████╗
██║███╗██║██║██║╚██╗██║██║  ██║██║   ██║██║███╗██║╚════██║
╚███╔███╔╝██║██║ ╚████║██████╔╝╚██████╔╝╚███╔███╔╝███████║
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝
        """, "cyan")

    elif "darwin" in os_name or "mac" in os_name:
        return color(r"""
            .:'
         __ :'__
      .'`__`-'__``.
     :__________.-'
     :_________:
      :_________`-;
       `.__.-.__.'
███╗   ███╗ █████╗  ██████╗ ██████╗ ███████╗
████╗ ████║██╔══██╗██╔════╝██╔═══██╗██╔════╝
██╔████╔██║███████║██║     ██║   ██║███████╗
██║╚██╔╝██║██╔══██║██║     ██║   ██║╚════██║
██║ ╚═╝ ██║██║  ██║╚██████╗╚██████╔╝███████║
╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
        """, "white")

    elif "linux" in os_name:
        try:
            import distro
            dist = distro.id().lower()
        except Exception:
            dist = "linux"

        if "kali" in dist:
            return color(r"""
██╗  ██╗ █████╗ ██╗     ██╗
██║ ██╔╝██╔══██╗██║     ██║
█████╔╝ ███████║██║     ██║
██╔═██╗ ██╔══██║██║     ██║
██║  ██╗██║  ██║███████╗██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝
            """, "blue")

        elif "ubuntu" in dist:
            return color(r"""
██╗   ██╗██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗
██║   ██║██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██║   ██║
██║   ██║██████╔╝██║   ██║██╔██╗ ██║   ██║   ██║   ██║
██║   ██║██╔══██╗██║   ██║██║╚██╗██║   ██║   ██║   ██║
╚██████╔╝██████╔╝╚██████╔╝██║ ╚████║   ██║   ╚██████╔╝
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝    ╚═════╝ 
            """, "yellow")

        elif "arch" in dist or "manjaro" in dist or "endeavour" in dist:
            return color(r"""
      /\
     /  \
    /\   \
   /      \
  /   ,,   \
 /   |  |  -\
/_-''    ''-_\
█████╗ ██████╗  ██████╗██╗  ██╗
██╔══██╗██╔══██╗██╔════╝██║  ██║
███████║██████╔╝██║     ███████║
██╔══██║██╔══██╗██║     ██╔══██║
██║  ██║██║  ██║╚██████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
            """, "cyan")

        elif "debian" in dist:
            return color(r"""
██████╗ ███████╗██████╗ ██╗ █████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔══██╗██║██╔══██╗████╗  ██║
██║  ██║█████╗  ██████╔╝██║███████║██╔██╗ ██║
██║  ██║██╔══╝  ██╔══██╗██║██╔══██║██║╚██╗██║
██████╔╝███████╗██████╔╝██║██║  ██║██║ ╚████║
╚═════╝ ╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
            """, "red")

        else:
            return color(r"""
   .---.
  /     \
 | () () |
  \  _  /
   /___\\
  /     \\
 ((_____))
██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗
██║     ██║████╗  ██║██║   ██║╚██╗██╔╝
██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝ 
██║     ██║██║╚██╗██║██║   ██║ ██╔██╗ 
███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗
╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝
            """, "green")

    else:
        return color(r"""
     .---.
    /  _  \
    | (_) |
    \___  /
        / /
       (_)
██╗   ██╗███╗   ██╗██╗  ██╗███╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║   ██║████╗  ██║██║ ██╔╝████╗  ██║██╔═══██╗██║    ██║████╗  ██║
██║   ██║██╔██╗ ██║█████╔╝ ██╔██╗ ██║██║   ██║██║ █╗ ██║██╔██╗ ██║
██║   ██║██║╚██╗██║██╔═██╗ ██║╚██╗██║██║   ██║██║███╗██║██║╚██╗██║
╚██████╔╝██║ ╚████║██║  ██╗██║ ╚████║╚██████╔╝╚███╔███╔╝██║ ╚████║
 ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
        [?] Sistem Operasi Tidak Teridentifikasi
        """, "magenta")

# ====== [NEW] 1. Interactive Cyber Quiz Module ======
QUIZ_QUESTIONS = [
    {
        "q": "Serangan social engineering yang memanipulasi korban melalui email tiruan institusi resmi disebut?",
        "options": ["A. SQL Injection", "B. Phishing", "C. Buffer Overflow", "D. Man-in-the-Middle"],
        "answer": "B",
        "explanation": "Phishing adalah teknik penipuan digital untuk memancing korban memberikan kredensial atau informasi sensitif."
    },
    {
        "q": "Algoritma kriptografi manakah yang merupakan Asymmetric (Public-Key) Encryption?",
        "options": ["A. AES-256", "B. DES", "C. RSA", "D. ChaCha20"],
        "answer": "C",
        "explanation": "RSA menggunakan sepasang kunci (Public Key untuk enkripsi dan Private Key untuk dekripsi)."
    },
    {
        "q": "Port default manakah yang digunakan untuk koneksi aman Secure Shell (SSH)?",
        "options": ["A. 21", "B. 22", "C. 23", "D. 25"],
        "answer": "B",
        "explanation": "Port 22 adalah port standar IANA untuk protokol SSH (Secure Shell)."
    },
    {
        "q": "Perbedaan utama antara Hashing dan Enkripsi adalah?",
        "options": [
            "A. Hashing satu arah (one-way), Enkripsi dua arah (reversible)",
            "B. Hashing menggunakan private key, Enkripsi tidak",
            "C. Enkripsi selalu menghasilkan panjang output tetap",
            "D. Hashing hanya untuk file teks"
        ],
        "answer": "A",
        "explanation": "Hash bersifat one-way (tidak dapat didekripsi kembali), sedangkan enkripsi dapat didekripsi dengan kunci yang sesuai."
    },
    {
        "q": "Vulnerabilitas web yang terjadi ketika input pengguna yang tidak disanitasi dimasukkan ke dalam query database adalah?",
        "options": ["A. Cross-Site Scripting (XSS)", "B. SQL Injection (SQLi)", "C. CSRF", "D. IDOR"],
        "answer": "B",
        "explanation": "SQL Injection memungkinkan penyerang menyisipkan perintah SQL berbahaya ke dalam query backend."
    },
    {
        "q": "Apa fungsi dari 'Salt' dalam proses hashing password?",
        "options": [
            "A. Mempercepat proses login",
            "B. Mencegah serangan Rainbow Table dan Hash Lookup",
            "C. Mengubah hash menjadi teks biasa",
            "D. Mengompres ukuran database"
        ],
        "answer": "B",
        "explanation": "Salt adalah string acak yang ditambahkan ke password sebelum di-hash untuk mencegah precomputed rainbow table attacks."
    },
    {
        "q": "Serangan jaringan di mana penyerang berada di antara komunikasi dua pihak tanpa diketahui disebut?",
        "options": ["A. DoS Attack", "B. Man-in-the-Middle (MITM)", "C. Ransomware", "D. Brute-force"],
        "answer": "B",
        "explanation": "MITM memungkinkan penyerang menyadap (eavesdrop) atau memodifikasi data yang lewat antara dua titik."
    },
    {
        "q": "Berapakah subnet mask standar dari notasi CIDR /24?",
        "options": ["A. 255.255.0.0", "B. 255.255.255.0", "C. 255.255.255.128", "D. 255.255.255.252"],
        "answer": "B",
        "explanation": "CIDR /24 mewakili 24 bit network (11111111.11111111.11111111.00000000 = 255.255.255.0)."
    },
    {
        "q": "Protokol apa yang digunakan untuk mengenkripsi lalu lintas web antara browser dan server?",
        "options": ["A. HTTP 1.1", "B. TLS/SSL (HTTPS)", "C. Telnet", "D. SNMP"],
        "answer": "B",
        "explanation": "TLS (Transport Layer Security) menyediakan enkripsi dan autentikasi end-to-end pada protokol HTTPS."
    },
    {
        "q": "Kategori keamanan manakah yang fokus pada pengumpulan data intelijen dari sumber-sumber publik terbuka?",
        "options": ["A. OSINT (Open Source Intelligence)", "B. Reverse Engineering", "C. Kernel Exploitation", "D. Hardware Hacking"],
        "answer": "A",
        "explanation": "OSINT adalah metodologi pengumpulan dan analisis informasi dari data yang tersedia secara publik/terbuka."
    }
]

def cyber_quiz():
    print(color("\n╔═══════════════════════════════════════════════════════════════════╗", "cyan"))
    print(f"║ {color('🎓 CYBER EDUCATION INTERACTIVE QUIZ', 'yellow'):<75}║")
    print(color("╚═══════════════════════════════════════════════════════════════════╝", "cyan"))
    print(color("Uji pemahaman keamanan siber Anda! Dapatkan XP dan Badge prestisius.\n", "white"))

    score = 0
    total = 5 # Mainkan 5 pertanyaan acak per sesi
    selected_questions = random.sample(QUIZ_QUESTIONS, min(total, len(QUIZ_QUESTIONS)))

    for i, q in enumerate(selected_questions, 1):
        print(color(f"┌─ Soal {i}/{total} ───────────────────────────────────────────────────", "magenta"))
        print(f"│ {color(q['q'], 'bold')}")
        print("│")
        for opt in q["options"]:
            print(f"│  {opt}")
        print(color("└──────────────────────────────────────────────────────────────", "magenta"))

        ans = input(color("👉 Jawaban Anda [A/B/C/D]: ", "yellow")).strip().upper()

        if ans == q["answer"]:
            score += 1
            print(color("✅ JAWABAN BENAR! (+20 XP)", "green"))
            play_beep(1500, 70)
        else:
            print(color(f"❌ SALAH! Jawaban yang benar adalah: {q['answer']}", "red"))
            play_beep(600, 100)

        print(color(f"💡 Penjelasan: {q['explanation']}\n", "gray"))
        time.sleep(0.3)

    percent = int((score / total) * 100)
    xp_earned = score * 20
    print(color("═══════════════════════════════════════════════════════════════════", "cyan"))
    print(f" Hasil Kuis : {score}/{total} Soal Benar ({percent}%)")
    
    p = load_profile()
    p["quizzes_completed"] = p.get("quizzes_completed", 0) + 1
    if percent > p.get("quiz_high_score", 0):
        p["quiz_high_score"] = percent
    save_profile(p)

    add_xp(xp_earned, f"Kuis Skor {percent}%")
    unlock_badge("quiz_cadet")

    if percent == 100:
        print(color("🌟 LUAR BIASA! Nilai Sempurna 100%! 🌟", "yellow"))
        unlock_badge("quiz_master")

# ====== [NEW] 2. Interactive Cheat Sheet / Terminal Wiki ======
TERMINAL_DOCS = {
    "linux": {
        "title": "🐧 Linux & Bash Essentials",
        "content": """
[ File & Navigasi ]
  ls -la               : Tampilkan semua file termasuk hidden file & permission
  cd /var/log          : Masuk ke direktori target
  pwd                  : Cetak working directory saat ini
  cat file.txt         : Tampilkan isi file teks
  tail -f /var/log/syslog : Pantau log realtime

[ Permission & User ]
  chmod 755 script.sh  : rwxr-xr-x (Owner baca/tulis/eksekusi, grup/lainnya baca/eksekusi)
  chmod +x file        : Beri izin eksekusi
  chown user:group file: Ganti kepemilikan file
  sudo su -            : Masuk ke sesi superuser / root

[ Pencarian & Filter ]
  grep -rnw "password" /etc/ : Cari rekursif string dalam file
  find / -perm -u=s 2>/dev/null : Cari binary SUID untuk audit privesc
  ps aux | grep python : Cari proses python yang sedang berjalan
  kill -9 <PID>        : Hentikan proses secara paksa
"""
    },
    "network": {
        "title": "🌐 Network & Ports Cheat Sheet",
        "content": """
[ Port Standar Penting ]
  21  : FTP (File Transfer Protocol - Cleartext)
  22  : SSH / SFTP (Secure Shell - Encrypted)
  23  : Telnet (Cleartext terminal - Rawan disadap)
  25  : SMTP (Mail routing)
  53  : DNS (Domain Name System - UDP/TCP)
  80  : HTTP (Web traffic - Unencrypted)
  443 : HTTPS (HTTP over TLS/SSL - Encrypted)
  445 : SMB (Windows File Sharing)
  3306: MySQL Database
  3389: RDP (Remote Desktop Protocol)

[ Perintah Analisis Jaringan ]
  ping -c 4 8.8.8.8    : Uji latensi koneksi ICMP
  netstat -tulnp       : Tampilkan port listening dan proses pemiliknya
  ss -tulpn            : Alternatif modern pengganti netstat
  traceroute target.com: Lacak hop router menuju target
  ip a / ifconfig      : Cek konfigurasi IP interface
"""
    },
    "owasp": {
        "title": "🛡️ OWASP Top 10 Web Vulnerabilities",
        "content": """
1. Broken Access Control: Pengguna dapat mengakses resource di luar izinnya (contoh: IDOR).
   Mitigasi: Terapkan otorisasi ketat di backend, jangan percaya parameter ID dari client.

2. Cryptographic Failures: Transmisi data sensitif tanpa enkripsi atau cipher usang.
   Mitigasi: Wajibkan HTTPS (TLS 1.3), gunakan algoritma hashing modern (Argon2/bcrypt).

3. Injection (SQLi, Command Injection, LDAP):
   Mitigasi: Gunakan Parameterized Queries (Prepared Statements) dan ORM.

4. Insecure Design: Celah arsitektural sebelum kode ditulis.
   Mitigasi: Terapkan Threat Modeling dan Secure Development Lifecycle (SDLC).

5. Security Misconfiguration: Konfigurasi default, debug mode aktif di production, header bocor.
   Mitigasi: Hardening server, nonaktifkan directory listing, hapus default credentials.

6. Vulnerable and Outdated Components: Menggunakan library atau framework yang punya CVE.
   Mitigasi: Software Composition Analysis (SCA), patch update berkala.

7. Identification & Authentication Failures: Password lemah, tidak ada rate limiting, session hijacking.
   Mitigasi: Multi-Factor Authentication (MFA), lockout policy, session token acak.
"""
    },
    "crypto": {
        "title": "🔐 Cryptography & Hashing Fundamentals",
        "content": """
[ Konsep Dasar ]
- Encoding (Base64, Hex): Mengubah format data agar mudah ditransmisikan. BUKAN keamanan!
- Hashing (SHA256, bcrypt): Komputasi satu arah (one-way) untuk integritas & verifikasi.
- Encryption: Mengamankan pesan dengan kunci agar hanya pihak berwenang yang bisa membaca.

[ Simetris vs Asimetris ]
- Simetris (AES, ChaCha20): Satu kunci rahasia untuk enkripsi & dekripsi. Sangat cepat.
- Asimetris (RSA, ECC): Sepasang kunci (Public Key menyebarkan, Private Key mendekripsi).

[ Password Hashing Standar Modern ]
- Hindari: MD5, SHA1 (Sudah rentan collision & brute force super cepat).
- Gunakan: Argon2id, bcrypt, PBKDF2 (Memory-hard & dilengkapi work factor/salt).
"""
    },
    "git": {
        "title": "🐙 Git Commands Quick Reference",
        "content": """
[ Manajemen Repository ]
  git init             : Inisialisasi repo git baru
  git clone <url>      : Download salinan repository dari remote
  git status           : Cek status file yang dimodifikasi

[ Staging & Committing ]
  git add .            : Stage seluruh perubahan
  git commit -m "msg"  : Rekam perubahan ke riwayat commit
  git log --oneline -10: Lihat riwayat commit ringkas

[ Branching & Syncing ]
  git branch -M main   : Ganti nama branch utama ke main
  git checkout -b fitur: Buat dan pindah ke branch baru
  git pull origin main : Ambil dan gabungkan perubahan dari server
  git push origin main : Unggah commit lokal ke remote repository
"""
    }
}

def terminal_docs(selected_topic=None):
    if not selected_topic:
        print(color("\n╔═══════════════════════════════════════════════════════════════════╗", "cyan"))
        print(f"║ {color('📖 INTERACTIVE TERMINAL WIKI & CHEAT SHEET', 'yellow'):<75}║")
        print(color("╚═══════════════════════════════════════════════════════════════════╝", "cyan"))
        print("Pilih topik dokumentasi yang ingin dipelajari:")
        print("  [1] Linux & Bash Essentials (linux)")
        print("  [2] Network & Ports Cheat Sheet (network)")
        print("  [3] OWASP Top 10 Web Vulnerabilities (owasp)")
        print("  [4] Cryptography & Hashing Fundamentals (crypto)")
        print("  [5] Git Commands Quick Reference (git)")
        choice = input(color("\nPilih nomor/nama topik: ", "yellow")).strip().lower()
        topic_map = {"1": "linux", "2": "network", "3": "owasp", "4": "crypto", "5": "git"}
        selected_topic = topic_map.get(choice, choice)

    doc = TERMINAL_DOCS.get(selected_topic)
    if not doc:
        print(color(f"❌ Topik '{selected_topic}' tidak ditemukan! Pilihan: linux, network, owasp, crypto, git", "red"))
        return

    print(color(f"\n═══ {doc['title']} ═══", "green"))
    print(color(doc["content"], "white"))

    p = load_profile()
    read_list = p.get("docs_read", [])
    if selected_topic not in read_list:
        read_list.append(selected_topic)
        p["docs_read"] = read_list
        save_profile(p)
        add_xp(15, f"Membaca Dokumen {selected_topic.upper()}")
        unlock_badge("cyber_scholar")

# ====== [NEW] 3. Advanced Password Health & Brute-force Checker ======
def calculate_crack_time(combinations, speed_per_sec):
    if speed_per_sec <= 0:
        return "Unknown"
    seconds = combinations / speed_per_sec
    if seconds < 0.001:
        return "< 1 milidetik (Instan ⚡)"
    elif seconds < 1:
        return f"{seconds*1000:.1f} milidetik"
    elif seconds < 60:
        return f"{seconds:.1f} detik"
    elif seconds < 3600:
        return f"{seconds/60:.1f} menit"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} jam"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} hari"
    elif seconds < 31536000 * 100:
        return f"{seconds/31536000:.1f} tahun"
    elif seconds < 31536000 * 1000000:
        return f"{seconds/(31536000*1000):.1f} ribu tahun"
    else:
        trillions = seconds / (31536000 * 10**12)
        return f"{trillions:.2e} Triliun Tahun 🔒"

def password_health_checker(pwd=None):
    print(color("\n╔═══════════════════════════════════════════════════════════════════╗", "cyan"))
    print(f"║ {color('🛡️ ADVANCED PASSWORD HEALTH & BRUTE-FORCE CHECKER', 'yellow'):<75}║")
    print(color("╚═══════════════════════════════════════════════════════════════════╝", "cyan"))
    
    if not pwd:
        pwd = input("Masukkan password untuk diuji: ")

    if not pwd:
        print(color("Password tidak boleh kosong!", "red"))
        return

    length = len(pwd)
    has_lower = any(c.islower() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_digits = any(c.isdigit() for c in pwd)
    has_symbols = any(c in string.punctuation for c in pwd)

    pool_size = 0
    if has_lower: pool_size += 26
    if has_upper: pool_size += 26
    if has_digits: pool_size += 10
    if has_symbols: pool_size += 32

    # Entropy H = L * log2(R)
    entropy = length * math.log2(pool_size) if pool_size > 0 else 0
    total_combinations = pool_size ** length if pool_size > 0 else 0

    # Common word checks
    COMMON_BAD = ["password", "123456", "admin", "qwerty", "iloveyou", "secret", "root", "pass123", "bismillah"]
    is_common = any(bad in pwd.lower() for bad in COMMON_BAD)

    score = 0
    feedback = []

    if length >= 12: score += 25
    elif length >= 8: score += 15
    else: feedback.append("Panjang kurang dari 8 karakter (terlalu pendek)")

    if has_lower and has_upper: score += 25
    else: feedback.append("Campurkan huruf besar dan huruf kecil")

    if has_digits: score += 25
    else: feedback.append("Tambahkan kombinasi angka")

    if has_symbols: score += 25
    else: feedback.append("Tambahkan simbol/karakter khusus (!@#$ dll)")

    if is_common:
        score = max(5, score - 40)
        feedback.append("Mengandung kata sandi pasaran yang umum ditebak")

    # Grades
    if score >= 90 and entropy >= 60: grade, grade_color = "A+ (SUPER AMAN)", "green"
    elif score >= 75 and entropy >= 50: grade, grade_color = "A (KUAT)", "green"
    elif score >= 50: grade, grade_color = "B (SEDANG)", "yellow"
    elif score >= 30: grade, grade_color = "C (LEMAH)", "red"
    else: grade, grade_color = "F (SANGAT RENTAN)", "red"

    print(color("\n[+] Laporan Kesehatan Password:", "green"))
    print(f"  Panjang Karakter : {length}")
    print(f"  Character Pool   : {pool_size} variasi karakter")
    print(f"  Entropi Bit      : {entropy:.2f} bits")
    print(f"  Skor Keamanan    : {score}/100 -> Grade: {color(grade, grade_color)}")

    print(color("\n[+] Estimasi Waktu Retas (Brute-Force Cracking Time):", "yellow"))
    print(f"  👉 Online Attack (100 req/detik)        : {calculate_crack_time(total_combinations, 100)}")
    print(f"  👉 Standar PC / CPU (100 Ribu hash/detik): {calculate_crack_time(total_combinations, 100000)}")
    print(f"  👉 Fast GPU Rig (100 Miliar hash/detik) : {calculate_crack_time(total_combinations, 100000000000)}")
    print(f"  👉 Supercomputer Cluster (100 Triliun/s): {calculate_crack_time(total_combinations, 100000000000000)}")

    if feedback:
        print(color("\n[!] Rekomendasi Penguatan:", "cyan"))
        for fb in feedback:
            print(f"  • {fb}")

    p = load_profile()
    add_xp(10, "Password Health Check")
    unlock_badge("password_sentinel")

# ====== [NEW] 4. User Progress & Status Dashboard ======
def progress_tracker():
    p = load_profile()
    lvl, title, next_xp = get_level_info(p["xp"])
    
    print(color("\n╔═══════════════════════════════════════════════════════════════════╗", "cyan"))
    print(f"║ {color('🏆 PROFIL & LEARNING PROGRESS DASHBOARD', 'yellow'):<75}║")
    print(color("╚═══════════════════════════════════════════════════════════════════╝", "cyan"))
    
    print(f"  Agent Name   : {color(p.get('username', 'CyberAgent'), 'bold')}")
    print(f"  Pangkat      : {color(f'Level {lvl} - {title}', 'green')}")
    print(f"  Total XP     : {color(str(p.get('xp', 0)), 'yellow')} XP (Next Level: {next_xp} XP)")
    print(f"  Tools Digunakan: {p.get('tools_used', 0)} kali")
    print(f"  Kuis Selesai : {p.get('quizzes_completed', 0)} sesi (High Score: {p.get('quiz_high_score', 0)}%)")
    print(f"  Docs Dibaca  : {len(p.get('docs_read', []))} topik")
    print(f"  Audio Effect : {'Aktif (ON) 🔊' if p.get('sound_enabled') else 'Nonaktif (OFF) 🔇'}")

    print(color("\n[+] Koleksi Lencana (Virtual Badges):", "yellow"))
    unlocked = p.get("badges", [])
    for b_id, b_data in ALL_BADGES.items():
        if b_id in unlocked:
            print(f"  ✅ {color(b_data['name'], 'green')} : {b_data['desc']}")
        else:
            print(f"  🔒 {color(b_data['name'], 'gray')} : {b_data['desc']}")

def toggle_sound():
    p = load_profile()
    p["sound_enabled"] = not p.get("sound_enabled", False)
    save_profile(p)
    status = "AKTIF (ON) 🔊" if p["sound_enabled"] else "NONAKTIF (OFF) 🔇"
    print(color(f"\nPengaturan suara terminal berhasil diubah: {status}", "green"))
    if p["sound_enabled"]:
        play_beep(1500, 100)

# ====== Existing Core Tools ======

def system_info():
    print(color("\n[+] Info Sistem", "yellow"))
    print(os_banner())
    print("OS           :", platform.system(), platform.release())
    print("Versi Python :", platform.python_version())
    print("User         :", os.getenv("USER") or os.getenv("USERNAME"))
    print("Arsitektur   :", platform.machine())

    if psutil:
        ram = psutil.virtual_memory()
        print(f"RAM Total    : {ram.total // (1024**3)} GB ({ram.total // (1024**2)} MB)")
        print(f"RAM Tersisa  : {ram.available // (1024**3)} GB ({ram.available // (1024**2)} MB)")
        print(f"CPU Usage    : {psutil.cpu_percent(interval=0.5)}%")

    if shutil:
        try:
            root_path = "C:\\" if platform.system() == "Windows" else "/"
            total, used, free = shutil.disk_usage(root_path)
            print(f"Storage Total: {total // (1024**3)} GB")
            print(f"Storage Free : {free // (1024**3)} GB")
        except Exception:
            pass
    add_xp(5, "Cek Info Sistem")

def hashing_tools():
    print(color("\n[ Hashing Tools ]", "yellow"))
    text = input("Masukkan teks: ")
    data = text.encode("utf-8")
    print("MD5      :", hashlib.md5(data).hexdigest())
    print("SHA1     :", hashlib.sha1(data).hexdigest())
    print("SHA224   :", hashlib.sha224(data).hexdigest())
    print("SHA256   :", hashlib.sha256(data).hexdigest())
    print("SHA384   :", hashlib.sha384(data).hexdigest())
    print("SHA512   :", hashlib.sha512(data).hexdigest())
    add_xp(5, "Hashing Teks")
    unlock_badge("crypto_adept")

def checksum_file():
    print(color("\n[ Checksum File ]", "yellow"))
    path = input("Path file: ").strip('"\'')
    if not os.path.exists(path) or not os.path.isfile(path):
        print(color("❌ File tidak ditemukan!", "red"))
        return
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)
    print("MD5    :", md5.hexdigest())
    print("SHA1   :", sha1.hexdigest())
    print("SHA256 :", sha256.hexdigest())
    add_xp(10, "Checksum File")

def base64_tools():
    print(color("\n[ Base64 Tools ]", "yellow"))
    pilih = input("[1] Encode [2] Decode : ")
    teks = input("Masukkan teks: ")
    if pilih == "1":
        print("Encode:", base64.b64encode(teks.encode("utf-8")).decode())
    elif pilih == "2":
        try:
            print("Decode:", base64.b64decode(teks.encode("utf-8")).decode(errors="ignore"))
        except Exception:
            print(color("❌ Input bukan Base64 valid!", "red"))
    else:
        print(color("Pilihan tidak valid!", "red"))
    add_xp(5, "Base64 Encoding")

def url_tools():
    print(color("\n[ URL Encode/Decode Tools ]", "yellow"))
    pilih = input("[1] Encode [2] Decode : ")
    teks = input("Masukkan teks/URL: ")
    if pilih == "1":
        print("Encode:", urllib.parse.quote(teks, safe=""))
    elif pilih == "2":
        print("Decode:", urllib.parse.unquote(teks))
    else:
        print(color("Pilihan tidak valid!", "red"))
    add_xp(5, "URL Tools")

def password_gen():
    print(color("\n[ Password Generator ]", "yellow"))
    try:
        panjang = int(input("Panjang password (default 16): ") or "16")
    except ValueError:
        panjang = 16
    include_symbols = input("Gunakan karakter simbol? (y/n, default y): ").lower() != "n"
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    pwd = "".join(random.choice(chars) for _ in range(panjang))
    print(color(f"Password ({panjang} karakter): ", "green") + pwd)
    add_xp(5, "Generate Password")

def uuid_gen():
    print(color("\n[ UUID Generator ]", "yellow"))
    u4 = uuid.uuid4()
    print("UUID v4 (Random) :", str(u4))
    print("UUID Hex         :", u4.hex)
    add_xp(5, "Generate UUID")

def ping_host():
    print(color("\n[ Ping Host ]", "yellow"))
    host = input("Masukkan host/IP (misal google.com): ").strip()
    if not host:
        return
    param = "-n 4" if platform.system() == "Windows" else "-c 4"
    os.system(f"ping {param} {host}")
    add_xp(5, "Ping Host")

def geoip_lookup():
    print(color("\n[ GeoIP Lookup ]", "yellow"))
    ip = input("Masukkan IP/domain: ").strip()
    if not ip:
        return
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query", timeout=6).json()
        if r.get("status") == "success":
            print(color("[+] Hasil GeoIP:", "green"))
            print("IP Query   :", r.get("query"))
            print("Negara     :", f"{r.get('country')} ({r.get('countryCode')})")
            print("Provinsi   :", r.get("regionName"))
            print("Kota       :", r.get("city"))
            print("Kode Pos   :", r.get("zip"))
            print("Koordinat  :", f"{r.get('lat')}, {r.get('lon')}")
            print("Timezone   :", r.get("timezone"))
            print("ISP        :", r.get("isp"))
            print("Organisasi :", r.get("org"))
            print("ASN        :", r.get("as"))
            add_xp(10, "GeoIP Lookup")
        else:
            print(color(f"❌ Gagal lookup: {r.get('message', 'Unknown error')}", "red"))
    except Exception as e:
        print(color(f"❌ Error: {e}", "red"))

def http_headers():
    print(color("\n[ HTTP Header Viewer ]", "yellow"))
    url = input("Masukkan URL (misal: https://example.com): ").strip()
    if not url:
        return
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    try:
        r = requests.get(url, timeout=7, allow_redirects=True)
        print(color(f"\n[+] Status Code: {r.status_code} {r.reason}", "green"))
        print(color(f"[+] Final URL  : {r.url}", "cyan"))
        print(color("\n[+] Response Headers:", "yellow"))
        for k, v in r.headers.items():
            print(f"  {color(k, 'magenta')}: {v}")
        add_xp(10, "HTTP Header Analysis")
    except Exception as e:
        print(color(f"❌ Error: {e}", "red"))

def virus_total():
    print(color("\n[ VirusTotal Scanner ]", "yellow"))
    if not VT_API_KEY:
        print(color("⚠️ API Key VirusTotal belum diatur di config.json!", "red"))
        print("Silakan buat config.json dengan isi: {\"VT_API_KEY\": \"your_api_key_here\"}")
        return
    pilih = input("[1] Scan URL [2] Scan File Hash (MD5/SHA256): ")
    if pilih == "1":
        url = input("Masukkan URL: ").strip()
        params = {"apikey": VT_API_KEY, "resource": url}
        endpoint = "https://www.virustotal.com/vtapi/v2/url/report"
    elif pilih == "2":
        h = input("Masukkan Hash: ").strip()
        params = {"apikey": VT_API_KEY, "resource": h}
        endpoint = "https://www.virustotal.com/vtapi/v2/file/report"
    else:
        print(color("Pilihan tidak valid", "red"))
        return
    try:
        r = requests.get(endpoint, params=params, timeout=10)
        data = r.json()
        if data.get("response_code") == 1:
            positives = data.get("positives", 0)
            total = data.get("total", 0)
            det_color = "green" if positives == 0 else "yellow" if positives < 5 else "red"
            print("Status Deteksi :", color(f"{positives} / {total} engine terdeteksi berbahaya", det_color))
            print("Scan Date      :", data.get("scan_date"))
            print("Laporan Lengkap:", color(data.get("permalink"), "cyan"))
            add_xp(15, "VirusTotal Scan")
        else:
            print(color("ℹ️ Data tidak ditemukan di database VirusTotal.", "yellow"))
    except Exception as e:
        print(color(f"❌ Error VirusTotal API: {e}", "red"))

def caesar_cipher():
    print(color("\n[ Caesar Cipher ]", "yellow"))
    teks = input("Masukkan teks: ")
    try:
        shift = int(input("Shift (angka, misal 3): "))
    except ValueError:
        print(color("Shift harus berupa angka!", "red"))
        return
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
    print(color("Hasil: ", "green") + hasil)
    add_xp(5, "Caesar Cipher")

def list_files():
    print(color("\n[ List Files & Directory ]", "yellow"))
    path = input("Folder path (default .): ").strip() or "."
    if not os.path.exists(path):
        print(color("❌ Folder tidak ditemukan!", "red"))
        return
    try:
        entries = os.listdir(path)
        print(f"\nTotal item dalam '{path}': {len(entries)}")
        print("-" * 50)
        for f in entries:
            fp = os.path.join(path, f)
            if os.path.isfile(fp):
                size = os.path.getsize(fp)
                print(f"📄 [FILE] {f:<30} ({size:,} bytes)")
            elif os.path.isdir(fp):
                print(f"📁 [DIR]  {f:<30}")
        print("-" * 50)
    except Exception as e:
        print(color(f"❌ Error: {e}", "red"))

def matrix_rain():
    print(color("\n[ Matrix Rain Effect ] (Tekan Ctrl+C untuk berhenti)", "green"))
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンABCDEF0123456789"
    try:
        while True:
            line = "".join(random.choice(chars) if random.random() > 0.4 else " " for _ in range(78))
            print(f"\033[92m{line}\033[0m")
            time.sleep(0.04)
    except KeyboardInterrupt:
        print("\n" + color("Matrix rain stopped.", "yellow"))

def binary_tools():
    print(color("\n[ Binary Tools ]", "yellow"))
    print("[1] Text → Binary")
    print("[2] Binary → Text")
    choice = input("Pilih: ")
    if choice == "1":
        text = input("Masukkan teks: ")
        binary = " ".join(format(ord(c), "08b") for c in text)
        print(color("Binary: ", "green") + binary)
    elif choice == "2":
        binary = input("Masukkan binary (dipisahkan spasi): ").strip()
        try:
            tokens = binary.split()
            text = "".join(chr(int(b, 2)) for b in tokens)
            print(color("Teks: ", "green") + text)
        except Exception:
            print(color("❌ Format binary tidak valid!", "red"))
    else:
        print(color("Pilihan tidak valid!", "red"))
    add_xp(5, "Binary Converter")

def sha256_tools():
    print(color("\n[ SHA256 Tools ]", "yellow"))
    print("[1] Hash Text")
    print("[2] Hash File")
    choice = input("Pilih: ")
    if choice == "1":
        text = input("Masukkan teks: ")
        hashed = hashlib.sha256(text.encode("utf-8")).hexdigest()
        print(color("SHA256: ", "green") + hashed)
    elif choice == "2":
        file = input("Masukkan path file: ").strip('"\'')
        try:
            file_hash = hashlib.sha256()
            with open(file, "rb") as f:
                while chunk := f.read(65536):
                    file_hash.update(chunk)
            print(color("SHA256 File: ", "green") + file_hash.hexdigest())
        except FileNotFoundError:
            print(color("❌ File tidak ditemukan", "red"))
        except Exception as e:
            print(color(f"❌ Error: {e}", "red"))
    else:
        print(color("Pilihan tidak valid", "red"))
    add_xp(5, "SHA256 Tools")

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 1433: "MSSQL", 1521: "Oracle DB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
    8080: "HTTP-Proxy/Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
}

def scan_single_port(ip, port, timeout=0.8):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown Service")
                return port, True, service
    except Exception:
        pass
    return port, False, ""

def port_scanner(target=None):
    print(color("\n[ 🔍 Fast TCP Port Scanner ]", "yellow"))
    if not target:
        target = input("Masukkan target IP/Domain: ").strip()
    if not target:
        return

    try:
        target_ip = socket.gethostbyname(target)
        print(f"Target: {target} ({color(target_ip, 'cyan')})")
    except socket.gaierror:
        print(color("❌ Host tidak dapat diresolusi!", "red"))
        return

    print("\n[1] Scan Port Populer (Top 21 Common Ports)")
    print("[2] Scan Range Port Kustom (misal: 1-1000 atau 80,443,8080)")
    mode = input("Pilih mode (default 1): ").strip() or "1"

    ports_to_scan = []
    if mode == "1":
        ports_to_scan = sorted(list(COMMON_PORTS.keys()))
    elif mode == "2":
        p_input = input("Masukkan port range (contoh: 20-100 atau 80,443,3306): ").strip()
        if "-" in p_input:
            try:
                start, end = p_input.split("-")
                start_p, end_p = int(start), int(end)
                if 1 <= start_p <= end_p <= 65535:
                    ports_to_scan = list(range(start_p, end_p + 1))
                else:
                    print(color("Range port di luar batas 1-65535!", "red"))
                    return
            except ValueError:
                print(color("Format range tidak valid!", "red"))
                return
        else:
            try:
                ports_to_scan = [int(p.strip()) for p in p_input.split(",") if p.strip()]
            except ValueError:
                print(color("Format port tidak valid!", "red"))
                return
    else:
        print(color("Pilihan tidak valid!", "red"))
        return

    print(f"\nMemulai scanning {len(ports_to_scan)} port pada {target_ip}...")
    start_time = time.time()
    open_ports = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_single_port, target_ip, p) for p in ports_to_scan]
        for f in futures:
            p, is_open, service = f.result()
            if is_open:
                open_ports.append((p, service))
                print(f"  {color('[OPEN]', 'green')} Port {color(str(p), 'bold'):<6} - {service}")
                play_beep(1600, 30)

    elapsed = time.time() - start_time
    print(f"\nSelesai dalam {elapsed:.2f} detik.")
    if not open_ports:
        print(color("Tidak ditemukan port terbuka.", "yellow"))
    else:
        print(color(f"Total port terbuka ditemukan: {len(open_ports)}", "green"))
    add_xp(15, "TCP Port Scanning")
    unlock_badge("port_hunter")

def subnet_calculator(cidr_input=None):
    print(color("\n[ 🌐 Subnet & IP CIDR Calculator ]", "yellow"))
    if not cidr_input:
        cidr_input = input("Masukkan IP dengan CIDR (contoh: 192.168.1.50/24 atau 10.0.0.0/16): ").strip()
    if not cidr_input:
        return
    try:
        net = ipaddress.ip_network(cidr_input, strict=False)
        ip_obj = ipaddress.ip_interface(cidr_input)

        print(color("\n[+] Hasil Analisis Subnet:", "green"))
        print(f"Versi IP        : IPv{net.version}")
        print(f"Input Interface : {ip_obj}")
        print(f"Network Address : {net.network_address}")
        print(f"Netmask         : {net.netmask}")
        print(f"Wildcard Mask   : {net.hostmask}")
        print(f"Broadcast       : {net.broadcast_address}")
        
        if net.version == 4 and net.num_addresses > 2:
            first_host = net.network_address + 1
            last_host = net.broadcast_address - 1
            usable_hosts = net.num_addresses - 2
            print(f"Usable Host Range: {first_host} - {last_host}")
            print(f"Total Usable Hosts: {usable_hosts:,}")
        else:
            print(f"Total Host Range: {net.network_address} - {net.broadcast_address}")
            print(f"Total Usable Hosts: {net.num_addresses:,}")

        print(f"Total Addresses : {net.num_addresses:,}")
        print(f"Is Private?     : {net.is_private}")
        print(f"Is Global/Pub?  : {net.is_global}")
        print(f"Is Loopback?    : {net.is_loopback}")
        add_xp(10, "Subnetting Analysis")
        unlock_badge("subnet_guru")
    except Exception as e:
        print(color(f"❌ Input CIDR / Subnet tidak valid: {e}", "red"))

def hash_identifier(h=None):
    print(color("\n[ 🔎 Hash Identifier & Analyzer ]", "yellow"))
    if not h:
        h = input("Masukkan hash string: ").strip()
    if not h:
        return

    length = len(h)
    is_hex = bool(re.fullmatch(r"^[0-9a-fA-F]+$", h))
    is_base64 = bool(re.fullmatch(r"^[0-9a-zA-Z+/=]+$", h))

    print(f"\nPanjang Hash : {length} karakter | Format Hex: {is_hex}")
    possible = []

    if h.startswith("$2a$") or h.startswith("$2b$") or h.startswith("$2y$"):
        possible.append(("bcrypt", "Password hashing format (OpenBSD/Blowfish)"))
    elif h.startswith("$6$"):
        possible.append(("SHA-512 Crypt", "Linux /etc/shadow password hash"))
    elif h.startswith("$5$"):
        possible.append(("SHA-256 Crypt", "Linux /etc/shadow password hash"))
    elif h.startswith("$1$"):
        possible.append(("MD5 Crypt", "Legacy Unix password hash"))
    elif h.startswith("$argon2id$") or h.startswith("$argon2i$"):
        possible.append(("Argon2", "Modern memory-hard password hash"))
    elif is_hex:
        if length == 8:
            possible.append(("CRC32 / Adler32", "Checksum 32-bit"))
        elif length == 32:
            possible.append(("MD5", "Message Digest 5 (128-bit) - Sangat Populer"))
            possible.append(("NTLM", "Windows NT LAN Manager Hash"))
            possible.append(("MD4", "Message Digest 4"))
        elif length == 40:
            possible.append(("SHA-1", "Secure Hash Algorithm 1 (160-bit)"))
            possible.append(("RIPEMD-160", "RACE Integrity Primitives (160-bit)"))
        elif length == 56:
            possible.append(("SHA-224", "SHA-2 Family (224-bit)"))
            possible.append(("SHA3-224", "Keccak SHA-3 (224-bit)"))
        elif length == 64:
            possible.append(("SHA-256", "SHA-2 Family (256-bit) - Sangat Populer"))
            possible.append(("SHA3-256", "Keccak SHA-3 (256-bit)"))
            possible.append(("BLAKE2s", "BLAKE2s 256-bit"))
        elif length == 96:
            possible.append(("SHA-384", "SHA-2 Family (384-bit)"))
            possible.append(("SHA3-384", "Keccak SHA-3 (384-bit)"))
        elif length == 128:
            possible.append(("SHA-512", "SHA-2 Family (512-bit)"))
            possible.append(("SHA3-512", "Keccak SHA-3 (512-bit)"))
            possible.append(("Whirlpool", "Whirlpool 512-bit"))
            possible.append(("BLAKE2b", "BLAKE2b 512-bit"))

    if not possible and is_base64:
        possible.append(("Base64 Encoded String", "Data encoding, bukan hash kriptografis"))

    if possible:
        print(color("\n[+] Kemungkinan Jenis Algoritma Hash:", "green"))
        for algo, desc in possible:
            print(f"  👉 {color(algo, 'bold'):<18} : {desc}")
    else:
        print(color("⚠️ Algoritma tidak dapat diidentifikasi secara pasti.", "yellow"))
    add_xp(10, "Hash Analysis")

def _base64url_decode(payload_str):
    rem = len(payload_str) % 4
    if rem > 0:
        payload_str += "=" * (4 - rem)
    return base64.urlsafe_b64decode(payload_str.encode("utf-8")).decode("utf-8", errors="ignore")

def jwt_decoder(token=None):
    print(color("\n[ 🎫 JWT (JSON Web Token) Inspector ]", "yellow"))
    if not token:
        token = input("Masukkan JWT Token: ").strip()
    if not token:
        return

    parts = token.split(".")
    if len(parts) != 3:
        print(color("❌ Format JWT tidak valid! JWT harus terdiri dari 3 bagian (header.payload.signature).", "red"))
        return

    header_raw, payload_raw, signature = parts
    try:
        header_json = json.loads(_base64url_decode(header_raw))
        payload_json = json.loads(_base64url_decode(payload_raw))

        print(color("\n[+] HEADER (Algorithm & Token Type):", "cyan"))
        print(json.dumps(header_json, indent=2))

        print(color("\n[+] PAYLOAD (Claims & Data):", "green"))
        print(json.dumps(payload_json, indent=2))

        print(color("\n[+] ANALISIS KLAIM & MASA BERLAKU:", "yellow"))
        now_ts = datetime.now(timezone.utc).timestamp()

        if "exp" in payload_json:
            exp_ts = payload_json["exp"]
            exp_date = datetime.fromtimestamp(exp_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            if exp_ts < now_ts:
                print(f"  Expired (exp) : {exp_date} -> {color('❌ TOKEN SUDAH KADALUARSA (EXPIRED)', 'red')}")
            else:
                sisa_detik = int(exp_ts - now_ts)
                print(f"  Expired (exp) : {exp_date} -> {color(f'✅ TOKEN MASIH AKTIF (Sisa ~{sisa_detik} detik)', 'green')}")
        else:
            print("  Expired (exp) : Tidak ada klaim 'exp' (Token tidak punya batas waktu)")

        if "iat" in payload_json:
            iat_ts = payload_json["iat"]
            iat_date = datetime.fromtimestamp(iat_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"  Issued At (iat): {iat_date}")

        if "nbf" in payload_json:
            nbf_ts = payload_json["nbf"]
            nbf_date = datetime.fromtimestamp(nbf_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"  Not Before (nbf): {nbf_date}")

        print(f"\nSignature (Base64URL): {signature[:20]}... [Truncated]")
        add_xp(10, "JWT Inspection")
    except Exception as e:
        print(color(f"❌ Gagal mendekode JWT: {e}", "red"))

def url_defanger(raw=None):
    print(color("\n[ 🛡️ URL / IP Defanger & Refanger (SOC / Threat Intel) ]", "yellow"))
    print("[1] Defang (Ubah URL/IP agar aman dibagikan, misal https://malware.com -> hxxps://malware[.]com)")
    print("[2] Refang (Kembalikan ke URL/IP asli)")
    choice = input("Pilih (default 1): ").strip() or "1"

    if choice == "1":
        if not raw:
            raw = input("Masukkan URL / IP / Domain: ").strip()
        defanged = raw.replace("http://", "hxxp://").replace("https://", "hxxps://")
        defanged = defanged.replace(".", "[.]").replace("@", "[@]")
        print(color("\nHasil Defang (Aman untuk laporan):", "green"))
        print(defanged)
    elif choice == "2":
        if not raw:
            raw = input("Masukkan URL / IP yang di-defang: ").strip()
        refanged = raw.replace("hxxps://", "https://").replace("hxxp://", "http://")
        refanged = refanged.replace("[.]", ".").replace("[@]", "@")
        print(color("\nHasil Refang (URL/IP Asli):", "green"))
        print(refanged)
    else:
        print(color("Pilihan tidak valid!", "red"))
    add_xp(5, "Threat Intel Defang")

def vigenere_cipher():
    print(color("\n[ 🔐 Vigenère Cipher (Polyalphabetic Substitution) ]", "yellow"))
    mode = input("[E]ncrypt / [D]ecrypt : ").lower()
    if mode not in ["e", "d"]:
        print(color("Pilihan mode tidak valid!", "red"))
        return

    text = input("Masukkan teks: ")
    key = input("Masukkan kata kunci (key huruf): ").strip()
    if not key.isalpha():
        print(color("❌ Kunci harus berupa huruf alfabet!", "red"))
        return

    key = key.upper()
    key_idx = 0
    result = []

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            base = ord('A') if is_upper else ord('a')
            c_val = ord(char.upper()) - ord('A')
            k_val = ord(key[key_idx % len(key)]) - ord('A')

            if mode == "e":
                res_val = (c_val + k_val) % 26
            else:
                res_val = (c_val - k_val + 26) % 26

            res_char = chr(res_val + base)
            result.append(res_char)
            key_idx += 1
        else:
            result.append(char)

    output = "".join(result)
    print(color("Hasil: ", "green") + output)
    add_xp(10, "Vigenere Cipher")
    unlock_badge("crypto_adept")

def dns_lookup():
    print(color("\n[ 📡 DNS & Reverse DNS Resolver ]", "yellow"))
    print("[1] Forward DNS (Domain → IP Address / A & AAAA)")
    print("[2] Reverse DNS (IP Address → PTR Hostname)")
    choice = input("Pilih: ")

    if choice == "1":
        domain = input("Masukkan nama domain (misal: google.com): ").strip()
        if not domain:
            return
        try:
            addr_info = socket.getaddrinfo(domain, None)
            ip_set = set()
            for item in addr_info:
                ip_addr = item[4][0]
                family = "IPv4" if item[0] == socket.AF_INET else "IPv6" if item[0] == socket.AF_INET6 else "Other"
                ip_set.add((ip_addr, family))

            print(color(f"\n[+] Hasil DNS Record untuk '{domain}':", "green"))
            for ip, fam in sorted(ip_set, key=lambda x: x[1]):
                print(f"  👉 [{fam}] {ip}")
            add_xp(10, "Forward DNS Lookup")
        except socket.gaierror as e:
            print(color(f"❌ Gagal DNS lookup: {e}", "red"))

    elif choice == "2":
        ip = input("Masukkan IP Address: ").strip()
        if not ip:
            return
        try:
            hostname, aliases, _ = socket.gethostbyaddr(ip)
            print(color(f"\n[+] Reverse DNS (PTR) untuk {ip}:", "green"))
            print(f"  Hostname : {color(hostname, 'cyan')}")
            if aliases:
                print(f"  Aliases  : {', '.join(aliases)}")
            add_xp(10, "Reverse DNS Lookup")
        except Exception as e:
            print(color(f"❌ Reverse lookup gagal: {e}", "red"))
    else:
        print(color("Pilihan tidak valid!", "red"))

def konoha_easter_egg():
    print(color(r"""
           .-'""'-.
         .'        `.
        /   .-""-.   \
       /   /  🌀  \   \
      |   | KONOHA |   |
      |   |VILLAGE |   |
       \   \      /   /
        \   '-..-'   /
         `.        .'
           '-....-'

🔥 Selamat datang di Desa Daun Tersembunyi (Konoha)! 🔥
Tekad Api membara di setiap baris kode Cyber Edu CLI! 🍃🌀
""", "green"))
    add_xp(25, "Menemukan Easter Egg Konoha")
    unlock_badge("first_blood")

# ====== CLI Subcommand Handler ======
def handle_cli_args():
    if len(sys.argv) <= 1:
        return False

    cmd = sys.argv[1].lower()
    
    if cmd in ["quiz", "kuis"]:
        cyber_quiz()
    elif cmd in ["docs", "wiki"]:
        topic = sys.argv[2] if len(sys.argv) > 2 else None
        terminal_docs(topic)
    elif cmd in ["check", "password", "audit"]:
        pwd = sys.argv[2] if len(sys.argv) > 2 else None
        password_health_checker(pwd)
    elif cmd in ["quote", "quotes"]:
        cyber_quote_generator()
    elif cmd in ["status", "profile", "stats"]:
        progress_tracker()
    elif cmd in ["scan", "portscan"]:
        target = sys.argv[2] if len(sys.argv) > 2 else None
        port_scanner(target)
    elif cmd in ["subnet", "cidr"]:
        cidr = sys.argv[2] if len(sys.argv) > 2 else None
        subnet_calculator(cidr)
    elif cmd in ["jwt"]:
        tok = sys.argv[2] if len(sys.argv) > 2 else None
        jwt_decoder(tok)
    elif cmd in ["defang"]:
        raw = sys.argv[2] if len(sys.argv) > 2 else None
        url_defanger(raw)
    elif cmd in ["help", "--help", "-h"]:
        print(color("""
Cyber Edu CLI - Subcommand Usage:
  python main.py                    # Menu Interaktif Lengkap
  python main.py quiz               # Kuis Keamanan Siber Interaktif
  python main.py docs [topik]       # Terminal Wiki (linux, network, owasp, crypto, git)
  python main.py check [password]   # Analisis Kekuatan & Waktu Retas Password
  python main.py status             # Cek Profil, Level, XP, dan Badges
  python main.py quote              # Tampilkan Cyber Quote of the Day
  python main.py scan <target>      # Fast TCP Port Scanner
  python main.py subnet <cidr>      # Kalkulator Subnetting CIDR
  python main.py jwt <token>        # Inspector & Decoder JWT
  python main.py defang <url/ip>    # URL/IP Threat Intel Defanger
""", "cyan"))
    else:
        print(color(f"Subcommand '{cmd}' tidak dikenali. Ketik 'python main.py help' untuk bantuan.", "red"))
    return True

# ====== Interactive Menu ======
def menu():
    opsi = {
        "1": system_info,
        "2": hashing_tools,
        "3": checksum_file,
        "4": base64_tools,
        "5": url_tools,
        "6": password_gen,
        "7": password_health_checker,
        "8": uuid_gen,
        "9": ping_host,
        "10": geoip_lookup,
        "11": http_headers,
        "12": virus_total,
        "13": caesar_cipher,
        "14": list_files,
        "15": matrix_rain,
        "16": binary_tools,
        "17": sha256_tools,
        "18": port_scanner,
        "19": subnet_calculator,
        "20": hash_identifier,
        "21": jwt_decoder,
        "22": url_defanger,
        "23": vigenere_cipher,
        "24": dns_lookup,
        "25": cyber_quiz,
        "26": terminal_docs,
        "27": progress_tracker,
        "28": cyber_quote_generator,
        "29": toggle_sound,
        "konoha": konoha_easter_egg,
        "hokage": konoha_easter_egg
    }

    # Play boot sequence on startup
    cyber_boot_animation()
    cyber_quote_generator()
    unlock_badge("first_blood")

    while True:
        p = load_profile()
        lvl, title, _ = get_level_info(p["xp"])
        sound_ico = "🔊 ON" if p.get("sound_enabled") else "🔇 OFF"

        banner()
        print(color(f" 👤 Agent: {p['username']} | 🎖️ Lvl {lvl} ({title}) | 💎 XP: {p['xp']} | Audio: {sound_ico}", "green"))
        print(color("""
 ─── 🎓 MODUL EDUKASI & GAMIFIKASI ─────────────────────────────────────────
 [25] 🎓 Cyber Quiz (Kuis Interaktif)   [27] 🏆 Profil, Level & Badges
 [26] 📖 Terminal Wiki & Cheat Sheet   [28] 💬 Cyber Quote of the Day
 
 ─── 🌐 JARINGAN & RECONNAISSANCE ──────────────────────────────────────────
 [18] 🔍 Fast TCP Port Scanner          [10] 🛰️ GeoIP Lookup
 [19] 🌐 Subnet & CIDR Calculator       [11] 🌐 HTTP Header Viewer
 [24] 📡 DNS & Reverse DNS Resolver     [9]  📡 Ping Host
 
 ─── 🔐 KRIPTOGRAFI & KEAMANAN DATA ────────────────────────────────────────
 [2]  🔑 Hashing Multi-Algoritma        [13] 🔏 Caesar Cipher
 [3]  📂 Checksum File (Integritas)     [23] 🔐 Vigenère Cipher
 [17] 🔒 Dedicated SHA256 Tools         [7]  🛡️ Password Health & Crack Time
 [20] 🔎 Hash Identifier / Analyzer     [6]  🎲 Password Generator
 
 ─── 🛠️ ENKODING & THREAT INTEL ────────────────────────────────────────────
 [21] 🎫 JWT Token Inspector            [4]  🔐 Base64 Tools
 [22] 🛡️ URL/IP Defanger (Threat Intel) [5]  🌍 URL Encode/Decode
 [12] 🛡️ VirusTotal Scanner             [16] 💾 Binary (Text ↔ Binary)
 
 ─── 💻 SISTEM & UTILITAS ──────────────────────────────────────────────────
 [1]  🖥️ Info Sistem & OS Banner        [15] 💻 Matrix Rain Effect
 [8]  🆔 UUID Generator                 [14] 📁 List Files & Size
 [29] 🔊 Toggle Audio / Sound Beep      [0]  🚪 Keluar / Exit
 ───────────────────────────────────────────────────────────────────────────
""", "cyan"))

        pilih = input(color("Pilih menu [0-29]: ", "yellow")).strip().lower()

        if pilih in ["0", "exit", "quit", "q"]:
            print(color("\nTerima kasih telah belajar bersama Cyber Edu CLI! Tetap aman & etis 👋", "green"))
            sys.exit(0)

        func = opsi.get(pilih)
        if func:
            func()
        else:
            print(color("❌ Pilihan menu tidak valid!", "red"))

        input(color("\nTekan Enter untuk kembali ke menu utama...", "white"))

if __name__ == "__main__":
    if not handle_cli_args():
        menu()
