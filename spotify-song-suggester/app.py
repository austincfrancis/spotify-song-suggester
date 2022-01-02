import pandas as pd
from flask import Flask, render_template, request, redirect
from os import getenv
from mongoDB import Mongo
from predict import Predict

def create_app():
    app = Flask(__name__)
    
    PW = getenv('PW')
    URI = f'mongodb+srv://admin:{PW}@spotifydb.sfcpj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

    @app.route('/')
    def root():
        return render_template('base.html')

    @app.route('/results', methods=['POST'])
    def results():
        if request.method == 'POST':
            mongo = Mongo(URI)
            predict = Predict()

            songname = request.form.get('search')

            song_data = mongo.find_one({'name': songname}) 

            df = pd.DataFrame.from_dict(song_data, orient='index')

            X = df.drop(['name', 'artists', '_id', 'record_number'])

            X_scaled = predict.preprocess(X.T)
            X_PCA = predict.PCA(X_scaled)
            predictions = predict.predict(X_PCA)

            data = []
            songs = []

            for i in predictions:
                data.append(mongo.find_one({'record_number': int(i)}))

            for i in data:
                songs.append(i['name'])

        return render_template('results.html', songs=songs)
    
    return app
