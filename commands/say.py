from commandsample import C

class Say(C):
	async def cmd_say(self, message, *args):
		message_f = "𝅳" # Protect fucking bots of running commands on these.
		message_f += message.content # Adding the content of the message.
		message_f = message_f.replace("@everyone", "@𝅳everyone") # Disabling @everyone.
		message_f = message_f.replace("@here", "@𝅳here") # Disabling @here.
		await message.channel.send(message_f)
		
def load(client):
	client.add_command(Say(client))