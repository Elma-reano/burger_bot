import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands

import asyncio

class Voicechat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test1(self, ctx: commands.Context):
        # Check if the bot is connected to a voice channel
        if ctx.voice_client is None:
            await ctx.send("Bot is not connected to a voice channel.")
        else:
            await ctx.send("Bot is connected to a voice channel.")

    @commands.command()
    async def test2(self, ctx: commands.Context):
        # Check if the author is connected to a voice channel
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
        else:
            await ctx.send("You are connected to a voice channel.")

    # async def __join(self, ctx: commands.Context | discord.ApplicationContext, channel: discord.VoiceChannel | None = None) -> tuple[int, str]:
    #     if channel is None:
    #         if ctx.author.voice:
    #             channel = ctx.author.voice.channel
    #         else:
    #             await ctx.send("You are not connected to a voice channel.")
    #             raise commands.CommandError("Author not connected to a voice channel.")

    #     if ctx.voice_client is not None:
    #         return await ctx.voice_client.move_to(channel)

    #     await channel.connect()

    @commands.command()
    async def join(self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
        """Joins a voice channel"""

        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")

        if channel is None:
            channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


    @commands.command()
    async def stop(self, ctx: commands.Context):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect(force=True)


    @commands.command(name="testaudio", help="Test join and play test audio")
    async def test_audio(self, ctx, path: str | None = None):

        if path is None:
            path = "tests/sample_audios/test_1.mp3"

        await ctx.send(f"Voice connected to: {ctx.voice_client.channel}")
        voice = ctx.voice_client

        if voice is None:
            await ctx.send("Not connected to a voice channel")

        source = PCMVolumeTransformer(
            FFmpegPCMAudio(path,
                           options="-vn -f s16le",
                        #    options='-vn -ar 48000 -ac 2 -f s16le'
                           )
        )

        voice.play(
            source,
            after=lambda e: print('Player error: %s' % e) if e else None
        )
        await ctx.send("Playing test audio...")

    @test_audio.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        await self.join(self, ctx)
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    print("Setting up Voicechat cog...")
    bot.add_cog(Voicechat(bot))