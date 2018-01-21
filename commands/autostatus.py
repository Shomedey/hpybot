from commandsample import C
from utils.answers import embed as E
import asyncio

class AutoStatus(C):
	"""
	This is command is easy to use!
	Just do &&setstatus. ^-^
	Only works if you're the bot owner!
	"""
	async def on_loaded(self):
		appinfo = await self.bot.application_info()
		self.owner = appinfo.owner
		self.last_guild = "X"
		self.tmp = False
		exists = True
		try:
			self.bot.sql("CREATE TABLE bots (id INTEGER NOT NULL PRIMARY KEY, AutoStatus VARCHAR(255) DEFAULT '')")
			exists = False
		except:
			pass
		if exists == False:
			self.bot.sql("INSERT INTO bots (id) VALUES (%s)" %(self.bot.user.id))
		self.status = self.bot.sql("SELECT AutoStatus FROM bots WHERE ID = %s" %(self.bot.user.id))[0][0]
		await self.editStatus()
		
	def set(self, newStatus):
		self.bot.sql("UPDATE bots SET AutoStatus = '%s' WHERE id = %s" %(newStatus, self.bot.user.id))
		self.status = newStatus
		
	async def on_member_join(self, member):
		await self.editStatus()
		
	async def on_member_remove(self, member):
		await self.editStatus()
	
	async def on_guild_join(self, guild):
		self.last_guild = guild.name
		await self.editStatus()
		
	async def on_guild_remove(self, guild):
		self.last_guild = guild.name
		await self.editStatus()
		
	async def cmd_setstatus(self, message, *args):
		if message.author.id == self.owner.id:
			if len(args) == 0:
				await message.channel.send(None, embed=E(message.author, """**What do you want to set for the new message?**
• $users_count ▬ Count of users
• $guilds_count ▬ Count of guilds
• $last_guild ▬ Last guild's name joined
• $streaming ▬ Add "Streaming" in your status
• $listening ▬ Add "Listening" in your status
• $watching ▬ Add "Watching" in your status"""))
				def check(m):
					return m.author.id == message.author.id and m.channel.id == message.channel.id
				_message = await self.bot.wait_for("message", check=check)
				if _message.content.lower() in ["off","nul","none","null","disable"]:
					self.set("")
				else:
					self.set(_message.content)
				await _message.add_reaction("✅")
			else:
				if message.content.lower() in ["off","nul","none","null","disable"]:
					self.set("")
				else:
					self.set(" ".join(args))
				await message.add_reaction("✅")
		else:
			_message = await message.channel.send(None, embed=E(message.author, "You are not allowed to use that command!"))
			await asyncio.sleep(5)
			await _message.delete()
		await self.editStatus()
		
	async def editStatus(self):
		if self.status != "" and not self.tmp:
			self.tmp = True
			type = 0
			status = self.status
			status = status.lower().replace("$guilds_count", str(len(self.bot.guilds)))
			status = status.lower().replace("$users_count", str(len(self.bot.users)))
			status = status.lower().replace("$last_guild", self.last_guild)
			if "$watching" in status.lower():
				status = status.lower().replace("$watching", "")
				type = 3
			if "$listening" in status.lower():
				status = status.lower().replace("$listening", "")
				type = 2
			if "$streaming" in status.lower():
				status = status.lower().replace("$streaming", "")
				type = 1
			await self.bot.change_presence(
					status = self.discord.Status.online,
					game = self.discord.Game(
							type=type,
							url="https://twitch.tv/discordapp",
							name=status
						)
				)
			await asyncio.sleep(60)
			self.tmp = False
	
def load(client):
	client.add_command(AutoStatus(client))