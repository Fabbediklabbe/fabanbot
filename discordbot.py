#!/usr/bin/python
import discord
import os
import random
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

cs_folder_path = "/home/pi/fabians-python/csgo/"

def update_skin_count(user_id, rarity):

	json_path = "/home/pi/fabians-python/discord_data.json"

	if os.path.exists(json_path):
		with open(json_path, "r") as file:
			all_users_data = json.load(file)
	else:
		all_users_data = {}

	user_data = all_users_data.get(user_id, {})

	user_data[rarity] = user_data.get(rarity, 0) + 1

	all_users_data[user_id] = user_data

	with open(json_path, "w") as file:
		json.dump(all_users_data, file)

def get_color_and_path(rarity):
	color = None
	folder_path = None

	if rarity <= 299:
		color = "Blue"
		folder_path = "blue/"
	elif rarity <= 359:
		color = "Purple"
		folder_path = "purple/"
	elif rarity <= 371:
		color = "Pink"
		folder_path = "pink/"
	elif rarity <= 374:
		color = "Red"
		folder_path = "red/"
	else:
		color = "Gold"
		folder_path = "knife/"

	return color, folder_path

@bot.event
async def on_ready():

	print(f'We have logged in as {bot.user}')
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('!cs, !stats'))

@bot.event
async def on_message(message):

	if message.author == bot.user:
		return
	await bot.process_commands(message)

@bot.command()
async def stats(ctx):

	user_id = str(ctx.message.author.id)
	json_path = "/home/pi/fabians-python/discord_data.json"
	colors = ["Blue", "Purple", "Pink", "Red", "Gold"]

	if os.path.exists(json_path):
		with open(json_path, "r") as file:
			all_users_data = json.load(file)
	else:
		all_users_data = {}

	user_data = all_users_data.get(user_id, {})

	stats = "\n".join([f"{color.capitalize()}: {user_data.get(color, 0)}" for color in colors])

	await ctx.reply(f"Your stats:\n{stats}")


@bot.command()
async def cs(ctx):


	rarity = random.randint(0, 375)
	float = random.uniform(0.0, 1.0)
	stattrak_int = random.randint(1,10)
	user_id = str(ctx.message.author.id)

	color, folder_path = get_color_and_path(rarity)

	if color is not None and folder_path is not None:
		rarity_folder_path = cs_folder_path + folder_path
		cs_dirListing = os.listdir(rarity_folder_path)
		cs_picture_amount = len(os.listdir(rarity_folder_path))
		cs_picture_to_print = random.randint(0, (cs_picture_amount - 1))
		update_skin_count(user_id, color)

	#if float <= 0.07:
	#	wear = "Factory-New (FN)"
	#elif float <= 0.15:
	#	wear = "Minimal-Wear (MW)"
	#elif float <= 0.38:
	#	wear = "Field-Tested (FT)"
	#elif float <= 0.45:
	#	wear = "Well-Worn (WW)"
	#else:
	#	wear = "Battle-Scarred (BS)"

	if stattrak_int == 10:
		stattrak = "**--------------------------------------STATTRAK--------------------------------------**"
	else:
		stattrak = ""


	await ctx.reply (stattrak, file = discord.File (rarity_folder_path + cs_dirListing[cs_picture_to_print]))
	#mention_author = True

bot.run(DISCORD_TOKEN)
