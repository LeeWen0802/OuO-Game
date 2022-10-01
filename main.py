import discord
import json
import asyncio
import random
from discord.ext import commands

with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
CHANNEL = data["channel"]
TOKEN = data["token"]

with open('number.txt', 'w') as file:
    number = random.randint(1, 1000)
    file.write(str(number))

bot = commands.Bot(help_command=None, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'>>{bot.user}上線<<')
    while True:
        game = discord.Game(f'/help 得到指令清單')
        await bot.change_presence(status=discord.Status.idle, activity=game)
        await asyncio.sleep(5)
        game = discord.Game(f'正在服務{len(bot.guilds)}個群組')
        await bot.change_presence(status=discord.Status.idle, activity=game)
        await asyncio.sleep(5)


@bot.event
async def on_message(msg):
    if msg.channel.type is discord.ChannelType.private:
        pass
    else:
        try:
            if msg.channel.id == CHANNEL:
                with open('number.txt', 'r') as file:
                    data = file.read()
                if msg.content == data:
                    with open('number.txt', 'w') as file:
                        number = random.randint(1, 1000)
                        file.write(str(number))
                    await msg.add_reaction('🛐')
                    await msg.channel.send(f'{msg.author.mention}你猜到了!\n答案是{data}')
                    await msg.channel.send('==============================')
                elif int(msg.content) < int(data):
                    await msg.add_reaction('⬆')
                elif int(msg.content) > int(data):
                    await msg.add_reaction('⬇')
        except:
            pass


bot.run(TOKEN)
