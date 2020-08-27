# Rate my Spotify

This will eventually be a web app that takes recent Spotify listening history and finds Metacritic scores for the top albums the user listens to. So far only the back end is set up. `album_scores.py` scrapes Wikipedia for Metacritic scores and `spotify_top_albums.py` gets the user's top tracks and albums. It can also be used to get audio features from the user's top tracks and compare them with the US Top 50 playlist from Spotify.

## Getting Started

### Prerequisites

This uses the spotipy module to interact with the Spotify API. Install with
```
pip install spotipy
```

You'll also need `pandas`, `tqdm`, `numpy`, `requests`, `re`, and `bs4`.

### Setup 

In order to run the scripts you will need to log in to your [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard/) and create an app. Once you've created the app, open it in your dashboard to find your client id and client secret. You'll also need to add a redirect uri in Edit Settings. Then you need to set environment variables before running either script.

On Linux or macOS:
```
export CLIENT_ID='your_client_id'
export CLIENT_SECRET='your_client_secret'
export REDIRECT_URI='your_redirect_uri'
```

and on Windows:
```
set CLIENT_ID='your_client_id'
set CLIENT_SECRET='your_client_secret'
set REDIRECT_URI='your_redirect_uri'
```

### Running

Right now running `spotify_top_albums.py` will write a csv of your top albums (derived from your top tracks) along with their primary artist, the audio features of your top track from the album and a link to the album cover art to `output`. Running `album_scores.py` will write a csv of your top albums (derived from your top tracks and last 50 saved albums), their primary artist, a link to their album cover art, and their Metacritic score (if one was found). I have examples from my account in the output folder.

## License

This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for details.
