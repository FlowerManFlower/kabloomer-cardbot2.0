import psycopg2
from psycopg2 import Error
from credentials import token, db_credentials
from classes.fetch_query import fetch_query

def getElo(name, discord_id):
	elo_query = fetch_query('''
			SELECT score, name
			FROM elo
			WHERE discord_id = %s''', "Elo score obtained", "Error retrieving score from elo,")

	results = elo_query.run(discord_id)
	if(len(results) > 0):
		elo = results[0][0]
		if(results[0][1] != name):
			updateElo(name, discord_id, elo)
	else:
		createRow(name, discord_id)
		elo = 1000

	return elo


def createRow(name, discord_id):
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		insert_query = '''
		INSERT INTO elo(name, discord_id, score)
		VALUES (%s, %s, 1000)
		'''

		cursor.execute(insert_query, (name, discord_id))
		connection.commit()
		print("New Player added to elo")

	except (Exception, psycopg2.Error) as error :
		print ("Error creating new row in ELO,", error)
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")

def updateElo(name, discord_id, score):
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		update_query = '''
		UPDATE elo
		SET score = %s, 
			name = %s
		WHERE discord_id = %s
		'''

		cursor.execute(update_query, (score, name, discord_id))
		connection.commit()
		print("Elo updated")

	except (Exception, psycopg2.Error) as error :
		print ("Error updating ELO,", error)
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")

def getLeaderboard():
	elo_query = fetch_query('''
		SELECT score, name
		FROM elo
		ORDER BY score DESC
		LIMIT 10''', "ELO leaderboard obtained", "Error retrieving leaderboard from elo")

	results = elo_query.run()
	print(results)
	return_string = "__ELO__ | __Name__"

	for row in range(len(results)):
		return_string += "\n%-5s %s" % (results[row][0], results[row][1])

	return return_string

def resetElo():
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		select_query = '''
		SELECT score, discord_id
		FROM elo
		ORDER BY score DESC
		LIMIT 1'''

		cursor.execute(select_query)

		results = cursor.fetchall()[0]
		print(results)

		delete_query = '''DELETE FROM elo'''

		cursor.execute(delete_query)
		connection.commit()

	except (Exception, psycopg2.Error) as error :
		print ("Error resetting ELO,", error)
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(results)

def calculateResults(winner, winner_id, loser, loser_id):
	start_winner_elo = getElo(winner, winner_id)
	start_loser_elo = getElo(loser, loser_id)

	winner_expected = 1 / (1 + pow(10, (start_loser_elo - start_winner_elo) / 400))
	loser_expected = 1 / (1 + pow(10, (start_winner_elo - start_loser_elo) / 400))

	final_winner_elo = round(start_winner_elo + 30 * (1 - winner_expected))
	final_loser_elo = round(start_loser_elo + 30 * (0 - loser_expected))

	return([start_winner_elo, final_winner_elo, start_loser_elo, final_loser_elo])

def applyResults(winner, winner_id, loser, loser_id):
	results = calculateResults(winner, winner_id, loser, loser_id)
	updateElo(winner, winner_id, results[1])
	updateElo(loser, loser_id, results[3])
	return(results)

