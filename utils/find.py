class UnsupportedType(Exception):
	pass

def user(abc, guild=None):
	if abc.__class__ == int:
		if guild == None:
			return client.get_user(abc)
		else:
			return guild.get_member(abc)
	elif abc.__class__ == str:
		abd = ""
		for letter in abc:
			if letter.isdigit():
				abd += letter
		try:
			abd = int(abd)
			if guild == None:
				return client.get_user(abd)
			else:
				return guild.get_member(abd)
		except:
			pass
		if guild == None:
			for member in bot.users:
				if abc.lower() in str(member).lower():
					return member
		else:
			for member in guild.members:
				if abc.lower() in str(member).lower():
					return member
	else:
		raise UnsupportedType("Type {0} unsupported.".format(abc.__class__.__name__))