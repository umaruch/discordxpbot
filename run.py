import discord
from discord.ext import commands
from discord.utils import get
import datetime
import asyncio

from config import TOKEN, PREFIX,SERVER_ID, ONLINE_METER_ID
#from other import dialog
from user import Users

users = Users()
bot = commands.Bot(command_prefix = PREFIX)
bot.remove_command('help')
print("Bot object has created")



#CHECK ONLINE STATUS ON SERVER
async def online_status():
	while True:
		guild = bot.get_guild(int(SERVER_ID))
		N = sum(member.status!=discord.Status.offline and not member.bot for member in guild.members)
		channel = bot.get_channel(int(ONLINE_METER_ID))

		await discord.VoiceChannel.edit(channel, name = f"Онлайн: {N}")
		print("<{time}> Обновлено число пользователей онлайн".format(
			time = datetime.datetime.now()
		))
		await asyncio.sleep(30)

async def check_voices():
	while True:
		guild = bot.get_guild(int(SERVER_ID))
		voices = guild.voice_channels
		for voice in voices:
			voice_members = voice.members
			if not voice_members == []:
				for member in voice_members:
					users.add_voice(member.id)
					#print(f"<{datetime.datetime.now()}> Пользователю name={member.name} id={member.id} начислен опыт за активность в голосовом общении")
		await asyncio.sleep(10)
		
@bot.event
async def on_message(mes):
	if mes.content.startswith(PREFIX):
		await bot.process_commands(mes)
	else:
		if mes.author == bot.user:
			return
		print("<{time}> {username} {userid}: {content}".format(
			time = datetime.datetime.now(),
			username = mes.author.name,
			userid = mes.author.id,
			content = mes.content
		))
		users.add_message(mes.author.id)

@bot.event
async def on_ready():
	bot.loop.create_task(online_status())
	bot.loop.create_task(check_voices())	
	print("Successful connect to server")
	


@bot.command(pass_context = True)
async def help(ctx):
	await ctx.channel.purge( limit = 1)
	print(f"<{datetime.datetime.now()}> {ctx.author.name} попросил о помощи")
	await ctx.send(f"<@!{ctx.author.id}>")

@bot.command(pass_context = True)
async def info(ctx):
	user_info = users.get_info(ctx.author.id)
	embed=discord.Embed(title="Статистика пользователя", color=0x030303)
	embed.set_author(name=ctx.author.name)
	embed.add_field(name="Сообщений", value=user_info[1], inline=True)
	embed.add_field(name="Времени  в войсе", value=user_info[2]+"h", inline=True)
	embed.add_field(name="Опыт", value=user_info[3], inline=True)
	embed.set_footer(text="А теперь уебывай на хуй")
	await ctx.send(embed=embed)


bot.run(TOKEN)