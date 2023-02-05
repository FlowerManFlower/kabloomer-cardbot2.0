import psycopg2
from psycopg2 import Error
from credentials import db_credentials

class Query:
	def __init__(self, query_string, query_confirmation, query_error):
		self.query = query_string
		self.query_confirmation = query_confirmation
		self.query_error = query_error
		self.credentials = db_credentials
