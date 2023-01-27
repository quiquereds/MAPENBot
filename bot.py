import os
import nextcord # Discord API
import asyncio
import aiosqlite # Base de datos SQL Lite
import datetime  # Librería para utilizar timestamps
from config import TOKEN # TOKEN del bot declarado en config.py
from nextcord import slash_command, Interaction
from nextcord.ext import commands

# Configuramos los intentos de bot asi como el prefijo para utilizarlo en Discord
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix= "m!",intents= intents)

#Comando para ejecutar el bot y cambiar su presencia
@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type = nextcord.ActivityType.watching, name = "MAPEN Tech en YT"))
    # Avisa en terminal cuando el bot se ha conectado
    print(f'He iniciado sesion como {bot.user}')
    # Iniciamos la conexión a la base de datos usando aioslite
    bot.db = await aiosqlite.connect("warns.db")
    # Configuramos un tiempo de espera para la inicialización de la base de datos para prevenir errores
    await asyncio.sleep(3)
    # Se crea la tabla de la base de datos para el miembro si no existe
    async with bot.db.cursor() as cursor:
        await cursor.execute("CREATE TABLE IF NOT EXISTS warns(member INTEGER, reason TEXT, time INTEGER, guild INTEGER)")
    await bot.db.commit()

# Comando para verificar el estatus del bot
@bot.slash_command(name="ping",description= "Verifica que el bot funcione correctamente 🏓")
async def hello(interaction: nextcord.Interaction):
    await interaction.response.send_message(f"Haciendo ping a MAPEN Tech con 33 bytes de datos... \n\n Respuesta desde MAPEN Tech tiempo 15ms... \n Respuesta desde MAPEN Tech tiempo 11ms... \n Respuesta desde MAPEN Tech tiempo 5ms... \n Respuesta desde MAPEN Tech tiempo 1ms... \n\n Paquetes: enviados = 4, recibidos = 4, perdidos = 0 \n Pero si no hablas taka taka... 🏓 pong!")

# Evento para detectar cuando nuevos usuarios se unen al servidor
@bot.event
async def on_member_join(member):
    # Creamos una variable para almacenar el guild del servidor (ID)
    guild = member.guild
    # Creamos una variable para almacenar el embed
    embed = nextcord.Embed(
        # Dentro del embed, se coloca un mensaje para dar la bienvenida, mencionando al usuario y el total de usuarios utilizando la variable guild 
        description= f"**Bienvenid@ a MAPEN Gang {member.mention}!** <a:_:1062238851185266798>\n\nContigo ya somos {guild.member_count} <a:_:1062238871527620728><a:_:1062238871527620728>\n\nEstamos agradecidos de todo corazón que te hayas unido al server, esperamos que tengas una muy buena experiencia, puedes hacer aquí lo siguiente:\n\n<a:_:1062238851185266798> Compartir tu pasión tech con todos\n<a:_:1019057180697174016> Encontrar gangas tech en productos tecnológicos\n<a:_:1019795438863384727> Pasar un momento cool con todos eschando música o jugando\n<a:_:1041814614448537704> Subir de nivel mientras participas desbloqueando canales nuevos\n<:_:1015097359916605461> Conseguir puntos del canal para comprar roles\n<a:_:1015882420370804856> Contar con apoyo siempre para dudas, recomendaciones y consejos\n\n**Lo primero que tienes que hacer...**\n\n<:_:1062236697858953246> Visita <#1014691143545536542> para personalizar el server a tu manera\n<:_:1062236697858953246> Consulta <#1015063262708121610> para conocer más sobre el server\n<:_:1062236697858953246> Dile hola a todos en <#986683116171182105>"
    )
    # Se define el autor del Embed
    embed.set_author(
        name= "MAPEN Tech",
        icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
        url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )
    # Se coloca una imágen en el embed que será igual a la foto de perfil del usuario
    embed.set_thumbnail(
        url= member.display_avatar
    )
    # Se añade otra imágen en la parte inferior del embed personalizada del servidor
    embed.set_image(
        url= "https://cdn.discordapp.com/attachments/1012130067649921040/1067232233565462539/bienvenidaMAPENTech.gif"

    )
    # Se crea una variable para almacenar el ID del canal de bienvenidas
    channel = bot.get_channel(986683116171182101)
    # El bot envía una imágen personalizada del servidor antes del embed al canal definido
    await channel.send(file=nextcord.File("holaMAPENTech.png"))
    # El bot envía el embed creado anteriormente al canal definido
    await channel.send(embed = embed)

# Evento para detectar cuando los usuarios abandonan el servidor
@bot.event
async def on_member_remove(member):
    # Creamos una variable para almacenar el guild del servidor (ID)
    guild = member.guild
    # Creamos una variable para almacenar el embed
    embed = nextcord.Embed(
        # Dentro del embed, se coloca un mensaje para despedir mencionando al usuario 
        description= f"<a:_:1065019205679841390>**Gracias por haber estado aquí {member.mention}!**\n\nEsperamos que te hayas divertido por aquí , aprovechado de alguna oferta y alivianado de tus dudas 😌\n\n***Ójala volvamos a verte pronto***"
    )
    # Se define el autor del Embed
    embed.set_author(
        name= "MAPEN Tech",
        icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
        url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )
    # Se coloca una imágen en el embed que será igual a la foto de perfil del usuario
    embed.set_thumbnail(
        url= member.display_avatar
    )
    # Se crea una variable para almacenar el ID del canal de despedidas
    channel = bot.get_channel(1012084418615201822)
    # El bot envía una imágen personalizada del servidor antes del embed al canal definido
    await channel.send(file=nextcord.File("adiosMAPENTech.png"))
    # El bot envía el embed creado anteriormente al canal definido
    await channel.send(embed = embed)

# Evento para detectar cuando los usuarios son baneados
@bot.event
async def on_member_ban(guild, member):
    # Creamos una variable para almacenar el guild del servidor (ID)
    guild = member.guild
    # Creamos una variable para almacenar el embed
    embed = nextcord.Embed(
        # Dentro del embed, se coloca un mensaje de ban mencionando al usuario 
        description= f"<a:_:1041814509779693710> **Pa tu casa {member.mention}!**\n\nPor infringir nuestras <#986736827136376882> te hemos baneado del servidor con el objetivo de mantener un ambiente sano\n\n*Puedes apelar la sanción haciendo [click aquí](https://forms.gle/tGujMHC9SrK3SDHU6)*"
    )

    # Se define el autor del Embed
    embed.set_author(
        name= "MAPEN Tech",
        icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
        url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )
    
    # Se coloca una imágen en el embed que será igual a la foto de perfil del usuario
    embed.set_thumbnail(
        url= member.display_avatar
    )

    # Se coloca una imágen personalizada con referencia a Among Us en la parte inferior del embed
    embed.set_image(
        url= "https://cdn.discordapp.com/attachments/1012130067649921040/1067540640180748298/banMAPENTech.gif"

    )

    # Se coloca un pie de página al embed con la información del sitio en donde se generó la imágen anterior
    embed.set_footer(
        icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1067548574008754217/web.png",
        text= "Imagen creada con https://ejector.kassellabs.io/"
    )

    # Se crea una variable para almacenar el ID del canal de bans
    channel = bot.get_channel(1050231800443715666)
    # El bot envía una imágen personalizada del servidor antes del embed al canal definido
    await channel.send(file=nextcord.File("banMAPENTech.png"))
    # El bot envía el embed creado anteriormente al canal definido
    await channel.send(embed = embed)

# Se crea un método para añadir advertencias a un usuario en específico, recibiendo el contexto (mensaje, razón y el miembro a sancionar)
async def addWarn(ctx, reason, member):
    # Creamos un objeto de tipo cursor para ejecutar comandos de SQL
    async with bot.db.cursor() as cursor:
        # Insertamos dentro de la tabla warns información sobre el usuario, advertencias y su fecha de creación
        await cursor.execute("INSERT INTO warns (member, reason, time, guild) VALUES (?, ?, ?, ?)", (member.id, reason, int(datetime.datetime.now().timestamp()), ctx.guild.id))
    # Guardamos cambios en la tabla
    await bot.db.commit()

# Creamos el comando para hacer warn a un miembro con el prefijo del bot
@bot.command(description= "Alerta a un usuario")
# Definimos el comando que va a recibir el contexto, la mención del miembro y la razón de warn
async def warn(ctx: commands.Context, member: nextcord.Member, *, reason: str= "No hay razón de advertencia"):
    # Se ejecuta el método para registrar en la base de datos el warn del miembro
    await addWarn(ctx, reason, member)
    # Se crea una variable para almacenar un embed
    embed = nextcord.Embed(
        # Dentro del embed se coloca una descripción sobre el warn, mencionando al usuario e indicando la razón del warn
        description= f"<a:_:1062238854586834944> **Cuidado {member.mention} estás advertido!**\n\nPor infringir nuestras <#986736827136376882> has recibido una advertencia. Si juntas 3 serás acreedor@ a un ban\n\n**Razón:**\n{reason}"
    )
    # Se define el autor del embed
    embed.set_author(
        name= "Moderación de MAPEN Gang",
        icon_url= "https://cdn.discordapp.com/attachments/1012130067649921040/1014703404334972948/Logo2022.png",
        url="https://www.youtube.com/channel/UC3nQBkZDOemTx3ZHXfLg1ug"
        )
    
    # Se coloca la foto de perfil del usuario warneado dentro del embed
    embed.set_thumbnail(
        url= member.display_avatar
    )

    # En la parte inferior del embed, se agrega una imagen personalizada haciendo referencia a una tarjeta amarilla
    embed.set_image(
        url= "https://cdn.discordapp.com/attachments/1012130067649921040/1067562376578224270/warnMAPENTech.gif"

    )

    # Se crea un pie de página en el embed
    embed.set_footer(
        text= "¿Existe alguna injusticia? Envíanos un ticket"
    )

    # Se almacena en la variable canal el ID del canal de warns
    channel = bot.get_channel(1050230733588942868)
    # El bot primero envía una imagen personalizada con el título Warn
    await channel.send(file=nextcord.File("warnMAPENTech.png"))
    # El bot envía el embed creado anteriormente
    await channel.send(embed = embed)


# Creamos el comando para eliminar las advertencias de un miembro
@bot.command(description= "Quita alerta a un usuario")
# Definimos el comando que va a recibir el contexto del mensaje y la mención del miembro
async def quitarwarn(ctx: commands.Context, member: nextcord.Member):
    # Usamos el objeto cursor para interactuar con la base de datos y ejecutar comandos SQL
    async with bot.db.cursor() as cursor:
        # Hacemos una consulta a la tabla de advertencias para buscar los warns de un miembro en específico
        await cursor.execute('SELECT reason FROM warns WHERE member = ? AND guild = ?', (member.id, ctx.guild.id))
        # Capturamos la consulta en la variable data
        data = await cursor.fetchone()
        # Iniciamos una sentencia if para detectar si se detectaron warns en el usuario mencionado
        if data:
            # Si existen datos, ejecutamos un comando SQL para eliminar los warns del usuario de la tabla warns
            await cursor.execute('DELETE FROM warns WHERE member = ? AND guild = ?', (member.id, ctx.guild.id))
            # El bot envía un mensaje de que los datos han sido eliminados
            await ctx.send("Advertencia eliminada")
        else:
            # Si no hay warns, el bot envía un mensaje avisando que no hay ningún warn para ese usuario
            await ctx.send("No hay ninguna advertencia")
    # Guardamos cambios en la BDD
    await bot.db.commit()


bot.run(TOKEN)