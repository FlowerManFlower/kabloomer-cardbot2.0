import psycopg2
from psycopg2 import Error
from credentials import token, db_credentials

def createTable():
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		create_table_query = '''CREATE TABLE card_type
								(id SERIAL PRIMARY KEY,
								type varchar(16));'''

		cursor.execute(create_table_query)
		connection.commit()
		print("Table \"card_type\" Addition Successful!")

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error adding table to PostgreSQL", error)
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

		delete_table_query = 'DROP TABLE card_type'

		cursor.execute(delete_table_query)
		connection.commit()
		print("Table \"card_type\" Deletion Successful!")

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error removing table from PostgreSQL", error)
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

		postgres_insert_query = """ INSERT INTO card_type(type) VALUES (%s)"""
		cursor.execute(postgres_insert_query, (record))

		connection.commit()
		print("Row added to table \"card_type\"")

	except (Exception, psycopg2.Error) as error :
		print ("Error checking table in PostgreSQL", error)
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
		cursor.execute("INSERT INTO card_type(type) VALUES " + args_str)

		connection.commit()
		print("Multiple rows added to \"cardtypr\"")

	except (Exception, psycopg2.Error) as error :
		print ("Error checking table in PostgreSQL", error)
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

		postgres_delete_query = """ Delete from card_type where id = %s"""
		cursor.execute(postgres_delete_query, (recordId, ))
		connection.commit()
		print("Row deleted from \"card_type\"")
		
	except (Exception, psycopg2.Error) as error :
		print ("Error checking table in PostgreSQL", error)
	finally:
		#closing database connection.
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")

def pullFromTable(column, identifier):
	try:
		connection = psycopg2.connect(db_credentials)
		cursor = connection.cursor()

		postgres_pull_query = """ SELECT * from card_type where id = %s"""
		cursor.execute(postgres_delete_query, (recordId, ))
		results = cursor.fetchall()
		print("Results from \"card_type\" where id = %s" % (recordId))
		for row in results:
			for col in row:
				print(col, end='')
			print('')

	except (Exception, psycopg2.Error) as error :
		print ("Error checking table in PostgreSQL", error)
	finally:
		#closing database connection.
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")


def pullColumnFromTable(pullColumn, identifier, identifyingValue):
	try:
		connection = psycopg2.connect(db_credentials)
		cursor = connection.cursor()

		postgres_pull_query = """ SELECT * from card where id = %s"""
		cursor.execute(postgres_delete_query, (recordId, ))
		results = cursor.fetchall()
		print("Results from \"card\" where id = %s" % (recordId))
		for row in results:
			for col in row:
				print(col, end='')
			print('')

	except (Exception, psycopg2.Error) as error :
		print ("Error checking table in PostgreSQL", error)
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
		postgres_pull_query = """ SELECT id from card_type where type = %s"""
		cursor.execute(postgres_pull_query, (recordValue,))
		results = cursor.fetchall()
		result = None
		try:
			result = results[0][0]
		except:
			result = None

	except (Exception, psycopg2.Error) as error :
		print ("Error checking table in PostgreSQL", error)
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			#print("PostgreSQL connection is closed")
		return(result)
