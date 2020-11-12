import discord
from discord.ext import commands
import requests
import os
import soundcloud
import random
import time
import asyncio


class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def play(self, ctx):
        await ctx.channel.purge(limit=1)
        channel = self.client.get_channel(773155351485874216)
        vc = await channel.connect()
        # create a client object with your app credentials
        client = soundcloud.Client(client_id='679195bf4a6d645ba1e74291c02d7a72')
                
        tracklist = []
        list = client.get('/resolve', url='https://soundcloud.com/perfectmsc/sets/lofi')
        ctx.channel.send('working')
        playlist = client.get('/playlists/' + str(list.id))

        for track in playlist.tracks:
            tracklist.append((track['id'], track['title']))
        random.shuffle(tracklist)
        print('added: %s songs to the list' % (len(tracklist)))
        for x in tracklist:
            ctx.channel.send('working2')
            if not vc.is_playing():
                print(x[1])
                song = client.get('/tracks/' + str(x[0]) + '/stream', allow_redirects=False).location
                vc.play(discord.FFmpegPCMAudio(song))
                await self.client.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.listening, name=(str(x[1]))))
            while vc.is_playing():
                await asyncio.sleep(0.1)


def setup(client):
    client.add_cog(Voice(client))
