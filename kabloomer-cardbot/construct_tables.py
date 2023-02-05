import psycopg2
from psycopg2 import Error
from credentials import token, db_credentials

from tables.card import card_constructor, card_set, card_to_class, card_to_trait, card_to_tribe, card_type, card, cost_type, game_class, nickname, rarity, trait, tribe
from tables.deck import card_to_deck, deck
from tables.hero import hero_constructor, hero_to_card, hero_to_class, hero
from tables.request import request_type, request
from tables.tournament import tournament
from tables.elo import elo

from cardobject import cardObject
from constructorRows import card_constructor_rows, nicknameTuple, classTuple, setTuple, typeTuple, cost_typeTuple, rarityTuple, traitTuple, tribeTuple, heroTuple, requestTypeTuple

#Function names:
#createTable()
#dropTable()
#addToTable(record)
#addManyToTable(recordTuple)
#deleteFromTable(recordId)
#pullFromTable(recordId)
#pullidFromTable(recordValue)

def construct_request():
	request.dropTable()
	request.createTable()

def construct_request_type():
	request_type.dropTable()
	request_type.createTable()
	request_type.addManyToTable(requestTypeTuple)

def construct_card_tables():
	success = True

	card.dropTable()
	game_class.dropTable()
	card_set.dropTable()
	card_to_class.dropTable()
	card_to_trait.dropTable()
	card_to_tribe.dropTable()
	card_type.dropTable()
	card_constructor.dropTable()
	cost_type.dropTable()
	nickname.dropTable()
	rarity.dropTable()
	trait.dropTable()
	tribe.dropTable()

	card.createTable()
	game_class.createTable()
	card_set.createTable()
	card_to_class.createTable()
	card_to_trait.createTable()
	card_to_tribe.createTable()
	card_type.createTable()
	card_constructor.createTable()
	cost_type.createTable()
	nickname.createTable()
	rarity.createTable()
	trait.createTable()
	tribe.createTable()

	game_class.addManyToTable(classTuple)
	card_set.addManyToTable(setTuple)
	card_type.addManyToTable(typeTuple)
	card_constructor.addManyToTable(card_constructor_rows)
	cost_type.addManyToTable(cost_typeTuple)
	nickname.addManyToTable(nicknameTuple)
	rarity.addManyToTable(rarityTuple)
	trait.addManyToTable(traitTuple)
	tribe.addManyToTable(tribeTuple)


	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()
		# Print PostgreSQL Connection properties
		print(connection.get_dsn_parameters(),"\n")
		
		join_table_query = '''SELECT * FROM card_constructor'''

		cursor.execute(join_table_query)
		results = cursor.fetchall()


		"""print("Printing Table")
		print(results)
		for row in results:
			for col in row:
				print(col)"""

		for row in results:
			record_name = row[1]
			record_classes = row[2].split(", ")
			record_tribesandtype = row[3].split()
			record_cost = row[4]
			record_strength = row[5]
			record_health = row[6]
			record_traits = row[7].split(", ")
			record_ability = row[8]
			record_flavor = row[9]
			record_card_set = row[10]
			record_rarity = row[11]
			record_cost_type = row[12]
			record_card_type = record_tribesandtype[-1]
			record_tribes = record_tribesandtype[0:-1]

			setid = card_set.pullidFromTable(record_card_set) if record_card_set is not None else None
			rarityid = rarity.pullidFromTable(record_rarity)
			typeid = card_type.pullidFromTable(record_card_type)
			cost_typeid = cost_type.pullidFromTable(record_cost_type)

			card_record = (record_name, record_cost, record_strength, record_health, record_ability, record_flavor, setid, rarityid, cost_typeid, typeid)

			print("\n(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % card_record)
			card.addToTable(card_record)
			cardid = card.pullidFromTable(record_name)
			print("cardid: " + str(cardid))

			for record_class in record_classes:
				print("Record Class: %s" % record_class)
				classid = game_class.pullidFromTable(record_class)
				record_card_to_class = (cardid, classid)
				print("Record Tuple: %s" % str(record_card_to_class))
				card_to_class.addToTable(record_card_to_class)

			for record_trait in record_traits:
				if(len(record_trait) < 1):
					continue
				print("Record Trait: %s" % record_trait)
				traitid = trait.pullidFromTable(record_trait)
				record_card_to_trait = (cardid, traitid)
				print("Record Tuple: %s" % str(record_card_to_trait))
				card_to_trait.addToTable(record_card_to_trait)

			for record_tribe in record_tribes:
				if(len(record_tribe) < 1):
					continue
				print("Record Tribe: %s" % record_tribe)
				tribeid = tribe.pullidFromTable(record_tribe)
				record_card_to_tribe = (cardid, tribeid)
				print("Record Tuple: %s" % str(record_card_to_tribe))
				card_to_tribe.addToTable(record_card_to_tribe)



		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error working with card_constructor in PostgreSQL", error)
		success = False
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed. Card should be built." if success else "Something went wrong while creating card")
			return(", you have regenerated the database." if success else ", something went wrong while creating card")


def construct_hero_tables():

	hero.dropTable()
	hero_constructor.dropTable()
	hero_to_class.dropTable()
	hero_to_card.dropTable()

	hero.createTable()
	hero_constructor.createTable()
	hero_to_class.createTable()
	hero_to_card.createTable()

	hero_constructor.addManyToTable(heroTuple)

	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()
		# Print PostgreSQL Connection properties
		print(connection.get_dsn_parameters(),"\n")
		
		join_table_query = '''SELECT * FROM hero_constructor'''

		cursor.execute(join_table_query)
		results = cursor.fetchall()


		print("Printing Table")
		print(results)
		for row in results:
			print(row)

		for row in results:
			record_name = row[1]
			record_abbreviation = row[2]
			record_classes = row[3].split(", ")
			record_supers = row[4].split(", ")
			record_flavor = row[5]
			record_side = row[6]

			hero_record = (record_name, record_abbreviation, record_flavor, record_side)
			print("\nHero Record: (%s,%s,%s, %s)" % hero_record)
			hero.addToTable(hero_record)
			heroid = hero.pullidFromTable(record_name)

			for record_class in record_classes:
				print("Record Class: %s" % record_class)
				classid = game_class.pullidFromTable(record_class)
				record_hero_to_class = (heroid, classid)
				print("Record Tuple: %s" % str(record_hero_to_class))
				hero_to_class.addToTable(record_hero_to_class)

			for herosuper in record_supers:
				print("Hero Super: %s" % herosuper)
				superid = card.pullidFromTable(herosuper)
				record_hero_to_card = (heroid, superid)
				print("Record Tuple: %s" % str(record_hero_to_card))
				hero_to_card.addToTable(record_hero_to_card)

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error working with hero_constructor in PostgreSQL", error)
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed. Hero should be built.")

def construct_tournament():
	tournament.dropTable()
	tournament.createTable()

def construct_nickname():
	nickname.dropTable()
	nickname.createTable()
	nickname.addManyToTable(nicknameTuple)

def construct_elo():
	elo.dropTable()
	elo.createTable()