import discord
import random
from discord.ext import commands

class Math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    math = discord.SlashCommandGroup("math", "Spooky math stuff") # create a Slash Command Group called "math"
    advanced_math = math.create_subgroup(
        "advanced",
        "super hard math commands!"
    )

    @math.command()
    async def add(self, ctx, a: int, b: int):
        c = a + b
        await ctx.respond(f"{a} + {b} is {c}.")

    @math.command()
    async def random_number(self, ctx):
        num = random.randint(1, 100)
        await ctx.respond(f"Your random number is {num}.")
  
    @advanced_math.command()
    async def midpoint(self, ctx, x1: float, y1: float, x2: float, y2: float):
        mid_x = (x1 + x2)/2
        mid_y = (y1 + y2)/2
        await ctx.respond(f"The midpoint between those coordinates is ({mid_x}, {mid_y}).")

    @advanced_math.command()
    async def euler_derivative(self, ctx):
        await ctx.respond("The derivative of e^x is e^x. (You're welcome!)")

    
def setup(bot):
    print("Setting up Math cog...")
    bot.add_cog(Math(bot))