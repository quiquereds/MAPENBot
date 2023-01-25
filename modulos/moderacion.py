import nextcord
import asyncio
import aiosqlite
import datetime
from bot import bot 
from nextcord import slash_command, Interaction
from nextcord.ext import commands

class Moderacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="warn", description="❌ Genera una advertencia para el usuario", guild_ids=[986683115701415936])
    async def warn(
        self,
        ctx:Interaction,
        
        member: nextcord.Member = nextcord.SlashOption(
            name="Miembro",
            description="Escoge un miembro"
        ),

        reason: str = nextcord.SlashOption(
            name="Razón",
            description="Motivo de warn",
            required=False
        )
    ):
        await addWarn(ctx, reason, member)
        embed = nextcord.Embed(
            description= f"<a:_:1041814509779693710> **Cuidado {member.mention} estás advertido!**\n\nPor infringir nuestras <#986736827136376882> has recibido una advertencia. Si juntas 3 serás acreedor@ a un ban\n\n**Razón:**\n{reason}"
        )
        embed.set_author(
            name= "Moderación de MAPEN Gang",
            icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
            url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )
        embed.set_thumbnail(
        url= member.display_avatar
        )
        embed.set_image(
            url= "https://cdn.discordapp.com/attachments/1012130067649921040/1067562376578224270/warnMAPENTech.gif"
        )
        embed.set_footer(
            text= "¿Existe alguna injusticia? Envíanos un ticket"
        )
        channel = bot.get_channel(1050230733588942868)
        await channel.send(file=nextcord.File("warnMAPENTech.png"))
        await channel.send(embed = embed)


def setup(bot):
    bot.add_cog(Moderacion(bot))
    print("He cargado los comandos de moderación")