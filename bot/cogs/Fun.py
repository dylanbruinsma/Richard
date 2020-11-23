import io
import os

import discord
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from discord.ext import commands


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx, *args):
        image = requests.get(ctx.message.attachments[0].url)
        if str(ctx.message.attachments[0].url[-5:]) == '.jpeg':
            ext = str(ctx.message.attachments[0].url[-5:])
        else:
            ext = str(ctx.message.attachments[0].url[-4:])
        await ctx.channel.purge(limit=1)
        image_bytes = io.BytesIO(image.content)
        img = Image.open(image_bytes)

        text = []

        for x in args:
            text.append(x)

        topText, bottomText = listToString(text).split(',')
        imageSize = img.size

        fontSize = int(imageSize[1] / 6)
        font = ImageFont.truetype("Aura Regular.ttf", fontSize)
        topTextSize = font.getsize(topText)
        bottomTextSize = font.getsize(bottomText)
        while topTextSize[0] > imageSize[0] - 20 or bottomTextSize[0] > imageSize[0] - 20:
            fontSize = fontSize - 1
            font = ImageFont.truetype("Aura Regular.ttf", fontSize)
            topTextSize = font.getsize(topText)
            bottomTextSize = font.getsize(bottomText)

        # find top centered position for top text
        topTextPositionX = (imageSize[0] / 2) - (topTextSize[0] / 2)
        topTextPositionY = 0
        topTextPosition = (topTextPositionX, topTextPositionY)

        # find bottom centered position for bottom text
        bottomTextPositionX = (imageSize[0] / 2) - (bottomTextSize[0] / 2)
        bottomTextPositionY = imageSize[1] - bottomTextSize[1]
        bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

        draw = ImageDraw.Draw(img)

        # draw outlines
        # there may be a better way
        outlineRange = int(fontSize / 15)
        for x in range(-outlineRange, outlineRange + 1):
            for y in range(-outlineRange, outlineRange + 1):
                draw.text((topTextPosition[0] + x, topTextPosition[1] + y), topText, (0, 0, 0), font=font)
                draw.text((bottomTextPosition[0] + x, bottomTextPosition[1] + y), bottomText, (0, 0, 0), font=font)

        draw.text(topTextPosition, topText, (255, 255, 255), font=font)
        draw.text(bottomTextPosition, bottomText, (255, 255, 255), font=font)

        img.save('sample-out' + ext)
        await ctx.send(file=discord.File('sample-out' + ext))
        os.remove('sample-out' + ext)


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 = (str1 + " " + ele)

        # return string
    return str1


def setup(client):
    client.add_cog(Memes(client))
