import os
import pytz
import time
import requests
from datetime import datetime
from colorama import Fore, Style, init
from fake_useragent import UserAgent

init(autoreset=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def art():
    GREEN = Fore.GREEN
    RED = Fore.LIGHTRED_EX
    BLUE = Fore.CYAN
    YELLOW = Fore.YELLOW
    RESET = Style.RESET_ALL

    print(f"{GREEN}██████   █████  ███    ██  █████       ██████  ██████  ██████  ███████ ███████{RESET}")
    print(f"{GREEN}██   ██ ██   ██ ████   ██ ██   ██     ██      ██    ██ ██   ██ ██      ██     {RESET}")
    print(f"{YELLOW}██████  ███████ ██ ██  ██ ███████     ██      ██    ██ ██   ██ █████   ███████{RESET}")
    print(f"{RED}██   ██ ██   ██ ██  ██ ██ ██   ██     ██      ██    ██ ██   ██ ██           ██{RESET}")
    print(f"{RED}██████  ██   ██ ██   ████ ██   ██      ██████  ██████  ██████  ███████ ███████{RESET}\n")

    print(f"{YELLOW} Made and written by {BLUE}ZERO CODES{RESET} {RED}||{RESET} {BLUE}@zerodcode{RESET}")
    print(f"{GREEN} Join Telegram group: {YELLOW} https://t.me/+FfYIYEJSKQFhZmRk{RESET}\n")

    print(f"{RED}➡Auto claim{RESET}")
    print(f"{GREEN}➡Auto tasks{RESET}")
    print(f"{BLUE}➡Auto spin{RESET}")

def load_or_ask_query_id(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            query_id = file.read().strip()
            if query_id:
                print(f"{Fore.LIGHTYELLOW_EX}Found saved query_id: {Fore.LIGHTCYAN_EX}{query_id}")
                use_saved = input(f"{Fore.LIGHTGREEN_EX}Do you want to use the saved query_id? (y/n): ").strip().lower()
                if use_saved == 'y':
                    return query_id

    query_id = input(f"{Fore.LIGHTGREEN_EX}Enter your query_id: ").strip()
    with open(filename, 'w') as file:
        file.write(query_id)
    print(f"{Fore.LIGHTBLUE_EX}Your query_id has been saved successfully!")
    return query_id

def load_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_headers(token):
    ua = UserAgent()
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-length': '0',
        'dnt': '1',
        'origin': 'https://cf.seeddao.org',
        'priority': 'u=1, i',
        'referer': 'https://cf.seeddao.org/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'telegram-data': token,
        'user-agent': ua.random
    }

def handle_request(method, url, headers, data=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        print(f"{Fore.RED + Style.BRIGHT}Request timed out.")
    except requests.ConnectionError:
        print(f"{Fore.RED + Style.BRIGHT}Connection error occurred.")
    except requests.RequestException as e:
        if "login-bonuses" in str(e):
            print(f"{Fore.YELLOW + Style.BRIGHT}Daily bonus already claimed, please come back tomorrow.")
        elif "seed/claim" in str(e):
            print(f"{Fore.YELLOW + Style.BRIGHT}Claim is not available now.")
        else:
            print(f"{Fore.RED + Style.BRIGHT}Request failed.")
    return None

def login(token):
    url_profile = "https://elb.seeddao.org/api/v1/profile2"
    url_balance = "https://elb.seeddao.org/api/v1/profile/balance"
    headers = get_headers(token)

    data = handle_request('GET', url_profile, headers)
    balance_data = handle_request('GET', url_balance, headers)
    if balance_data:
        balance = balance_data.get("data") / 1000000000
        print(f"{Fore.GREEN + Style.BRIGHT}Balance: {Fore.WHITE + Style.BRIGHT}{balance:.3f}")

def daily_bonus(token):
    url_bonus = "https://elb.seeddao.org/api/v1/login-bonuses"
    headers = get_headers(token)

    response_data = handle_request('POST', url_bonus, headers)
    if response_data:
        reward = response_data.get("data", {}).get("amount")
        print(f"{Fore.GREEN + Style.BRIGHT}Daily Reward Claimed: {Fore.WHITE + Style.BRIGHT}{int(reward)/1000000000}" if reward else f"{Fore.YELLOW + Style.BRIGHT}Daily Reward Already Claimed")

def claim(token):
    url_claim = "https://elb.seeddao.org/api/v1/seed/claim"
    headers = get_headers(token)

    response_data = handle_request('POST', url_claim, headers)
    if response_data:
        amount = response_data.get("data", {}).get("amount")
        print(f"{Fore.GREEN + Style.BRIGHT}Seed Claimed: {Fore.WHITE + Style.BRIGHT}{int(amount)/1000000000}" if amount else f"{Fore.YELLOW + Style.BRIGHT}Seed Already Claimed")

def spin(token):
    url_ticket = "https://elb.seeddao.org/api/v1/spin-ticket"
    url_spin = "https://elb.seeddao.org/api/v1/spin-reward"
    headers = get_headers(token)

    ticket_data = handle_request('GET', url_ticket, headers)
    if ticket_data:
        tickets = ticket_data.get('data', [])
        for ticket in tickets:
            body_spin = {'ticket_id': ticket['id']}
            spin_data = handle_request('POST', url_spin, headers, data=body_spin)
            if spin_data:
                print(f"{Fore.CYAN + Style.BRIGHT}Spin Reward: {spin_data.get('data', {}).get('type')}")

def task(token):
    url_tasks = "https://elb.seeddao.org/api/v1/tasks/progresses"
    headers = get_headers(token)

    task_data = handle_request('GET', url_tasks, headers)
    if task_data:
        tasks = task_data.get('data', [])
        for task in tasks:
            url_complete = f"https://elb.seeddao.org/api/v1/tasks/{task['id']}"
            task_complete_data = handle_request('POST', url_complete, headers)
            if task_complete_data:
                task_name = task.get('name', 'Unknown Task')
                print(f"{Fore.GREEN + Style.BRIGHT}Task '{task_name}' Completed")
            time.sleep(5)

def countdown_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print(f"{Fore.CYAN + Style.BRIGHT}Wait {hours:02}:{mins:02}:{secs:02}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("Wait 00:00:00          ", end='\r')

def main():
    clear_terminal()
    art()

    query_id = load_or_ask_query_id('data.txt')
    run_task = input("Do you want to run task(token)? (y/n): ").strip().lower()
    
    while True:
        tokens = load_tokens('data.txt')
        if not tokens:
            print(f"{Fore.RED}No tokens found! Please ensure the file contains valid tokens.")
            break

        clear_terminal()
        art()

        for i, token in enumerate(tokens, start=1):
            print(f"{Fore.CYAN + Style.BRIGHT}------Account No.{i}------{Style.RESET_ALL}")
            login(token)
            daily_bonus(token)
            claim(token)
            spin(token)
            if run_task == 'y':
                task(token)

        countdown_timer(1 * 60 * 60)  # Wait for 1 hour before running again

if __name__ == "__main__":
    main()