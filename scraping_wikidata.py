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

re = []
for item in data ['results']['bindings']:
	re.append({
		'Name' : item['reactorsLabel']['value'],
		'Coord' : item['coord']['value'],
		#'Lat' : item['coord']['value'][1]
	})
df = pd.DataFrame(re)
print(len(df))
df.head()

# now put it into the sqlite database

sqlite_file = 'test.sqlite'   
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS testTable;')

sql = '''
CREATE TABLE testTable(
	'index', 'Name' OBJECT, 'Coord' OBJECT
)
'''

c.execute(sql)
df.to_sql(name = 'testTable', con = conn, if_exists = 'append', index = True)

conn.close()