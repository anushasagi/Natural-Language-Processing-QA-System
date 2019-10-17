import sqlite3

rows = tuple ()

def movie_database(query):
	conn = sqlite3.connect('oscar-movie_imdb.sqlite')
	cur = conn.cursor()
	print ("Opened database successfully")
	try:
		cur.execute(query)
		rows = cur.fetchall()
	except:
		rows = ('I do not know',)
	
	print ("Operation done successfully")
	print (rows)
	conn.close()

	return rows

def music_database(query):
	conn = sqlite3.connect('music.sqlite')
	cur = conn.cursor()
	print ("Opened database successfully")
	try:
		cur.execute(query)
		rows = cur.fetchall()
	except:
		rows = ('I do not know',)
	
	print ("Operation done successfully")
	print (rows)
	conn.close()

	return rows

def geography_database(query):
	conn = sqlite3.connect('WorldGeography.sqlite')
	cur = conn.cursor()
	print ("Opened database successfully")
	try:
		cur.execute(query)
		rows = cur.fetchall()
		print("success")
	except:
		rows = ('I do not know',)
		print("Fail")
	
	print ("Operation done successfully")
	print (rows)
	conn.close()

	return rows

def get_movie_names():
	conn = sqlite3.connect('oscar-movie_imdb.sqlite')
	cur = conn.cursor()
	print ("Opened database successfully")

	cur.execute("select name from Movie")
	rows = cur.fetchall()

	print ("Operation done successfully")
	conn.close()

	return rows

def get_album_names():
	conn = sqlite3.connect('music.sqlite')
	cur = conn.cursor()
	print ("Opened database successfully")

	cur.execute("select name from Album")
	rows = cur.fetchall()

	print ("Operation done successfully")
	conn.close()

	return rows

def get_track_names():
	conn = sqlite3.connect('music.sqlite')
	cur = conn.cursor()
	print ("Opened database successfully")

	cur.execute("select name from Track")
	rows = cur.fetchall()

	print ("Operation done successfully")
	conn.close()

	return rows
