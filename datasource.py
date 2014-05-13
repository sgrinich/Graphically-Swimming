#Written by Stephen Grinich and Robert Krossa

import psycopg2
import cgi
import cgitb

cgitb.enable()



class DataSource: 
	def __init__(self):
		pass
	def getTimes(self, name,event, course):

		# Start with the database login info
	    database = 'grinichs'
	    user = 'grinichs'

	    # Login to the database
	    try:
	    	connection = psycopg2.connect(database=database, user=user, password=_password)
	    except Exception, e:
	    	print 'Connection error: ', e
	    	exit()
	    #Finds the id number of the name in the nameids table
	    try:
	    	cursor = connection.cursor()
	    	query = "SELECT id FROM nameids WHERE name=(%s)" 
	    	cursor.execute(query,(name,))
	    except Exception, e:
	    	print 'Cursor error', e
	    # Fetches the ID number
	    try:
	    	nameid = cursor.fetchall()
	    	nameid = nameid[0]
	    except Exception,e:
	    	return []
	    # Query the database and print out its results.
	    try:
	    	cursor = connection.cursor()
	    	query = "SELECT time, day FROM times WHERE event=(%s) AND nameid=(%s) AND course=(%s) ORDER BY day DESC" 
	    	cursor.execute(query,(event,nameid,course))
	    except Exception, e:
	    	#print 'Cursor error', e
	    	pass

	    # We have a cursor now. Use it to return a table of results.
	    # If there is an error in fetching a.k.a no times possible for the provided search, then returns empty list, index.py knows that this means unsuccesful search
	    try:
	    	return cursor.fetchall() 
	    except Exception,e:
	    	return []



	

