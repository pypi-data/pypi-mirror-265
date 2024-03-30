import requests
import os
from dotenv import load_dotenv
import base64
from requests import post
import json


#added some comments

class Client:
    AUTH_URL = "https://accounts.spotify.com/api/token"
    BASE_URL = "https://api.spotify.com/v1/"
    def __init__(self, CLIENT_ID, CLIENT_SECRET):
        
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.token = self.authenticate()

    def authenticate(self):
        """
        Authenticates the Spotify user to be able to use this package.
        Return: access_token = Token that allows you to access the Spotify data.
        """

        # if(self.CLIENT_ID != os.getenv("CLIENT_ID")):
        #     # print("true")
        #     return "Invalid ID"
        # if(self.CLIENT_SECRET != os.getenv("CLIENT_SECRET")):
        #     # print("true")
        #     return "Invalid secret"
        auth_string = self.CLIENT_ID + ":" + self.CLIENT_SECRET
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }


    
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]

        
        
        return token

    def search(self, headers,name,keyword):
        """
        Searches the Spotify database for the queried item 
        Inputs: headers = Headers for the HTTP response, name = the name of the item you want to search, keyword = the type of item.
        Returns: artist_id = the id of the item you are looking for
        """

        response = requests.get(self.BASE_URL + f'search?q={keyword}:{str.lower(name)}&type={keyword}', headers=headers)

        # Convert the response to JSON
        response_data = response.json()

        # # Get the album's Spotify ID
        # album_id = response_data[keyword+"s"]['items'][0]['id']
        plural = keyword+"s"

        # Get the artist's Spotify ID
        if plural in response_data and 'items' in response_data[plural] and response_data[plural]['items']:
            item_id = response_data[plural]['items'][0]['id']
            return item_id
        else:
            return ""

    
    # def get_artist_id(self, artist):
    #     headers = {
    #         'Authorization': 'Bearer {token}'.format(token=self.token)
    #     }

    #     response = requests.get(self.BASE_URL + f'search?q=artist:{str.lower(artist)}&type=artist', headers=headers)

    #     response_data = response.json()
        
    #     # Get the artist's Spotify ID
    #     artist_id = response_data['artists']['items'][0]['id']

    #     return artist_id

    # def search_for_artist(self, artist_name):
    #     """
    #     Search for an artist by name.

    #     Args:
    #         - artist_name (str): the name of the artist to search for.

    #     Returns:
    #         - dict: About the artist.
    #     """  
    #     access_token = self.authenticate()

    #     headers = {
    #         'Authorization': 'Bearer {token}'.format(token=access_token)
    #     }

    #     response = requests.get(self.BASE_URL + 'search?q=' + artist_name + '&type=artist', headers=headers)

    #     if response.status_code == 200:
    #         artist_data = response.json()['artists']['items'][0]
    #         return artist_data
    #     else:
    #         print(f"Failed to get artist's information: {response.status_code}")
    #         return None

    def get_top_ten(self, artist):
        """
        Retrieves the top ten songs of an artist.
        Input: artist = The artist you are searching for
        Return: retStr = the string that contains an enumerated list of the artist's top 10 songs.
        """
        # retArray = []
        retStr = ""

        access_token = self.authenticate()

        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        artist_id = self.search(headers, artist, "artist")

        # print(artist_id)

        # Use the artist's Spotify ID to get their top tracks
        response = requests.get(self.BASE_URL + 'artists/' + artist_id + '/top-tracks?country=US', headers=headers)

        # Error handling
        if response.status_code != 200:
            return (f"The artist request was invalid, error:{response.status_code}")
            # return
        elif artist == "":
            return "Please enter an artist query."


        

        # Convert the response to JSON
        response_data = response.json()

        # Print the names of the artist's top 10 tracks
        for i, track in enumerate(response_data['tracks'][:10]):
            # retArray.append(track['name'])
            retStr = retStr + f"{i+1}. {track['name']}\n"
            #print(f"{i+1}. {track['name']}")

        
        # print(retArray)
        return retStr


    def get_song(self, song):
        """
        Retrives the song from the query.
        Input: song = The song to look for.
        Returns: An array containing the name of the song and its length in milliseconds.
        """

        access_token = self.authenticate()

        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        song_id = self.search(headers, song, "track")

        # Use the song's Spotify ID to get more information
        response = requests.get(self.BASE_URL + 'tracks/' + song_id, headers=headers)

        # Error handling
        if response.status_code != 200:
            print(f"The song request was invalid, error:{response.status_code}")
            return "No such track ID found."
        elif song == "":
            return "Please enter the name of a song."
        

        # Convert the response to JSON
        response_data = response.json()    

        return [response_data['name'],response_data['duration_ms']]
    
    # def get_track_id(self, song):
    #     access_token = self.authenticate()
    #     headers = {
    #     'Authorization': 'Bearer {token}'.format(token=access_token)
    #     }
    #     response = requests.get(self.BASE_URL + f'search?q=track:{str.lower(song)}&type=track',headers=headers)
    #     response_data = response.json()
    #     # print(response_data['tracks']['items'])
    #     # Get the song's Spotify ID
    #     if response_data['tracks']['items'] == []:
    #         return "No such track ID found"
    #     elif song == "":
    #         # print("Please enter the name of a song.")
    #         return "Please enter the name of a song."
    #     else: song_id = response_data['tracks']['items'][0]['id']
    #     return song_id
    
    

    def analyze(self, song):
        """
        Returns an analysis of a song and its key information.
        Input: song = The song to be analyzed.
        Return: feature_list = The list of features, such as key, tempo, etc. that the song contains.'
        """
        access_token = self.authenticate()

        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        if self.get_song(song) == "No such track ID found.":
            # print("Invalid track ID")
            return "Invalid track ID"
        elif song == "":
            # print("Please enter the name of a song.")
            return "Please enter the name of a song."
        else:
            song_id = self.search(headers, song, "track")
            #print(song_id)
            response = requests.get(self.BASE_URL + 'tracks/' + song_id, headers=headers)
            response_data = response.json()
            # print(response_data["artists"])
            print(f"{response_data['name']} by {response_data['artists'][0]['name']}:")

            #Use the song's Spotify ID to get their audio features
            features_response = requests.get(self.BASE_URL + 'audio-features/' + song_id, headers=headers)
            features_response_data = features_response.json()
            # print(features_response_data)

            feature_list = ''
            for feature in features_response_data:
                # print(f"{feature}: {features_response_data[feature]}")
                feature_list = feature_list + f"{feature}: {features_response_data[feature]}\n"
            # print(feature_list)
            return feature_list

    def search_for_artist(self, artist_name):
        """
            Search for an artist by name.

             Args:

            -artist_name (str): the name of the artist to search for.

            Returns:

            -dict: About the artist.

        """   


        access_token = self.authenticate()

        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
            }

        response = requests.get(self.BASE_URL + 'search?q=' + artist_name + '&type=artist', headers=headers)

        if artist_name == "":
            return "Invalid artist name."
        # print(response.json()['artists']['items'])
        if response.json()['artists']['items'] == []:
            return "Artist not found."
        
        if response.status_code == 200:
            artist_data = response.json()['artists']['items'][0]
            return artist_data

        else:
            print(f"Failed to get artist's information: {response.status_code}")
            return None
        

    
        
    def get_artist_albums(self, artist):
        """
        Retrieve the albums of a given artist.
        Input: artist = The artist to search for.
        Return: album_names = The list of albums the artist has released.
        """
        access_token = self.authenticate()
        headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
        artist_id = self.search(headers, artist, "artist")
        if artist_id:
            response = requests.get(self.BASE_URL + 'artists/' + artist_id + '/albums', headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                
                if 'items' in response_data:
                    albums = [album for album in response_data['items'] if album.get('album_type') == 'album']
                    album_names = [album["name"] for album in albums]
                    return album_names
                    
                else:
                    print("No albums found for the artist.")
                    return []
            else:
                print(f"Failed to fetch albums for artist {artist_id}. Status code: {response.status_code}")
                return []
        else:
            print(f"No artist found with name '{artist}'")
            return []