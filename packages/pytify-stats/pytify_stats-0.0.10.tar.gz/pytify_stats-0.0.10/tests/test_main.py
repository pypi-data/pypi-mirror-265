import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from dotenv import load_dotenv
from src.pytify_stats.client import Client



class Tests:

    def test_sanity_check(self):
        expected = True  # the value we expect to be present
        actual = True  # the value we see in reality
        assert actual == expected, "Expected True to be equal to True!"
    
    def test_get_env(self):
        load_dotenv()
        CLIENT_ID = os.getenv('CLIENT_ID')
        CLIENT_SECRET =  os.getenv('CLIENT_SECRET')
        

        assert isinstance(CLIENT_ID, str)
        assert len(CLIENT_ID) > 0
        assert isinstance(CLIENT_SECRET, str)
        assert len(CLIENT_SECRET) > 0
        


    def test_get_spofify_auth(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        assert isinstance(access_token, str)

    # def test_get_spofify_auth(self):
    #     load_dotenv()
    #     CLIENT_ID = os.getenv("CLIENT_ID")
    #     CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
    #     spy = Client(CLIENT_ID,CLIENT_SECRET)
    #     access_token = spy.authenticate()
    #     assert isinstance(access_token, str)
    #     assert len(access_token) > 0

    def test_auth_no_id(self):
        load_dotenv()
        CLIENT_ID = ""
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        spy2 = Client(os.getenv("CLIENT_ID"),CLIENT_SECRET)
        access_token = spy.authenticate()
        access_token2 = spy2.authenticate()
        assert len(access_token) == len(access_token2)

    def test_auth_no_secret(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  ""
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        spy2 = Client(CLIENT_ID,os.getenv("CLIENT_SECRET"))
        access_token = spy.authenticate()
        access_token2 = spy2.authenticate()
        assert len(access_token) == len(access_token2)

    
    def test_search_get_artist_id(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        artist_id = spy.search(headers, "J Cole", "artist")

        assert isinstance(artist_id, str)
        
    # def test_search_get_artist_id(self):
    #     load_dotenv()
    #     CLIENT_ID = os.getenv("CLIENT_ID")
    #     CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
    #     spy = Client(CLIENT_ID,CLIENT_SECRET)
    #     access_token = spy.authenticate()
    #     headers = {
    #     'Authorization': 'Bearer {token}'.format(token=access_token)
    #     }
    #     artist_id = spy.get_artist_id("J Cole")
    #     assert isinstance(artist_id, str)


    def test_search_get_track_id(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        artist_id = spy.search(headers, "She Knows", "track")
        assert isinstance(artist_id, str)

    def test_search_get_album_id(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        artist_id = spy.search(headers, "2014 Forest", "album")
        assert isinstance(artist_id, str)


        
    def test_get_song(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        song = spy.get_song("Hello")

        assert isinstance(song, list)

    def test_get_song_dne(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        song = spy.get_song("nkewfnnanfsdikesd")

        assert song == "No such track ID found."

    def test_get_song_no_search(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        song = spy.get_song("")
        assert song == "Please enter the name of a song."

    def test_analyze(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        analysis = spy.analyze("Hello")
        assert isinstance(analysis, str)

    def test_analyze_dne(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        analysis = spy.analyze("dcinneoenndsiweinwo")
        assert analysis == "Invalid track ID"

    def test_analyze_no_search(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        analysis = spy.analyze("")
        assert analysis == "Please enter the name of a song."
    
    def test_result_format(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)

        artist = "wallows" 
        albums = spy.get_artist_albums(artist)

        # Check if the function returns a list
        assert isinstance(albums, list)

        if not albums:
            # if no albums, return empty list
            assert albums == []
            print("No albums found for the artist.")
        else:
            # else check the format of albums
            for album in albums:
                assert isinstance(album, str)
                assert len(album) > 0

    def test_correct_info(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        
        # Call a successful response with albums
        artist = 'wallows'

        # Call the function
        albums = spy.get_artist_albums(artist)

        # Check with correct information
        assert albums == ['Tell Me That It’s Over', 'Nothing Happens']
    
    def test_invalid_artist(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        # Call a response with no artists found
        artist = 'nonexist_artist_name_1234567'
        
        # Call the function
        albums = spy.get_artist_albums(artist)
        
        # Check if album list is empty
        assert albums == []

    def test_get_top_ten(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        topten = spy.get_top_ten("J Cole")
        assert isinstance(topten, str)

    def test_get_top_ten_error(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        topten = spy.get_top_ten("erjjroijejeoeoririj")
        assert topten == f"The artist request was invalid, error:400"

    def test_get_top_ten_no_search(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        topten = spy.get_top_ten("")
        assert topten == "Please enter an artist query."
        
    # def test_search_for_artist(self):
    #     load_dotenv()
    #     CLIENT_ID = os.getenv("CLIENT_ID")
    #     CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
    #     spy = Client(CLIENT_ID,CLIENT_SECRET)

    #     artist_name = "J. Cole"
    #     artist_data = spy.search_for_artist(artist_name)
    #     assert artist_data is not None, "No artist data"
    #     assert artist_data['name'] == artist_name, "Artist name is incorrect" 
    
    def test_search_for_artist(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        artist_name = "J. Cole"
        artist_data = spy.search_for_artist(artist_name)
        assert isinstance(artist_data, dict) 

    def test_search_for_artist_error(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        artist_name = "jodsjoejfsjosjofojjowjo"
        artist_data = spy.search_for_artist(artist_name)
        assert artist_data == "Artist not found."
    
    def test_search_for_artist_blank(self):
        load_dotenv()
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET =  os.getenv("CLIENT_SECRET")
        spy = Client(CLIENT_ID,CLIENT_SECRET)
        access_token = spy.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        artist_name = ""
        artist_data = spy.search_for_artist(artist_name)
        assert artist_data == "Invalid artist name."