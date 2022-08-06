import os
import re
import urllib.request
from timeit import default_timer as timer

import mutagen
import spotipy
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3
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
        "track_number": track["track_number"],
        "isrc": track["external_ids"]["isrc"],
        "album_art": track["album"]["images"][1]["url"],
        "album_name": track["album"]["name"],
        # "total_tracks": track["album"]["total_tracks"],
        "release_date": track["album"]["release_date"],
        "artists": [artist["name"] for artist in track["artists"]],
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
    print("Time take by find_youtube_url:", end - start)

    return first_vid


def download_yt(yt_link, track_info):
    """download the video in mp3 format from youtube"""
    start = timer()
    # TODO: show progres
    # TODO: check if the file doesn't already exist in the directory /music
    # TODO: return True if the video is downloaded, False otherwise
    print(
        f"Downloading '{track_info['track_title']}' by '{track_info['artist_name']}' ..."
    )
    yt = YouTube(yt_link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path="../music")
    base = os.path.splitext(out_file)[0]
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    file_path = os.path.realpath(new_file)
    fsize = round(os.path.getsize(file_path) / 1024**2, 2)
    set_metadata(track_info, file_path)

    print("=====================================================")
    end = timer()
    print("Time take by download_yt:", end - start)
    print(f"Download size: {fsize} MB")


def set_metadata(metadata, file_path):
    """adds metadata to the downloaded mp3 file"""

    mp3file = MP3(file_path)
    try:
        mp3file.add_tags(ID3=EasyID3)
    except mutagen.id3._util.error:
        print("Tag already exists")

    # add metadata
    mp3file["albumartist"] = metadata["artist_name"]
    mp3file["artist"] = metadata["artists"]
    mp3file["album"] = metadata["album_name"]
    mp3file["title"] = metadata["track_title"]
    mp3file["date"] = metadata["release_date"]
    mp3file["tracknumber"] = str(metadata["track_number"])
    mp3file["isrc"] = metadata["isrc"]
    mp3file.save()

    # add album cover
    audio = ID3(file_path)
    with urllib.request.urlopen(metadata["album_art"]) as albumart:
        audio["APIC"] = APIC(
            encoding=3, mime="image/jpeg", type=3, desc="Cover", data=albumart.read()
        )
    audio.save(v2_version=3)


if __name__ == "__main__":
    main()
