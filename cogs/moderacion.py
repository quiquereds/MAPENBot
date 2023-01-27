import nextcord
import aiosqlite
import asyncio
from bot import bot
import datetime
from nextcord.ext import commands

# Se crea un método para añadir advertencias a un usuario en específico
async def addWarn(ctx, reason, member):
    # Utilizamos un objeto cursor para ejecutar comandos de SQL
    async with bot.db.cursor() as cursor:
        # Insertamos dentro de la tabla warns información sobre el usuario y el warn recibido
        await cursor.execute("INSERT INTO warns (member, reason, time, guild) VALUES (?, ?, ?, ?)", (member.id, reason, int(datetime.datetime.now().timestamp()), ctx.guild.id))
    # Guardamos cambios en la tabla
    await bot.db.commit()

# Creamos la clase moderación que incluirá todos los comandos de este tipo
class Moderacion(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # Comando para ejecutar el bot y cambiar su presencia
    @commands.Cog.listener()
    async def on_ready(self):
        await bot.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.watching, name = "MAPEN Tech en YT"))
        # Avisa en terminal cuando el bot se ha conectado a Discord
        print(f'He iniciado sesión como {bot.user}')
        # Iniciamos conexión a la base de datos utilizando SQLite
        bot.db = await aiosqlite.connect("warns.db")
        # Damos un tiempo de espera para que se inicialice la BDD
        await asyncio.sleep(3)
        # Se crea la tabla warns en la base de datos si no existe
        async with bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS warns(member INTEGER, reason TEXT, time INTEGER, guild INTEGER)")
        await bot.db.commit()

    # Evento para detectar cuando los nuevos miembros se unen al servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Creamos una variable para almacenar el guild del servidor
        guild = member.guild
        # Creamos una variable para almacenar el embed
        embed = nextcord.Embed(
            # Dentro del embed, se coloca un mensaje para dar la bienvenida
            description= f"**Bienvenid@ a MAPEN Gang {member.mention}!** <a:_:1062238851185266798>\n\nContigo ya somos {guild.member_count} <a:_:1062238871527620728><a:_:1062238871527620728>\n\nEstamos agradecidos de todo corazón que te hayas unido al server, esperamos que tengas una muy buena experiencia, puedes hacer aquí lo siguiente:\n\n<a:_:1062238851185266798> Compartir tu pasión tech con todos\n<a:_:1019057180697174016> Encontrar gangas tech en productos tecnológicos\n<a:_:1019795438863384727> Pasar un momento cool con todos eschando música o jugando\n<a:_:1041814614448537704> Subir de nivel mientras participas desbloqueando canales nuevos\n<:_:1015097359916605461> Conseguir puntos del canal para comprar roles\n<a:_:1015882420370804856> Contar con apoyo siempre para dudas, recomendaciones y consejos\n\n**Lo primero que tienes que hacer...**\n\n<:_:1062236697858953246> Visita <#1014691143545536542> para personalizar el server a tu manera\n<:_:1062236697858953246> Consulta <#1015063262708121610> para conocer más sobre el server\n<:_:1062236697858953246> Dile hola a todos en <#986683116171182105>"
        )

        #Se define el autor del embed
        embed.set_author(
            name= "MAPEN Tech",
            icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
            url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )

        # Se coloca una imágen en el embed que será igual a la foto de perfil del miembro
        embed.set_thumbnail(
            url = member.display_avatar
        )

        # Se añade una imágen personalizada en la parte inferior del embed
        embed.set_image(
            url = "https://cdn.discordapp.com/attachments/1012130067649921040/1067232233565462539/bienvenidaMAPENTech.gif"
        )

        # Se crea una variable para almacenar el ID del canal (guild) de bienvenida
        channel = bot.get_channel(986683116171182101)
        # El bot envía una imágen personalizada del servidor antes del embed
        await channel.send(file=nextcord.File("holaMAPENTech.png"))
        # El bot envía el embed creado al canal definido
        await channel.send(embed = embed)

    # Evento para detectar cuando los usuarios abandonan el servidor
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Creamos una variable para almacenar el guild del servidor (ID)
        guild = member.guild
        # Creamos una variable para almacenar el embed
        embed = nextcord.Embed(
            # Dentro del embed, se coloca un mensaje para despedir mencionando al miembro
            description= f"<a:_:1065019205679841390>**Gracias por haber estado aquí {member.mention}!**\n\nEsperamos que te hayas divertido por aquí , aprovechado de alguna oferta y aliviado tus dudas 😌\n\n***Ójala volvamos a verte pronto***"
        )

        # Se define el autor del embed
        embed.set_author(
            name= "MAPEN Gang",
            icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
            url= "https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )

        # Se coloca una imágen en el embed que será igual a la imágen de perfil del usuario
        embed.set_thumbnail(
            url= member.display_avatar
        )

        # Se crea una variable para almacenar el ID del canal de despedidas
        channel = bot.get_channel(1012084418615201822)
        # El bot envía una imágen personalizada del servidor antes del embed
        await channel.send(file=nextcord.File("adiosMAPENTech.png"))
        # El bot envía el embed creado al canal definido
        await channel.send(embed = embed)

    # Evento para detectar cuando un usuario es baneado
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        # Creamos una variable para almacenar el guild del servidor (ID)
        guild = member.guild
        # Creamos una variable para almacenar el embed
        embed = nextcord.Embed(
            # Dentro del embed, se coloca un mensaje de ban mencionando al usuario
            description= f"<a:_:1041814509779693710> **Pa tu casa {member.mention}!**\n\nPor infringir nuestras <#986736827136376882> te hemos baneado del servidor con el objetivo de mantener un ambiente sano\n\n*Puedes apelar la sanción haciendo [click aquí](https://forms.gle/tGujMHC9SrK3SDHU6)*"
        )

        # Se define el autor del embed
        embed.set_author(
            name= "Moderación de MAPEN Gang",
            icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
            url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )

        # Se coloca una imágen en el embed que será igual a la foto de perfil del usuario
        embed.set_thumbnail(
            url= member.display_avatar
        )

        # Se añade una imágen personalizada en el embed
        embed.set_image(
            url= "https://cdn.discordapp.com/attachments/1012130067649921040/1067540640180748298/banMAPENTech.gif"
        )

        # Se coloca un pie de página en el embed
        embed.set_footer(
            icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1067548574008754217/web.png",
            text= "Imagen creada con https://ejector.kassellabs.io/"
        )

        # Se coloca un pie de página al embed con la información del sitio en donde se generó la imágen
        channel = bot.get_channel(1050231800443715666)
        # El bot envía una imágen personalizada antes del embed
        await channel.send(file=nextcord.File("banMAPENTech.png"))
        # Se envía el embed
        await channel.send(embed = embed)

    # Comando para hacer warn a un usuario
    @commands.has_role(1041426879044915250)
    @commands.command(description= "Alerta a un usuario")
    # Definimos el comando que va a recibir el contexto, la mención del miembro y la razón del warn
    async def warn(self, ctx: commands.Context, member: nextcord.Member, *, reason: str = "Sin motivo"):
        # Se ejecuta el método para añadir un warn en la tabla de la BDD
        await addWarn(ctx, reason, member)
        # Se crea una variable para almacenar un embed
        embed = nextcord.Embed(
            description= f"<a:_:1062238854586834944> **Cuidado {member.mention} estás advertido!**\n\nPor infringir nuestras <#986736827136376882> has recibido una advertencia. Si juntas 3 serás acreedor@ a un ban\n\n**Razón:**\n{reason}"
        )

        embed.set_author(
            name="Moderación de MAPEN Gang",
            icon_url="https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
            url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )

        embed.set_thumbnail(
            url = member.display_avatar
        )

        embed.set_image(
            url = "https://cdn.discordapp.com/attachments/1012130067649921040/1067562376578224270/warnMAPENTech.gif"
        )

        embed.set_footer(
            text= "¿Existe alguna injusticia? Envíanos un ticket"
        )

        channel = bot.get_channel(1050230733588942868)
        #await channel.send(file=nextcord.File("./media/warnMAPENTech.png"))
        await channel.send(file = nextcord.File("warnMAPENTech.png"))
        await channel.send(embed = embed)
    


    # Se crea el comando para quitar los warn del usuario
    @commands.has_role(1041426879044915250)
    @commands.command(description= "Quitar alerta a un usuario")
    # Definimos el comando que va a recibir el contextp del mensaje y al miembro
    async def quitarwarn(self, ctx: commands.Context, member: nextcord.Member):
        # Usamos el cursor para interactuar con la base de datos
        async with bot.db.cursor() as cursor:
            # Hacemos una consulta a la tabla para buscar las advertencias del usuario
            await cursor.execute('SELECT reason FROM warns WHERE member = ? AND guild = ?', (member.id, ctx.guild.id))
            # Capturamos la consulta en la variable data
            data = await cursor.fetchone()
            # Iniciamos sentendia if para detectar si hay datos
            if data:
                # Si existen datos, ejecutamos un comando SQL para borrar los warns
                await cursor.execute('DELETE FROM warns WHERE member = ? AND guild = ?', (member.id, ctx.guild.id))
                # Mediante un embed, avisamos en Discord que los warns han sido borrados
                embed = nextcord.Embed(
                    description= f"<a:_:1065023533681479681> **Advertencias de {member.mention} eliminadas!**\n\nYa puede estar con la conciencia tranquila..."
                )
                embed.set_author(
                    name="Moderación de MAPEN Gang",
                    icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
                    url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
                )
                embed.set_thumbnail(
                    url= "https://cdn.discordapp.com/attachments/1012130067649921040/1068394718968422461/elite679.gif"
                )
                channel = bot.get_channel(1050230733588942868)
                await channel.send(embed = embed)
            else:
                # Si no hay warns, se utiliza un embed para indicar que no tiene warns el usuario
                embed = nextcord.Embed(
                    description= f"<a:_:1065023533681479681> **Ups! No hay warns para {member.mention}!**"
                )
                embed.set_author(
                    name="Moderación de MAPEN Gang",
                    icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
                    url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
                )
                embed.set_thumbnail(
                    url= "https://cdn.discordapp.com/attachments/1012130067649921040/1068395693175226428/think3d-smile.gif"
                )
                channel = bot.get_channel(1050230733588942868)
                await channel.send(embed = embed)
        await bot.db.commit()
    

# Declaramos el método setup que va a cargar el cog (clase Moderacion)
def setup(bot):
    bot.add_cog(Moderacion(bot))
    # Se muestra en terminal si los comandos se cargaron
    print("He añadido los comandos de moderación")
