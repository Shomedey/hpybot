import discord, asyncio, json, os, aiohttp, random, textwrap, io, importlib, sys
from contextlib import redirect_stdout
from discord import Webhook, AsyncWebhookAdapter

class DiscordBot(discord.Client):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.commands = []
		self.discord = discord
		self.loaded = False
		
	def add_command(self, object):
		self.commands.append(object)
		
	def load_command(self, object):
		if object.__class__ == str:
			command = importlib.import_module(object)
			if not hasattr(command, 'load'):
				del command
				del sys.modules[object]
				self.log("Missing load() function for {0}".format(command.__name__[9:]+".py"))
			else:
				command.load(self)
				self.log("Loaded file {0}".format(command.__name__[9:]+".py"))
		else:
			object.load(self)
			self.log("Loaded file {0}".format(object.__name__[9:]+".py"))
			
	def unload_command(self, object):
		if object.__class__ == str:
			for command in self.commands:
				if object in command.__class__.__name__:
					del sys.modules[command.__class__.__name__]
					self.commands.remove(command)
			
	def del_command(self, object):
		self.unload_command(object)

	def log(self, message, me=False):
		if me == True:
			texte = "* {0} {1}".format(str(self.user), str(message))
		else:
			texte = "[{0}] {1}".format(str(self.user), str(message))
		print(texte)
		
	async def on_connect(self):
		self.log("est maintenant connecté à Discord", me=True)
		self.log("ID: {0.id}".format(self.user))
		
		for command in self.commands:
			self.loop.create_task(command.on_connect())

	async def on_ready(self):
		if self.loaded == False: # Premier démarrage ?
			self.loaded = True # Premier démarrage accompli.
		
			for file in os.listdir("commands"):
				if file.endswith('.py'):
					try:
						self.load_command("commands." + file[:-3])
					except Exception as e:
						self.unload_command(file[:-3])
						self.log('La ou le groupe de commande(s) {} n\'a pas pu être chargé.'.format(file))
						self.log('→ {}: {}'.format(type(e).__name__, e))
						
			for command in self.commands:
				self.loop.create_task(command.on_loaded())
		
		for command in self.commands:
			self.loop.create_task(command.on_ready())
		
	async def on_guild_join(self, guild):
		self.log("a rejoint le serveur {0} de {1}".format(
			str(guild.name),
			str(guild.owner)
		), me=True)
		
		for command in self.commands:
			self.loop.create_task(command.on_guild_join(guild))
		
	async def on_guild_remove(self, guild):
		self.log("a quitté le serveur {0} de {1}".format(
			str(guild.name),
			str(guild.owner)
		), me=True)
		
		for command in self.commands:
			self.loop.create_task(command.on_guild_remove(guild))
			
	async def on_guild_update(self, before, after):
		for command in self.commands:
			self.loop.create_task(command.on_guild_update(before, after))
		
	async def on_member_join(self, member):
		for command in self.commands:
			self.loop.create_task(command.on_member_join(member))
		
	async def on_member_remove(self, member):
		for command in self.commands:
			self.loop.create_task(command.on_member_remove(member))
			
	async def on_command(self, message, _command, *args):
		for command in self.commands:
			if hasattr(command, "cmd_"+_command.lower()):
				function = getattr(command, "cmd_"+_command.lower())
				self.loop.create_task(function(message, *args))
		
	async def on_message(self, message):
		for command in self.commands:
			self.loop.create_task(command.on_message(message))
			
		if self.user.bot:
			await self.check_command(message)
		else:
			if self.user.id == message.author.id:
				await self.check_command(message)
			
	async def check_command(self, message):
		command = None
		args = None
		for prefix in ["hpybot ","hpybot"]:
			if message.content.startswith(prefix):
				words = message.content[len(prefix):].split(" ")
				if len(words) != 0:
					command = words[0]
					if len(words) > 1:
						args = words[1:]
					else:
						args = []
				else:
					command = None
			else:
				command = args = None
		
		if command != None:
			await self.on_command(message, command, *args)
		
	async def on_message_edit(self, before, after):
		for command in self.commands:
			self.loop.create_task(command.on_message_edit(before, after))
			
		await self.check_command(after)
			
	async def on_message_delete(self, message):
		for command in self.commands:
			self.loop.create_task(command.on_message_delete(message))
			
	async def on_guild_channel_pins_update(self, channel, last_pin):
		for command in self.commands:
			self.loop.create_task(command.on_guild_channel_pins_update(channel, last_pin))
		
	async def on_member_update(self, before, after):		
		for command in self.commands:
			self.loop.create_task(command.on_member_update(before, after))
			
# Chargement et vérification de la configuration
print("[•] TOKEN ?")
token = input(">>> ")
			
# Démarrage du bot
client = DiscordBot()
client.run(token)