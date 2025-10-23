import discord
from discord.ext import commands

class Voicechat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def __join(self, ctx: discord.ApplicationContext) -> tuple[bool, str]:
        """Make the bot join the voice channel of the user.

        Args:
            ctx (discord.ApplicationContext): The context of the command.

        Returns:
            tuple[bool, str]: A tuple containing a boolean indicating success, and a message.
            If the boolean is True, the bot successfully joined the voice channel.
            If the boolean is None, the user is not in a voice channel.
            If the boolean is False, an error not concerning the user occurred.

            The message contains information about the result.
        """
        try:
            if ctx.author.voice is None:
                return None, "You are not connected to a voice channel."
            voice_channel = ctx.author.voice.channel
            
            if ctx.guild.voice_client is not None:
                ctx.guild.voice_client.move_to(voice_channel)
            else:
                await voice_channel.connect()

            return True, f"Joined {voice_channel.name}!"
        except Exception as e:
            print("Error:", e)
            return False, "An error occurred :("
    
    async def __disconnect(self, ctx: discord.ApplicationContext) -> tuple[bool, str]:
        """Make the bot leave the voice channel.

        Args:
            ctx (discord.ApplicationContext): The context of the command.

        Returns:
            tuple[bool, str]: A tuple containing a boolean indicating success, and a message.
            If the boolean is True, the bot successfully disconnected from the voice channel.
            If the boolean is None, the bot was not connected to any voice channel.
            If the boolean is False, an error not concerning the user occurred.
            The message contains information about the result.
        """
        try:
            if ctx.guild.voice_client is None:
                return None, "I am not connected to any voice channel tho."
            
            await ctx.guild.voice_client.disconnect()
            return True, "Disconnected from the voice channel!"
        except Exception as e:
            print("Error:", e)
            return False, "An error occurred :("


    @discord.slash_command(name="join", description="Make the bot join your voice channel")
    async def join(self, ctx: discord.ApplicationContext):
        # if ctx.author.voice is None:
        #     await ctx.respond("You are not connected to a voice channel.", ephemeral=True)
        #     return

        # voice_channel = ctx.author.voice.channel

        # if ctx.guild.voice_client is not None:
        #     await ctx.guild.voice_client.move_to(voice_channel)
        # else:
        #     await voice_channel.connect()

        # await ctx.respond(f"Joined {voice_channel.name}!")

        success, message = await self.__join(ctx)
        if success:
            await ctx.respond(message)
        else:
            await ctx.respond(message, ephemeral=True)

    @commands.command(name="join", help="Make the bot join your voice channel")
    async def join_command(self, ctx: discord.ApplicationContext):
        # await self.join(ctx)
        _, message = await self.__join(ctx)
        await ctx.send(message)
    
    @discord.slash_command(name="disconnect", description="Make the bot leave the voice channel")
    async def disconnect(self, ctx: discord.ApplicationContext):
        # if ctx.guild.voice_client is None:
        #     await ctx.respond("I am not connected to any voice channel tho.", ephemeral=True)
        #     return
        
        # await ctx.guild.voice_client.disconnect()
        # await ctx.respond("Disconnected from the voice channel!")
        success, message = await self.__disconnect(ctx)
        if success:
            await ctx.respond(message)
        else:
            await ctx.respond(message, ephemeral=True)


    @commands.command(name="disconnect", help="Make the bot leave the voice channel")
    async def disconnect_command(self, ctx: discord.ApplicationContext):
        _, message = await self.__disconnect(ctx)
        await ctx.send(message)

def setup(bot):
    print("Setting up Voicechat cog...")
    bot.add_cog(Voicechat(bot))