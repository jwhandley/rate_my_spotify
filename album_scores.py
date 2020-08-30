import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import os
import spotify_top_albums

url = 'https://en.wikipedia.org/wiki/'

s = requests.Session()


def parse_album(x):
    # Parses album name so that it will work with Wikipedia
    x = re.sub(r' ?\([^)]+\)','',x).replace('"','').replace(' ','_')
    if x.isupper():
        return x.title()
    else:
        return x

def parse_artist(x):
    # Parses artist name so that it will work with Wikipedia
    if x.isupper():
        return x.title().replace(' ','_')
    else:
        return x.replace(' ','_')

def get_score(name,artist):
    # Scrapes Wikipedia for metacritic scores for a given album/artist combo
    # Wikipedia album pages have urls in one of three formats:
    #   - Album_Name -- if there is no ambiguity
    #   - Album_Name_(Artist_Name_album) -- if there are other albums of the same name by different artists
    #   - Album_Name_(album) -- if the album name also points to another page
    # This function tries each of these formats and then looks for a table with the header "Aggregate scores" and finds the row for Metacritic scores, returns the score
    try:
        try:
            r = s.get(''.join([url,name]))

            soup = BeautifulSoup(r.content,'html.parser')

            return int(soup.find('th',text='Aggregate scores').find_parent().find_parent().find('a',title='Metacritic').find_parent().find_next_sibling().text[:2])
        except:
            pass

        try:
            r = s.get(''.join([url,name,f'_({artist}_album)']))

            soup = BeautifulSoup(r.content,'html.parser')

            return int(soup.find('th',text='Aggregate scores').find_parent().find_parent().find('a',title='Metacritic').find_parent().find_next_sibling().text[:2])
        except:
            pass

        try:
            r = s.get(''.join([url,name,'_(album)']))

            soup = BeautifulSoup(r.content,'html.parser')

            return int(soup.find('th',text='Aggregate scores').find_parent().find_parent().find('a',title='Metacritic').find_parent().find_next_sibling().text[:2])
        except:
            pass
    except:
        return np.nan

def main():
    user = spotify_top_albums.SpotifyUser(input('Please input Spotify username: '))

    
    albums = pd.concat([user.top_albums,
                        user.get_saved_albums(limit=50)],axis=0).drop_duplicates(subset=['Name']).reset_index(drop=True)


    names = [parse_album(albums.loc[i,'Name']) for i in range(len(albums))]
    artists = [parse_artist(albums.loc[i,'Artist']) for i in range(len(albums))]

    print('Downloading Metacritic scores from Wikipedia.')
    scores = [get_score(names[i],artists[i]) for i in tqdm(range(len(names)))]
    

    albums['Score'] = scores
    albums = albums.dropna(subset=['Score'])

    print(albums.head(10))
    print('Your popularity-weighted average score is: ',round(np.average(albums['Score'],weights=albums['Popularity']),1))
    print('Your unweighted average score is: ',round(np.mean(albums['Score']),1))
    print('The standard deviation of your scores is: ',round(albums['Score'].std(),1))

    if not os.path.exists('output'):
        os.mkdir('output')

    albums.to_csv('output/album_scores.csv')

if __name__ == '__main__':
    main()
