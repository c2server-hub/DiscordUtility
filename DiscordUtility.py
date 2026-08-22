#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import time
import os
from datetime import datetime

# ---------- ANSI colors (UI améliorée) ----------
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"

def print_color(text, color=COLOR_RESET):
    print(f"{color}{text}{COLOR_RESET}")

# ---------- Banner ----------
BANNER = """
 ██████████    ███                                          █████ █████  █████  █████     ███  ████   ███   █████              
▒▒███▒▒▒▒███  ▒▒▒                                          ▒▒███ ▒▒███  ▒▒███  ▒▒███     ▒▒▒  ▒▒███  ▒▒▒   ▒▒███               
 ▒███   ▒▒███ ████   █████   ██████   ██████  ████████   ███████  ▒███   ▒███  ███████   ████  ▒███  ████  ███████   █████ ████
 ▒███    ▒███▒▒███  ███▒▒   ███▒▒███ ███▒▒███▒▒███▒▒███ ███▒▒███  ▒███   ▒███ ▒▒▒███▒   ▒▒███  ▒███ ▒▒███ ▒▒▒███▒   ▒▒███ ▒███ 
 ▒███    ▒███ ▒███ ▒▒█████ ▒███ ▒▒▒ ▒███ ▒███ ▒███ ▒▒▒ ▒███ ▒███  ▒███   ▒███   ▒███     ▒███  ▒███  ▒███   ▒███     ▒███ ▒███ 
 ▒███    ███  ▒███  ▒▒▒▒███▒███  ███▒███ ▒███ ▒███     ▒███ ▒███  ▒███   ▒███   ▒███ ███ ▒███  ▒███  ▒███   ▒███ ███ ▒███ ▒███ 
 ██████████   █████ ██████ ▒▒██████ ▒▒██████  █████    ▒▒████████ ▒▒████████    ▒▒█████  █████ █████ █████  ▒▒█████  ▒▒███████ 
▒▒▒▒▒▒▒▒▒▒   ▒▒▒▒▒ ▒▒▒▒▒▒   ▒▒▒▒▒▒   ▒▒▒▒▒▒  ▒▒▒▒▒      ▒▒▒▒▒▒▒▒   ▒▒▒▒▒▒▒▒      ▒▒▒▒▒  ▒▒▒▒▒ ▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒    ▒▒▒▒▒███ 
                                                                                                                      ███ ▒███ 
                                                                                                                     ▒▒██████  
                                                                                                                      ▒▒▒▒▒▒                                                                           
"""


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def parser():
    print("=" * 80, COLOR_CYAN)

def banner():
    print(BANNER, COLOR_CYAN)

def get_own_user(token):
    """Fetch own user info."""
    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

def get_guilds(token):
    """Fetch list of guilds the user is in."""
    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

def leave_guild(token, guild_id):
    """Leave a guild."""
    headers = {"Authorization": token}
    r = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", headers=headers)
    return r.status_code == 204

def fetch_relationships(token):
    """Fetch all relationships."""
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = "https://discord.com/api/v9/users/@me/relationships"
    try:
        r = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print_color(f"[!] Network error: {e}", COLOR_RED)
        return None
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 401:
        print_color("[!] Invalid or expired token.", COLOR_RED)
        return None
    elif r.status_code == 429:
        retry = r.headers.get('Retry-After', 'a few')
        print_color(f"[!] Rate limited. Wait {retry} seconds.", COLOR_YELLOW)
        return None
    else:
        print_color(f"[!] Error {r.status_code}: {r.text[:200]}", COLOR_RED)
        return None

def get_friends_list(token):
    """Return list of friends (type=1) with user info and status if available."""
    data = fetch_relationships(token)
    if data is None:
        return None
    friends = []
    for rel in data:
        if rel.get("type") == 1:
            user = rel.get("user", {})
            # Add a status field (will be filled later if possible)
            user["status"] = "unknown"  # placeholder
            friends.append(rel)
    return friends

def get_friend_status(token, user_id):
    return "unknown"

def format_date(date_iso):
    if not date_iso:
        return "Unknown date"
    try:
        dt = datetime.fromisoformat(date_iso.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y at %H:%M")
    except:
        return date_iso

def send_dm(token, user_id, content, file_path=None):
    """Send a DM with optional attachment."""
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    # Create DM channel
    r = requests.post(
        "https://discord.com/api/v9/users/@me/channels",
        headers=headers,
        json={"recipient_id": user_id}
    )
    if r.status_code not in [200, 201]:
        print_color(f"[!] Failed to create DM for {user_id} (code {r.status_code})", COLOR_RED)
        return False
    dm_channel = r.json()
    channel_id = dm_channel['id']

    # Send message
    payload = {"content": content}
    files = None
    if file_path and os.path.isfile(file_path):
        files = {'file': open(file_path, 'rb')}
        # For file upload, we need multipart form-data, not JSON
        # We'll use the requests.post with files param, but need to drop Content-Type header
        headers.pop("Content-Type", None)
        r = requests.post(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            data={"content": content},
            files=files
        )
    else:
        r = requests.post(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            json=payload
        )
    if r.status_code == 200:
        print_color(f"[+] Message sent to {user_id}", COLOR_GREEN)
        return True
    else:
        print_color(f"[!] Failed to send to {user_id} (code {r.status_code})", COLOR_RED)
        return False

# ---------- Progress bar ----------
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Call in a loop to create terminal progress bar.
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()

# ---------- Display functions ----------
def display_friend_list(friends, show_status=False):
    if not friends:
        print_color("[!] No friends found.", COLOR_YELLOW)
        return
    print_color(f"\n[+] {len(friends)} friend(s) found.", COLOR_GREEN)
    print("=" * 80)
    for i, rel in enumerate(friends, 1):
        user = rel.get("user", {})
        uid = user.get("id", "N/A")
        username = user.get("username", "N/A")
        global_name = user.get("global_name") or "No display name"
        avatar_hash = user.get("avatar", "")
        avatar_url = f"https://cdn.discordapp.com/avatars/{uid}/{avatar_hash}.png" if avatar_hash else "No avatar"
        since = format_date(rel.get("since"))
        status = user.get("status", "unknown")  # will always be unknown

        print(f"{i}. @{username} (ID: {uid})")
        print(f"   Display name : {global_name}")
        print(f"   Added on     : {since}")
        print(f"   Avatar       : {avatar_url}")
        if show_status:
            print(f"   Status       : {status}")
        print("-" * 80)

def search_friends(friends, query):
    """Search by username or display name (case-insensitive)."""
    query = query.lower()
    results = []
    for rel in friends:
        user = rel.get("user", {})
        username = user.get("username", "").lower()
        global_name = user.get("global_name", "").lower()
        if query in username or query in global_name:
            results.append(rel)
    return results

def display_own_info(user):
    if not user:
        print_color("[!] Could not fetch your info.", COLOR_RED)
        return
    banner()
    parser()
    print_color("\n[+] Your Discord account:", COLOR_CYAN)
    print(f"  ID            : {user.get('id')}")
    print(f"  Username      : {user.get('username')}")
    print(f"  Discriminator : {user.get('discriminator', '0')}")
    print(f"  Global name   : {user.get('global_name', 'None')}")
    print(f"  Email         : {user.get('email', 'Hidden')}")
    print(f"  Verified      : {user.get('verified', False)}")
    print(f"  Created at    : {format_date(user.get('created_at'))}")

def display_guilds(guilds):
    if not guilds:
        print_color("[!] No guilds found.", COLOR_YELLOW)
        return
    print_color(f"\n[+] You are in {len(guilds)} guild(s):", COLOR_CYAN)
    for i, g in enumerate(guilds, 1):
        name = g.get('name', 'Unknown')
        gid = g.get('id')
        owner = g.get('owner', False)
        print(f"{i}. {name} (ID: {gid}) - {'Owner' if owner else 'Member'}")

def display_statistics(friends):
    total = len(friends)
    oldest_date = None
    oldest_user = None
    for rel in friends:
        since = rel.get("since")
        if since:
            try:
                dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
                if oldest_date is None or dt < oldest_date:
                    oldest_date = dt
                    oldest_user = rel.get("user", {}).get("username")
            except:
                pass
    banner()
    parser()
    print_color("\n[+] Statistics:", COLOR_CYAN)
    print(f"  Total friends        : {total}")
    if oldest_date:
        print(f"  Oldest friend added  : {oldest_user} on {oldest_date.strftime('%d/%m/%Y at %H:%M')}")
    else:
        print("  Oldest friend added  : N/A")

# ---------- Main menu ----------
def main_menu():
    cls()
    print_color(BANNER, COLOR_BLUE)
    print_color("=" * 50, COLOR_BOLD)
    print_color("  Discord Utility - Main Menu", COLOR_CYAN)
    print_color("=" * 50, COLOR_BOLD)
    print("  1. Friends Management")
    print("  2. Messaging")
    print("  3. Account & Servers")
    print("  4. Information & Statistics")
    print("  5. Quit")
    print_color("=" * 50, COLOR_BOLD)
    return input("Enter your choice (1-5): ").strip()

def friends_management(token, friends):
    while True:
        cls()
        banner()
        parser()
        print_color("\n--- Friends Management ---", COLOR_CYAN)
        print("  1. List all friends")
        print("  2. Search friends by name")
        print("  3. Show status (placeholder - not available via REST)")
        print("  4. Back to main menu")
        parser()
        choice = input("Choice: ").strip()
        if choice == "1":
            display_friend_list(friends, show_status=False)
            input("\nPress Enter to continue...")
        elif choice == "2":
            query = input("Enter name to search: ").strip()
            if query:
                results = search_friends(friends, query)
                if results:
                    display_friend_list(results, show_status=False)
                else:
                    print_color("[!] No friends match.", COLOR_YELLOW)
            else:
                print_color("[!] Empty query.", COLOR_YELLOW)
            input("\nPress Enter to continue...")
        elif choice == "3":
            # Show status - we can't, but we inform.
            print_color("[!] Status is not available via REST API. To get presence, use the Gateway.", COLOR_YELLOW)
            input("\nPress Enter to continue...")
        elif choice == "4":
            break
        else:
            print_color("[!] Invalid choice.", COLOR_RED)
            time.sleep(1)

def messaging(token, friends):
    while True:
        cls()
        banner()
        parser()
        print_color("\n--- Messaging ---", COLOR_CYAN)
        print("  1. Send message to a single friend")
        print("  2. Send message to multiple friends (select by numbers)")
        print("  3. Send message to ALL friends (with progress bar)")
        print("  4. Back to main menu")
        parser()
        choice = input("Choice: ").strip()
        if choice == "1":
            if not friends:
                print_color("[!] No friends.", COLOR_YELLOW)
                time.sleep(1)
                continue
            # Display friends list with indices
            for idx, rel in enumerate(friends):
                user = rel.get("user", {})
                print(f"{idx}. @{user.get('username')} (ID: {user.get('id')})")
            target_idx = input("Enter friend number or ID: ").strip()
            if target_idx.isdigit():
                idx = int(target_idx)
                if 0 <= idx < len(friends):
                    target_id = friends[idx]['user']['id']
                else:
                    target_id = target_idx  # might be an ID
            else:
                target_id = target_idx
            message = input("Message content: ").strip()
            if not message:
                print_color("[!] Empty message.", COLOR_YELLOW)
                continue
            file_path = input("Attachment path (leave empty for none): ").strip() or None
            send_dm(token, target_id, message, file_path)
            input("\nPress Enter to continue...")
        elif choice == "2":
            if not friends:
                print_color("[!] No friends.", COLOR_YELLOW)
                time.sleep(1)
                continue
            # Show list
            for idx, rel in enumerate(friends):
                user = rel.get("user", {})
                print(f"{idx}. @{user.get('username')} (ID: {user.get('id')})")
            indices = input("Enter friend numbers separated by commas (e.g., 0,2,5): ").strip()
            if not indices:
                continue
            selected = []
            for part in indices.split(','):
                part = part.strip()
                if part.isdigit():
                    idx = int(part)
                    if 0 <= idx < len(friends):
                        selected.append(friends[idx]['user']['id'])
            if not selected:
                print_color("[!] No valid selections.", COLOR_YELLOW)
                continue
            message = input("Message content: ").strip()
            if not message:
                print_color("[!] Empty message.", COLOR_YELLOW)
                continue
            file_path = input("Attachment path (leave empty for none): ").strip() or None
            print_color(f"\nSending to {len(selected)} friends...", COLOR_CYAN)
            success = 0
            total = len(selected)
            for i, uid in enumerate(selected, 1):
                print_progress_bar(i, total, prefix='Progress', suffix='Complete')
                if send_dm(token, uid, message, file_path):
                    success += 1
                time.sleep(2)  # rate limit protection
            print_color(f"\nDone. {success}/{total} messages sent.", COLOR_GREEN)
            input("\nPress Enter to continue...")
        elif choice == "3":
            if not friends:
                print_color("[!] No friends.", COLOR_YELLOW)
                time.sleep(1)
                continue
            print_color(f"[!] You are about to send a message to ALL {len(friends)} friends.", COLOR_YELLOW)
            confirm = input("Type 'yes' to confirm: ").strip().lower()
            if confirm != "yes":
                continue
            message = input("Message content: ").strip()
            if not message:
                print_color("[!] Empty message.", COLOR_YELLOW)
                continue
            file_path = input("Attachment path (leave empty for none): ").strip() or None
            delay = input("Delay between each send (seconds, default=2): ").strip()
            try:
                delay = int(delay) if delay else 2
            except:
                delay = 2
            print_color(f"\nSending to all friends...", COLOR_CYAN)
            success = 0
            total = len(friends)
            for i, rel in enumerate(friends, 1):
                uid = rel['user']['id']
                print_progress_bar(i, total, prefix='Progress', suffix='Complete')
                if send_dm(token, uid, message, file_path):
                    success += 1
                if i < total:
                    time.sleep(delay)
            print_color(f"\nDone. {success}/{total} messages sent.", COLOR_GREEN)
            input("\nPress Enter to continue...")
        elif choice == "4":
            break
        else:
            print_color("[!] Invalid choice.", COLOR_RED)
            time.sleep(1)

def account_servers(token):
    while True:
        cls()
        banner()
        parser()
        print_color("\n--- Account & Servers ---", COLOR_CYAN)
        print("  1. View my account info")
        print("  2. List my servers")
        print("  3. Leave a server")
        print("  4. Back to main menu")
        parser()
        choice = input("Choice: ").strip()
        if choice == "1":
            user = get_own_user(token)
            display_own_info(user)
            input("\nPress Enter to continue...")
        elif choice == "2":
            guilds = get_guilds(token)
            display_guilds(guilds)
            input("\nPress Enter to continue...")
        elif choice == "3":
            guilds = get_guilds(token)
            if not guilds:
                print_color("[!] No guilds.", COLOR_YELLOW)
                time.sleep(1)
                continue
            display_guilds(guilds)
            gid = input("Enter the ID of the server to leave: ").strip()
            if not gid:
                continue
            confirm = input(f"Are you sure you want to leave server ID {gid}? (yes/no): ").strip().lower()
            if confirm == "yes":
                if leave_guild(token, gid):
                    print_color("[+] Successfully left server.", COLOR_GREEN)
                else:
                    print_color("[!] Failed to leave server.", COLOR_RED)
            else:
                print_color("[!] Cancelled.", COLOR_YELLOW)
            input("\nPress Enter to continue...")
        elif choice == "4":
            break
        else:
            print_color("[!] Invalid choice.", COLOR_RED)
            time.sleep(1)

def statistics_menu(friends):
    cls()
    display_statistics(friends)
    input("\nPress Enter to continue...")


def main():
    cls()
    print_color(BANNER, COLOR_BLUE)
    print_color("[!] WARNING: This script uses private Discord endpoints.", COLOR_RED)
    print_color("[!] Its use may result in your account being BANNED.\n", COLOR_RED)
    token = input("Paste your Discord user token: ").strip()
    if not token:
        print_color("[!] Token required.", COLOR_RED)
        return

    print("\n[*] Connecting to Discord...")
    friends = get_friends_list(token)
    if friends is None:
        print_color("[!] Unable to retrieve friends. Check your token.", COLOR_RED)
        return
    # Also store user info for later
    user = get_own_user(token)
    if user:
        print_color(f"[+] Logged in as {user.get('username')} (ID: {user.get('id')})", COLOR_GREEN)
    else:
        print_color("[!] Could not fetch your own info.", COLOR_YELLOW)

    print_color(f"[+] Found {len(friends)} friend(s).", COLOR_GREEN)
    time.sleep(1)

    while True:
        choice = main_menu()
        if choice == "1":
            friends_management(token, friends)
        elif choice == "2":
            messaging(token, friends)
        elif choice == "3":
            account_servers(token)
        elif choice == "4":
            statistics_menu(friends)
        elif choice == "5":
            print_color("[+] Goodbye!", COLOR_GREEN)
            break
        else:
            print_color("[!] Invalid choice.", COLOR_RED)
            time.sleep(1)

if __name__ == "__main__":
    main()