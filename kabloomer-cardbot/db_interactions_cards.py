import psycopg2
from psycopg2 import Error
from credentials import token, db_credentials
from cardobject import cardObject
from heroobject import heroObject
from classes.fetch_query import fetch_query

#Function names:
#createTable()
#dropTable()
#addToTable(record)
#addManyToTable(recordTuple)
#deleteFromTable(recordId)
#pullFromTable(recordId)
#pullColumnFromTable(pullColumn, identifier, identifyingValue)

#log request function
def logRequest(requestAuthor, requestString, requestType, fuzzyRequest):
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		if(len(requestString) < 513):
			postgres_insert_query = '''
			INSERT INTO request(author, message, typeid, is_fuzzy)
			VALUES (%s,%s,%s,%s)
			'''
			cursor.execute(postgres_insert_query, (requestAuthor, requestString, requestType, fuzzyRequest))
			connection.commit()
			print("Request logged in \"request\"")
		else:
			raise ValueError('request message was too long to store')

	except (Exception, psycopg2.Error) as error :
		print ("Error logging request in request,", error)
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")


def getBestCardMatchId(recordName):
	name_query = fetch_query('''SELECT name
		FROM nickname
		WHERE SIMILARITY(nickname, %s) > 0.25
		OR LOWER(nickname) LIKE LOWER(%s)
		ORDER BY SIMILARITY(nickname, %s) DESC,
		LOWER(nickname) LIKE LOWER(%s) DESC
		LIMIT 1''', "Retrieved Card information", "Error retrieving Card information,")

	try:
		recordStart = recordName[0:3] + '%'
	except:
		recordStart = recordName[0:] + '%'

	orString = '%'
	for word in recordName.split():
		orString += word + '%'
	orString += '%'

	name_tuple = name_query.run(recordName, orString, recordName, recordStart)

	if len(name_tuple) > 0:
		result_name = name_tuple[0][0]

		id_query = fetch_query('''
		SELECT id
		FROM card
		where name = %s''', "Retrieved Card id", "Error retrieving Card id,")

		results = id_query.run(result_name)[0][0]
	else:
		results = None

	return results


def pullCardRecord(recordName):
	card_id = getBestCardMatchId(recordName)
	print("Result id: " + str(card_id))

	if(card_id is None):
		return("There are no matches. Start your message with -fuzzy for close matches or -help to get a list of commands.")

	card_query = fetch_query('''
	SELECT	card.name,
			game_class.name,
			tribe.name,
			card_type.type,
			card.cost,
			cost_type.cost_type,
			card.strength,
			trait.strengthmodifier,
			card.health,
			trait.healthmodifier,
			trait.name,
			card.ability,
			card.flavor,
			card_set.name,
			rarity.name
	FROM card
	LEFT JOIN card_to_class ON card.id = card_to_class.cardid
	LEFT JOIN game_class ON card_to_class.classid = game_class.id
	LEFT JOIN card_to_trait ON card_to_trait.cardid = card.id
	LEFT JOIN trait ON card_to_trait.traitid = trait.id
	LEFT JOIN card_to_tribe ON card.id = card_to_tribe.cardid
	LEFT JOIN tribe ON card_to_tribe.tribeid = tribe.id
	LEFT JOIN card_type ON card_type.id = card.typeid
	LEFT JOIN card_set ON card_set.id = card.setid
	LEFT JOIN rarity ON card.rarityid = rarity.id
	LEFT JOIN cost_type ON card.cost_typeid = cost_type.id
	WHERE card.id = %s''', "Retrieved Card information", "Error retrieving Card information,")

	results = card_query.run(card_id)

	cardInstance = cardObject(results)
	print(cardInstance.information())

	return(cardInstance.information())


def getBestHeroMatchId(recordName):
	name_query = fetch_query('''
		SELECT id, SIMILARITY(name, %s)
		FROM hero
		ORDER BY SIMILARITY(name, %s) DESC
		LIMIT 1''', "Retrieved Hero name", "Error retrieving Hero name,")

	name_results = name_query.run(recordName, recordName)

	abbreviation_query = fetch_query('''
		SELECT id, SIMILARITY(abbreviation, %s)
		FROM hero
		ORDER BY SIMILARITY(abbreviation, %s) DESC
		LIMIT 1''', "Retrieved Hero abbreviation", "Error retrieving Hero abbreviation,")

	abbreviation_results = abbreviation_query.run(recordName, recordName)

	if(name_results[0][1] > abbreviation_results[0][1]):
		hero_id = name_results[0][0]
	else:
		hero_id = abbreviation_results[0][0]

	return(hero_id)


def pullHeroRecord(recordName):
	hero_id = getBestHeroMatchId(recordName)
	print("Hero id: " + str(hero_id))

	hero_query = fetch_query('''
		SELECT	hero.name,
				hero.abbreviation,
				hero_class.name AS hero_class,
				card.name,
				game_class.name,
				card.ability,
				hero.flavor
		FROM hero
		LEFT JOIN hero_to_class ON hero.id = hero_to_class.heroid
		LEFT JOIN game_class AS hero_class ON hero_to_class.classid = hero_class.id
		LEFT JOIN hero_to_card ON hero.id = hero_to_card.heroid
		LEFT JOIN card ON hero_to_card.cardid = card.id
		LEFT JOIN card_to_class ON card.id = card_to_class.cardid
		LEFT JOIN game_class ON card_to_class.classid = game_class.id
		WHERE hero.id = %s''', "Retrieved Hero information", "Error retrieving Hero information,")

	results = hero_query.run(hero_id)

	heroInstance = heroObject(results)
	print(heroInstance.information())

	return(heroInstance.information())


def pullFuzzyCardRecord(recordName):
	returnString = "Here are the closest matches:"

	name_query = fetch_query('''
	SELECT name
	FROM nickname
	ORDER BY SIMILARITY(nickname, %s) DESC,
	LOWER(nickname) LIKE %s DESC
	LIMIT 5''', "Retrieved Card names", "Error retrieving Card names,")

	try:
		recordStart = recordName[0:3].lower() + '%'
	except:
		recordStart = recordName[0:].lower() + '%'

	results = name_query.run(recordName, recordStart)

	for row in results:
		for col in row:
			returnString += "\n" + col

	return(returnString)


def pullFuzzyHeroRecord(recordName):
	returnString = "Here are the closest matches:"

	name_query = fetch_query('''
	SELECT name, abbreviation
	FROM hero
	ORDER BY SIMILARITY(name, %s) DESC,
	SIMILARITY(abbreviation, %s) DESC
	LIMIT 5''', "Retrieved Hero names", "Error retrieving Hero names,")

	results = name_query.run(recordName, recordName)

	for row in results:
		returnString += "\n" + row[0] + " (" + row[1] + ")"

	return(returnString)
	
def registerStrength(discord_name, strength):
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_insert_query = '''
		INSERT INTO strengths(discord_name, strength)
		VALUES (%s,%s)
		'''

		cursor.execute(postgres_insert_query, (discord_name, strength))
		connection.commit()
		print("Strength %s registered for %s" % (strength, discord_name))

	except (Exception, psycopg2.Error) as error :
		print("Error creating matchup,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return("Strength %s registered for %s" % (strength, discord_name))

def displayBrand(discord_name):
	returnString = ""
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_insert_query = '''
		SELECT strength
		FROM strengths
		WHERE discord_name = %s
		'''

		cursor.execute(postgres_insert_query, (discord_name,))
		results = cursor.fetchall()
		for row in results:
			for col in row:
				returnString += col + "\n"


	except (Exception, psycopg2.Error) as error :
		print("Error creating matchup,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(returnString)