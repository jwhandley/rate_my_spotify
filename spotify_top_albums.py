from spotipy import SpotifyClientCredentials, oauth2, Spotify

class SpotifyUser():
    def __init__(self,username):
        self.sp = Spotify(auth_manager=oauth2.SpotifyOAuth(scope='user-top-read user-library-read',username=username))

        self.top_tracks = self.get_top_tracks()
        self.saved_albums = self.get_saved_albums()
        self.top_albums = albums_from_tracks(self.top_tracks)

    def get_top_tracks(self):
        # Gets the current user's top tracks
        # and returns their id's in a list
        user_top_tracks = self.sp.current_user_top_tracks(limit=50)
        user_top_track_ids = [user_top_tracks['items'][i]['id'] for i in range(50)]

        return user_top_track_ids

    def get_saved_albums(self,limit=20):
        # Gets the current user's saved albums
        # and returns a dictionary with their name, artist, a link to their album cover, popularity out of 100, and id
        saved_albums = self.sp.current_user_saved_albums(limit=limit)['items']
        
        albums = {
            'name': [],
            'artist': [],
            'cover': [],
            'popularity': [],
            'id': []
        }

        for i in range(limit):
            if (saved_albums[i]['album']['total_tracks'] > 5) and (saved_albums[i]['album']['popularity']>20) and (saved_albums[i]['album']['type'] == 'album'):
                albums['name'].append(saved_albums[i]['album']['name'])
                albums['artist'].append(saved_albums[i]['album']['artists'][0]['name'])
                albums['cover'].append(saved_albums[i]['album']['images'][0]['url'])
                albums['popularity'].append(saved_albums[i]['album']['popularity'])
                albums['id'].append(saved_albums[i]['album']['id'])


        return albums

# The following functions don't require user authentication, so I created a new instance of spotipy that uses the correct authentication stream
sp_client = Spotify(auth_manager = SpotifyClientCredentials())

def top_50_tracks():
    # Not used in the main program
    # Gets the tracks from the US Top 50 playlist and returns their id's in a list
    top_50 = sp_client.playlist(playlist_id='37i9dQZEVXbLRQDuF5jeBp')
    top_50_track_ids = [top_50['tracks']['items'][i]['track']['id'] for i in range(50)]

    return top_50_track_ids

def albums_from_tracks(ids):
    # Gets the albums from track id's
    # Drops duplicates in case multiple tracks are from the same album
    # Returns the name, artist, link to cover are, popularity and track id for the first track from the album
    tracks = sp_client.tracks(ids)['tracks']

    albums = {
        'name': [],
        'artist': [],
        'cover': [],
        'popularity': [],
        'id': []
    }
    names = []
    for i in range(len(tracks)):
        name = tracks[i]['album']['name']
        if (name not in names) and (tracks[i]['album']['total_tracks']>5) and (tracks[i]['popularity']>20):
            albums['name'].append(name)
            albums['artist'].append(tracks[i]['artists'][0]['name'])
            albums['cover'].append(tracks[i]['album']['images'][0]['url'])
            albums['popularity'].append(tracks[i]['popularity'])
            albums['id'].append(ids[i])
        names.append(name)
    
    return albums

def get_features(ids):
    # Gets audio features for given tracks
    features = sp_client.audio_features(tracks=ids)
    keys = ['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']

    return {key: [features[i][key] for i in range(len(ids))] for key in keys}

def main():
    import os
    import pandas as pd
    user = SpotifyUser(input('Please input Spotify username: '))
    albums = user.top_albums

    albums = pd.DataFrame().from_dict({**albums,**get_features(albums['id'])}).set_index('name')


    if not os.path.exists('output'):
        os.mkdir('output')

    albums.to_csv('output/album_data.csv')

if __name__ == '__main__':
    main()