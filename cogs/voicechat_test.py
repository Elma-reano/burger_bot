from cogs.voicechat import VoicechatBase

import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands


class VoicechatTest(commands.Cog, VoicechatBase):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test1", help="Test if bot is connected to a voice channel")
    async def test1(self, ctx: commands.Context):
        # Check if the bot is connected to a voice channel
        if ctx.voice_client is None:
            await ctx.send("Bot is not connected to a voice channel.")
        else:
            await ctx.send("Bot is connected to a voice channel.")

    @commands.command(name="test2", help="Test if author is connected to a voice channel")
    async def test2(self, ctx: commands.Context):
        # Check if the author is connected to a voice channel
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
        else:
            await ctx.send("You are connected to a voice channel.")

    @commands.command(name="test3", help="Test command that requires author to be in a voice channel")
    async def test3(self, ctx: commands.Context):
        await ctx.send("You must be in a voice channel to run this command.")

    @commands.command(name="testaudio", help="Test join and play test audio")
    # @VoicechatBase.voice_required
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
    @test3.before_invoke
    async def ensure_voice(self, ctx: commands.Context | discord.ApplicationContext):
        await self._ensure_voice(ctx)

def setup(bot):
    print("Setting up VoicechatTest cog...")
    bot.add_cog(VoicechatTest(bot))