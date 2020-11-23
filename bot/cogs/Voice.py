import asyncio
import sqlite3

import discord
import youtube_dl
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('playlist.db')
        self.cur = self.conn.cursor()

    @commands.command()
    async def stream(self, ctx, *args):
        await ctx.channel.purge(limit=1)
        channel = self.bot.get_channel(735213841235050536)
        # urls = self.cur.execute('''SELECT * FROM main.playlist''').fetchall()
        url = ''
        for x in args:
            url = url + x
        vc = await channel.connect()

        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        vc.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=player.title))


class Playlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('playlist.db')
        self.cur = self.conn.cursor()

    @commands.command()
    async def speel(self, ctx, url):
        author = ctx.author.name
        self.cur.execute('''CREATE TABLE IF NOT EXISTS playlist (url TEXT, aanvrager TEXT)''')
        self.cur.execute('''INSERT INTO playlist VALUES (?,?)''', (url, author))
        self.conn.commit()


def setup(client):
    client.add_cog(Music(client))
    client.add_cog(Playlist(client))
