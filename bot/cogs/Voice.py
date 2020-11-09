import discord
from discord.ext import commands
import requests
import os
import soundcloud
import random

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    



def setup(client):
    client.add_cog(Voice(client))
