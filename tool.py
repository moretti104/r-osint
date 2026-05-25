#!/usr/bin/env python3
import os
import sys
import time

try:
    import core
except ImportError:
    print("\033[31m[-]no nano named:core.py.\033[0m")
    sys.exit(1)

# clean screen
def clear_screen():
    print("\033[H\033[J", end="")

def lolcat_print(text):
    colors = [
        "\033[38;5;196m", "\033[38;5;202m", "\033[38;5;208m", "\033[38;5;214m",
        "\033[38;5;220m", "\033[38;5;226m", "\033[38;5;190m", "\033[38;5;154m",
        "\033[38;5;118m", "\033[38;5;82m", "\033[38;5;46m", "\033[38;5;48m",
        "\033[38;5;51m", "\033[38;5;45m", "\033[38;5;39m", "\033[38;5;27m",
        "\033[38;5;21m", "\033[38;5;57m", "\033[38;5;93m", "\033[38;5;129m",
        "\033[38;5;165m", "\033[38;5;201m"
    ]
    lines = text.split('\n')
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(f"{color}{line}\033[0m")

C = "\033[36m" # Ciano
G = "\033[32m" # Verde
R = "\033[31m" # Rosso
Y = "\033[33m" # Giallo
W = "\033[0m" # Reset

def pause():
    print(f"\n{Y}[*] task finished.{W}")
    input(f"{G}Press enter [/] to go on menu{W}")

def banner():
    figlet_art = """
   ____code by moretti_____
                     _       _
 _ __       ___  ___(_)_ __ | |_
| '__|____ / _ \/ __| | '_ \| __|
| | |_____| (_) \__ \ | | | | |_
|_|        \___/|___/_|_| |_|\__|
    """
    lolcat_print(figlet_art)
    print(f"{C}" + "═"*57 + f"{W}")
    print(f"{G} [ R-OSINT SEC v2.5 - LIBPHONENUMBER RECON ] {W}")
    print(f"{C}" + "═"*57 + f"{W}\n")

def main():
    while True:
        clear_screen()
        banner()
        print(f"{C}1){W} show my ip")
        print(f"{C}2){W} ip tracker")
        print(f"{C}3){W} osint email")
        print(f"{C}4){W} osint phone")
        print(f"{C}5){W} osint social username (Live Check)")
        print(f"{C}6){W} network reconnaissance (Port Scanner)")
        print(f"{R}0){W} exit\n")

        choice = input(f"{G}select option > {W}").strip()

        if choice == "1":
            clear_screen()
            core.my_ip()
            pause()
        elif choice == "2":
            clear_screen()
            core.ip_tracker()
            pause()
        elif choice == "3":
            clear_screen()
            core.osint_email()
            pause()
        elif choice == "4":
            clear_screen()
            core.osint_phone()
            pause()
        elif choice == "5":
            clear_screen()
            core.osint_social()
            pause()
        elif choice == "6":
            clear_screen()
            core.port_scanner()
            pause()
        elif choice == "0":
            clear_screen()
            print(f"{Y}r-osint is closing...{W}")
            sys.exit(0)
        else:
            print(f"\n{R}[!] please select an correct option{W}")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] closing process...{W}")
        sys.exit(0)
