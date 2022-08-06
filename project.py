import os
import re
import urllib.request
from timeit import default_timer as timer

import spotipy
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def main():
    # TODO: get this url from the user, and validate it
    url = "https://open.spotify.com/track/1AI7UPw3fgwAFkvAlZWhE0?si=19066311c4e84d11"
    
    track_info = get_track_info(url)
    search_term = f"{track_info['track_title']} {track_info['artist_name']} audio"
    video_link = find_youtube(search_term)
    download_yt(video_link, track_info)


def get_track_info(track_url):
    track = sp.track(track_url)
    # TODO: handle request errors
    # TODO: handle potential KeyError and IndexError
    track_metadata = {
        "artist_name": track["album"]["artists"][0]["name"],
        "track_title": track["name"],
        "album_art": track["album"]["images"][1]["url"],
        "album_name": track["album"]["name"],
        "release_date": track["album"]["release_date"],
        "artists": [artist["name"] for artist in track["artists"]],
        "isrc": track["external_ids"]["isrc"]
    }

    return track_metadata


def get_playlist_info(sp_playlist):
    # TODO: exctract the url of all songs in the playlist then call get_track_info() on each url
    # TODO: return a list of dictionaries containing the info of each song    
    # playlist = sp.playlist_tracks(url)

    ...


def find_youtube(query):
    # TODO: handle request errors
    # TODO: automatically retry if error is raised after a few seconds
    start = timer()
    words = query.replace(" ", "+")
    search_link = "https://www.youtube.com/results?search_query=" + words
    response = urllib.request.urlopen(search_link)
    search_results = re.findall(r"watch\?v=(\S{11})", response.read().decode())
    first_vid = "https://www.youtube.com/watch?v=" + search_results[0]
    end = timer()
    print("Time take by find_youtube_url:", end-start)

    return first_vid


def download_yt(yt_link, vid_name):
    """download the video in mp3 format from youtube"""
    start = timer()
    # TODO: show progressbar
    # TODO: check if the file doesn't exist in the directory /music
    # TODO: return True if the video is downloaded, False otherwise
    print(f"Downloading \"{vid_name}\" ...")
    yt = YouTube(yt_link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path="../music")
    base = os.path.splitext(out_file)[0]
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    print("=" * len(vid_name))
    end = timer()
    print("Time take by download_yt:", end-start)



def set_metadata(metadata):
    ...

if __name__ == "__main__":
    main()
