# 🎉 Birthday Bot 🎂
To Rafael, who inspired me to create this project

A Discord bot that reminds your server when it's someone's birthday! It allows users to register their birthdays, lists all registered birthdays, and sends a message in a specified channel on the special day.


---

## Features

- **Register Birthdays**: Users can register their birthdays using the `/date` command.
- **Birthday Reminders**: The bot sends a message in a specified channel on a user's birthday.
- **List Birthdays**: Admins and users can view all registered birthdays using the `/birthdays` command.
- **Simple and Lightweight**: Built with Python, SQLite, and the `discord.py` library.

---

## Commands

| Command              | Description                                      | Example                     |
|----------------------|--------------------------------------------------|-----------------------------|
| `/date DD/MM`        | Register your birthday.                          | `/date 10/07`               |
| `/birthdays`         | List all registered birthdays in the server.     | `/birthdays`                |


---

## Setup

### Prerequisites

1. **Python 3.8 or higher**: Download and install Python from [python.org](https://www.python.org/).
2. **Discord Bot Token**: Create a bot on the [Discord Developer Portal](https://discord.com/developers/applications) and get the bot token.
3. **Server ID and Channel ID**: Enable Developer Mode in Discord to get the server ID and channel ID.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/birthday-bot.git
   cd birthday-bot
2. **Install Dependencies:**
   ```bash
    pip install -r requirements.txt
3. **Set Up Environment Variables:**

    Create a .env file in the root directory:
    ```env

    DISCORD_TOKEN=your-discord-bot-token
    SERVER_ID=your-server-id
    CHANNEL_ID=your-channel-id

4. **Run the Bot:**
    ```bash
    python bot.py
 ---
### Future Additions
- Birthday Roles: Automatically assign a special role (e.g., "🎂 Birthday Person") to users on their birthday and remove it after 24 hours.
- Birthday Countdown: Add a command to show how many days are left until a user's birthday.
- Birthday Leaderboard: Display a leaderboard of upcoming birthdays in the server.
- Admin Commands: Allow admins to manage birthdays (e.g., delete or update birthdays for other users).