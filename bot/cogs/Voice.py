import discord
from discord.ext import commands
import requests
import os
import soundcloud
import random

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready')
        channel = self.client.get_channel(773155351485874216)
        vc = await channel.connect()
        print(vc.is_playing())
        # create a client object with your app credentials
        client = soundcloud.Client(client_id='679195bf4a6d645ba1e74291c02d7a72')

        # fetch track to stream
        list = client.get('/resolve', url='https://soundcloud.com/bitbirdradio/sets/san-holo-bitbird-radio')
        playlist = client.get('/playlists/'+str(list.id))
        print(playlist)
        tracklist = []
        for track in playlist.tracks:
            tracklist.append(str(track['id']))
        curr_song = random.choice(tracklist)

        song = client.get('/tracks/'+curr_song+'/stream', allow_redirects=False)
        tracklist.pop(tracklist.index(curr_song))
        vc.play(discord.FFmpegPCMAudio(song.location))




def setup(client):
    client.add_cog(Voice(client))
