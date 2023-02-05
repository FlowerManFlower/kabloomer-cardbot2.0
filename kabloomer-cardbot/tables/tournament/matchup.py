import psycopg2
from psycopg2 import Error
from credentials import token, db_credentials

def createTable():
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		create_table_query = '''CREATE TABLE matchup
								(id SERIAL PRIMARY KEY,
								first_participant_id int,
								second_participant_id int,
								tournament_id int,
								winner_id int DEFAULT NULL,
								confirmed boolean DEFAULT 'f'
								);'''
		
		cursor.execute(create_table_query)
		connection.commit()
		print("Table \"matchup\" Addition Successful!")

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error creating matchup in PostgreSQL", error)
	finally:
		#closing database connection.
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")

def dropTable():
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		delete_table_query = '''DROP TABLE matchup'''

		cursor.execute(delete_table_query)
		connection.commit()
		print("Table \"matchup\" Deletion Successful!")

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error removing matchup from PostgreSQL", error)
	finally:
		#closing database connection.
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")


#Adding to database
def addToTable(record):
	try:
		connection = psycopg2.connect(db_credentials)
		cursor = connection.cursor()

		postgres_insert_query = """INSERT INTO matchup(first_participant_id, second_participant_id, winner_id, confirmed) VALUES %s"""
		cursor.execute(postgres_insert_query, (record,))

		connection.commit()
		print("Row added to \"matchup\"")

	except (Exception, psycopg2.Error) as error :
		print ("Error adding row to matchup in PostgreSQL", error)
	finally:
		#closing database connection.
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")

def addManyToTable(recordTuple):
	try:
		connection = psycopg2.connect(db_credentials)
		cursor = connection.cursor()

		args_str = ','.join(cursor.mogrify("(%s)", x).decode("utf-8") for x in recordTuple)
		print(args_str)
		cursor.execute("INSERT INTO matchup(first_participant_id, second_participant_id, winner_id, confirmed) VALUES " + args_str)

		connection.commit()
		print("Multiple rows added to \"matchup\"")


	except (Exception, psycopg2.Error) as error :
		print ("Error adding rows to matchup in PostgreSQL", error)
	finally:
		#closing database connection.
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")


def deleteFromTable(recordId):
	try:
		connection = psycopg2.connect(db_credentials)
		cursor = connection.cursor()

		postgres_delete_query = """ Delete from matchup where id = %s"""
		cursor.execute(postgres_delete_query, (recordId, ))
		connection.commit()
		print("Row deleted from \"matchup\"")


	except (Exception, psycopg2.Error) as error :
		print ("Error deleting from matchup in PostgreSQL", error)
	finally:
		#closing database connection.
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")

def pullFromTable(recordId):
	try:
		connection = psycopg2.connect(db_credentials)
		cursor = connection.cursor()

		postgres_pull_query = """ SELECT * from matchup where id = %s"""
		cursor.execute(postgres_delete_query, (recordId, ))
		results = cursor.fetchall()
		print("Results from \"matchup\" where id = %s" % (recordId))
		for row in results:
			for col in row:
				print(col, end='')
			print('')

	except (Exception, psycopg2.Error) as error :
		print ("Error pulling from matchup in PostgreSQL", error)
	finally:
		#closing database connection.
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")


def pullidFromTable(recordValue):
	try:
		connection = psycopg2.connect(db_credentials)
		cursor = connection.cursor()
		results = []
		postgres_pull_query = """
		SELECT id
		FROM matchup
		WHERE first_participant_id = %s"""

		cursor.execute(postgres_pull_query, (recordValue,))
		results = cursor.fetchall()
		result = None
		try:
			result = results[0][0]
		except:
			result = None

	except (Exception, psycopg2.Error) as error :
		print ("Error pulling id from matchup in PostgreSQL", error)
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			#print("PostgreSQL connection is closed")
		return(result)
