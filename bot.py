import re
import discord
from discord.ext import commands

desc='Tutorial Bot'

bot_prefix=':stat'

client = commands.Bot(description=desc, command_prefix=bot_prefix)
pat = ':stat(?P<mat> [a-zA-Z]+)? (?P<winner>:[a-zA-Z]+:) (?P<coins>\d+)[c|C] [r|R](?P<round>\d+) vs(?P<l1> :[a-zA-Z]+:)?(?P<l2> :[a-zA-Z]+:)?(?P<l3> :[a-zA-Z]+:)?(?P<l4> :[a-zA-Z]+:)?(?P<l5> :[a-zA-Z]+:)?(?P<l6> :[a-zA-Z]+:)?'
factionPattern = re.compile(pat)
factions = ['Nordic', 'Rusviet', 'Saxony', 'Polania', 'Crimean', 'Albion', 'Togawa']
mats = ['Industrial', 'Engineering', 'Militant', 'Patriotic', 'Innovative', 'Mechanical', 'Agricultural']

@client.event
async def on_ready():
	print('Logged in')
	print('Name: {}'.format(client.user.name))
	print('ID: {}'.format(client.user.id))
	print(discord.__version__)

@client.command(pass_context=True)
async def ping(ctx):
	await client.say('pong')

@client.event
async def on_message(message):
	if(message.content.startswith(':stat ')):
		errors = []
		m = factionPattern.match(message.content)
		if m:
			winnerPat= re.compile(':(?P<faction>[a-zA-Z]+):')
			winner = winnerPat.match(m.group("winner")).group('faction').capitalize()
			mat = m.group('mat')
			if mat : 
				mat = mat.strip().capitalize() 
				if mat not in mats: errors.append('{} is not a valid player mat'.format(mat))
			else : mat = ''
			coins = m.group('coins')
			round_ = m.group('round')
			if (winner not in factions): errors.append("{} is not a valid faction".format(winner))

			loserPat= re.compile(' :(?P<faction>[a-zA-Z]+):')
			l = [m.group("l1"), m.group("l2"), m.group("l3"), m.group("l4"), m.group("l5"), m.group("l6")]
			losers = [loserPat.match(f).group('faction').capitalize() for f in l if f]
			for f in losers: 
				if (f not in factions): errors.append("{} is not a valid faction".format(f))
		else:
			errors.append('Wrong Format')
		for e in errors: await client.send_message(message.channel, '```{}```'.format(e))
		if not len(errors): await client.send_message(message.channel, '```stats saved: {} {} won with {} coins on round {} ```'.format(mat, winner, coins, round_))
	await client.process_commands(message)﻿
	
client.run('')
