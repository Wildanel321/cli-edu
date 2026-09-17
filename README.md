# 🌀 Cyber Edu CLI Tools

**Cyber Edu CLI** adalah platform dan kumpulan **Command Line Tools** interaktif berbasis Python untuk pembelajaran **cyber security**, kriptografi, networking, audit keamanan, dan utilitas sehari-hari.

Dilengkapi modul **Cyber Quiz interaktif**, **Terminal Wiki & Cheat Sheet**, **Advanced Password Health & Brute-Force Checker**, **Gamifikasi (Level, XP, Badges)**, **Fast Port Scanner**, **Subnet Calculator**, **JWT Inspector**, **Threat Intel Defanger**, hingga animasi booting retro cyberpunk!

> ⚠️ **Disclaimer**: Tools ini dibuat murni untuk **tujuan edukasi, analisis, & penelitian etis**.  
> Gunakan secara **bijak & bertanggung jawab**. Penulis tidak bertanggung jawab atas penyalahgunaan tools ini.

---

## ✨ Fitur Utama

### 🎓 1. Modul Edukasi & Gamifikasi
- **🎓 Cyber Quiz (`python main.py quiz`)**: Kuis interaktif beragam topik keamanan siber (Phishing, Cryptography, SQLi, MITM, Network Ports, OWASP) lengkap dengan skor, poin XP, dan ulasan edukatif.
- **📖 Terminal Wiki & Cheat Sheet (`python main.py docs [topik]`)**: Dokumentasi cepat & panduan praktis langsung di CLI:
  - `linux` : Perintah esensial Linux, permission, process management, log analysis.
  - `network` : Tabel port standar IANA, protokol penting, network diagnostic.
  - `owasp` : OWASP Top 10 Web Vulnerabilities & panduan mitigasi.
  - `crypto` : Konsep Enkripsi vs Hashing vs Encoding, Simetris vs Asimetris.
  - `git` : Cheat sheet alur kerja Git harian.
- **🏆 Profil & Learning Tracker (`python main.py status`)**: Sistem Level, akumulasi XP, dan perolehan **Virtual Badges** (seperti *First Blood*, *Quiz Master*, *Password Sentinel*, *Port Hunter*, *Cyber Scholar*, *Hokage Sec*).
- **💬 Cyber Quote of the Day (`python main.py quote`)**: Kutipan inspiratif & filosofis dari para pakar keamanan siber legendaris dunia.

### 🛡️ 2. Audit Keamanan & Kriptografi
- **🛡️ Advanced Password Health Checker (`python main.py check [password]`)**: Perhitungan matematis entropi bit ($H = L \log_2(R)$) dan estimasi waktu retas (*Brute-force crack time*) terhadap serangan online, CPU, multi-GPU rig, hingga superkomputer.
- **🔎 Hash Identifier / Analyzer**: Identifikasi otomatis jenis algoritma hash (MD5, SHA1, SHA256, NTLM, bcrypt, Argon2, SHA-512 crypt, dll).
- **🔑 Hashing Multi-Algoritma**: MD5, SHA1, SHA224, SHA256, SHA384, SHA512 teks & file.
- **📂 File Integrity Checksum**: Streaming hashing chunk untuk verifikasi keutuhan file.
- **🔏 Kriptografi Klasik**: Caesar Cipher & Vigenère Polyalphabetic Cipher.
- **🎲 Password Generator**: Pembuat password acak berbasis entropi tinggi.

### 🌐 3. Jaringan, Reconnaissance & Threat Intel
- **🔍 Fast TCP Port Scanner (`python main.py scan [host]`)**: Scan port terbuka (top 21 port populer atau custom range) dengan multi-threading socket cepat.
- **🌐 Subnet & CIDR Calculator (`python main.py subnet [cidr]`)**: Kalkulasi lengkap IPv4/IPv6: Network, Broadcast, Netmask, Wildcard, Usable Hosts, Status Private/Public.
- **📡 DNS & Reverse DNS Resolver**: Forward DNS (Domain ➡️ IP A/AAAA) dan Reverse DNS (IP ➡️ PTR Hostname).
- **🛡️ URL/IP Threat Intel Defanger (`python main.py defang [url]`)**: Format aman URL/IP untuk laporan SOC & incident response (`https://bad.com` ↔ `hxxps://bad[.]com`).
- **🛰️ GeoIP Lookup**: Pelacakan lokasi negara, kota, ISP, dan ASN dari target IP/Domain.
- **🌐 HTTP Header Viewer**: Inspeksi header respons server dan status code.
- **🛡️ VirusTotal Scanner**: Integrasi API VirusTotal untuk scan URL & hash malware.

### 💻 4. Sistem & Visual Terminal Hacker
- **🖥️ Info Sistem & OS Banner**: Menampilkan OS, user, versi Python, RAM, Storage, CPU usage dengan banner ASCII unik per distro/OS (Windows, Ubuntu, Kali, Arch Linux, Linux Umum).
- **🚀 Cyber Boot Sequence Animation**: Animasi pembuka booting kernel retro cyberpunk saat startup.
- **🔊 Retro Sound Effect (Toggle ON/OFF)**: Efek audio bip terminal elektronik (bisa diaktifkan/dinonaktifkan).
- **💻 Matrix Rain Effect**: Animasi digital rain hacker-style di terminal.
- **🌀 Easter Egg Mode**: Rahasia mode Konoha (`konoha` / `hokage`).

---

## ⚡ Mode Penggunaan: Dual-Interface

Anda dapat menggunakan **Cyber Edu CLI** melalui **Menu Interaktif Lengkap** atau **Perintah Subcommand Langsung**:

### A. Menu Interaktif
```bash
python main.py
```

### B. Perintah Subcommand Langsung
| Perintah | Deskripsi |
|---|---|
| `python main.py quiz` | Memulai Kuis Keamanan Siber Interaktif |
| `python main.py docs [linux/network/owasp/crypto/git]` | Membuka Terminal Wiki topik tertentu |
| `python main.py check "P@ssw0rd!2026"` | Uji kekuatan & estimasi waktu retas password |
| `python main.py status` | Cek profil, Level, XP, dan koleksi Badges |
| `python main.py quote` | Tampilkan Cyber Quote of the Day |
| `python main.py scan google.com` | Fast TCP Port Scanner ke target |
| `python main.py subnet 192.168.1.1/24` | Kalkulator subnetting CIDR |
| `python main.py jwt <token>` | Decode & inspeksi klaim token JWT |
| `python main.py defang <url/ip>` | Ubah URL/IP berbahaya ke format aman |
| `python main.py help` | Tampilkan panduan penggunaan subcommand |

---

## 📦 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/Wildanel321/cli-edu.git
cd cli-edu
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi VirusTotal (Opsional)
```bash
cp config.json.example config.json
```
Isi API Key Anda di `config.json`:
```json
{
  "VT_API_KEY": "API_KEY_VIRUSTOTAL_ANDA"
}
```

---

## 📜 Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).
