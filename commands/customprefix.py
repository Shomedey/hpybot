from commandsample import C
from utils.answers import embed as E
import asyncio

class CustomPrefix(C):

	async def on_loaded(self):
		self.default = ""
		try: self.bot.sql("CREATE TABLE guilds (id INTEGER NOT NULL UNIQUE PRIMARY KEY)")
		except: pass
		try: self.bot.sql("ALTER TABLE guilds ADD CustomPrefix_prefix varchar(20) DEFAULT ''")
		except: pass
		
	def get(self, guild):
		try: self.bot.sql("INSERT INTO guilds (id) VALUES (%s)" %(guild.id))
		except: pass
		return self.bot.sql("SELECT CustomPrefix_prefix FROM guilds WHERE id = %s" %(guild.id))[0][0]
		
	def set(self, guild, value):
		self.get(guild)
		self.bot.sql("UPDATE guilds SET CustomPrefix_prefix = '%s' WHERE id = %s" %(value, guild.id))
		
	async def cmd_setprefix(self, message, *args):
		if self.bot.user.bot:
			if message.author.guild_permissions.manage_guild:
				if len(args) > 0:
					value = " ".join(args)
					value = value.replace("{space}", " ") # Replace {space} by a space
					if value in ["off","disable","f4ck","stop","nope"]:
						value = ""
					self.set(message.guild, value)
					await message.add_reaction("✅")
				else:
					_message = await message.channel.send(None, embed=E(message.author, "**Actual prefix** : ``%s``\nDo %ssetprefix [new] to edit the prefix" %(get(message.guild), self.bot.config["prefixs"][0])))
					await asyncio.sleep(5)
					await _message.delete()
			else:
				_message = await message.channel.send(None, embed=E(message.author, "You are not allowed to use that command."))
				await asyncio.sleep(5)
				await _message.delete()
		else:
			_message = await message.channel.send(None, embed=E(message.author, "Selfbots can't do that."))
			await asyncio.sleep(5)
			await message.delete()
			await _message.delete()
			
	async def on_message(self, message):
		prefix = self.get(message.guild)
		command = None
		args = None
		if prefix != "":
			if message.content.startswith(prefix):
				parts = message.content[len(prefix):].split(" ")
				if len(parts) > 0:
					command = parts[0]
					if len(parts) > 1:
						args = parts[1:]
					else:
						args = []
		if command != None:
			await self.bot.on_command(message, command, *args)
				
def load(client):
	client.add_command(
			CustomPrefix(client)
		)