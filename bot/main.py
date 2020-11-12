import discord
from discord.ext import commands
import os

client = commands.Bot(commands.when_mentioned_or('pp '))
token = os.getenv("DISCORD_BOT_TOKEN")

for root, dirs, files in os.walk("cogs"):
    for name in files:
        if name.endswith('.py'):
            print(f'cogs.{name[:-3]}')
            client.load_extension(f'.{name[:-3]}')

@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name='test'))
    print('Richard is er klaar voor!')


client.run(token)
