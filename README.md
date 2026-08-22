DiscordUtility

A command-line interactive tool to manage your Discord friends, send bulk
messages, and administer your servers using your user token.


IMPORTANT WARNING

Using a user token for automated actions is strictly prohibited by Discord's
Terms of Service. This tool is provided for educational purposes only. You are
solely responsible for any consequences, including the permanent ban of your
account.


FEATURES

Friend Management
- Display full friend list (name, ID, avatar, added date)
- Search friends by name (username or display name)
- Show statistics (total count, oldest friend)

Advanced Messaging
- Send a message to a specific friend
- Send to multiple selected friends (by numbers)
- Send to ALL friends with a progress bar and configurable delay
- Attach a file to messages

Account & Server Management
- View your own account information (ID, email, etc.)
- List all servers you are in
- Leave a server (with confirmation)

Enhanced User Interface
- Interactive menus with ANSI colors
- Clear messages and confirmations for dangerous actions
- Error handling and rate-limit management


INSTALLATION

Prerequisites:
- Python 3.6 or higher
- The 'requests' module

Steps:
1. Download the script (e.g., with git):
   git clone https://github.com/your-username/DiscordUtility.git
   cd DiscordUtility

2. Install dependencies:
   pip install requests

3. Run the script:
   python DiscordUtility.py


GETTING YOUR USER TOKEN

Caution: Handling your token is risky. Never share it with anyone.

1. Open Discord in your browser (web version).
2. Press F12 to open Developer Tools.
3. Go to the Application (or Storage) tab.
4. Under Cookies, look for the cookie named 'token'.
5. Copy its value (a long alphanumeric string).

You can also use a browser extension dedicated to retrieving tokens, but be
cautious.


USAGE

Run the script. You will be greeted by a main menu:

  Discord Utility - Main Menu
  1. Friends Management
  2. Messaging
  3. Account & Servers
  4. Information & Statistics
  5. Quit
  Enter your choice (1-5):

Example workflows:
- View all your friends: 1 -> 1
- Send a message to all friends: 2 -> 3 -> yes -> enter message -> delay ->
  progress bar
- Leave a server: 3 -> 3 -> select the server ID -> confirm

All actions are guided step-by-step.


ADVANCED OPTIONS

- Delay between sends: adjustable in the mass-send menu (default 2 seconds).
- File attachment: you can provide a local file path to send with the message.
- Name search: case-insensitive, filters on 'username' and 'global_name'.


CODE STRUCTURE

The script is organized into modular functions:
- get_friends_list() – fetch friend list
- send_dm() – send a message (with or without file)
- print_progress_bar() – display progress bar
- display_*() – formatted outputs
- friends_management(), messaging(), account_servers() – sub-menus


SECURITY & BEST PRACTICES

- Never share your token.
- Prefer using a secondary account for testing.
- Respect delays between requests to avoid rate-limiting.
- Be aware that any automated action can be detected.


CONTRIBUTING

Contributions are welcome! You can:
- Suggest new features
- Report bugs
- Propose code improvements

Open an issue or a pull request on GitHub.


LICENSE

This project is licensed under the MIT License – see the LICENSE file for
details.


FAQ

Q: Why is online status not displayed?
A: The Discord REST API does not provide presence status. To obtain status, you
   would need to use the Gateway (WebSocket), which is not implemented here.

Q: Can I use this script with a bot?
A: No. The script uses a user token, not a bot token. It acts as if you are
   logged in with your own account.

Q: Can the script get me banned?
A: Yes. Automated use of a user token violates Discord's Terms of Service. Use
   at your own risk.


ACKNOWLEDGEMENTS

Thanks to the Discord community for the API and to all developers who share
their knowledge.

Last updated: August 2026
Author: Your Name
