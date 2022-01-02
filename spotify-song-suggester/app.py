import re
import pandas as pd
from flask import Flask, render_template, request, redirect
from os import getenv
from mongoDB import Mongo
from predict import Predict

def create_app():
    app = Flask(__name__)
    
    app.secret_key = getenv('SECRET_KEY')
    
    PW = getenv('PW')
    URI = f'mongodb+srv://admin:{PW}@spotifydb.sfcpj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

    @app.route('/', methods=['GET', 'POST'])
    def root():
        return render_template('base.html')

    @app.route('/results', methods=['GET', 'POST'])
    def results():
        if request.method == 'POST':
            mongo = Mongo(URI)
            predict = Predict()

            songname = request.form.get('search')
            
            try: 
                song_data = mongo.find_one({'name': songname.lower()})
            except:
                return redirect('/')

            df = pd.DataFrame.from_dict(song_data, orient='index')

            X = df.drop(['name', 'artists', '_id', 'record_number'])

            X_scaled = predict.preprocess(X.T)
            X_PCA = predict.PCA(X_scaled)
            predictions = predict.predict(X_PCA)

            data = []
            songs = []

            for i in predictions[1:]:
                try:
                    data.append(mongo.find_one({'record_number': int(i)}))
                except:
                    return redirect('/')

            for i in data:
                songs.append(re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                lambda word: word.group(0).capitalize(),
                i['name']))
                songs.append(i['artists'])

        return render_template('results.html', songs=songs)

    @app.route('/about')
    def about():
        return render_template('about.html')
    
    return app
