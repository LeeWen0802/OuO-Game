import discord
import json
import asyncio
import random
from discord.ext import commands

with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
CHANNEL = data["channel"]
TOKEN = data["token"]
GUESSBASE = random.randint(1, 1000)

bot = commands.Bot(help_command=None, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'>>{bot.user}上線<<')
    while True:
        # change the bot status
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(f'/help 得到指令清單'))
        await asyncio.sleep(5)
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(f'正在服務{len(bot.guilds)}個群組'))
        await asyncio.sleep(5)


@bot.event
async def on_application_command_error(ctx, error):
    # globally handle app command error
    embed = discord.Embed(title="❌ 發生未知錯誤",
                          description=f"請回報此錯誤:```{error}```", color=discord.Colour.red())
    await ctx.respond(embed=embed, ephemeral=True)


@bot.event
async def on_message(msg):
    # determine if a user is sending messages in the PM
    if msg.channel.type is discord.ChannelType.private:
        # if yes, return the event
        return
    if msg.channel.id == CHANNEL:
        # determine if the message bot got is a number not a string
        try:
            # if yes, continue
            guessing = int(msg.content)
        except:
            # if no, delete the weird thing
            return await msg.delete()
        # global declare the answer because we might change it
        global GUESSBASE
        # guessed it correctly
        if guessing == GUESSBASE:
            GUESSBASE = random.randint(1, 1000)
            await msg.add_reaction('🛐')
            await msg.channel.send(f'{msg.author.mention}你猜到了!\n答案是{data}')
            return await msg.channel.send('==============================')
        # the guessing is lower than answer
        elif guessing < GUESSBASE:
            return await msg.add_reaction('⬆')
        # the guessing is higher than answer
        return await msg.add_reaction('⬇')


bot.run(TOKEN)
