import discord
from discord.ext import commands
import requests
import os
import soundcloud
import random

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def play(self, ctx):

        channel = self.client.get_channel(773155351485874216)
        vc = await channel.connect()
        # create a client object with your app credentials
        client = soundcloud.Client(client_id='679195bf4a6d645ba1e74291c02d7a72')

        # fetch track to stream
        list = client.get('/resolve', url='https://soundcloud.com/perfectmsc/sets/lofi')

        playlist = client.get('/playlists/'+str(list.id))


        for track in playlist.tracks:

            song = client.get('/tracks/'+str(track['id'])+'/stream', allow_redirects=False)
            vc.play(discord.FFmpegPCMAudio(song.location))
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=str(track['title'])))




def setup(client):
    client.add_cog(Voice(client))
