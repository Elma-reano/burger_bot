import discord
from discord.ext import commands

from random import choice

from emojis import get_app_emoji, get_server_emoji

class Questions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ask", description="Ask burger bot a question")
    async def ask(self, ctx, question: str):
        guild_people = list(filter(lambda member: not member.bot, ctx.guild.members))
        random_person_from_server = choice(guild_people)
        responses = [
            "It's a mystery even to me.",
            "The real question is, where's McQueen?",
            "Ask me again later.",
            "Shhh. _They_ will hear you", #noqa
            "Don't know, don't care.",
            "Huh, yeah.",
            "Good question",
            "What kind of question is that?",
            "What are you implying?",
            get_app_emoji("eyebrow"),
            get_server_emoji(ctx),
            f"{random_person_from_server.mention} knows the answer",
            f"If it's bad, it's {random_person_from_server.mention}'s fault"
        ]
        await ctx.respond(f"> _{question}_?\n{choice(responses)}")


def setup(bot):
    print("Setting up Questions cog...")
    bot.add_cog(Questions(bot))