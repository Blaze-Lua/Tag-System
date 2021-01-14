import discord
import random
import asyncio
import string

from discord.ext import commands 
_custom_tags = {}

def guild_check(_custom_tags):
    async def predicate(ctx):

        return _custom_tags.get(ctx.command.qualified_name) and ctx.guild.id in _custom_tags.get(ctx.command.qualified_name)

    return commands.check(predicate)

class Economy(commands.Cog):
    def _init_(self , client):
        self.client = client

    _custom_tags = {}
    @commands.group(hidden=True , invoke_without_command=True)
    @commands.guild_only()
    async def tag(self ,ctx , tag):
    
        
        await ctx.send(_custom_tags[tag])

    @tag.command()
    async def create(self ,ctx , name ,*,output):
        
        existing_command = _custom_tags.get(name)
       
        if existing_command is None and ctx.bot.get_command(name):
            return await ctx.send(f"A built in command with the name {name} is already registered")

       
        if existing_command:
            _custom_tags[name][ctx.guild.id] = output
        
        else:
            @commands.command(name=name, help=f"Custom command: Outputs your custom provided output")
            @guild_check(self._custom_tags)
            async def cmd(self, ctx):
                await ctx.send(_custom_tags[ctx.invoked_with][ctx.guild.id])

            cmd.cog = self
            # And add it to the cog and the bot
            
            # Now add it to our list of custom commands
            _custom_tags[name] = output
        await ctx.send(f"Added a tag called {name}")
     
    @tag.command()
    async def remove(self ,ctx , name):
     
        if name not in _custom_tags or ctx.guild.id not in _custom_tags[name]:
            return await ctx.send(f"There is no custom command called {name}")
       
        del _custom_tags[name][ctx.guild.id]
        await ctx.send(f"Removed a tag called {name}")

  

def setup(client):
    client.add_cog(Economy(client))