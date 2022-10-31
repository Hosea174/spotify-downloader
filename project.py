import os
import re
import time
import urllib.request

import spotipy
from moviepy.editor import *
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from pytube import YouTube
from rich.console import Console
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def main():

    url = get_url()
    if "track" in url:
        songs = [get_track_info(url)]
    elif "playlist" in url:
        songs = get_playlist_info(url)
        # songs.extend(get_playlist_info(url))

    start = time.time()
    downloaded = 0
    for i, track_info in enumerate(songs, start=1):
        search_term = f"{track_info['artist_name']} {track_info['track_title']} audio"
        video_link = find_youtube(search_term)

        console.print(
            f"[magenta]({i}/{len(songs)})[/magenta] Downloading '[cyan]{track_info['artist_name']} - {track_info['track_title']}[/cyan]'..."
        )
        audio = download_yt(video_link)
        if audio:
            set_metadata(track_info, audio)
            os.replace(audio, f"../music/{os.path.basename(audio)}")
            console.print(
                "[blue]______________________________________________________________________"
            )
            downloaded += 1
        else:
            print("Skipping...")
    os.rmdir("../music/tmp")
    end = time.time()

    console.print(
        f"DOWNLOAD COMPLETED: {downloaded}/{len(songs)} song(s) dowloaded".center(
            70, " "
        ),
        style="on green",
    )
    console.print(
        f"Total time taken: {round(end - start)} sec".center(70, " "), style="on white"
    )


def get_url():
    url = input("Enter a spotify url: ")
    if re.search(r"^(https?://)?open\.spotify\.com/(playlist|track)/.+$", url):
        return url

    raise ValueError("Invalid spotify url")


def get_track_info(track_url):
    track = sp.track(track_url)
    # TODO: handle request errors
    # TODO: handle potential KeyError and IndexError
    track_metadata = {
        "artist_name": track["artists"][0]["name"],
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

    playlist = sp.playlist_tracks(sp_playlist)
    tracks = [item["track"] for item in playlist["items"]]
    tracks_info = []
    for track in tracks:
        track_info = get_track_info(track["uri"])
        tracks_info.append(track_info)

    return tracks_info


def find_youtube(query):
    # TODO: handle request errors
    # TODO: automatically retry if error is raised after a few seconds
    phrase = query.replace(" ", "+")
    search_link = "https://www.youtube.com/results?search_query=" + phrase
    try:
        response = urllib.request.urlopen(search_link)
    except:
        raise ValueError("Please check your internet connection and try again later.")
    search_results = re.findall(r"watch\?v=(\S{11})", response.read().decode())
    first_vid = "https://www.youtube.com/watch?v=" + search_results[0]

    return first_vid


def prompt_exists_action():
    global file_exists_action
    if file_exists_action == "SA":  # SA == 'Skip All'
        return False
    elif file_exists_action == "RA":  # RA == 'Replace All'
        return True

    print("This file already exists.")
    while True:
        resp = (
            input("replace[R] | replace all[RA] | skip[S] | skip all[SA]: ")
            .upper()
            .strip()
        )
        if resp in ("RA", "SA"):
            file_exists_action = resp
        if resp in ("R", "RA"):
            return True
        elif resp in ("S", "SA"):
            return False
        print("---Invalid response---")


def download_yt(yt_link):
    """download the video in mp3 format from youtube"""
    yt = YouTube(yt_link)
    # don't download existing files if the user wants to skip them
    exists = os.path.exists(f"../music/{yt.title}.mp3")
    if exists and not prompt_exists_action():
        return False

    # download the music
    video = yt.streams.filter(only_audio=True).first()
    vid_file = video.download(output_path="../music/tmp")
    # convert the downloaded video to mp3
    base = os.path.splitext(vid_file)[0]
    audio_file = base + ".mp3"
    mp4_no_frame = AudioFileClip(vid_file)
    mp4_no_frame.write_audiofile(audio_file, logger=None)
    mp4_no_frame.close()
    os.remove(vid_file)
    os.replace(audio_file, f"../music/tmp/{yt.title}.mp3")
    audio_file = f"../music/tmp/{yt.title}.mp3"
    # fsize = round(os.path.getsize(audio_file) / 1024**2, 2)
    # print(f"Download size: {fsize} MB")
    return audio_file


def set_metadata(metadata, file_path):
    """adds metadata to the downloaded mp3 file"""

    mp3file = EasyID3(file_path)

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
    file_exists_action = ""
    console = Console()
    main()
