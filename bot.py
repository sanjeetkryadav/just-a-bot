import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

# Prefix storage file
PREFIX_FILE = 'prefix.json'

def load_prefix(guild_id=None):
    if os.path.exists(PREFIX_FILE):
        with open(PREFIX_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if guild_id and str(guild_id) in data:
                return data[str(guild_id)]
            return data.get('default', '$')
    return '$'

def save_prefix(guild_id, prefix):
    data = {}
    if os.path.exists(PREFIX_FILE):
        with open(PREFIX_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    if guild_id:
        data[str(guild_id)] = prefix
    else:
        data['default'] = prefix
    with open(PREFIX_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)

# Use a function for command_prefix
async def get_prefix(bot, message):
    guild_id = message.guild.id if message.guild else None
    return load_prefix(guild_id)

bot = commands.Bot(command_prefix=get_prefix, intents=intents)

guild_id = os.getenv('GUILD_ID')
if guild_id:
    guild = discord.Object(id=int(guild_id))
else:
    guild = None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync(guild=guild)
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return
    # % prefix feature
    if message.content.startswith('%'):
        content = message.content[1:]
        if content.strip():
            await message.channel.send(content)
    # Dynamic delete command
    prefix = await get_prefix(bot, message)
    if message.content.startswith(f'{prefix}delete'):
        # Check if user has administrator permissions
        if not message.author.guild_permissions.administrator:
            confirm_msg = await message.channel.send("❌ You need administrator permissions to use this command!")
            await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=3))
            await confirm_msg.delete()
            return
        parts = message.content.split()
        if len(parts) == 2:
            arg = parts[1].strip().lower()
            if arg == 'all':
                # Delete all messages in the channel (limit 100 at a time)
                deleted = await message.channel.purge(limit=None)
                confirm_msg = await message.channel.send(f"Deleted {len(deleted)} messages.")
                await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=2))
                await confirm_msg.delete()
            elif arg.isdigit():
                num = int(arg)
                if num > 0:
                    deleted = await message.channel.purge(limit=num+1)  # +1 to include the command message
                    confirm_msg = await message.channel.send(f"Deleted {len(deleted)-1} messages.")
                    await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=2))
                    await confirm_msg.delete()
                else:
                    confirm_msg = await message.channel.send("Please provide a positive number.")
                    await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=2))
                    await confirm_msg.delete()
            else:
                confirm_msg = await message.channel.send(f"Usage: {prefix}delete all or {prefix}delete <number>")
                await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=2))
                await confirm_msg.delete()
        else:
            confirm_msg = await message.channel.send(f"Usage: {prefix}delete all or {prefix}delete <number>")
            await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=2))
            await confirm_msg.delete()
        return  # Prevent further processing for delete command
    # Allow commands to work
    await bot.process_commands(message)

# /greet command
greet_cmd = app_commands.Command(
    name="greet",
    description="Sends a greeting message.",
    callback=lambda interaction: interaction.response.send_message("hey how are you doing")
)
if guild:
    greet_cmd.guilds = [guild]
bot.tree.add_command(greet_cmd)

# /sendthis command
@app_commands.command(name="sendthis", description="Send your input as a message.")
@app_commands.describe(message="The message to send.")
async def sendthis(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)
if guild:
    sendthis.guilds = [guild]
bot.tree.add_command(sendthis)

@bot.command(name='setprefix')
async def setprefix(ctx, new_prefix: str):
    # Check if user has administrator permissions
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ You need administrator permissions to change the prefix!")
        return
    guild_id = ctx.guild.id if ctx.guild else None
    save_prefix(guild_id, new_prefix)
    await ctx.send(f'Prefix for this server changed to `{new_prefix}`!')

bot.run(TOKEN) 