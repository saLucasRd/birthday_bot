import os
import discord
import sqlite3
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

#db settings
os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect("data/bot.db")
    cursor = conn.cursor()
    # not ideal, only for debug lol
    # cursor.execute('DROP TABLE IF EXISTS birthdays')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS birthdays ( 
        user_id TEXT PRIMARY KEY NOT NULL UNIQUE,
        username TEXT NOT NULL UNIQUE,
        date TEXT NOT NULL
    )
    ''')
    conn.commit()
    return conn

db_conn = init_db()

#load env
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
server_id = os.getenv("SERVER_ID")
channel_id = int(os.getenv("CHANNEL_ID"))

GUILD_ID = discord.Object(id=server_id)

class Client(commands.Bot):
## avoid an ifinite loop 
    async def on_message(self, message):
        if message.author == self.user:
            return
## test response 
        if message.content.startswith("hello"):
            await message.channel.send(f"Hi there {message.author}") 



intents = discord.Intents.default()
intents.message_content = True
#commands prefix are outdated
client = Client(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    try:
            guild = discord.Object(id=server_id)
            synced = await client.tree.sync(guild=guild)
            print(f"synced {len(synced)} commands to guild {guild.id}")
    except Exception as e:
            print(f"Error syncing commands: {e}")

    client.loop.create_task(check_birthdays())


async def check_birthdays():
    await client.wait_until_ready()
    last_checked_date = None
    
    while not client.is_closed():
        try:
            current_date = datetime.now(timezone.utc).strftime("%d/%m")
            
            # Only check if the date has changed since last check
            if current_date != last_checked_date:
                last_checked_date = current_date
                
                cursor = db_conn.cursor()
                cursor.execute(
                    "SELECT user_id, username FROM birthdays WHERE date LIKE ?",
                    (f"%{current_date}%",))
                birthdays = cursor.fetchall()
                
                if birthdays:
                    channel = client.get_channel(channel_id)
                    if channel:
                        for user_id, username in birthdays:
                            await channel.send(f"🎉 @everyone, today is <@{user_id}>'s birthday! 🎂")
            
            # Check every minute (adjust as needed)
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"Error checking birthdays: {e}")
            await asyncio.sleep(3600)

# create slash / command
#@client.tree.command(name="input", description="add your birthday", guild=GUILD_ID)
#async def birthday_input(interaction: discord.Integration):
#    await interaction.response.send_message("input test")

@client.tree.command(name="date", description="Input your birthday in day/month format", guild=GUILD_ID)
async def birthday_date(interaction: discord.Integration, date: str):
    try:
        datetime.strptime(date, "%d/%m/%Y")

        cursor = db_conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO birthdays (user_id ,username, date) VALUES (?, ?, ?)",
            (str(interaction.user.id), str(interaction.user.name), date)
        )
        db_conn.commit()

        await interaction.response.send_message((f"🎉 <@{interaction.user.id}> birthday ({date}) has been saved!"))
    except ValueError:
        await interaction.response.send_message("❌ Invalid date format! Please use DD/MM/YY")
    except Exception as e:
        await interaction.response.send_message(f"❌ An error occurred: {str(e)}")


@client.tree.command(name="birthdays", description="List all birthdays registered in the server", guild=GUILD_ID)
async def query_bd(interaction: discord.Integration):
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT username, date FROM birthdays")
        rows = cursor.fetchall()

        if not rows:
            await interaction.response.send_message("No birthdays have been registered yet! 😭")
            return
    
        message = "📆 **Birthdays Registered in the Server:**\n"
        for username, date in rows:
            message += f"- {username}: {date}\n"

        await interaction.response.send_message(message)
    except Exception as e:
        await interaction.response.send_message(f"❌ An error occurred: {str(e)}")

client.run(discord_token)