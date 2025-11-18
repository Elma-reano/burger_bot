from cogs.voicechat import VoicechatBase

import discord
from discord.ext import commands

import json

RADIO_CATALOGUE_PATH = "config/radio_catalogue.json"

with open(RADIO_CATALOGUE_PATH, 'r') as f:
    catalogue = json.load(f)

catalogue_options = [station['name'] for station in catalogue]

# TODO Multiple urls per station (for fallback)

class Radio(commands.Cog, VoicechatBase):

    def __init__(self, bot):
        self.bot = bot

    def __get_station_info(self, station_name: str | None = None, station_id: str | None = None) -> dict | None:
        assert station_name is not None or station_id is not None, "Either station_name or station_id must be provided."
        if station_id is not None:
            for station in catalogue:
                if station['id'] == station_id:
                    return station
            return None
        elif station_name is not None:
            for station in catalogue:
                if station['name'] == station_name:
                    return station
        return None
    
    def __get_radio_list(self) -> str:
        message = "## Available Radio Stations:\n"
        for station in catalogue:
            message += f"### {station['name']}:\n- ID: {station['id']}\n- {station['genre']}\n- {station['Description']}\n"
        message += "> The list of radios of the slash command may take some time to update after adding new stations.\n"
        return message
    
    @commands.command(name="reset_radio_catalogue", help="Reload the radio catalogue from file", admin_only=True, hidden=True)
    async def reset_radio_catalogue(self, ctx: commands.Context):
        global catalogue
        with open(RADIO_CATALOGUE_PATH, 'r') as f:
            catalogue = json.load(f)
        await ctx.send("Radio catalogue reloaded.")

    @commands.command(name="list_radios", help="List available radio stations")
    async def list_radios(self, ctx: commands.Context):
        await ctx.send(self.__get_radio_list())

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

    @commands.command(name="radio", help="Join voice channel and play radio stream. The station id must be provided.")
    async def radio(self, ctx: commands.Context, station_id: str):
        station = self.__get_station_info(station_id=station_id)
        if station is None:
            await ctx.send(f"Station '{station_id}' not found.")
            return
        station_url = station['url']
        station_name = station['name']
        await ctx.send(f"Connecting to radio stream: {station_name}")
        success, message, error = await self.__play_radio(ctx, station_url)
        if success:
            await ctx.send(message)
        else:
            await ctx.send(f"{message}")
            raise commands.CommandError(error)

    @discord.slash_command(name="radio", description="Join voice channel and play radio stream")
    @discord.option("station", type=str, description="Select a radio station", choices=catalogue_options, required=True)
    async def radio_slash(self, ctx: discord.ApplicationContext, station_name: str):
        station = self.__get_station_info(station_name=station_name)
        station_url = station['url'] if station is not None else None
        if station_url is None:
            await ctx.respond(f"Station '{station_name}' not found.")
            return
        success, message, error = await self.__play_radio(ctx, station_url)
        if success:
            await ctx.respond(message)
        else:
            await ctx.respond(f"{message}")
            raise commands.CommandError(error)
        
    @commands.command(name="custom_radio", help="Join voice channel and play custom radio stream from URL")
    async def custom_radio(self, ctx: commands.Context, url: str):
        await ctx.send(f"Connecting to custom radio stream: {url}")
        success, message, error = await self.__play_radio(ctx, url)
        if success:
            await ctx.send(message)
        else:
            await ctx.send(f"{message}")
            raise commands.CommandError(error)

    @radio.before_invoke
    @radio_slash.before_invoke
    @custom_radio.before_invoke
    async def ensure_voice(self, ctx: discord.ApplicationContext | commands.Context):
        await self._ensure_voice(ctx)


def setup(bot):
    print("Setting up Radio cog...")
    bot.add_cog(Radio(bot))