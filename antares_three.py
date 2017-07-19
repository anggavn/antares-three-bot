import asyncio
import os
import sys
import time

from getch import pause

import discord
from discord.ext import commands
#from discord.ext.commands import Bot

#settings
bot_prefix = 'a3.'
bot_token = 'MzM1OTY2MzcxMjQwNDc2Njgz.DExcmw.GTIEPHAexF_7Iq0-OfeeoBkeR9s'
playing_text = 'with Python3.5'
playing_type = 1

flightplan_id = '335918281615736834'
afterhours_id = '335918709476687875'

bot_description = '''antares three developing phase'''

#init
#Client = discord.Client()
client = commands.Bot(command_prefix = bot_prefix, description = bot_description)

#startup
os.system('cls' if os.name == 'nt' else 'clear')
#while not client.is_logged_in:
#   print('Connecting to discord', end='')
#   count = 1
#   count_max = 3
#   while not client.is_logged_in and count<=count_max:
#   print('.', end=' ', flush=True)
#       time.sleep(0.5)
#       count += 1
#   sys.stdout.write('\r\x1b[K')
#   sys.stdout.flush()

print('Starting bot')
@client.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('{} Online'.format(client.user.name))
    print('ID  : {}\n'.format(client.user.id))
    
    await client.change_presence(game = discord.Game(name = playing_text, type = playing_type))

#relay to console for commands
@client.event
async def on_message(message):
    await client.wait_until_ready()

    message_content = message.content.strip()
    if not message_content.startswith(bot_prefix):
        return
    if message.author == client.user:
        print('[Warning] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
        space_len = len('[Command] {0.id}[{0.name}]:'.format(message.author)) - 9
        print('[   ~   ]', end='')
        for _ in range(space_len):
            print(' ', end='')
        print('  ^')
        print('[   ~   ] {} was forced to command himself'.format(client.user.name))
        return

    print('[Command] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
    await client.process_commands(message)
        
##here we go
#iff function
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

#adding functßion
@client.command()
async def add(one:int, two:int):
    await client.say('{0} + {1} = {2}'.format(one, two, one + two))

#echo function
@client.command()
async def echo(*, text:str):
    await client.say(text)

#shutdown function
@client.command()
async def dismiss():
    await client.say('Antares Three, Out!')
    print('Logging out {}'.format(client.user.name))
    await client.close()

client.run(bot_token)

print('\n{} offline'.format(client.user.name))
pause()
os.system('cls' if os.name == 'nt' else 'clear')
exit()
