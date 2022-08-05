import os
import re
import urllib.request
from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID  = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]


# spotify_url = "http://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6"
# urn = "spotify:track:1AI7UPw3fgwAFkvAlZWhE0"
def main():
    # TODO: get this url from the user, and validate it
    url = "https://open.spotify.com/track/1AI7UPw3fgwAFkvAlZWhE0?si=19066311c4e84d11"
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    track = sp.track(url)

    # for now only gives the name of the song and the artist name to search on yt
    track_info = get_track_info(track) 
    video_link = find_youtube(track_info)
    download_yt(video_link)

def get_track_info(track):
    artist_name = track["artists"][0]["name"]
    track_name = track["name"]
    # return dictionary_containing_all_track_info
    return  f"{artist_name} {track_name} audio"

def find_youtube(query):
    words = query.replace(" ", "+")
    search_link = "https://www.youtube.com/results?search_query=" + words
    # TODO: handle request errors
    # automatically retry if error is raised after a few seconds 
    response = urllib.request.urlopen(search_link)
    search_results = re.findall(r"watch\?v=(\S{11})", response.read().decode())
    first_vid = "https://www.youtube.com/watch?v=" + search_results[0]
    return first_vid

def download_yt(yt_link):
    #download the video in mp3 format from youtube
    ...

if __name__ == "__main__":
    main()
