import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm
import pandas as pd
import numpy as np
import os

# For the script to work you need to set the environment variables for your client id, client secret and redirect uri:
# export CLIENT_ID='your_client_id'
# export CLIENT_SECRET='your_client_secret'
# export REDIRECT_URI='your_redirect_uri'
# 
# The redirect uri needs to be explicitly allowed in your spotify app. It can be any url, preferably the url to your web app

scope = 'user-top-read'
username = None

def set_user(user):
    username = user

    return username

# This creates a spotipy instance to use for the rest of the script
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username=username))
except:
    print('Please set a user (run function set_user("you_usernamae"))')

def user_top_tracks():
    # Gets the current user's top tracks
    # and returns their id's in a list
    user_top_tracks = sp.current_user_top_tracks(limit=50)
    user_top_track_ids = [user_top_tracks['items'][i]['id'] for i in range(50)]

    return user_top_track_ids

def user_saved_albums(limit=20):
    # Gets the current user's saved albums
    # and returns a dataframe with their name, artist, a link to their album cover, popularity out of 100, and id
    saved_albums = sp.current_user_saved_albums(limit=limit)
    
    albums = [(saved_albums['items'][i]['album']['name'],
               saved_albums['items'][i]['album']['artists'][0]['name'],
               saved_albums['items'][i]['album']['images'][0]['url'],
               saved_albums['items'][i]['album']['popularity'],
               saved_albums['items'][i]['album']['id']) for i in range(limit) if (saved_albums['items'][i]['album']['total_tracks'] > 5) and (saved_albums['items'][i]['album']['popularity']>20) and (saved_albums['items'][i]['album']['type'] == 'album')]

    albums = pd.DataFrame(albums,columns=['Name','Artist','Album Art URL','Popularity','Spotify ID'])

    
    return albums.reset_index(drop=True)

def top_50_tracks():
    # Not used in the main program
    # Gets the tracks from the US Top 50 playlist and returns their id's in a list
    top_50 = sp.playlist(playlist_id='37i9dQZEVXbLRQDuF5jeBp')
    top_50_track_ids = [top_50['tracks']['items'][i]['track']['id'] for i in range(50)]

    return top_50_track_ids

def albums_from_tracks(ids):
    # Gets the albums from track id's
    # Drops duplicates in case multiple tracks are from the same album
    # Returns the name, artist, link to cover are, popularity and track id for the first track from the album
    tracks = sp.tracks(ids)['tracks']

    albums = [(tracks[i]['album']['name'],
               tracks[i]['artists'][0]['name'],
               tracks[i]['album']['images'][0]['url'],
               tracks[i]['popularity'],
               ids[i]) for i in range(len(ids)) if (tracks[i]['album']['total_tracks']>5) and (tracks[i]['popularity']>20)]

    albums = pd.DataFrame(albums,columns=['Name','Artist','Album Art URL','Popularity','Spotify ID'])
    albums = albums.drop_duplicates(subset=['Name'])
    
    return albums.reset_index(drop=True)
    
def get_features(ids):
    # Gets audio features for given tracks
    features = sp.audio_features(tracks=ids)
    keys = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']

    return pd.DataFrame().from_dict({key: [features[i][key] for i in range(len(ids))] for key in keys}).reset_index(drop=True)

def main():
    set_user(input('Please input your Spotify username: '))
    ids = user_top_tracks()
    albums = albums_from_tracks(ids)
    # albums = pd.concat([albums_from_tracks(ids),
    #                     user_saved_albums()],axis=0).drop_duplicates(subset=['Name'])


    albums = pd.concat([albums,get_features(albums['Spotify ID'])],axis=1)

    if not os.path.exists('output'):
        os.mkdir('output')

    albums.to_csv('output/album_data.csv')
    print(albums.head())

if __name__ == '__main__':
    main()