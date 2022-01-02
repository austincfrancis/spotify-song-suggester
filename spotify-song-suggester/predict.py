import pickle

class Predict:
    def __init__(self):
        self.pca = pickle.load(open('../pca.pkl', 'rb'))
        self.nn = pickle.load(open('../nearest_neighbors.pkl', 'rb'))
        self.scaler = pickle.load(open('../min_max_scaler.pkl', 'rb'))

    def preprocess(self, X):
        '''
        Use 'MinMaxScaler' to prep data for PCA

        Args:
            X (object)
        Returns:
            X_scaled (object)
        '''

        X_scaled = self.scaler.transform(X)

        return X_scaled


    def PCA(self, X_scaled):
        '''
        Use PCA for dimensionality reduction

        Args:
            X_scaled (object)
        Returns:
            X_reduced (object)
        '''

        X_reduced = self.pca.transform(X_scaled)

        return X_reduced


    def predict(self, vect):
        '''
        Use k-Nearest Neighbors to predict 10 similar songs

        Args:
            vect (list) of song features
        Returns:
            indices (list) of top 10 similar songs
        '''

        distance, indices = self.nn.kneighbors(vect)

        return indices[0]
