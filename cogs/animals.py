import discord
from discord.ext import commands

import aiohttp

import io

DOG_URL = "https://random.dog/woof.json"
CAT_URL = "https://cataas.com/cat"
DUCK_URL = "https://random-d.uk/api/v2/random"

class Animals(commands.Cog):
    """Animal-related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cat', help='Sends a random cat image.')
    async def cat(self, ctx):
        cat_url = CAT_URL
        async with aiohttp.ClientSession() as session:
            async with session.get(cat_url) as response:
                data = await response.read()
                await ctx.send(file=discord.File(fp=io.BytesIO(data), filename='cat.jpg'))

    @commands.command(name='dog', help='Sends a random dog image.')
    async def dog(self, ctx):
        dog_url = DOG_URL
        async with aiohttp.ClientSession() as session:
            async with session.get(dog_url) as response:
                data = await response.json()
                await ctx.send(data['url'])

    @commands.command(name='duck', help='Sends a random duck image.')
    async def duck(self, ctx):
        duck_url = DUCK_URL
        async with aiohttp.ClientSession() as session:
            async with session.get(duck_url) as response:
                data = await response.json()
                await ctx.send(data['url'])

    @discord.slash_command(name='choose_animal', help='Choose an animal to get an image from (cat, dog, duck).')
    @discord.option("animal", str, description= "Choose an animal", choices=["cat", "dog", "duck"])
    async def choose_animal(self, ctx, animal: str):
        if animal == "cat":
            await self.cat(ctx)
        elif animal == "dog":
            await self.dog(ctx)
        elif animal == "duck":
            await self.duck(ctx)
        else:
            await ctx.send("Unknown animal!")

def setup(bot):
    print("Setting up Animals cog...")
    bot.add_cog(Animals(bot))