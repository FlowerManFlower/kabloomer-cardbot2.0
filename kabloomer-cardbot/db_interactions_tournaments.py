import psycopg2
from psycopg2 import Error
from credentials import token, db_credentials
from cardobject import cardObject
from heroobject import heroObject

#Participant Functions
def registerParticipant(discordName, timezoneid):
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_insert_query = '''
		INSERT INTO participant(discord_username, timezone_id)
		VALUES (%s,%s)
		'''

		cursor.execute(postgres_insert_query, (discordName, timezoneid))
		connection.commit()
		print("Participant logged in \"participant\"")

		postgres_select_query = '''
		SELECT discord_username, timezone_id
		FROM participant
		WHERE discord_username = %s
		'''

		cursor.execute(postgres_select_query, (discordName,))

		registration_info = cursor.fetchall()[0]
		print(registration_info)

		postgres_select_query = '''
		SELECT abbreviation, utc_offset
		FROM timezone
		WHERE id = %s
		'''

		cursor.execute(postgres_select_query, (registration_info[1],))

		timezone_info = cursor.fetchall()[0]

	except (Exception, psycopg2.Error) as error :
		print("Error registering participant with cardbot,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return("%s, you registered in the timezone %s, which has a UTC offset of %s" % (registration_info[0], timezone_info[0], timezone_info[1]))

def isRegistered(discordName):
	is_registered_and_id = []
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_select_query = '''
		SELECT id FROM participant
		WHERE discord_username = %s
		'''

		cursor.execute(postgres_select_query, (discordName,))

		results = cursor.fetchall()

		if(len(results) > 0):
			is_registered_and_id = [True, results[0][0]]
			print("Participant is already registered in \"participant\"")
		else:
			print("Participant is not registered in \"participant\"")

	except (Exception, psycopg2.Error) as error :
		is_registered_and_id = [False, results[0][0]]
		print("Error chacking if participant is registered,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(is_registered_and_id)

def deRegister(discordName):
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_delete_query = '''
		DELETE FROM participant
		WHERE discord_username = %s
		'''

		cursor.execute(postgres_delete_query, (discordName,))
		connection.commit()

		print("Participant removed from \"participant\"")

	except (Exception, psycopg2.Error) as error :
		print("Error deregistering participant,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")

def getTimezoneId(timezone_abbreviation):
	return_timezone_id = 0
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_select_query = '''
		SELECT id from timezone
		ORDER BY SIMILARITY(LOWER(abbreviation), LOWER(%s)) DESC
		LIMIT 1
		'''

		cursor.execute(postgres_select_query, (timezone_abbreviation,))
		connection.commit()
		results = cursor.fetchall()

		print("Timezone id: %s" % (results))
		return_timezone_id = results[0][0]

	except (Exception, psycopg2.Error) as error :
		return_timezone_id = 0
		print("Error obtaining timezone id,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(return_timezone_id)

def createTournament(tournament_name, number_of_bans, require_ign, creator_name):
	success = True
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_insert_query = '''
		INSERT INTO tournament(name, number_of_bans, require_ign, creator)
		VALUES (%s,%s,%s,%s)
		'''

		cursor.execute(postgres_insert_query, (tournament_name, number_of_bans, require_ign, creator_name))
		connection.commit()
		print("Tournament '%s' created" % (tournament_name))

	except (Exception, psycopg2.Error) as error :
		success = False
		print("Error creating tournament,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(success)

def verifyTournament(tournament_name):
	success = True
	id_and_bans = []
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		select_table_query = '''
		SELECT id, number_of_bans, require_ign, creator, has_started
		FROM tournament
		WHERE SIMILARITY(LOWER(name), LOWER(%s)) > 0.5
		LIMIT 1'''

		cursor.execute(select_table_query, (tournament_name,))
		results = cursor.fetchall()

		print(results)

		if(len(results) > 0):
			id_and_bans = [results[0][0], results[0][1], results[0][2], results[0][3], results[0][4]]
			print("A tournament with id %s exists" % (id_and_bans[0]))
		else:
			success = False

	except (Exception, psycopg2.Error) as error :
		success = False
		print("Error verifiying tournament,", error)
	finally:
		#closing database connection
		id_and_bans.insert(0, success)
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(id_and_bans)

def hasJoined(participant_id, tournament_id):
	already_joined = True
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		select_table_query = '''
		SELECT id
		FROM participant_to_tournament
		WHERE participantid = %s
		AND tournamentid = %s
		'''

		cursor.execute(select_table_query, (participant_id, tournament_id))
		results = cursor.fetchall()

		print(results)

		if(len(results) > 0):
			print("Participant is already in the tournament")
		else:
			already_joined = False


	except (Exception, psycopg2.Error) as error :
		already_joined = False
		print("Error checking if participant has joined tournament,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(already_joined)

def joinTournament(participant_id, tournament_id):
	returnid = 0
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_insert_query = '''
		INSERT INTO participant_to_tournament(participantid, tournamentid)
		VALUES (%s,%s)
		'''

		cursor.execute(postgres_insert_query, (participant_id, tournament_id))
		connection.commit()

		postgres_select_query = '''
		SELECT id
		FROM participant_to_tournament
		WHERE participantid = %s
		'''

		cursor.execute(postgres_select_query, (participant_id,))

		returnid = cursor.fetchall()[0][0]

		print("Participant added to tournament")

	except (Exception, psycopg2.Error) as error :
		print("Error joining tournament,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(returnid)

def joinBan(part_to_tournament_id, hero_id):
	returnid = 0
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_insert_query = '''
		INSERT INTO tournament_participant_to_bans(tournament_to_participant_id, hero_id)
		VALUES (%s,%s)
		'''

		cursor.execute(postgres_insert_query, (part_to_tournament_id, hero_id))
		connection.commit()

		print("Participant added to tournament")

	except (Exception, psycopg2.Error) as error :
		print("Error adding ban,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")

def joinIGN(part_to_tournament_id, ign):
	returnid = 0
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_insert_query = '''
		INSERT INTO tournament_participant_to_ign(tournament_to_participant_id, ign)
		VALUES (%s,%s)
		'''

		cursor.execute(postgres_insert_query, (part_to_tournament_id, ign))
		connection.commit()

		print("Participant added to tournament")

	except (Exception, psycopg2.Error) as error :
		print("Error adding ign,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")

def getParticipants(tournament_id):
	return_info = []
	participant_ids = []
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		select_table_query = '''
		SELECT participantid
		FROM participant_to_tournament
		WHERE tournamentid = %s
		'''

		cursor.execute(select_table_query, (tournament_id,))
		results = cursor.fetchall()
		print(results)
		for row in results:
			for col in row:
				participant_ids.append(col)

		for participant_id in participant_ids:
			select_table_query = '''
			SELECT participant.id,
				   participant.discord_username,
				   timezone.abbreviation
			FROM participant
			LEFT JOIN timezone on participant.timezone_id = timezone.id
			WHERE participant.id = %s
			'''

			cursor.execute(select_table_query, (participant_id,))
			return_info.append(cursor.fetchall()[0])
		print(return_info)

	except (Exception, psycopg2.Error) as error :
		print("Error getting list of participants,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(return_info)

def createMatchup(first_participant_info, second_participant_info, tournament_id):
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_insert_query = '''
		INSERT INTO matchup(first_participant_id, second_participant_id, tournament_id)
		VALUES (%s,%s,%s)
		'''

		cursor.execute(postgres_insert_query, (first_participant_info[0], second_participant_info[0], tournament_id))
		connection.commit()
		print("Matchup created between participant ids %s and %s" % (first_participant_info[0], second_participant_info[0]))

	except (Exception, psycopg2.Error) as error :
		print("Error creating matchup,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return("%s will play %s" % (first_participant_info[1], second_participant_info[1]))

def getParticipantInfo(participant_name_or_id, tournament_id):
	return_info = []
	participant_ids = []
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		try:
			int(participant_name_or_id)
			print("Participant info is an integer")
			select_table_query = '''
			SELECT participant.id,
				   participant.discord_username,
				   timezone.abbreviation,
				   participant_to_tournament.in_game,
				   participant_to_tournament.num_of_wins,
				   participant_to_tournament.num_of_losses,
				   participant_to_tournament.eliminated
			FROM participant
			LEFT JOIN timezone on participant.timezone_id = timezone.id
			LEFT JOIN participant_to_tournament on participant.id = participant_to_tournament.participantid
			WHERE participant.id = %s
			AND participant_to_tournament.tournamentid = %s
			'''

			cursor.execute(select_table_query, (int(participant_name_or_id), tournament_id))
			print(cursor.fetchall())
			for row in cursor.fetchall():
				for col in row:
					return_info.apppend(col)

		except:
			print("Participant info is a string")
			select_table_query = '''
			SELECT participant.id,
				   participant.discord_username,
				   timezone.abbreviation,
				   participant_to_tournament.in_game,
				   participant_to_tournament.num_of_wins,
				   participant_to_tournament.num_of_losses,
				   participant_to_tournament.eliminated
			FROM participant
			LEFT JOIN timezone on participant.timezone_id = timezone.id
			LEFT JOIN participant_to_tournament on participant.id = participant_to_tournament.participantid
			WHERE participant.discord_username = %s
			AND participant_to_tournament.tournamentid = %s
			'''

			cursor.execute(select_table_query, (participant_name_or_id, tournament_id))
			print(cursor.fetchall())
			for row in cursor.fetchall():
				for col in row:
					return_info.apppend(col)

		print("Return info is: %s" % (return_info))

	except (Exception, psycopg2.Error) as error :
		print("Error getting participant info,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
			return(return_info)

def startTournament(tournament_id):
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_update_query = '''
		UPDATE tournament
		SET has_started = 't'
		WHERE id = %s
		'''

		cursor.execute(postgres_update_query, (tournament_id,))
		connection.commit()

		print("Tournament started successfully")

	except (Exception, psycopg2.Error) as error :
		print("Error starting tournament,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")

def reportWin(participant_id, tournament_id):
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		postgres_update_query = '''
		UPDATE matchup
		SET winner_id = %s
		WHERE tournament_id = %s
		AND confirmed = 'f'
		AND (first_participant_id = %s OR second_participant_id = %s)
		'''

		cursor.execute(postgres_update_query, (participant_id, tournament_id, participant_id, participant_id))
		connection.commit()

		print("Win reported")

	except (Exception, psycopg2.Error) as error :
		print("Error reporting win,", error)
	finally:
		#closing database connection
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
