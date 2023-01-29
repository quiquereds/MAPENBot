import os
import nextcord # Discord API
from config import TOKEN # TOKEN del bot declarado en config.py
from nextcord import slash_command, Interaction
from nextcord.ext import commands

# Configuramos los intentos de bot asi como el prefijo para utilizarlo en Discord
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix= "m!",intents= intents)

# Creamos un método para cargar los módulos (comandos) del bot
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

# Creamos un método para eliminar los módulos (comandos) del bot
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

# Iteramos en la carpeta "cogs" para cargar todos los módulos del bot
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Inicializa el proceso del bot con su TOKEN
bot.run(TOKEN)