# %%
import pandas as pd
import numpy as np
import scipy as sp
import pickle
from scipy import sparse
from collections import Counter
from sklearn.preprocessing import MinMaxScaler

from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# %%
df = pd.read_csv('data/cosine.csv')
df.columns
tfidf_vectorizer = TfidfVectorizer()
text_data_about = df['About the game'].astype(str)
text_data_genre = df['Genres'].astype(str)
text_data_categories = df['Categories'].astype(str)
text_data_developers = df['Developers'].astype(str)
text_data_title = df['Name'].astype(str)
text_data = text_data_about + ' ' + text_data_genre + ' ' + text_data_developers + ' ' +  text_data_categories + ' ' + text_data_title
tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)
similarity_matrix = cosine_similarity(tfidf_matrix,tfidf_matrix)

#load our old 
# tfidf_matrix = sparse.load_npz("data/tfidf_matrix.npz")
# similarity_matrix = np.load("data/similarity_matrix.npy")
# with open("data/tf_vectorizer.pk1", 'rb') as file:
#     tfidf_vectorizer = pickle.load(file)
# %%
def CosineGameRecommended(gamename:str, recommended_games:int=5,tfidf_vectorizer=tfidf_vectorizer, similarity_matrix=similarity_matrix,tfidf_matrix=tfidf_matrix, df_reset=df):
    # Combine text data from 'About the game' and 'Genres'
    text_data_combined = df_reset['About the game'].astype(str) + ' ' + df_reset['Genres'].astype(str) + ' ' + df_reset['Categories'].astype(str)  + ' ' + df_reset['Developers'].astype(str)  + ' ' + df_reset['Name'].astype(str) 

    # Transform the combined text data into a TF-IDF vector
    game_tfidf_vector = tfidf_vectorizer.transform([text_data_combined[df_reset['Name'] == gamename].values[0]])

    # Calculate cosine similarity for the given game vector
    similarity_scores = cosine_similarity(game_tfidf_vector, tfidf_matrix).flatten()

    # Get the indices of games with the highest similarity scores
    top_indices = np.argsort(similarity_scores)[-recommended_games-1:-1][::-1]

    # Retrieve corresponding games using the reset index
    top_games = df_reset.loc[top_indices, 'Name'].tolist()

    return pd.DataFrame(top_games)

# %%


# recommendations = CosineGameRecommended('PUBG: BATTLEGROUNDS', 8)
# print("Top Recommendations:", recommendations)


