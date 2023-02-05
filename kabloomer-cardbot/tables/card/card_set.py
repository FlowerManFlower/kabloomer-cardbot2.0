import psycopg2
from psycopg2 import Error
from credentials import token, db_credentials

def createTable():
	try:
		print("Trying")
		connection = psycopg2.connect(db_credentials)
		print("connected")
		cursor = connection.cursor()

		create_table_query = '''CREATE TABLE card_set
								(id SERIAL PRIMARY KEY,
								name varchar(16));'''

		cursor.execute(create_table_query)
		connection.commit()
		print("Table \"card_set\" Addition Successful!")

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error adding card_set in PostgreSQL", error)
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

		delete_table_query = '''DROP TABLE card_set'''

		cursor.execute(delete_table_query)
		connection.commit()
		print("Table \"card_set\" Deletion Successful!")

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error removing card_set from PostgreSQL", error)
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

		postgres_insert_query = """ INSERT INTO card_set(name) VALUES (%s)"""
		cursor.execute(postgres_insert_query, (record))

		connection.commit()
		print("Row added to table \"card_set\"")


	except (Exception, psycopg2.Error) as error :
		print ("Error adding to card_set in PostgreSQL", error)
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
		cursor.execute("INSERT INTO card_set(name) VALUES " + args_str)

		connection.commit()
		print("Multiple rows added to \"card_set\"")

	except (Exception, psycopg2.Error) as error :
		print ("Error adding many to card_set in PostgreSQL", error)
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

		postgres_delete_query = """ Delete from card_set where id = %s"""
		cursor.execute(postgres_delete_query, (recordId, ))
		connection.commit()
		print("Row deleted from \"card_set\"")
		
	except (Exception, psycopg2.Error) as error :
		print ("Error deleting from card_set in PostgreSQL", error)
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

		postgres_pull_query = """ SELECT * from card_set where id = %s"""
		cursor.execute(postgres_delete_query, (recordId, ))
		results = cursor.fetchall()
		print("Results from \"card_set\" where id = %s" % (recordId))
		for row in results:
			for col in row:
				print(col, end='')
			print('')

	except (Exception, psycopg2.Error) as error :
		print ("Error pulling from card_set in PostgreSQL", error)
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
		postgres_pull_query = """ SELECT id from card_set where name = %s"""
		cursor.execute(postgres_pull_query, (recordValue,))
		results = cursor.fetchall()
		result = None
		try:
			result = results[0][0]
		except:
			result = None

	except (Exception, psycopg2.Error) as error :
		print ("Error checking card_set in PostgreSQL", error)
	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			#print("PostgreSQL connection is closed")
		return(result)
