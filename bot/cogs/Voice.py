import discord
from discord.ext import commands
import requests
import os
import soundcloud
import random
import asyncio


class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def play(self, ctx):
        await ctx.channel.purge(limit=1)
        channel = self.client.get_channel(774957379061547038)
        vc = await channel.connect()
        # create a client object with your app credentials
        vclient = soundcloud.Client(client_id='679195bf4a6d645ba1e74291c02d7a72')
        ctx.channel.send('Hallo')
        sets = ['https://soundcloud.com/jennifer-naremskaya/sets/gg-magree-1',
                'https://soundcloud.com/perfectmsc/sets/lofi',
                'https://soundcloud.com/sanholobeats/sets/album1',
                'https://soundcloud.com/mugatunesofficial/sets/audible-adderall-14'
                ]
        tracklist = []
        for setx in sets:
            ctx.channel.send(setx)
            list = vclient.get('/resolve', url=setx)
            playlist = vclient.get('/playlists/' + str(list.id))

            for track in playlist.tracks:
                tracklist.append((track['id'], track['title']))
        random.shuffle(tracklist)
        ctx.channel.send(f'added: {len(tracklist)} songs to the list')
        for x in tracklist:
            if not vc.is_playing():
                print(x[1])
                song = vclient.get('/tracks/' + str(x[0]) + '/stream', allow_redirects=False).location
                vc.play(discord.FFmpegPCMAudio(song))
                ctx.channel.send(f'ik speel nu: {song}')
                await self.client.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.listening, name=(str(x[1]))))
            while vc.is_playing():
                await asyncio.sleep(0.1)


def setup(client):
    client.add_cog(Voice(client))
