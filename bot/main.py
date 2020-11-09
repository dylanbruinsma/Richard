import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='pp ')
token = os.getenv("DISCORD_BOT_TOKEN")
# token = 'NzczMTg5MjE0ODExNTg2NTYy.X6FmkQ.zLMqc-de9QTKoYWsAAYAhlaFFeQ'

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
