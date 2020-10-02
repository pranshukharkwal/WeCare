import requests
from bs4 import BeautifulSoup
import pandas as pd
def imdb(id):
    data = {}
    url = "https://www.imdb.com/title/tt0" + id
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    data['rating'] = soup.find('span' , attrs={'itemprop' : 'ratingValue'}).text
    data['storyline'] = soup.find('div' , attrs={'class' : 'inline canwrap'}).find('span').text.strip()
    data['ratingCount'] = soup.find('span' , attrs={'itemprop' : 'ratingCount'}).text
    subtext = soup.find('div' , attrs={'class' : 'subtext'})
    data['length'] = subtext.find('time').text.strip()
    data['release'] = subtext.find('a' , attrs={'title' : 'See more release dates'}).text.strip()
    data['thumbnail'] = soup.find('div' , attrs={'class':'poster'}).find('img')['src'].strip()
    return data
    
movies = pd.read_csv('movies.csv')
links = pd.read_csv('links.csv')
data = {}
for i in range(5):
    movieid = movies['movieId'][i]
    imdbid = imdbid = str(links['imdbId'].where(links['movieId'] == movieid).dropna()).split()[1].split('.')[0]
    title = movies['title'][i]
    moviedata = imdb(imdbid)
    genres = movies['genres'][i].split('|')
    print(movieid , imdbid , title , genres)
    print(moviedata)
    print()
    for genre in genres:
        if genre not in data:
            data[genre] = [{title : moviedata}]
        else:
            data[genre].append({title : moviedata})

print(data)
