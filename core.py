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
    print("\033[31m[-] Errore: La libreria 'phonenumbers' non e' installata.\033[0m")
    print("\033[33m[*] Esegui prima: pip install phonenumbers\033[0m")

G = "\033[32m" # Verde
R = "\033[31m" # Rosso
Y = "\033[33m" # Giallo
B = "\033[34m" # Blu
C = "\033[36m" # Cyan
W = "\033[0m" # Reset

ssl_context = ssl._create_unverified_context()

def my_ip():
    print(f"{B}[+] Analisi della tua interfaccia di rete pubblica...{W}\n")
    try:
        req = urllib.request.Request("https://ipapi.co", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            print(f"{G}✦ IP Pubblico Rilevato:{W} {data.get('ip')}")
            print(f"{G}✦ Fornitore Rete / ISP:{W} {data.get('org')} ({data.get('asn', 'N/A')})")
            print(f"{G}✦ Geolocalizzazione standard:{W} {data.get('city')}, {data.get('region')}, {data.get('country_name')}")
    except Exception:
        print(f"{R}[-] Errore di rete: Impossibile interrogare i server di lookup pubblici.{W}")

def ip_tracker():
    target = input(f"{Y}[?] Inserisci l'indirizzo IP target da tracciare: {W}").strip()
    if not target:
        print(f"{R}[-] Input non valido. Operazione interrotta.{W}")
        return
    print(f"\n{B}[+] Interrogazione nodi geografici per il target: {target}...{W}\n")
    try:
        req = urllib.request.Request(f"https://ipapi.co{target}/json/", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            if "error" in data:
                print(f"{R}[-] Server Error: {data.get('reason', 'IP target non valido o privato')}{W}")
            else:
                print(f"{G}[RISULTATI GEOLOCALIZZAZIONE IP]{W}")
                print(f" • Host Target: {data.get('ip')}")
                print(f" • ASN / Provider: {data.get('org')} ({data.get('asn', 'N/A')})")
                print(f" • Nazione / Codice: {data.get('country_name')} ({data.get('country_code')})")
                print(f" • Regione / Citta': {data.get('region')} / {data.get('city')}")
                print(f" • Fuso Orario (TZ): {data.get('timezone')}")
                print(f" • Coordinate GPS: {data.get('latitude')}, {data.get('longitude')}")
                print(f" • {C}Google Maps Link: https://google.com{data.get('latitude')},{data.get('longitude')}{W}")
    except Exception:
        print(f"{R}[-] Errore di instabilita' della rete o formato IP errato.{W}")

def osint_email():
    email = input(f"{Y}[?] Inserisci l'indirizzo email target: {W}").strip()
    if "@" not in email or "." not in email:
        print(f"{R}[-] Formato email non valido per la ricognizione.{W}")
        return

    username, domain = email.split('@', 1)
    print(f"\n{B}[+] Avvio modulo Deep Reconnaissance su: {email}{W}")
    print(f"{C}─"*60 + f"{W}")

    print(f"{G} Tracciamento Record DNS MX (Mail Servers){W}")
    try:
        mx_records = os.popen(f"nslookup -type=mx {domain}").read()
        if "mail exchanger" in mx_records or "exchanger" in mx_records:
            print(f" {G}• Infrastruttura rilevata:{W}")
            for line in mx_records.split('\n'):
                if "exchanger" in line:
                    print(f" ↳ {line.strip()}")
        else:
            print(f" {Y}• Warning:{W} Nessun server MX esplicito isolato.")
    except Exception:
        print(f" {R}• Fail:{W} Strumento nslookup non disponibile.")

    print(f"\n{G} Analisi Data Breach & Credenziali Compromesse{W}")
    try:
        req = urllib.request.Request(f"https://leakcheck.io{email}", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context, timeout=6) as response:
            res_data = json.loads(response.read().decode())
            if res_data.get("success") and res_data.get("sources"):
                print(f" {R}[⚠️] EMERGENZA SICUREZZA: Email compromessa rilevata nei leak!{W}")
                print(f" {R}• Database Compromessi Rilevati:{W} {len(res_data['sources'])}")
                print(f" {R}• Elenco Breaches Noti (Primi 5):{W} {', '.join(res_data['sources'][:5])}")
            else:
                print(f" {G}[✓] Ottimo: Nessun leak immediato individuato nei database pubblici veloci.{W}")
    except Exception:
        print(f" {Y}• Note:{W} Server Leak-Check saturo o sotto rate limit.")

    print(f"\n{G} Vettori di Analisi Esterna (Pivot Search){W}")
    print(f" • Intelligence Identita': https://haveibeenpwned.com")
    print(f" • Storico Password Plain: https://leakcheck.io")
    print(f" • Mappatura Sottodomini: https://dnsdumpster.com")
    print(f" • Analisi SPF Anti-Spoof: https://mxtoolbox.com{domain}")
def osint_phone():
    phone_input = input(f"{Y}[?] Inserisci numero target (es. +393331234567): {W}").strip()
    print(f"\n{B}[+] Avvio parsing strutturato con la libreria Phonenumbers...{W}")
    print(f"{C}─"*60 + f"{W}")

    try:
        parsed_number = phonenumbers.parse(phone_input, None)
        if not phonenumbers.is_valid_number(parsed_number):
            print(f"{R}[-] ATTENZIONE: Il numero inserito non segue uno standard internazionale valido!{W}\n")

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
        print(f" • Stato Validita': {G if phonenumbers.is_valid_number(parsed_number) else R}{phonenumbers.is_valid_number(parsed_number)}{W}")
        print(f" • Struttura Logica: {G if is_possible else R}Coerente{W if is_possible else R} (Formato non standard){W}")
        print(f" • Codice Paese (CC): +{parsed_number.country_code}")
        print(f" • Numero Nazionale: {parsed_number.national_number}")
        print(f" • Tipologia Linea: {Y}{line_type_str}{W}")
        print(f" • REGIONE / GEOLOCAL: {G}{region_info if region_info else 'Non disponibile'}{W}")
        print(f" • OPERATORE REALE: {Y}{carrier_info if carrier_info else 'Non Rilevato / MVNO'}{W}")
        print(f" • Fusi Orari Rilevati: {', '.join(timezones_info)}")
        print(f"\n{G}[FORMATTAZIONE STANDARD RECON]{W}")
        print(f" • Formato E.164: {formatted_e164}")
        print(f" • Formato Internazionale: {formatted_intl}")
        print(f" • Formato Nazionale: {formatted_nat}")

        clean_phone = formatted_e164.replace('+', '')
    except Exception as e:
        print(f"{R}[-] Errore critico durante il parsing: {str(e)}{W}")
        return

    print(f"\n{G}[PUNTI DI ACCESSO SOCIAL MEDIA & INVESTIGAZIONE]{W}")
    print(f" • Lookup TrueCaller Web Interface: https://truecaller.com{clean_phone}")
    print(f" • Verifica Presenza Account WhatsApp: https://wa.me{clean_phone}")
    print(f" • Analisi Reputazionale Tellows: https://tellows.it{clean_phone}")

def osint_social():
    username = input(f"{Y}[?] Inserisci l'username target da scansionare sui social: {W}").strip()
    if not username:
        print(f"{R}[-] Target non valido.{W}")
        return
    print(f"\n{B}[+] Scansione pacchetti HTTP (Live Verification) per: {username}...{W}\n")

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
                    print(f" [{G}TROVATO{W}] {name}: {url}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f" [{R}NON TROVATO{W}] {name}")
            else:
                print(f" [{Y}PROBABILE{W}] {name} (Codice {e.code})")
        except Exception:
            print(f" [{Y}TIMED OUT{W}] {name}")

def port_scanner():
    target = input(f"{Y}[?] Inserisci l'host o IP bersaglio per il Port Scan: {W}").strip()
    if not target:
        print(f"{R}[-] Destinazione vuota.{W}")
        return
    print(f"\n{B}[+] Avvio mappatura della superficie d'attacco su: {target}...{W}\n")

    common_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 443: "HTTPS", 445: "SMB", 8080: "HTTP-ALT"}
    found_any = False

    for port, service in common_ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f" • Porta {G}{port}{W} [{service}]: {G}APERTA{W}")
            found_any = True
        s.close()
    if not found_any:
        print(f"{Y}[!] Nessuna porta tra quelle principali risulta esposta.{W}")
