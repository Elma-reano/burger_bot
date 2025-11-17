import discord
import os
from discord.ext.commands import Bot

import logging
logging.basicConfig(level=logging.INFO)

import dotenv
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))


EXTENSIONS = [
    'cogs.greetings',
    'cogs.math',
    'cogs.questions',
    'cogs.animals',
    'cogs.voicechat',
    'cogs.voicechat_test',
    'cogs.radio',
]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = Bot(command_prefix="!",
          intents= intents
          )

@bot.event
async def on_ready():
    print(f'{bot.user} is now connected!')

@bot.slash_command(name="ping", description="Ping the bot")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond("Pong!")
    print(f"Pinged {ctx.author.nick}")

@bot.slash_command(name="gamble", description="Let's go gambling!")
async def gamble(ctx: discord.ApplicationContext, amount: int):
    await ctx.respond(f"You lost {amount} coins :(")

@bot.event
async def update_commands():
    await bot.sync_commands(force = True)

for extension in EXTENSIONS:
    bot.load_extension(extension)
bot.run(token)
