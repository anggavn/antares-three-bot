import discord
from discord.ext import commands
#from discord.ext.commands import Bot

import asyncio

#settings
bot_prefix = 'a3.'
bot_token = 'MzM1OTY2MzcxMjQwNDc2Njgz.DExcmw.GTIEPHAexF_7Iq0-OfeeoBkeR9s'
playing_text = 'testasdf'
playing_type = 1

flightplan_id = '335918281615736834'
afterhours_id = '335918709476687875'

#fff
bot_description = '''antares three developing phase'''

#init
#Client = discord.Client()
client = commands.Bot(command_prefix = bot_prefix, description = bot_description)

#startup

@client.event
async def on_ready():
	print('{} Online'.format(client.user.name))
	print('ID  : {}\n'.format(client.user.id))
	
	await client.change_presence(game = discord.Game(name = playing_text, type = playing_type))


@client.event
async def on_message(message):
	await client.wait_until_ready()

	message_content = message.content.strip()
	if message_content.startswith(bot_prefix):
		print('[Command] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))

	await client.process_commands(message)
		
#here we go
	
#iff functions
@client.group(pass_context = True)
async def iff(ctx):
	if ctx.invoked_subcommand is None:
		await client.say('IFF request incomplete!')
@iff.command()
async def on(*, text:str):
	if text.strip().startswith('<@&'):
		await client.say('All {}s have been identified as a friend!'.format(text))
	elif text.strip().startswith('<@'):
		await client.say('{} has been identified as a friend!'.format(text))
	elif text.strip().startswith('@everyone'):
		await client.say('{} on this squadron has been identified as a friend!'.format(text))
	elif text.strip().startswith('@here'):
		await client.say('Everybody {} has been identified as a friend!'.format(text))
	else:
		await client.say('Can not perform IFF on said target!')
@iff.command()
async def help():
	await client.say('To perform an IFF (**I**dentify: **F**riend or **F**oe), enter:\n```{}iff on @[username]```'.format(bot_prefix))

@client.command()
async def add(one:int, two:int):
	await client.say('{0} + {1} = {2}'.format(one, two, one + two))
	
@client.group(pass_context = True)
async def isempty(ctx):
	await client.say('yes?')
	
@client.command()
async def echo(*, message:str):
	await client.say(message)
	
client.run(bot_token)