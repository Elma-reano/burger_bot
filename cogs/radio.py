from cogs.voicechat import VoicechatBase

import discord
from discord.ext import commands

import json

RADIO_CATALOGUE_PATH = "config/radio_catalogue.json"


with open(RADIO_CATALOGUE_PATH, 'r') as f:
    catalogue = json.load(f)


class Radio(commands.Cog, VoicechatBase):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list_radios", help="List available radio stations")
    async def list_radios(self, ctx: commands.Context):
        message = "## Available Radio Stations:\n"
        for station in catalogue:
            message += f"- {station['name']}: {station['genre']} - {station['Description']}\n"
        await ctx.send(message)

    @commands.command(name="radio", help="Join voice channel and play radio stream")
    @VoicechatBase.voice_required
    async def radio(self, ctx: commands.Context, url: str):
        await ctx.send(f"Connecting to radio stream: {url}")
        voice = ctx.voice_client

        if voice is None:
            await ctx.send("Not connected to a voice channel")
            return

        source = discord.FFmpegPCMAudio(url)
        voice.play(
            source,
            after=lambda e: print('Player error: %s' % e) if e else None
        )
        await ctx.send("Playing radio stream...")

    @discord.slash_command(name="radio", description="Join voice channel and play radio stream")
    @VoicechatBase.slash_voice_required
    async def radio_slash(self, 
                          ctx,
                          *,
                          station: discord.Option(str, choices=[s['name'] for s in catalogue])
                          ):
        ctx.respond("WIP :)")
        raise NotImplementedError("Slash command for radio not implemented yet.")


def setup(bot):
    print("Setting up Radio cog...")
    bot.add_cog(Radio(bot))