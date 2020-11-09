import discord
from discord.ext import commands
import requests
import os


class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready')

    @commands.command()
    @commands.has_role('fryslan')
    async def show(self, ctx, *args):
        response = 'Hallo'
        image_url = 'https://vignette.wikia.nocookie.net/lekkerspelen/images/c/c6/Richard.jpg/revision/latest/scale-to-width-down/220?cb=20181203192730&path-prefix=nl'
        img_data = requests.get(image_url).content
        with open('picture.jpg', 'wb') as handler:
            handler.write(img_data)
        await ctx.send(response)

        for x in range(int(args[0])):
            await ctx.send(file=discord.File('picture.jpg'))
        os.remove('picture.jpg')

    @commands.command()
    @commands.has_role('fryslan')
    async def clear(self, ctx, *args):
        if args[0] == "all":
            await ctx.channel.purge(limit=999999999999)
        await ctx.channel.purge(limit=int(args[0]) + 1)


def setup(client):
    client.add_cog(Example(client))
