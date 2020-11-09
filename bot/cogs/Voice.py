import discord
from discord.ext import commands
import requests
import os


class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role('fryslan')
    async def join(self, ctx):
        channel = self.client.get_channel(774957379061547038)
        vc = await channel.connect()
        print(vc.is_playing())
        vc.play(discord.FFmpegPCMAudio('https://21253.live.streamtheworld.com/RADIO538.mp3'))


def setup(client):
    client.add_cog(Voice(client))
