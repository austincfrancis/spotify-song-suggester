import json, csv
from mongoDB import Mongo
from os import getenv 
from alive_progress import alive_bar

PASS = getenv('PASS')

URI = f"mongodb+srv://admin:{PASS}@spotifydb.sfcpj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

mongo = Mongo(URI)

csvf = open('../data.csv', encoding='utf-8')
csvReader = csv.DictReader(csvf)

with alive_bar(171223, bar='classic2', spinner='classic') as bar:
    for i, row in enumerate(csvReader):
        row["name"] = row["name"].lower()
        mongo.insert_one({"_id": row["id"], "acousticness": row["acousticness"], "artists": row["artists"], "danceability": row["danceability"], "energy": row["energy"], "explicit": row["explicit"], "instrumentalness": row["instrumentalness"], "key": row["key"], "liveness": row["liveness"], "loudness": row["loudness"], "mode": row["mode"], "name": row["name"], "popularity": row["popularity"], "speechiness": row["speechiness"], "tempo": row["tempo"], "valence": row["valence"], "year": row["year"], "duration_min": row["duration_min"], "record_number": i})
        bar()

