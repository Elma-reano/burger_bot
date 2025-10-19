import discord
from discord.ext import commands

from random import choice

class Questions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="why", description="Ask the bot why something is the case")
    async def why(self, ctx, subject: str):
        guild_people = list(filter(lambda member: not member.bot, ctx.guild.members))
        random_person_from_server = choice(guild_people)
        responses = [
            "That's just how the universe works.",
            "It's a mystery even to me.",
            "The real question is, why not?",
            "Sometimes things just are.",
            "Ask me again later.",
            "Shhh. _They_ will hear you", #noqa
            "Sorry that's my fault",
            "Perhaps it's fate.",
            f"{random_person_from_server.mention} knows the answer",
            f"{random_person_from_server.mention}'s fault"
        ]
        await ctx.respond(f"> _{subject}_?\n{choice(responses)}")

def setup(bot):
    print("Setting up Questions cog...")
    bot.add_cog(Questions(bot))