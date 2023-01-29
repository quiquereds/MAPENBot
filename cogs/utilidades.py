from bot import bot
import nextcord
from nextcord.ext import commands

# Creamos la clase utilidades que incluirá todas los comandos de este tipo
class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Creamos un comando de slash para hacer ping al bot
    @bot.slash_command(name= "ping", description="🏓 Verifica el estado del bot")
    # El bot recibe el parámetro send y la interacción
    async def ping(self, interaction: nextcord.Interaction):
        # Creamos un embed que almacenará el resultado
        embed = nextcord.Embed(
            title="Haciendo ping a MAPEN Tech",
            # Calculamos el ping al multiplicar por 1000 la latencia del bot obteniendo los milisegundos (el resultado se redondea)
            description= f"<a:_:1041439685832081548>**Haciendo ping a MAPENTech con 33 bytes de datos...**\n\nPaquetes recibidos satisfactoriamente, mi ping es `{round(bot.latency)*1000} ms`\n\nPaquetes: enviados = 4, recibidos = 4, perdidos = 0\n*Pero si no hablas taka taka... 🏓 pong!*"
        )
        embed.set_author(
            name= "MAPEN Bot",
            icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
            url= "https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )
        embed.set_thumbnail(
            url=("https://cdn.discordapp.com/attachments/1012130067649921040/1068645922709438535/ezgif.com-gif-maker.gif")
        )
        embed.set_footer(
            text = f"Pedido por {interaction.user}",
            icon_url= interaction.user.display_avatar
        )
        # Mandamos el resultado en el canal donde se ejecutó el comando
        await interaction.send(embed = embed)

# Declaramos el método setup que va a cargar el cog (clase Utilidades)
def setup(bot):
    bot.add_cog(Utilidades(bot))
    # Se muestra en terminal que los comandos han sido cargados
    print("He añadido los comandos de utilidades")
