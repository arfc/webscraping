import requests
import pandas as pd
import sqlite3

header = {

    'yukun tan': 'wikidata scraping'
}

# query from wikidata, followed the tutorial

# REMEMBER TO FIX THE "COUNTRY" ISSUE (MISSING REACTORS)
# WAIT IT SEEMS THAT IT'S FIXED....? CHECK LATER

query_reactors = '''
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX v: <http://www.wikidata.org/prop/statement/>
PREFIX q: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?reactors ?reactorsLabel ?coord ?countryLabel
WHERE {
    ?reactors wdt:P31 wd:Q80877 .
    ?reactors wdt:P625 ?coord .
    ?reactors wdt:P17 ?country .
    ?reactors rdfs:label ?reactorsLabel filter (lang(?reactorsLabel) = "en")
    ?country rdfs:label ?countryLabel filter (lang(?countryLabel) = "en")
}
'''
url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data_reactors = requests.get(url, headers=header,
                             params={'query': query_reactors,
                                     'format': 'json'}).json()

query_plants = '''
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX v: <http://www.wikidata.org/prop/statement/>
PREFIX q: <http://www.wikidata.org/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?reactors ?reactorsLabel ?coord ?countryLabel
WHERE {
    ?reactors wdt:P31 wd:Q134447 .
    ?reactors wdt:P625 ?coord .
    ?reactors wdt:P17 ?country .
    ?reactors rdfs:label ?reactorsLabel filter (lang(?reactorsLabel) = "en")
    ?country rdfs:label ?countryLabel filter (lang(?countryLabel) = "en")
}
'''
url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data_plants = requests.get(url, headers=header,
                           params={'query': query_plants,
                                   'format': 'json'}).json()


def set_up_df(data):
    re = []
    for item in data['results']['bindings']:
        re.append({
            'Name': item['reactorsLabel']['value'],
            'Coord': item['coord']['value'],
            'Country': item['countryLabel']['value']
        })
    df = pd.DataFrame(re)
    return df


def extractCoord(df):
    """this function takes in a pandas df col
    it substrings every element of the col 'Coord'
    from the 6th to 2nd last character
    """
    dfcol = df['Coord']
    for i in range(len(dfcol)):
        dfcol[i] = dfcol[i][6:-1]
    return df


def seperateCoord(dfcol):
    """this function takes in a pandas df col with type string obj
    it seperates thte string with delimiter whitespace
    hold the 2 seperated strings using lists Long and Lat
    """
    lon = []
    lat = []
    for i in range(len(dfcol)):
        dfcol[i] = dfcol[i].split()
        lon.append(dfcol[i][0])
        lat.append(dfcol[i][1])
    return lon, lat


def into_sql(df):
    sqlite_file = 'test.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS testTable;')
    # THIS IS NOT WORKING "probably unsupported type"
    sql = '''
    CREATE TABLE testTable(
        'index', 'Name' TEXT, 'Long' REAL, 'Lat' REAL, 'Country' TEXT
    )
    '''
    c.execute(sql)
    df.to_sql(name='testTable',
              con=conn,
              if_exists='append',
              index=True)

    conn.close()
    return


def set_up_and_modify_df(data):
    df = set_up_df(data)
    df = extractCoord(df)
    lon, lat = seperateCoord(df['Coord'])
    df.drop('Coord', axis=1, inplace=True)
    # typecast from string to float
    df['Long'] = [float(i) for i in lon]
    df['Lat'] = [float(i) for i in lat]
    return df


df_reactors = set_up_and_modify_df(data_reactors)
df_plants = set_up_and_modify_df(data_plants)
df_whole = df_reactors.append(df_plants, ignore_index=True)

into_sql(df_whole)
