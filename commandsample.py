class C:
	
	def __init__(self, client):
		self.bot = client
		
	async def on_connect(self):
		pass
		
	async def on_loaded(self):
		pass
		
	async def on_ready(self):
		pass
	
	async def on_message(self, message):
		pass
		
	async def on_member_update(self, before, after):
		pass
		
	async def on_message_edit(self, before, after):
		pass
		
	async def on_message_delete(self, message):
		pass
		
	async def on_guild_channel_pins_update(self, channel, last_pin):
		pass
	
	async def on_guild_update(self, before, after):
		pass
		
	async def on_member_join(self, member):
		pass
		
	async def on_member_remove(self, member):
		pass
		
	async def on_guild_join(self, guild):
		pass
		
	async def on_guild_remove(self, guild):
		pass