from bot import bot
import typing
import nextcord
from nextcord.ext import commands
import wavelink

# Creamos la clase musica que va a contener todos los comandos e instrucciones relacionadas con los comandos de música y la conexión a LavaLink
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.create_nodes())

    # Creamos una función para que el bot se conecte al servidor de LavaLink
    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="lavalink.mariliun.ml", port="443", password="lavaliun", https=True)

    # Creamos un evento para detectar cuando el bot establece conexión con el nodo del servidor
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        # Mostramos en terminal que el bot se ha conectado al nodo
        print(f"El nodo {node.identifier} está listo!")

    # Creamos un comando para inicializar la conexión del bot al canal de voz
    @commands.command(name="party")
    async def party(self, ctx: commands.Context, channel: typing.Optional[nextcord.VoiceChannel]):
        # Si no se especifica canal de voz, el bot se conecta al canal de voz donde esté el usuario que ejecutó el comando
        if channel is None:
            channel = ctx.author.voice.channel
        
        # Creamos variables para obtener el nodo y el player de LavaLink
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        # Si el bot ya está conectado a un canal de voz, el bot manda un mensaje diciendo que ya está dentro de un canal de voz
        if player is not None:
            if player.is_connected():
                return await ctx.send("El bot ya está conectado a un canal de voz 😐")
        
        # El bot se conecta al canal de voz y envía un embed en el canal donde se ingresó el comando avisando que ya está listo
        await channel.connect(cls=wavelink.Player)
        embed = nextcord.Embed(
            title="Dile al DJ que apague luce' 😎",
            description=f"Ya me conecté a {channel.mention} para empezar con la música. Utiliza `m!reproduce` seguido de la canción que quieras para empezar\n\nEjemplo: `m!reproduce Hello Martin Solveig`"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1012130067649921040/1074191445088550993/ezgif.com-resize.gif"
        )
        await ctx.send(embed=embed)

    # Creamos un comando para desconectar al bot del canal de voz
    @commands.command(name="abandonar")
    async def abandonar(self, ctx: commands.Context):
        # Creamos variables para obtener el nodo y el player de LavaLink
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        # Si el player no está conectado a ningún canal de voz, el bot manda un mensaje avisando que no está conectado en ningún canal
        if player is None:
            return await ctx.send("El bot no está conectado a ningún canal 😵‍💫")

        # Si el player está conectado a un canal de voz, se desconecta y se envía un embed en el canal donde se ingresó el comando
        await player.disconnect()
        embed = nextcord.Embed(
            title="Y asi es como terminó la fiesta 🥲",
            description="Me he desconectado del canal de voz, si deseas que me una de nuevo utiliza `m!party` una vez que estés dentro de un canal de voz para continuar con el bailongo"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1012130067649921040/1074186582912942150/desaparicion.gif"
        )
        await ctx.send(embed=embed)

    # Creamos el comando para que el bot reproduzca contenido envíandole un string (búsqueda) como parámetro
    @commands.command(name="reproduce")
    async def reproduce(self, ctx: commands.Context, * , search: str):
        search = await wavelink.YouTubeTrack.search(query= search, return_first=True)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls= wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        
        # El bot reproduce la búsqueda del miembro en el canal de voz donde se conectó y envía un embed 
        await vc.play(search)
        embed = nextcord.Embed(
            title= "Pedido recibido!",
            description=f"Ahora estás escuchando {search}, puedes usar los siguientes comandos para interactuar conmigo:\n\n<:_:1062236691445862440> `m!stop` para detener la canción\n<:_:1062236691445862440> `m!pause` para pausar la canción\n<:_:1062236691445862440> `m!play` para resumir la canción"
            )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1012130067649921040/1074188705008467988/pepemusic.gif"
        )
        await ctx.send(embed=embed)

    # Creamos un comando para detener la reproducción
    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context):
        # Creamos variables para obtener el nodo y el player de LavaLink
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        # Si el bot no está conectado, envía un mensaje al canal informando que no está conectado
        if player is None:
            return await ctx.send("El bot no está conectado a ningún canal de voz 😵‍💫")

        # Si el bot está reproduciendo, detiene la reproducción y envía un embed
        if player.is_playing:
            await player.stop()
            embed = nextcord.Embed(title="He detenido la reproducción 😉")
            await ctx.send(embed=embed)
        else:
            # Si el bot está conectado pero sin reproducir contenido, manda mensaje
            return await ctx.send("Nada se está reproduciendo por ahora 🥲")

    @commands.command(name="pausa")
    async def pausa(self, ctx:commands.Context):
        # Creamos variables para obtener el nodo y el player de LavaLink
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        # Si el bot no está conectado, envía un mensaje al canal informando que no está conectado
        if player is None:
            return await ctx.send("El bot no está conectado a ningún canal de voz 😵‍💫")
        
        # Si el bot no está pausado y está reproduciendo, el bot pausa la reproducción y envía un embed
        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                embed = nextcord.Embed(title="He pausado la reproducción 😉")
                return await ctx.send(embed=embed)
            else:
                # Si el bot está conectado pero sin reproducir contenido, manda mensaje
                return await ctx.send("¡No estoy reproduciendo nada por el momento! 😐")
        else:
            # Si el contenido ya estaba en pausa, el bot informa que la reproducción está pausada
            return await ctx.send("¡La canción ya estaba pausada! 😐")

    @commands.command(name="play")
    async def play(self, ctx: commands.Context):
        # Creamos variables para obtener el nodo y el player de LavaLink
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        # Si el bot no está conectado, envía un mensaje al canal informando que no está conectado
        if player is None:
            return await ctx.send("El bot no está conectado a ningún canal de voz 😵‍💫")
        
        # Si el contenido está en pausa, el bot reanuda la reproducción
        if player.is_paused():
            await player.resume()
            embed = nextcord.Embed(title="He resumido la reproducción 😎")
            return await ctx.send(embed=embed)
        else:
            # Si el contenido no está en pausa, el bot avisa que la canción no está en pausa
            return await ctx.send("¡La reproduccion no esta pausada! 😐")

# Declaramos el método setup que va a cargar el cog (clase Música)
def setup(bot):
    bot.add_cog(Music(bot))
    # Se muestra en terminal si los comandos se cargaron
    print("He añadido los comandos de música")
