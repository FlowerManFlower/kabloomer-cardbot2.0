import psycopg2
from psycopg2 import Error
from credentials import token, db_credentials

def createTable():
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		create_table_query = '''CREATE TABLE game_class
								(id SERIAL PRIMARY KEY,
								name varchar(64));'''

		cursor.execute(create_table_query)
		connection.commit()
		print("Table \"game_class\" Addition Successful!")

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error adding game_class to PostgreSQL", error)
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

		delete_table_query = '''DROP TABLE game_class'''

		cursor.execute(delete_table_query)
		connection.commit()
		print("Table \"game_class\" Deletion Successful!")

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error removing game_class from PostgreSQL", error)
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
		postgres_insert_query = """ INSERT INTO game_class(name) VALUES (%s)"""
		cursor.execute(postgres_insert_query, (record))

		connection.commit()
		print("Row added to \"game_class\"")

	except (Exception, psycopg2.Error) as error :
		print ("Error adding to game_class in PostgreSQL", error)
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
		cursor.execute("INSERT INTO game_class(name) VALUES " + args_str)

		connection.commit()
		print("Multiple rows added to \"game_class\"")

	except (Exception, psycopg2.Error) as error :
		print ("Error adding many to game_class in PostgreSQL", error)
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
		postgres_delete_query = """ Delete from game_class where id = %s"""
		cursor.execute(postgres_delete_query, (recordId, ))
		connection.commit()
		print("Row deleted from \"game_class\"")

	except (Exception, psycopg2.Error) as error :
		print ("Error deleting from game_class in PostgreSQL", error)
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

		postgres_pull_query = """ SELECT * from game_class where id = %s"""
		cursor.execute(postgres_delete_query, (recordId, ))
		results = cursor.fetchall()
		print("Results from \"game_class\" where id = %s" % (recordId))
		for row in results:
			for col in row:
				print(col, end='')
			print('')

	except (Exception, psycopg2.Error) as error :
		print ("Error pulling from game_class in PostgreSQL", error)
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
		FROM game_class
		ORDER BY SIMILARITY(name, %s)DESC
		LIMIT 1 """

		cursor.execute(postgres_pull_query, (recordValue,))
		results = cursor.fetchall()
		print("Results: " + str(results))
		result = None
		try:
			result = results[0][0]
		except:
			result = None

	except (Exception, psycopg2.Error) as error :
		print ("Error checking game_class in PostgreSQL", error)
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			#print("PostgreSQL connection is closed")
		return(result)
