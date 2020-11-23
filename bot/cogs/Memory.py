import sqlite3
from discord.ext import commands


class Memory(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect('example.db')
        self.c = self.conn.cursor()


    @commands.command()
    async def playlist(self, ctx, url):
        requester = ctx.message.author.name
        self.c.execute('''CREATE TABLE IF NOT EXISTS playlist
                             (url text, requester text)''')
        self.c.execute("INSERT INTO playlist VALUES (?,?)", (url, requester))
        self.conn.commit()


def setup(client):
    client.add_cog(Memory(client))
