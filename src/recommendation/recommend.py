import pandas as pd # used to read and manipulate csv files
from sklearn.preprocessing import StandardScaler # used to normalize our data
from sklearn.metrics.pairwise import cosine_similarity # used for our distance metric

class Recommendation:
    def __init__(self, file_path="src/featurizer/test.csv"):
        self.file_path = file_path
        self.df = pd.read_csv(file_path) # Load the CSV file
        self.df_encoded = self.df.copy() # dont want to manipulate the OG dataset

        # want to convert major and minor (our non numerical data) into numerical data
        self.df_encoded['major'] = self.df_encoded['major'].astype('category').cat.codes
        self.df_encoded['minor'] = self.df_encoded['minor'].astype('category').cat.codes

        # grab all our feature columns i.e. rolloff1, rolloff2, centroid1, centroid2 ...
        self.feature_cols = [col for col in self.df_encoded.columns if col not in ['track_name']]
        
        # store our numerical data in 'features' (each song and its data for each column)
        self.features = self.df_encoded[self.feature_cols]

        # Normalize the data
        self.scaler = StandardScaler()
        self.features_scaled = self.scaler.fit_transform(self.features)

        # Compute the similarity matrix
        self.similarity_matrix = cosine_similarity(self.features_scaled)

        # Convert to DataFrame to allow for easier lookup, it turns the matrix back into a "csv" table like data visualization
        self.similarity_df = pd.DataFrame(self.similarity_matrix, index = self.df['track_name'], columns = self.df['track_name'])


    def get_similar_songs(self, reference_track, top_n=10):
        if reference_track not in self.similarity_df.index:
            return f"Track '{reference_track}' not found in dataset."
        
        # Get similarity scores and sort in descending order
        similar_tracks = self.similarity_df[reference_track].sort_values(ascending=False)
        
        # Exclude the reference track itself and get the top N results
        top_similar_tracks = similar_tracks.iloc[1:top_n+1]
        
        return top_similar_tracks


def main(reference_song):
    rec = Recommendation()
    our_recs = rec.get_similar_songs(reference_song)
    print(our_recs)

    # track_names = our_recs.index.to_numpy()
    # scores = our_recs.values
    # print(track_names)
    # print(scores)

if __name__ == "__main__":
    main("Serenata")
