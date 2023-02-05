from .query import Query
import psycopg2
from psycopg2 import Error

class fetch_query(Query):
	def run(self, *args):
		try:
			print("Trying...")
			connection = psycopg2.connect(self.credentials)
			print("Connected\n")
			cursor = connection.cursor()

			cursor.execute(self.query, args)

			results = cursor.fetchall()
			print(self.query_confirmation)

		except (Exception, psycopg2.Error) as error :
			print (self.query_error, error)
		finally:
			#closing database connection.
			if(connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")
				return(results)
