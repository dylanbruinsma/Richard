import discord
from discord.ext import commands
import requests
import os


TOKEN = 'NzczMTg5MjE0ODExNTg2NTYy.X6FmkQ.kNvKIHnc17AM1M3T-Jwz0cHebSg'
bot = commands.Bot(command_prefix=commands.when_mentioned_or("pp "),
                   description='Een hele malse bot')


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="you"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Dit mag jij helaas niet doen :)')


@bot.command(name='show', help='Zoek zelf hulp gast!')
@commands.has_role('fryslan')
async def show(ctx, *args):
    response = 'Hallo'
    image_url = 'https://vignette.wikia.nocookie.net/lekkerspelen/images/c/c6/Richard.jpg/revision/latest/scale-to-width-down/220?cb=20181203192730&path-prefix=nl'
    img_data = requests.get(image_url).content
    with open('picture.jpg', 'wb') as handler:
        handler.write(img_data)
    await ctx.send(response)

    for x in range(int(args[0])):
        await ctx.send(file=discord.File('picture.jpg'))
    os.remove('picture.jpg')


@bot.command(name='clear', help='Zoek zelf hulp gast!')
@commands.has_role('fryslan')
async def clear(ctx, *args):
    if args[0] == "all":
        await ctx.channel.purge(limit=999999999999)
    await ctx.channel.purge(limit=int(args[0]) + 1)


bot.run(TOKEN)
