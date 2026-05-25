#!/usr/bin/env python3
import os
import urllib.request
import json
import socket
import ssl

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    print("\033[31m[-] 'phonenumbers' is not downloaded.\033[0m")
    print("\033[33m[*] run: pip install phonenumbers\033[0m")

G = "\033[32m" # Verde
R = "\033[31m" # Rosso
Y = "\033[33m" # Giallo
B = "\033[34m" # Blu
C = "\033[36m" # Ciano
W = "\033[0m" # Reset

ssl_context = ssl._create_unverified_context()

def my_ip():
    print(f"{B}[+] searching databases...{W}\n")
    try:
        req = urllib.request.Request("https://ipapi.co", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            print(f"{G}✦ pubblic IP:{W} {data.get('ip')}")
            print(f"{G}✦ network / ISP:{W} {data.get('org')} ({data.get('asn', 'N/A')})")
            print(f"{G}✦ geo standard:{W} {data.get('city')}, {data.get('region')}, {data.get('country_name')}")
    except Exception:
        print(f"{R}[-] Error: impossible to find your IP. try later.{W}")

def ip_tracker():
    target = input(f"{Y}[?] enter IP target: {W}").strip()
    if not target:
        print(f"{R}[-] error: invalid imput.{W}")
        return
    print(f"\n{B}[+] searching databases... {target}...{W}\n")
    try:
        req = urllib.request.Request(f"https://ipapi.co{target}/json/", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            if "error" in data:
                print(f"{R}[-] Server Error: {data.get('reason', 'invalid IP')}{W}")
            else:
                print(f"{G}[IP founded:]{W}")
                print(f" • Host Target: {data.get('ip')}")
                print(f" • ASN / Provider: {data.get('org')} ({data.get('asn', 'N/A')})")
                print(f" • Nation / Code: {data.get('country_name')} ({data.get('country_code')})")
                print(f" • Region / City': {data.get('region')} / {data.get('city')}")
                print(f" • jet lag (TZ): {data.get('timezone')}")
                print(f" • xyz GPS: {data.get('latitude')}, {data.get('longitude')}")
                print(f" • {C}Google Maps Link: https://google.com{data.get('latitude')},{data.get('longitude')}{W}")
    except Exception:
        print(f"{R}[-] Error_404:IP not found.{W}")

def osint_email():
    email = input(f"{Y}[?] Enter email: {W}").strip()
    if "@" not in email or "." not in email:
        print(f"{R}[-] this is not a valid email.{W}")
        return

    username, domain = email.split('@', 1)
    print(f"\n{B}[+] starting Deep Reconnaissance : {email}{W}")
    print(f"{C}─"*60 + f"{W}")

    print(f"{G} tracking Record DNS MX (Mail Servers){W}")
    try:
        mx_records = os.popen(f"nslookup -type=mx {domain}").read()
        if "mail exchanger" in mx_records or "exchanger" in mx_records:
            print(f" {G}• Infrastruttura rilevata:{W}")
            for line in mx_records.split('\n'):
                if "exchanger" in line:
                    print(f" ↳ {line.strip()}")
        else:
            print(f" {Y}• Warning:{W} no MX server founded.")
    except Exception:
        print(f" {R}• Fail:{W} nsLookup tool disabled.")

    print(f"\n{G} error_404: page not founded{W}")
    try:
        req = urllib.request.Request(f"https://leakcheck.io{email}", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context, timeout=6) as response:
            res_data = json.loads(response.read().decode())
            if res_data.get("success") and res_data.get("sources"):
                print(f" {R}[⚠️] hacked email:stay awake{W}")
                print(f" {R}• compromitted databases:{W} {len(res_data['sources'])}")
                print(f" {R}• databases (first 5):{W} {', '.join(res_data['sources'][:5])}")
            else:
                print(f" {G}[✓] safe email. stay chill.{W}")
    except Exception:
        print(f" {Y}• Note:{W} safe leak-check.")

    print(f"\n{G} exter searching (Pivot Search){W}")
    print(f" • Intelligence Identity: https://haveibeenpwned.com")
    print(f" • Storic Password Plain: https://leakcheck.io")
    print(f" • under domains: https://dnsdumpster.com")
    print(f" • searching SPF Anti-Spoof: https://mxtoolbox.com{domain}")
def osint_phone():
    phone_input = input(f"{Y}[?] enter numbet (es. +393331234567): {W}").strip()
    print(f"\n{B}[+] starting phonenumbers database...{W}")
    print(f"{C}─"*60 + f"{W}")

    try:
        parsed_number = phonenumbers.parse(phone_input, None)
        if not phonenumbers.is_valid_number(parsed_number):
            print(f"{R}[-] ALLERT: invalid number{W}\n")

        is_possible = phonenumbers.is_possible_number(parsed_number)
        formatted_e164 = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        formatted_intl = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        formatted_nat = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)

        region_info = geocoder.description_for_number(parsed_number, "it")
        carrier_info = carrier.name_for_number(parsed_number, "it")
        timezones_info = timezone.time_zones_for_number(parsed_number)

        number_type = phonenumbers.number_type(parsed_number)
        type_mapping = {
            0: "Linea Fissa (Fixed Line)", 1: "Linea Mobile (Mobile)", 2: "Fissa o Mobile",
            3: "Toll-Free", 4: "Premium Rate", 5: "Shared Cost", 6: "VoIP",
            7: "Personal Number", 8: "Paging", 9: "Universal Access Number", 10: "Voicemail", -1: "Sconosciuto"
        }
        line_type_str = type_mapping.get(number_type, "Non identificato")

        print(f"{G}[DATI STRUTTURATI LIBRERIA PHONENUMBERS]{W}")
        print(f" • valid status': {G if phonenumbers.is_valid_number(parsed_number) else R}{phonenumbers.is_valid_number(parsed_number)}{W}")
        print(f" • logic structure: {G if is_possible else R}Coerente{W if is_possible else R} (Formato non standard){W}")
        print(f" • Country Code (CC): +{parsed_number.country_code}")
        print(f" • National number: {parsed_number.national_number}")
        print(f" • line type: {Y}{line_type_str}{W}")
        print(f" • REGION / GEOLOCAL: {G}{region_info if region_info else 'Non disponibile'}{W}")
        print(f" • OPERATOR: {Y}{carrier_info if carrier_info else 'Non Rilevato / MVNO'}{W}")
        print(f" • jet lag: {', '.join(timezones_info)}")
        print(f"\n{G}[FORMAT STANDARD RECON]{W}")
        print(f" • Format E.164: {formatted_e164}")
        print(f" • Internazional format: {formatted_intl}")
        print(f" • Nazional format: {formatted_nat}")

        clean_phone = formatted_e164.replace('+', '')
    except Exception as e:
        print(f"{R}[-] Error during process: {str(e)}{W}")
        return

    print(f"\n{G}[ENTER POINTS  SOCIAL MEDIA & INVESTIGATE]{W}")
    print(f" • Lookup TrueCaller Web Interface: https://truecaller.com{clean_phone}")
    print(f" • accoung whatsapp: https://wa.me{clean_phone}")
    print(f" • searching Tellows: https://tellows.it{clean_phone}")

def osint_social():
    username = input(f"{Y}[?] enter username: {W}").strip()
    if not username:
        print(f"{R}[-] invalid target.{W}")
        return
    print(f"\n{B}[+] Scanning HTTP (Live Verification) for: {username}...{W}\n")

    platforms = {
        "GitHub": f"https://github.com{username}",
        "Instagram": f"https://instagram.com{username}/",
        "TikTok": f"https://tiktok.com@{username}",
        "Twitter/X": f"https://x.com{username}",
        "Reddit": f"https://reddit.com{username}",
        "Pinterest": f"https://pinterest.com{username}/"
    }

    for name, url in platforms.items():
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            with urllib.request.urlopen(req, context=ssl_context, timeout=4) as response:
                if response.getcode() == 200:
                    print(f" [{G}FOUND{W}] {name}: {url}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f" [{R}NOT FOUND{W}] {name}")
            else:
                print(f" [{Y}LIKELY{W}] {name} (Code {e.code})")
        except Exception:
            print(f" [{Y}TIMED OUT{W}] {name}")

def port_scanner():
    target = input(f"{Y}[?] enter IP or port [ex:www.exemple.com]: {W}").strip()
    if not target:
        print(f"{R}[-] invalid target.{W}")
        return
    print(f"\n{B}[+] searching open doors on:{target}...{W}\n")

    common_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 443: "HTTPS", 445: "SMB", 8080: "HTTP-ALT"}
    found_any = False

    for port, service in common_ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f" • Door {G}{port}{W} [{service}]: {G}OPEN{W}")
            found_any = True
        s.close()
    if not found_any:
        print(f"{Y}[!] No one door is open.{W}")
