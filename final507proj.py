import requests
import json
from bs4 import BeautifulSoup
import codecs
import sys
import sqlite3
import csv
from googlekey import gkey
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
import plotly.plotly as py
#import pandas as pd
import csv
########################################################################
CACHE_FNAME="507final.json"
try:
    fopen=open(CACHE_FNAME, "r")
    fread=fopen.read()
    CACHE_DICTION=json.loads(fread)
except:
    CACHE_DICTION={}
########################################################################
# pyear=''
# while pyear != 'exit':
# 	pyear=input('Please enter a year between 2003-2014:')

########################################################################
def get_aef_data(year):
	years=[(2003, 'u110'), (2004, 'u111'), (2005, 'u112'), (2006, 'u113'), (2007, 'u114'), (2008, 'u115'), (2009, 'u116'), (2010, 'u122'), (2011, 'u129'), (2012, 'u136'), (2013, 'u131'), (2014, 'u169')]
	for yr in years:
		if year in yr:
			base_url='http://archive.arce.org/expeditions/aefprojectsarchive/'+yr[1]
	uniq=base_url+str(year)
	if uniq in CACHE_DICTION:
		return CACHE_DICTION[uniq]
	else:
		resp = requests.get(base_url)
		CACHE_DICTION[uniq] = resp.text
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close()
		return CACHE_DICTION[uniq]
#j=get_aef_data(pyear)
#print(j)
########################################################################
def get_projname(year):
    a=get_aef_data(year)
    soup = BeautifulSoup(a, 'html.parser')
    ylst=[2003, 2004, 2005, 2006, 2007, 2008, 2009]
    if year in ylst:
    	e=soup.find('p')
    	g=e.text
    	h=str(g)
    	i=h.split('\n')
    	for thing in i:
    		if thing=='':
    			i.remove(thing)
    	return i
    if year==2010:
    	kk=soup.find(class_="block description")
    	jj=kk.find_all('p')
    	ee=kk.text
    	ff=str(ee)
    	hh=ff.split('\n')
    	for thing in hh:
    		if thing=='':
    			hh.remove(thing)
    	hh.remove(hh[1])
    	hh.remove(hh[0])
    	hh.remove(hh[-1])
    	for thin in hh:
    		if '\r' == thin:
    			hh.remove(thin)
    	return hh
    if year==2011:
    	kk=soup.find(class_="block description")
    	#jj=kk.find_all('p')
    	ee=kk.text
    	ff=str(ee)
    	hh=ff.split('\n')
    	for thing in hh:
    		if thing=='':
    			hh.remove(thing)
    		if '>>' in thing:
    			hh.remove(thing)
    		if thing=='\r':
    			hh.remove(thing)
    	
    	if 'ROUND' in hh[0]:
    		hh.remove(hh[0])
    	hh.remove(hh[2])
    	# for thing in hh:
    	# 	if '\r' in thing:
    	# 		thing.strip('\r')
    	tup1lst=[]
    	tup2lst=[]
    	tup3lst=[]
    	while len(hh)>0:
    		tup1lst.append(hh[0]+'/r')
    		tup1lst.append(hh[1]+'/t')
    		tup3lst.append(hh[2])
    		hh.remove(hh[0])
    		hh.remove(hh[0])
    		hh.remove(hh[0])
    	hh=tup1lst
    	#print(hh)
    	return hh
    if year==2014 or year==2013 or year==2012:
    	kk=soup.find(class_="block description")
    	#jj=kk.find_all('p')
    	ee=kk.text
    	ff=str(ee)
    	hh=ff.split('\n')
    	if 'ROUND' in hh[0]:
    		hh.remove(hh[0])
    	for thing in hh:
    		if thing=='':
    			hh.remove(thing)
    		if '>>' in thing:
    			hh.remove(thing)
    	#print(hh)
    	#print(ee)		
    	tup1lst=[]
    	tup2lst=[]
    	tup3lst=[]
    	while len(hh)>0:
    		tup1lst.append(hh[0]+'/r')
    		tup1lst.append(hh[1]+'/t')
    		tup3lst.append(hh[2])
    		hh.remove(hh[0])
    		hh.remove(hh[0])
    		hh.remove(hh[0])			
    	
    	hh=tup1lst
    	#print(hh)
    	return hh


#zz=get_projname(2014)
#print(zz)


def get_rounds(year):
	vv=[[2003, 1], [2004, 2], [2005, 3], [2006, 4], [2007, 5], [2008, 6], [2009, 7], [2010, 8], [2011, 9], [2012, 10], [2013, 11], [2014, 12]]
	return vv
    

    #print(i)
    #print(type(j))


#k=get_director(pyear)
#print(k)

########################################################################
dicttt={}
#yyyy=[2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
#yyyy=[2011]
yyyy=[2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
for yy in yyyy:
	j=get_aef_data(yy)
	z=get_projname(yy)
	k=get_rounds(yy)
	dicttt[yy]=z
tups=dicttt.items()
tups2=[]
for th in tups:
	tups2.append(th)


class AEFProject():
    def __init__(self, projname='', dir=''):
        self.projname= projname
        self.dir=dir
        

    def __str__(self):
        return 'Project: {}, Director: {}'.format(self.projname, self.dir)
#####################


DBNAME = 'arce.db'

def init_db(db_name):
    try:
        conn = sqlite3.connect('arce.db')
        cur = conn.cursor()
    except:
        print('Oh no! Connection failed.')

    statement = '''
        DROP TABLE IF EXISTS 'Rounds';
    '''
    statement2 = '''
        DROP TABLE IF EXISTS 'AEFProjects';
    '''
    cur.execute(statement)
    cur.execute(statement2)
    conn.commit()


    statement2='''
        CREATE TABLE 'Rounds'(
             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
              'Year' INTEGER,
              'RoundNumber' INTEGER
              )
     '''

    statement = '''
        CREATE TABLE 'AEFProjects'(
        	'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
             'Round' TEXT,
             'Year' TEXT,
             'Name' TEXT,
             'Director' TEXT,
             FOREIGN KEY ('Round') REFERENCES 'Rounds'(RoundNumber))
    '''
    
    cur.execute(statement2)
    cur.execute(statement)
    conn.commit()
    conn.close()

init_db(DBNAME)

# # # ########################################################################


def insert_proj_data(projlst):
    conn = sqlite3.connect('arce.db')
    cur = conn.cursor()

   
    for tup in tups2:
    	aa=tup[0]
    	for thin in tup[1]:
    		if aa==2009 and '\r' not in thin and '\t' not in thin:
    			abc=thin
    		if aa==2009 and '\r' in thin:
    			m=thin.strip('	')
    			j=m.split(',')
    			insertion = (None, None, aa, abc, j[0])
		    	statement = 'INSERT INTO "AEFProjects"'
		    	statement += 'VALUES (?, ?, ?, ?, ?)'
		    	cur.execute(statement, insertion)
    		if aa==2010 and '\r' not in thin and '\t' not in thin:
    			abc=thin
    		if aa==2010 and '\r' in thin:
    			m=thin.strip('	')
    			j=m.split(',')
    			insertion3 = (None, None, aa, abc, j[0])
		    	statement3 = 'INSERT INTO "AEFProjects"'
		    	statement3 += 'VALUES (?, ?, ?, ?, ?)'
		    	cur.execute(statement3, insertion3)
    		if aa!=2009 and aa!=2010 and aa!=2014 and aa!=2013 and aa!=2012 and aa!=2011 and '\r' in thin and '\t' not in thin:
    			abc=thin
    		if aa!=2009 and aa!=2010 and aa!=2014 and aa!=2013 and aa!=2012 and aa!=2011 and'\t' in thin:
    			m=thin.strip('	')
    			j=m.split(',')
    			if len(j)>1:
	    			insertion2 = (None, None, aa, abc, j[0])
			    	statement2 = 'INSERT INTO "AEFProjects"'
			    	statement2 += 'VALUES (?, ?, ?, ?, ?)'
		    		cur.execute(statement2, insertion2)
    		if aa==2014 and '/r' in thin or aa==2013 and '/r' in thin or aa==2012 and '/r' in thin or aa==2011 and '/r' in thin:
    			abc=thin.strip('/r')
    		if aa==2014 and '/t' in thin or aa==2013 and '/t' in thin or aa==2012 and '/t' in thin or aa==2011 and '/t' in thin:
    			m=thin.strip('	')
    			n=m.strip('/t')
    			ii=n.replace(':', ',')
    			j=ii.split(',')
    			insertion4 = (None, None, aa, abc, j[0])
		    	statement4 = 'INSERT INTO "AEFProjects"'
		    	statement4 += 'VALUES (?, ?, ?, ?, ?)'
	    		cur.execute(statement4, insertion4)	    		

		    	
    conn.commit()
    conn.close()

insert_proj_data(z)

#if len(j) > 1:


def insert_rounds(roundlst):
    conn = sqlite3.connect('arce.db')
    cur = conn.cursor()

    for x in roundlst:
        insertion = (None, x[0], x[1])
        statement = 'INSERT INTO "Rounds" '
        statement += 'VALUES (?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

insert_rounds(k)

conn = sqlite3.connect('arce.db')
cur = conn.cursor()
insert='UPDATE AEFProjects SET Round=(SELECT RoundNumber FROM Rounds WHERE AEFProjects.Year=Rounds.Year)'
cur.execute(insert)
conn.commit()
conn.close()

# # # ########################################################################

def institutions(year):
	# j=get_aef_data(year)
	ll=get_projname(year)
	# dicttt[yy]=z
	# tups=dicttt.items()
	# tups2=[]
	# for th in tups:
	# 	tups2.append(th)
	places=[]
	if year==2009:
		for thin in ll:
			if '\r' in thin:
				m=thin.strip('	')
				j=m.split(',')
				if len(j) > 1:
					if 'University' in j[1] and 'Cairo' not in j[1]:
						places.append(j[1])
					if 'Museum' in j[1]:
						places.append(j[1])

	else:
		for thin in ll:
			if '\t' in thin:
				m=thin.strip('	')
				j=m.split(',')
				if len(j) > 1:
					if 'University' in j[1] and 'Cairo' not in j[1] and 'California' not in j[1]:
						places.append(j[1])
					if 'California' in j[1] and not 'Egyptian':
						mm=j[1]+j[2]
						places.append(mm)
					if 'Museum' in j[1] and not 'British' and not 'Egyptian':
						places.append(j[1])
					
	#print(places)
	return places

#print(institutions(2006))

def plot_institutions(year):
	lat_vals = []
	lon_vals = []
	text_vals = []
	bb=institutions(year)
	for place in bb:
		base_url='https://maps.googleapis.com/maps/api/place/textsearch/json?'
		parameters={}
		parameters['query']=place
		parameters['key']= gkey
		uniq4=base_url+place
		if uniq4 in CACHE_DICTION:
			dic=json.loads(CACHE_DICTION[uniq4])
		else:
			resp = requests.get(base_url, parameters)
			CACHE_DICTION[uniq4] = resp.text
			dumped_json_cache = json.dumps(CACHE_DICTION)
			fw = open(CACHE_FNAME,"w")
			fw.write(dumped_json_cache)
			fw.close()
			dic=json.loads(CACHE_DICTION[uniq4])
		#print(dic)
		latitude=str(dic['results'][0]['geometry']['location']['lat'])
		longitude=str(dic['results'][0]['geometry']['location']['lng'])
		name=str(dic['results'][0]['name'])
		lat_vals.append(latitude)
		lon_vals.append(longitude)
		text_vals.append(name)
		#print(latitude)
		#print(longitude)
		#print(name)
	data = [ dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = lon_vals,
            lat = lat_vals,
            text = text_vals,
            mode = 'markers',
            marker = dict(
                size = 8,
                symbol = 'star',
            ))]
	min_lat = 10000
	max_lat = -10000
	min_lon = 10000
	max_lon = -10000

	for str_v in lat_vals:
		if str_v != 'None':
			v = float(str_v)
			if v < min_lat:
				min_lat = v
			if v > max_lat:
				max_lat = v
	for str_v in lon_vals:
		if str_v != 'None':
			v = float(str_v)
			if v < min_lon:
				min_lon = v
			if v > max_lon:
				max_lon = v


	center_lat = (max_lat+min_lat) / 2
	center_lon = (max_lon+min_lon) / 2

	max_range = max(abs(max_lat - min_lat), abs(max_lon - min_lon))
	padding = max_range * .10
	lat_axis = [min_lat - padding, max_lat + padding]
	lon_axis = [min_lon - padding, max_lon + padding]


	layout = dict(
	title = 'AEF Project Institutions<br>(Hover for institution names)',
	geo = dict(
	    scope='usa',
	    projection=dict( type='albers usa' ),
	    showland = True,
	    landcolor = "rgb(250, 250, 250)",
	    subunitcolor = "rgb(100, 217, 217)",
	    countrycolor = "rgb(217, 100, 217)",
	    lataxis = {'range': lat_axis},
	    lonaxis = {'range': lon_axis},
	    center= {'lat': center_lat, 'lon': center_lon },
	    countrywidth = 3,
	    subunitwidth = 3
	),
	)


	fig = dict(data=data, layout=layout )
	py.plot( fig, validate=False)

#print(plot_institutions(2005))

def interactive_prompt():
	response=''
	while response != 'exit':
	    response = input('Choose a featured year 2004, 2007, 2008, or 2009: ')
	    if response != 'exit':
	    	resp2=int(response)
	    	print(plot_institutions(resp2))
        
print(interactive_prompt())

# if __name__=="__main__":
#     interactive_prompt()








# conn = sqlite3.connect('arce.db')
# cur = conn.cursor()





# # ########################################################################

##################################
#DONT FORGET REQUIREMENTS.TXT
##################################



#irfanview..image to deskew, select, ctrl y, s, rename file names with P? 
#gv: crop margin 50, click 9 in, make sure background and deskew checked