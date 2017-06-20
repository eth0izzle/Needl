import os

import spotipy
import spotipy.oauth2

import needl
import needl.schedule
import needl.utils

spotify_client = None


def register():
    client_id = needl.settings["spotify"]["client_id"]
    client_secret = needl.settings["spotify"]["client_secret"]
    if client_id and client_secret:
        os.environ["SPOTIPY_CLIENT_ID"] = client_id
        os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials()
        global spotify_client
        spotify_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        search_interval = needl.settings['spotify']['search_interval']
        args = map(int, search_interval.split('..'))
        needl.schedule.every(*args).minutes.do(search_artist)


def search_artist():
    global spotify_client
    first_name = needl.utils.get_line(needl.args.datadir + '/first-names.txt').title()
    spotify_client.search(q="artist:" + first_name, type="artist")
    needl.log.info("Searching Spotify for artist: {}".format(first_name))
