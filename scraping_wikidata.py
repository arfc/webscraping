import requests

header = {

	'yukun tan': 'wikidata scraping'
}
import pandas as pd
import sqlite3

# query from wikidata, followed the tutorial

query = '''
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX v: <http://www.wikidata.org/prop/statement/>
PREFIX q: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?reactors ?reactorsLabel ?coord
WHERE {
    ?reactors wdt:P31 wd:Q80877 .
    ?reactors wdt:P625 ?coord .
    ?reactors rdfs:label ?reactorsLabel filter (lang(?reactorsLabel) = "en")
}
'''
url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, headers=header, params={'query': query, 'format': 'json'}).json()

#data manipulation with pandas
re = []

for item in data ['results']['bindings']:
	re.append({
		'Name' : item['reactorsLabel']['value'],
		'Coord' : item['coord']['value']
	})
df = pd.DataFrame(re)

df.head()
# this function effectively get rid of the "Point()" part in the
# original Coord obj

def extractCoord(dfcol):
	for i in range(len(dfcol)):
		dfcol[i] = dfcol[i][6:-1]
	return
extractCoord(df['Coord'])

Long = []
Lat = []

# this function takes in a pandas df col with type string obj
# it seperates thte string with delimiter whitespace
# hold the 2 seperated strings using lists Long and Lat

def seperateCoord(dfcol, Long, Lat):
	for i in range(len(dfcol)):
		dfcol[i] = dfcol[i].split()
		Long.append(dfcol[i][0])
		Lat.append(dfcol[i][1])
	return
seperateCoord(df['Coord'], Long, Lat)
# typecast from string to float
Long = [float(i) for i in Long]
Lat = [float(i) for i in Lat]

df['Long'] = Long
df['Lat'] = Lat
#print(df['Long'].dtypes)

#need to reorder the columns after I have all the cols

# now put it into the sqlite database
def into_sql(df):
    sqlite_file = 'test.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS testTable;')
# THIS IS NOT WORKING "probably unsupported type"
    sql = '''
    CREATE TABLE testTable(
        'index', 'Name' TEXT, 'Coord' TEXT, 'Long' REAL, 'Lat' REAL
    )
    '''

    c.execute(sql)
    df.to_sql(name = 'testTable', con = conn, if_exists = 'append', index = True)

    conn.close()
    return

#into_sql(df)
