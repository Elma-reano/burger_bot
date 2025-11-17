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
    
    def __get_radio_list(self, print_urls: bool = False) -> str:
        message = "## Available Radio Stations:\n"
        for station in catalogue:
            message += f"###{station['name']}:\n- {station['genre']}\n- {station['Description']}\n"
            if print_urls:
                message += f"- URL: {station['url']}\n"
        return message

    @commands.command(name="list_radios", help="List available radio stations")
    async def list_radios(self, ctx: commands.Context):
        await ctx.send(self.__get_radio_list(print_urls=True))

    @discord.slash_command(name="list_radios", description="List available radio stations")
    async def slash_list_radios(self, ctx):
        await ctx.respond(self.__get_radio_list())

    async def __play_radio(self, ctx: commands.Context | discord.ApplicationContext, url: str) -> tuple[bool, str, str | None]:
        """
        Plays a radio stream from the given URL.
        Returns a tuple (success: bool, message: str, error: str | None)
        """
        try:
            voice = ctx.voice_client

            source = discord.FFmpegPCMAudio(url)
            voice.play(
                source,
                after=lambda e: print('Player error: %s' % e) if e else None
            )
            return (True, "Playing radio stream...", None)
        except Exception as e:
            return (False, f"Error playing radio stream :(", str(e))

    @commands.command(name="radio", help="Join voice channel and play radio stream")
    async def radio(self, ctx: commands.Context, url: str):
        await ctx.send(f"Connecting to radio stream: {url}")
        # voice = ctx.voice_client

        # source = discord.FFmpegPCMAudio(url)
        # voice.play(
        #     source,
        #     after=lambda e: print('Player error: %s' % e) if e else None
        # )
        success, message, error = await self.__play_radio(ctx, url)
        if success:
            await ctx.send(message)
        else:
            await ctx.send(f"{message}")
            raise commands.CommandError(error)

    @discord.slash_command(name="radio", description="Join voice channel and play radio stream")
    @discord.option("station", type=str, description="Select a radio station", choices=catalogue_options, required=True)
    async def radio_slash(self, ctx: discord.ApplicationContext, station: str):
        station_url = self.__get_station_url(station)
        if station_url is None:
            await ctx.respond(f"Station '{station}' not found.")
            return
        # voice = ctx.voice_client
        # source = discord.FFmpegAudio(station_url)
        # voice.play(
        #     source,
        #     after=lambda e: print('Player error: %s' % e) if e else None
        # )
        # await ctx.respond(f"Playing radio station: {station}")
        success, message, error = await self.__play_radio(ctx, station_url)
        if success:
            await ctx.respond(message)
        else:
            await ctx.respond(f"{message}")
            raise commands.CommandError(error)

    @radio.before_invoke
    @radio_slash.before_invoke
    async def ensure_voice(self, ctx: discord.ApplicationContext | commands.Context):
        await self._ensure_voice(ctx)


def setup(bot):
    print("Setting up Radio cog...")
    bot.add_cog(Radio(bot))