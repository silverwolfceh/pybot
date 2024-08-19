import io
import aiohttp
import json
import discord
from discord.ext import commands
from jsondb import jsondb

class botadapter:
	def __init__(self, identifier):
		self.data = jsondb(identifier, "userinfo")
		self.is_err = False
		self.errors = []
	

class DiscordBot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.prefix = "[Meow] "
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f'We have logged in as {self.bot.user.name}')

	@commands.Cog.listener()
	async def on_message(self, message):
		# Customize this method as needed
		pass

	@commands.command(name='smspool')
	async def smspool(self, ctx, *args):
		user_id = ctx.author.id
		data = botadapter(user_id)
		

	async def send_message(self, ctx, msg, tag = False):
		if self.prefix not in msg:
			msg = f"{self.prefix} {msg}"
		
		if tag:
			msg = f"{msg} {ctx.author.mention}"
		await ctx.send(msg)
	
	async def send_photo(self, ctx, photo_url, tag = False):
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(photo_url) as response:
					if response.status == 200:
						image_bytes = await response.read()
						with io.BytesIO(image_bytes) as image_file:
							await ctx.send(file=discord.File(image_file, filename='screenshot.jpg'))
					else:
						await ctx.send(f'Failed to fetch photo from URL {ctx.author.mention}')
		except Exception as e:
			await ctx.send(f'Error sending photo: {e}')