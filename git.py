import re
import discord
import json
from discord.ext import commands
from datetime import datetime
import functools

desc='Scythe Statistics Keeper'

lengthPat = re.compile("Game Length \| (?P<rounds>\d+) Rounds")
resolutionPat = re.compile("Resolution Tile \| (?P<resolution>[a-zA-Z ]+)")
passivePat = re.compile("Passive Ability \| (?P<passive>[a-zA-Z ]+)")
agressivePat = re.compile("Aggressive Ability \| (?P<agressive>[a-zA-Z ]+)")
playerPat = re.compile(":(?P<faction>[a-zA-Z]+): \| (?P<mat>[a-zA-Z]+) \| \$(?P<coins>\d+)(?P<winner>.*)")

bot_prefix='@Automa'

client = commands.Bot(description=desc, command_prefix=bot_prefix)

@client.event
async def on_ready():
	print('Logged in')
	print('Name: {}'.format(client.user.name))
	print('ID: {}'.format(client.user.id))
	print(discord.__version__)

@client.event
async def on_message(message):
	if(message.content.startswith(bot_prefix)):
		lines = str.split(message.content, '\n')
		factions = [(m.group("faction"), m.group("mat"), m.group("coins"), m.group("winner")) 
			for m in [playerPat.match(l) for l in lines[6:]]]
		
		winner = functools.reduce(lambda x,y: x if x[3] != "" or x[2] > y[2] else y, factions)[0:3]
		losers = [fac[0:3] for fac in factions if fac[0] != winner[0]]

		data = {'date': datetime.now().isoformat(),
				'rounds': lengthPat.match(lines[1]).group('rounds'), 
				'resolution': resolutionPat.match(lines[2]).group('resolution'),
				'passive': passivePat.match(lines[3]).group('passive'),
				'agressive': agressivePat.match(lines[4]).group('agressive'),
				'winner': winner,
				'losers': losers}

		print(json.dumps(data, indent=2))

		with open('data.json', 'r') as readfile:
			filedata = json.load(readfile)
			filedata.append(data)
			print(filedata)
			with open('data.json', 'w') as outfile:  
				json.dump(filedata, outfile, indent=2)


	await client.process_commands(message)

client.run('MzU2MjU0MDMyNjMwNzc1ODA5.DO00KQ.mq5rmDeOifVOEQr4VkfiWcAf6fE')