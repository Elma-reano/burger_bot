import discord
from discord.ext import commands

import asyncio

class VoicechatBase:

    def __init__(self, bot):
        self.bot = bot

    # async def __join(self, ctx: commands.Context | discord.ApplicationContext, channel: discord.VoiceChannel | None = None) -> tuple[int, str]:

    async def join(self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
        """Joins a voice channel"""
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")

        if channel is None:
            channel = ctx.author.voice.channel

        if not ctx.voice_client:
            await channel.connect()
        elif channel != ctx.voice_client.channel:
            await ctx.voice_client.move_to(channel)

    @staticmethod
    def voice_required(func):
        async def wrapper(self, ctx: commands.Context, *args, **kwargs):
            await self.join(ctx)
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            return await func(self, ctx, *args, **kwargs)
        return wrapper
    
class VoicechatControls(VoicechatBase, commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join", help="Make the bot join your voice channel")
    async def join_command(self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
        await self.join(ctx, channel=channel)
        await ctx.send(f"Joined {ctx.voice_client.channel}")

    @commands.command(name="stop", help="Make the bot leave the voice channel")
    async def stop(self, ctx: commands.Context):
        await self.disconnect(ctx)
        await ctx.send("Disconnected from voice channel")

    @commands.command(name="disconnect", help="Make the bot leave the voice channel")
    async def disconnect_command(self, ctx: commands.Context):
        await self.stop(ctx)


def setup(bot):
    print("Setting up VoicechatControls cog...")
    bot.add_cog(VoicechatControls(bot))