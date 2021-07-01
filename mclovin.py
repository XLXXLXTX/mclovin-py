#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""mclovin.py: Discord bot to generate fake id.
	       Usage: python3 mclovin.py
	       "template" folder is needed to run correctly the bot.
	       Repo Link: https://github.com/XLXXLXTX/mclovin-py
"""


from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter

import discord

#Text at the bottom of the photo
STREET = "123 FREDY FAZBEAR PiZZA"
LOCATION = "HONOLULUWU, HI 96820"
#Radius of blur effect for avatar pic
RADIUS = 5	

def blurEdgesAvatar(avatarFile):
	diam = 2*RADIUS
	avatar = Image.open(avatarFile)
	#Background ID color=> (228, 223, 223)
	back = Image.new('RGB', (avatar.size[0]+diam, avatar.size[1]+diam), (228, 223, 223))
	back.paste(avatar, (RADIUS, RADIUS))

	#Create blur mask
	mask = Image.new('L', (avatar.size[0]+diam, avatar.size[1]+diam), 255)
	blck = Image.new('L', (avatar.size[0]-diam, avatar.size[1]-diam), 0)
	mask.paste(blck, (diam, diam)) 

	#Blur avatar and paste blurred edge according to mask
	blur = back.filter(ImageFilter.GaussianBlur(RADIUS/2))
	back.paste(blur, mask=mask)
	back.save(avatarFile)

def generateID(avatarFile, templateFile, displayName):
	#Position for avatar ==> X=152, Y=540
	fileName = "./final.jpg"

	blurEdgesAvatar(avatarFile)

	avatar = Image.open(avatarFile)
	background = Image.open(templateFile)

	#print(avatar.size, background.size, displayName)
	#Resize fro the avatar to fit in the photo area
	avatar = avatar.resize((328, 375), Image.NEAREST)
	a = avatar.copy()
	b = background.copy()
	b.paste(a, (150, 65))

	#Finally draw text at the bottom
	draw = ImageDraw.Draw(b) 
	fontText = ImageFont.truetype("./template/arial.ttf", 30)

	draw.text((152,540), displayName.upper(), (0, 0, 0, 255), font=fontText)
	draw.text((152,572), STREET, (0, 0, 0, 255), font=fontText)
	draw.text((152,604), LOCATION, (0, 0, 0, 255), font=fontText)

	#Save final image
	b.save(fileName, quality=95)
	#Return name of the file to load it later
	return fileName


client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('>mclovin'):
		#Generate Fake ID:
		#1º save image from user who's mentioned or just the author of the message 
		
		#Debug print to check length of mentions array
		#print(message.author.avatar_url)
		#print("L=> ", len(message.mentions))
		#print("C=> ", message.mentions)
		displayName = ""

		#Only one user is mentioned
		if message.mentions and len(message.mentions) == 1:
			await message.mentions[0].avatar_url.save("avatar.jpg")
			displayName = message.mentions[0].display_name
		#No mentions
		elif not message.mentions:
			await message.author.avatar_url.save("avatar.jpg")
			displayName = message.author.display_name
		#More than one mentions, not allowed for now 
		else:
			await message.channel.send("**Type >help, to see usage uwu.**")
			return
		
		#2º Call function to generate the final ID
		idFile = generateID("avatar.jpg", "./template/id-template.png", displayName)

		#3º Send the image 
		file = discord.File(fp=idFile)
		await message.channel.send("", file=file)

	if message.content.startswith('>help'):
		await message.reply("**Usage**:\n>mclovin " + "\n>mclovin @user" )


client.run('YOUR_TOKEN_HERE')