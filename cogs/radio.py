from cogs.voicechat import VoicechatBase

import discord
from discord.ext import commands

import json

RADIO_CATALOGUE_PATH = "config/radio_catalogue.json"

with open(RADIO_CATALOGUE_PATH, 'r') as f:
    catalogue = json.load(f)

catalogue_options = [station['name'] for station in catalogue]

class Radio(commands.Cog, VoicechatBase):

    def __init__(self, bot):
        self.bot = bot

    def __get_station_url(self, station_name: str) -> str | None:
        for station in catalogue:
            if station['name'] == station_name:
                return station['url']
        return None
    
    def __get_radio_list(self) -> str:
        message = "## Available Radio Stations:\n"
        for station in catalogue:
            message += f"- {station['name']}: {station['genre']} - {station['Description']}\n"
        return message

    @commands.command(name="list_radios", help="List available radio stations")
    async def list_radios(self, ctx: commands.Context):
        await ctx.send(self.__get_radio_list())

    @discord.slash_command(name="list_radios", description="List available radio stations")
    async def slash_list_radios(self, ctx):
        await ctx.respond(self.__get_radio_list())

    @commands.command(name="radio", help="Join voice channel and play radio stream")
    # @VoicechatBase.voice_required
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
    @discord.option("station", type=str, description="Select a radio station", choices=catalogue_options)
    async def radio_slash(self, 
                          ctx,
                          *,
                        #   station: discord.Option(str, choices=catalogue_names, description="Select a radio station")
                            station: str
                          ):
        ctx.respond("WIP :)")
        raise NotImplementedError("Slash command for radio not implemented yet.")

    @radio.before_invoke
    @radio_slash.before_invoke
    async def ensure_voice(self, ctx: discord.ApplicationContext | commands.Context):
        await self._ensure_voice(ctx)


def setup(bot):
    print("Setting up Radio cog...")
    bot.add_cog(Radio(bot))