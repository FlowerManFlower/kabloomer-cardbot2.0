

"""Importing modules required to make bot function.
Dicord is for the functions and API connection while 
re is to obtain the reg ex module needed to extract
strings within [[]] brackets"""


from random import randrange
import discord
import re as regex
import psycopg2
import math

from timer import Countdown


from db_interactions_cards import pullCardRecord, pullHeroRecord, logRequest, pullFuzzyCardRecord, pullFuzzyHeroRecord, getBestHeroMatchId, registerStrength, displayBrand
from db_interactions_tournaments import createTournament, verifyTournament, registerParticipant, getTimezoneId, isRegistered, deRegister, joinTournament, hasJoined, joinBan, joinIGN, getParticipants, createMatchup, getParticipantInfo, startTournament
from construct_tables import construct_card_tables, construct_hero_tables, construct_nickname, construct_request, construct_request_type, construct_tournament, construct_elo
from credentials import token
from tempcode import handyman

from elo import calculateResults, applyResults, getElo, getLeaderboard, resetElo

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bot_spam_channel_id = 929032787523154001
cardbot_bugs_report_channel_id = 930534933083070534
chombler_id = 578801522800853002
bot_id = 950895961658519612
verified_id = 928930794108493834
mod_id = 994822965915025479

pvzh_chat_channel_id = 929032768170635315
card_ideas_channel_id = 929032774298521662
deck_help_channel_id = 929032769370198026

debug_channels = [bot_spam_channel_id, cardbot_bugs_report_channel_id]

slow_mode_channels = [pvzh_chat_channel_id, card_ideas_channel_id, deck_help_channel_id]

pvzh_timer = Countdown()
card_ideas_timer= Countdown()
deck_help_timer = Countdown()

channel_timers = [pvzh_timer, card_ideas_timer, deck_help_timer]

IS_FUZZY = True
IS_NOT_FUZZY = False


help_message = discord.Embed(
    title="<:Surprise_Box:1043602667882172548> Bot Commands:",
    description="<:discord_bulletin:993756222878650429> **Use** `[[Card Name]]` to return a specific card's information. __More than one card can be requested at one time.__\n\n<:discord_bulletin:993756222878650429> **Use** `{{Hero Name}}` to return a specific Hero's information. More than one Hero can be requested at one time.\n\n<:discord_bulletin:993756222878650429> **Use** `-fuzzy` **at the start of a card or Hero call to return a list of closest matches instead of a specific result.**\n\n<:discord_bulletin:993756222878650429> **Use** `-help-elo` to get a list of **__elo commands__**",
    color=discord.Color.blue()
)



elo_help_message = discord.Embed(
    title="<:PepeSword:991101661902807181> Elo Bot Commands:",
    description="<:discord_bulletin:993756222878650429> Use **-elo** `@winner` `@loser` to report the outcome of a set.\n\n<:discord_bulletin:993756222878650429> When you do this, the bot will reply with a message **asking the loser to __confirm__ the report.**\n\n<:discord_bulletin:993756222878650429> The loser must **react** to the message using <:Verify:1070632429322248212> in order to __**confirm**__ the results.\n\n<:discord_bulletin:993756222878650429> Use `-elo-score` to view your current **elo score.**\n",
    color=discord.Color.red()
)

async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	"""if message.author == client.user:
		return"""
	if(message.author.bot or message.content.startswith('-ignore')):
		pass
	else:
		message_author = ""
		try:
			message_author = message.author.nickname
		except:
			message_author = message.author.name

		database_was_regenerated = await checkForRegeneration(message)
		if(database_was_regenerated):
			return

		elif(message.content.startswith('-help-elo')):
			await message.channel.send(embed=elo_help_message)

		elif(message.content.startswith('-elo-score')):
    			score = getElo(message.author.name, message.author.id)
    			embed = discord.Embed(title="Elo Score", description="Your Elo Score is %s" % score, color=0xff0000)
    			await message.channel.send(embed=embed, delete_after=60)

		elif message.content.startswith("-elo-leaderboard"):
			leaderboard = getLeaderboard()
			embed = discord.Embed(
				title="<:List:990718262536966194> Score Leaderboard",
				description=">>> " + leaderboard,
				color=discord.Color.red()
			)
			await message.channel.send(embed=embed)


		elif(message.content.startswith('-elo-reset') and (message.author.id == chombler_id or mod_id in [role.id for role in message.author.roles])):
			winner = resetElo()
			await message.channel.send(f"ELO has been reset. This season's winner is <@{winner[1]}> with a score of {winner[0]}")

		elif(message.content.startswith('-elo-force') and message.author.id == chombler_id):
			names_mentioned = [mention.name for mention in message.mentions]
			ids_mentioned = [mention.id for mention in message.mentions]
			results = applyResults(names_mentioned[0], ids_mentioned[0], names_mentioned[1], ids_mentioned[1])
			await message.channel.send(content = f"-confirmed\
												\nWinner: [{names_mentioned[0]}] ({results[0]} -> {results[1]})\
												\nLoser:  [{names_mentioned[1]}] ({results[2]} -> {results[3]})")

		elif(message.content.startswith('-elo')):
			if verified_id in [role.id for role in message.author.roles] or message.author.id == chombler_id:
				names_mentioned = [mention.name for mention in message.mentions]
				ids_mentioned = [mention.id for mention in message.mentions]
				print("Names mentioned: %s\nIDs mentioned: %s" % (names_mentioned, ids_mentioned))
				other_name = [name for name in names_mentioned if name != message.author.name]
				other_id = [disc_id for disc_id in ids_mentioned if disc_id != message.author.id]
				if(len(names_mentioned) == 2):
					results = calculateResults(names_mentioned[0], ids_mentioned[0], names_mentioned[1], ids_mentioned[1])
					await message.channel.send(content = f"-unconfirmed\
												\nWinner: [{names_mentioned[0]}] ||@{ids_mentioned[0]}||({results[0]} -> {results[1]})\
												\nLoser:  [{names_mentioned[1]}] ||@{ids_mentioned[1]}||({results[2]} -> {results[3]})\
												\nReported By: {message.author.name}\
												\n<@{other_id[0]}> **must react with ✅ to confirm these results**",
												delete_after = 120)
				else:
					await message.channel.send("You need exactly two people in order to report a match", delete_after = 60)
			else:
				await message.channel.send("You must be verified in order to report matches", delete_after = 60)

		elif(message.content.startswith('-help')):
			logRequest(message.author.name, message.content, 3, None)
			await message.channel.send(embed=help_message)

		elif(message.content.startswith('-fuzzy')):
			await fuzzySearch(message)

		else:
			await regularSearch(message)

@client.event
async def on_reaction_add(reaction, user):
	confirmer_id = [mention.id for mention in reaction.message.mentions]
	message_is_unconfirmed = reaction.message.content.startswith('-unconfirmed')
	message_author_is_cardbot = reaction.message.author.id == bot_id

	if(message_is_unconfirmed and message_author_is_cardbot and reaction.emoji == '✅' and (user.id == confirmer_id[0] or user.id == chombler_id)):
		ids_mentioned = regex.findall('\|\|\@(.+?)\|\|', reaction.message.content)
		winner_name = regex.findall('Winner\: \[(.+?)\]', reaction.message.content)[0]
		loser_name = regex.findall('Loser\:  \[(.+?)\]', reaction.message.content)[0]
		winner_id = ids_mentioned[0]
		loser_id = ids_mentioned[1]
		results = applyResults(winner_name, winner_id, loser_name, loser_id)
		await reaction.message.edit(content = f"-confirmed\
											\nWinner: [{winner_name}] ({results[0]} -> {results[1]})\
											\nLoser:  [{loser_name}] ({results[2]} -> {results[3]})")

async def regularSearch(message):
    if '{{' and '}}' in message.content:
        stringInput = regex.findall('\{\{(.+?)\}\}', message.content)
        print("Terms input for search are: %s" % (stringInput))
        for text in stringInput:
            logRequest(message.author.name, message.content, 2, IS_NOT_FUZZY)
            response = pullHeroRecord(text)
            response = response.replace("|", "・")
            try:
                if(message.channel.id in slow_mode_channels):
                    print("This is a slow mode channel")
                    index = slow_mode_channels.index(message.channel.id)
                    if(channel_timers[index].isFinished()):
                        channel_timers[index].start(30)
                    else:
                        await message.channel.send("Sorry, cardbot still has %s seconds left on its cooldown" % (channel_timers[index].timeRemaining()))
                        return
                embed = discord.Embed(title="<:Info_Icon_PvZH:999559619301097532> Search Result", description=">>> " + response, color=0x0000ff)
                if(message.channel.id in debug_channels):
                    embed.add_field(name="||Record generated in response to command:||", value=f"||{{{{{text}}}}}||")
                await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title="<:Info_Icon_PvZH:999559619301097532> Search Result", description=">>> " + response, color=0x0000ff)
                await message.channel.send(embed=embed)

    if '[[' and ']]' in message.content:
        stringInput = regex.findall('\[\[(.+?)\]\]', message.content)
        print("Terms input for search are: %s" % (stringInput))
        for text in stringInput:
            logRequest(message.author.name, message.content, 1, IS_NOT_FUZZY)
            response = pullCardRecord(text)
            response = response.replace("|", "・")
			
            try:
                if(message.channel.id in slow_mode_channels):
                    print("This is a slow mode channel")
                    index = slow_mode_channels.index(message.channel.id)
                    if(channel_timers[index].isFinished()):
                        channel_timers[index].start(30)
                    else:
                        await message.channel.send("Sorry, cardbot still has %s seconds left on its cooldown" % (channel_timers[index].timeRemaining()), delete_after = channel_timers[index].timeRemaining())
                        return
                embed = discord.Embed(title="<:Info_Icon_PvZH:999559619301097532> Search Result", description=">>> " + response, color=0x0000ff)
                if(message.channel.id in debug_channels):
                    embed.add_field(name="||Record generated in response to command:||", value=f"||\[\[{text}\]\]||")
                await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title="<:Info_Icon_PvZH:999559619301097532> Search Result", description=">>> " + response, color=0x0000ff)
                await message.channel.send(embed=embed)



async def fuzzySearch(message):
	if '{{' and '}}' in message.content:
		stringInput = regex.findall('\{\{(.+?)\}\}', message.content)
		print(stringInput)
		for text in stringInput:
			logRequest(message.author.name, message.content, 2, IS_FUZZY)
			response = pullFuzzyHeroRecord(text)
			try:
				print("Channel name: %s" % (message.channel.name))
				print("Channel id: %s" % (message.channel.id))
				embed = discord.Embed(color=0x1E90FF)
				embed.add_field(name="<:Info_Icon_PvZH:999559619301097532> Search Result", value=">>> " + response)
				if(message.channel.id == bot_spam_channel_id or message.channel.id == cardbot_bugs_report_channel_id):
					embed.add_field(name="||Generated in response to command||", value="||{{%s}}||" % (text))
					await message.channel.send(embed=embed)
				else:
					await message.channel.send(embed=embed)
			except:
				await message.channel.send(embed=embed)

	if '[[' and ']]' in message.content:
		stringInput = regex.findall('\[\[(.+?)\]\]', message.content)
		print(stringInput)
		for text in stringInput:
			logRequest(message.author.name, message.content, 1, IS_FUZZY)
			response = pullFuzzyCardRecord(text)
			try:
				print("Channel name: %s" % (message.channel.name))
				print("Channel id: %s" % (message.channel.id))
				embed = discord.Embed(color=0x1E90FF)
				embed.add_field(name="<:Info_Icon_PvZH:999559619301097532> Search Result", value=">>> " + response)
				if(message.channel.id == bot_spam_channel_id or message.channel.id == cardbot_bugs_report_channel_id):
					embed.add_field(name="||Generated in response to command||", value="||[[%s]]||" % (text))
					await message.channel.send(embed=embed)
				else:
					await message.channel.send(embed=embed)
			except:
				await message.channel.send(embed=embed)

async def checkForRegeneration(message):
	if(message.author.name == "FlowerMan"):
		if message.content.startswith("$truehandyman"):
			await message.channel.send("FlowerMan " + handyman(True))
			return True

		elif message.content.startswith("$handyman"):
			await message.channel.send("FlowerMan " + handyman(False))
			return True

		if message.content.startswith('$[[Regenerate Database]]'):
			await message.channel.send("FlowerMan " + construct_card_tables())
			return True

		elif message.content.startswith("$[[Regenerate Nickname]]"):
			construct_nickname()
			await message.channel.send("FlowerMan, you have regenerated nickname.")
			return True

		elif message.content.startswith("$[[Regenerate Hero]]"):
			construct_hero_tables()
			await message.channel.send("FlowerMan, you have regenerated hero.")
			return True

		elif message.content.startswith("$[[Regenerate Request]]"):
			construct_request()
			await message.channel.send("FlowerMan, you have regenerated request.")
			return True

		elif message.content.startswith("$[[Regenerate Request Type]]"):
			construct_request_type()
			await message.channel.send("FlowerMan, you have regenerated request_type.")
			return True

		elif message.content.startswith("$[[Regenerate Tournament]]"):
			construct_tournament()
			await message.channel.send("FlowerMan, you have regenerated tournament.")
			return True
		
		elif message.content.startswith("$[[Regenerate Elo]]"):
			construct_elo()
			await message.channel.send("FlowerMan, you have regenerated Elo.")
			return True
	return False


client.run(token)

