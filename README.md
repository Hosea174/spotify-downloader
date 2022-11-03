# Spotify downloader
#### Video Demo:  https://youtu.be/bp0aS67imes
#### Description:

## About The Project

**Spotify downloader** is a python CLI program that downloads songs or even whole playlists from Spotify. It works by finding the YouTube URL of the music and downloading the video using a library called [pytube](https://github.com/pytube/pytube). Then, after converting the video to mp3, the program adds different metadata of the song(Album art, Album name, artists, release date...) to the downloaded audio file using the [mutagen](https://github.com/quodlibet/mutagen) library. This program also utilizes the [spotipy](https://spotipy.readthedocs.io/en/2.21.0/) library to interact with the Spotify API       

## Getting started
1. Create a [Spotify developers account](https://developer.spotify.com/dashboard/)
2. Create an app by clicking on *create an app* and giving name and description for the app
3. Take a note of your *Client ID* and *Client Secret* from the app's page
4. Open your terminal and run `git clone https://github.com/Hosea174/spotify-downloader` or optionally download the zip file
5. run `cd spotify-downloader`
6. run `export SPOTIPY_CLIENT_ID='<your-client-id>'` 
7. run `export SPOTIPY_CLIENT_SECRET='<your-client-secret>'`
8. Finally, run `python project.py` and follow the instructions to download a song or a playlist from spotify

## Prerequisites
Run the following command in the terminal after navigating to the project's directory:
```
pip install -r requirements.txt
```