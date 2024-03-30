[![log github events](https://github.com/software-students-spring2024/3-python-package-exercise-team-7/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-spring2024/3-python-package-exercise-team-7/actions/workflows/event-logger.yml) [![log github events multiple versions](https://github.com/software-students-spring2024/3-python-package-exercise-team-7/actions/workflows/event-log-multiple.yml/badge.svg)](https://github.com/software-students-spring2024/3-python-package-exercise-team-7/actions/workflows/event-log-multiple.yml)

# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

# Package Description

The package pytify_stats is a Python package that runs basic stats gathered from the Spotify API.  It can currently get stats such as artist information, track information, and an artist's top ten tracks.

# Function Documentation

def authenticate(self):

        Authenticates the Spotify user to be able to use this package.
        Return: access_token = Token that allows you to access the Spotify data.


def search(self, headers,name,keyword):
        
        Searches the Spotify database for the queried item 
        Inputs: headers = Headers for the HTTP response, name = the name of the item you want to search, keyword = the type of item.
        Return: artist_id = the id of the item you are looking for
        

def get_top_ten(self, artist):
        
        Retrieves the top ten songs of an artist.
        Input: artist = The artist you are searching for
        Return: retStr = the string that contains an enumerated list of the artist's top 10 songs.
        

def get_song(self, song):
        
        Retrives the song from the query.
        Input: song = The song to look for.
        Return: An array containing the name of the song and its length in milliseconds.
        

def analyze(self, song):
        
        Returns an analysis of a song and its key information.
        Input: song = The song to be analyzed.
        Return: feature_list = The list of features, such as key, tempo, etc. that the song contains.'
        

def search_for_artist(self, artist_name):
        
        Search for an artist by name.
        Input: artist_name = the name of the artist to search for.
        Return: dict = About the artist.
          

def get_artist_albums(self, artist):
        
        Retrieve the albums of a given artist.
        Input: artist = The artist to search for.
        Return: album_names = The list of albums the artist has released.
        

# How to Use

Here is how to set it up:


1. Run this code in the terminal:

```
pip install pytify-stats==0.0.9
```

2. Import it in your python file:

```
from pytify_stats import client
```

3. Create a new account or log in [here](https://developers.spotify.com/). Go to the dashboard, create an app and retrieve your new ID and SECRET


4. Authenicate using the Client class

The example below demonstrates how to do this:

```
from pytify_stats import client

spy = client.Client(CLIENT_ID, CLIENT_SECRET)

top_ten = spy.get_top_ten("J. Cole")

song = spy.get_song("She Knows")

album = spy.get_artist_albums("J. cole")

print(top_ten)
print(song)
print(album)
```

Put your client_id and client_secret you've recieved from Spotify in place of the parameters of the Client class

# How to Contribute

1. Download the source code and open it on a code editor

2. Install pipenv and install the following:

pipenv install requests
pipenv install python-dotenv
pipenv install pytest

3. Make changes and run unit test for it

4. Push changes onto a new branch on GitHub

5. Make a pull request and  wait for a review. If accpeted, the branches will be merged and the new code will be uploaded to PyPi

# Pypi Package Link

https://pypi.org/project/pytify-stats/0.0.9/


# Contributors

* [Denzel](https://github.com/denprud)
* [Joyce](https://github.com/joyxe-xie)
* [Neal](https://github.com/nhaulsey)
* [Rakshit](https://github.com/RakSridhar23)
