import discord
from discord.ext import commands
import os
import sqlite3




client = commands.Bot(commands.when_mentioned_or('pp '))
token = os.getenv("DISCORD_BOT_TOKEN")

client.load_extension('cogs.Tools')
client.load_extension('cogs.Voice')
client.load_extension('cogs.Fun')

@client.event
async def on_ready():

    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name='you'))
    print('Richard is er klaar voor!')


client.run(token)
