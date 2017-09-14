#!/usr/bin/env python3.5

import asyncio
import os
import sys
import time
import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup
import discord
from discord.ext import commands
#from discord.ext.commands import Bot
from getch import pause
import pytoml as toml
import requests

bot_description = '''antares three developing phase'''

class Config(object):
    def __init__(self, config_filename):
        self.config_filename = config_filename
        with open(config_filename, 'r') as config_file:
            cf = toml.load(config_file)
            #load credentials
            self.bot_token = cf['credentials']['bot_token']
            #load owner
            self.owner_id = cf['owner']['owner_id']
            #load settings
            cfset = cf['settings']
            self.command_prefix = cfset['command_prefix']
            self.playing_text = cfset['playing_text']
            self.playing_type = cfset['playing_type']
            self.channel_id_bind = cfset['channel_id_bind']
            self.server_id_bind = cfset['server_id_bind']

    #updates playing_text when changed
    def change_playing_text(self, playing_text):
        pass

def wowfreakz_status():
    try:
        wf_page = requests.get('https://www.wow-freakz.com/index.php')
        wf_parsed = BeautifulSoup(wf_page.text, 'html.parser')
    except: 
        return False
        
    # per server
    # in div 5 (legion)
    wf_5 = wf_parsed.find('div', class_="realm_div_5")
    wf_5_name = wf_5.find('b').get_text().lower().title()
    wf_5_uptime = wf_5.find('span', id='uptime_5').get_text()
    wf_5_player_online = int(wf_5.find('font', color='#FFC118').get_text())
    wf_5_player_record = int(wf_5.find('font', class_='font_green').get_text())
    wf_5 = {
        'name': wf_5_name,
        'uptime':wf_5_uptime,
        'online':wf_5_player_online,
        'record':wf_5_player_record,
    }
    # in div 1 (mists)
    wf_1 = wf_parsed.find('div', class_="realm_div_1")
    wf_1_name = wf_1.find('b').get_text().lower().title()
    wf_1_uptime = wf_1.find('span', id='uptime_1').get_text()
    wf_1_player_online = int(wf_1.find('font', color='#FFC118').get_text())
    wf_1_player_record = int(wf_1.find('font', class_='font_green').get_text())
    wf_1 = {
        'name': wf_1_name,
        'uptime':wf_1_uptime,
        'online':wf_1_player_online,
        'record':wf_1_player_record,
    }
    return wf_5, wf_1

config = Config('config.toml')
client = commands.Bot(command_prefix = config.command_prefix, description = bot_description)


#when bot is ready
@client.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('{} Online'.format(client.user.name))
    print('ID  : {}\n'.format(client.user.id))
    await client.change_presence(game = discord.Game(name = config.playing_text, type = config.playing_type))

#relay to console for commands
@client.event
async def on_message(message):
    last_message = message
    cmd_err = False
    await client.wait_until_ready()
    message_content = message.content.strip()

    if not message_content.startswith(config.command_prefix.lower()):
        return
    if message.author == client.user:
        print('[Warning] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
        space_len = len('[       ] {0.id}[{0.name}]:'.format(message.author)) - 9
        print('[   ~   ]', end='')
        for _ in range(space_len):
            print(' ', end='')
        print('  ^')
        print('[   ~   ] {} was forced to command himself'.format(client.user.name))
        return

    # command, *args = message_content.split()
    # command = command[len(config.command_prefix):].lower().strip()
    # if not bot_command:
    #     print('[Warning] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
    #     print('[   ~   ] Invalid command attempt')
    #     return

    # try:
    #     await client.process_commands(message)
    # except commands.errors.CommandNotFound as err:
    #     print('[ Error ] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
    #     print('[   ~   ] {}'.format(err))
    # except commands.errors.CommandError as err:
    #     print('[ Error ] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
    #     print('[   ~   ] Error Occured. {}'.format(err))
    # except:
    #     print('[ Error ] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
    #     print('[   ~   ] Error Occured.')
    # else:
    #     await client.send_typing(message.channel)
    #     print('[Command] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
    print('[Command] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
    await client.send_typing(message.channel)
    await client.process_commands(message)



# @client.event
# async def on_command(command, ctx):
#     print('[Command] {0.id}[{0.name}]: \"{1}\"'.format(message.author, message_content))
#     return


###################################here we go

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
    await client.say('To perform an IFF (**I**dentify: **F**riend or **F**oe), enter:\n```{}iff on @[username]```'.format(config.command_prefix))

#adding function
@client.command()
async def add(one:int, two:int):
    await client.say('{0} + {1} = {2}'.format(one, two, one + two))

#echo function
@client.command(alias='say')
async def echo(*, text:str):
    await client.say(text)

#wow function
@client.command()
async def wow():
    server = wowfreakz_status()
    msg = ''
    if server:
        msg = 'WOW-Freakz server status:\n'
        for idx in range(len(server)):
            msg += ('```'\
                +'{}:\n'.format(server[idx]['name'])\
                +'Server {}\n'.format(server[idx]['uptime'])\
                +'Online: {0} // Record: {1}\n'.format(server[idx]['online'], server[idx]['record'])
                +'```\n')
        
    else:
        msg = 'Can\'t access information. There is a communication problem.'
    await client.say(msg)

#shutdown function
@client.command(alias='shutdown')
async def dismiss():
    await client.say('Antares Three, Out!')
    print('Logging out {}'.format(client.user.name))
    await client.close()

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

print('// Starting bot. Please wait. . .')
# print('// Checking network connection. . .', end='')
client.run(config.bot_token)

#after done running
print('\n{} is now offline'.format(client.user.name))
pause()
os.system('cls' if os.name == 'nt' else 'clear')
exit()
