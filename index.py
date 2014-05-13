#!/usr/bin/python
#Written by Robert Krossa and Stephen Grinich


import cgi
import cgitb
import psycopg2
import json

from datasource import DataSource
cgitb.enable()

form = cgi.FieldStorage()

def sanitizeUserInput(s):
    ''' Code from Jeff Ondich
    Removes all potentially dangerous characters that could be used to do malicous things to our databases/servers
    '''
    charsToRemove = ';,\\/:\'"<>@'
    for ch in charsToRemove:
        s = s.replace(ch, '')
    return s

def getCGIParameters():
	'''handles every possible parameter that is passed through url, puts them in a dictionary, and the returns the dictionary
	also has a list of which source files can be shown, and which can't be'''
	form = cgi.FieldStorage()
	parameters = {'swimmername':'', 'event':'','timerange':'','course':''}

	if 'swimmername' in form:
		parameters['swimmername'] = sanitizeUserInput(form['swimmername'].value)

	if 'event' in form:
		parameters['event'] = sanitizeUserInput(form['event'].value)

	if 'timerange' in form:
		parameters['timerange'] = sanitizeUserInput(form['timerange'].value)

	if 'course' in form:
		parameters['course'] = sanitizeUserInput(form['course'].value)


	sourceFilesWeAreWillingToShow = ('index.py', 'template.html','datasource.py','plot.js','readme.html','swimstyle.css')

	if 'showsource' in form:
		sourceFileToShow = sanitizeUserInput(form['showsource'].value)
		if sourceFileToShow not in sourceFilesWeAreWillingToShow:
			sourceFileToShow = ''
			parameters['showsource'] = sourceFileToShow
		else:
			parameters['showsource'] = sourceFileToShow

	return parameters

def printFileAsPlainText(fileName):
    ''' Prints to standard output the contents of the specified file, preceded
        by a "Content-type: text/plain" HTTP header.
        removes the password of DataSource.py and anyother password variables that start with  = ''
    try:
    	f = open(fileName)
    	text = f.read()
    	f.close()
    except Exception, e:
        pass
    if '_password' in text:
    	index = text.index('_password')
    	text1 = text[:index]
    	text2 = text[index+26:]
    	text = text1+text2

    print 'Content-type: text/plain\r\n\r\n',
    print text

def displayTimesInTable(times,dates):
	'''Used to display the times in a table format for exact times'''
	tableString ="<p>"
	tableString+= '<table border = "1"><tr><th>Times</th><th>Date</th></tr>'
	for x in range(len(times)):
		tableString+="<tr><td>%s</td><td>%s</td></tr>" % (times[x],dates[x])
	tableString += "</tr></table></p>"
	return tableString

def getTimesFromDatasource(name,event,course):
	'''Function used to get times from the database, and format them correctly
	Returns to lists as a tuple, the first a list of times, the second a list of dates
	if empty list is returned, then returns two empty lists 
	'''

	times = []
	day = []
	source = DataSource()
	allinfo = source.getTimes(name,event,course)
	if len(allinfo)<1:
		return [],[]
	times.extend(allinfo)
	day.extend(allinfo)
	for x in range(len(allinfo)):
		times[x] = allinfo[x][0]
		day[x] = allinfo[x][1]
		
	return times, day

def getNumFromTimes(times):
	''' A function used to convert strings that contain times into seconds, this makes the times more easily comparable and graphable'''
	newTimes = []
	for time in times:
		if 'r' in time:
			time = time.replace("r","")
		if ":" in time:
			newTime = time.replace(":","")
			newTime = float(newTime)
			newTime = getSecFromTime(newTime)
			newTime = '%0.2f' % newTime
			newTimes.append(newTime)

	return newTimes

def getGraphList(name,event,course):
	'''This graph creates a list of lists, in the format that jqplot uses, in order for easy graphing'''
	plotList = []
	source = DataSource()
	allinfo = source.getTimes(name,event,course)
	for x in range(len(allinfo)):
		if ':' in allinfo[x][0]:
			time = getNumFromTimes([allinfo[x][0]])[0]
			plotList.append([allinfo[x][1].isoformat(),time])
		else:
			plotList.append([allinfo[x][1].isoformat(),allinfo[x][0]])
	return plotList

def getSecFromTime(time):
	'''Used to convert minutes to seconds'''
	minutes = int(float(time))/100
	sec = float(time)%100
	totalsec = (minutes * 60) + sec
	return totalsec


def main():
	'''main function, reads in template, populates it with data, and prints it out'''
	#reading in template
	try:
		openTemplate = open('template.html')
		template = openTemplate.read()
		openTemplate.close()
	except Exception, e:
		pass
	#If show source variable is called, then calls function print as plain text, otherwise, starts filling out the template
	sourceFileToShow = ''
	parameters = getCGIParameters()
	if parameters.has_key('showsource'):
		sourceFileToShow = parameters['showsource']

	if sourceFileToShow:
		printFileAsPlainText(sourceFileToShow)
	else:
		print 'Content-type: text/html\r\n\r\n',

		if parameters['swimmername']:
			template = template % ('%s',parameters['swimmername'],"%s","%s")
		else:
			template = template % ('%s',"","%s","%s")
		if parameters['course'] == 'LCM': 
			template = template % ('%s',"","checked")
		else:
			template = template % ('%s',"checked","")		
		#gets times from datasource for table
		if(parameters['swimmername'] and parameters['event']):
			timesFromDataSource, dates = getTimesFromDatasource(parameters['swimmername'], parameters['event'], parameters['course'])
			#checking to make sure times exist, adds table to datasource if the do
			if len(timesFromDataSource) <1:
				template = template % ("No Events Listed under this name and event combination, please try again")
			else:
				template = template % ("")
				template += displayTimesInTable(timesFromDataSource,dates)
			#gets the list to create the graph
			graphList = getGraphList(parameters['swimmername'], parameters['event'], parameters['course']) 
			dataFile = open("data.txt","w")
			dataFile.write(json.dumps([graphList]))
			dataFile.close()
		#checks to make sure there arent anymore %s's that may have been missed, if so, it removes it.
		if '%s' in template:
			template = template % ('')
		print template

		

#calls function
if __name__ == '__main__':
	main()





