import spotipy
import numpy as np
import pandas as pd
import datetime

from sklearn.decomposition import PCA
from spotipy.oauth2 import SpotifyClientCredentials
from secret import client_id, client_secret


# Create the query to the spotify web API using spotipy along with the playlist URL's
client_credentials_manager = SpotifyClientCredentials(
                                client_id=client_id,
                                client_secretsecret=client_secret)
sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)

url_house = ""
url_breaks = ""


def analyse_playlist(url):
    """Retrieve all songs from the training playlist URL
    then takes the song ID, song, album, artist and puts into a panda dataframe"""

    #Song Titles
    offset = 0
    name = []

    while True:
        response = sp.playlist_tracks(url,
                                    offset=offset,
                                    fields=['items.track.name,total'])
        name.append(response['items'])
        offset = offset + len(response['items'])

        if len(response['items']) == 0:
            break

    name_list = [b['track']['name'] for a in name for b in a]
    len(name_list)

    #Album Titles
    offset = 0
    album = []
    
    while True:
        response = sp.playlist_tracks(url,
                                        offset=offset,
                                        fields=['items.track.album.name,total'])
        album.append(response['items'])
        offset = offset + len(response['items'])
        
        if len(response['items']) == 0:
            break
    album_list = [b['track']['album']['name'] for a in album for b in a]
    
    #Artist Names
    offset = 0
    artist = []
    
    while True:
        response = sp.playlist_tracks(url,
                                      offset=offset,
                                      fields=['items.track.album.artists.name,total'])
        artist.append(response['items'])
        offset = offset + len(response['items'])
        
        if len(response['items']) == 0:
            break
        
    artist_list = [b['track']['album']['artists'][0]['name'] for a in artist for b in a]
    
    # ID
    offset = 0
    identifier = []

    while True:
        response = sp.playlist_tracks(url,
                                      offset=offset,
                                      fields=['items.track.id,total'])

        identifier.append(response["items"])
        offset = offset + len(response['items'])
        
        if len(response['items']) == 0:
            break

    identifier_list= [b["track"]["id"] for a in identifier for b in a]
    len(identifier_list)

    #Get audio features
    features = [sp.audio_features(identifier) for identifier in identifier_list]
    
    #Get each invidividual features
    danceability = [(b["danceability"]) for a in features for b in a]    
    mode = [(b["mode"]) for a in features for b in a]
    energy = [(b["energy"]) for a in features for b in a]
    key = [(b["key"]) for a in features for b in a]        
    loudness = [(b["loudness"]) for a in features for b in a]       
    speechiness = [(b["speechiness"]) for a in features for b in a]
    acousticness = [(b["acousticness"]) for a in features for b in a]        
    instrumentalness = [(b["instrumentalness"]) for a in features for b in a] 
    liveness = [(b["liveness"]) for a in features for b in a]
    valence = [(b["valence"]) for a in features for b in a]        
    tempo = [(b["tempo"]) for a in features for b in a] 
    duration_ms = [(b["duration_ms"]) for a in features for b in a] 
    identifier_ = [(b["id"]) for a in features for b in a]
    
    #DataFrame 1 for the lists for song names, artist names, albums, and spotify categories
    df = pd.DataFrame({"Song Name": name_list, "Artist": artist_list, "Album": album_list, "ID": identifier_list})
    
    #Dataframe 2 for each spotify song category
    
    df_2 = pd.DataFrame({"Danceability":danceability,
                         "Mode":mode,
                         "Energy":energy,
                         "Key":key,
                         "Loudness":loudness,
                         "Speechiness":speechiness,
                         "Acousticness":acousticness,
                         "Instrumentalness":instrumentalness,
                         "Liveness":liveness,
                         "Valence":valence,
                         "Tempo":tempo,
                         "Duration (ms)": duration_ms,
                         "ID_CHECK":identifier_
                               })
    df_combined = df_2.join(df)
    df_combined.to_excel("df" + datetime.now.strftime(format="%f") + ".xlsx")
    
    return df_combined.tail()
    
    
def PCA(excel_file):
    df = pd.read_excel(excel_file, index_col=0)
    
    df_scaled = pd.DataFrame()
    
    for col in df.loc[:,"Danceability": "Duration (ms)"]:
        df_scaled[col] = (df[col] - df[col].mean() / df[col].std())
    
    df_scaled
    
    #Initialise PCA
    pca = PCA(n_components=len(df_scaled.columns))
    pca_series = pca.fit_transform(df_scaled).T
    
    df_pca = pd.DataFrame
