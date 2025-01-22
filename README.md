# Spotify downloader
# English
#### Video Demo:  https://youtu.be/bp0aS67imes
#### Description: bifurcation of the @Hosea174

## About The Project

**Spotify downloader** is a python CLI program that downloads songs or even whole playlists from Spotify. It works by finding the YouTube URL of the music and downloading the video using a library called [pytube](https://github.com/pytube/pytube). Then, after converting the video to mp3, the program adds different metadata of the song(Album art, Album name, artists, release date...) to the downloaded audio file using the [mutagen](https://github.com/quodlibet/mutagen) library. This program also utilizes the [spotipy](https://spotipy.readthedocs.io/en/2.21.0/) library to interact with the Spotify API       

## Getting started
1. Install Python 3.x.x, download of `https://www.python.org/downloads/` for Windows or Ubuntu (Linux) `sudo apt install python3`
2. Create a [Spotify developers account](https://developer.spotify.com/dashboard/)
3. Create an app by clicking on *create an app* and giving name and description for the app
4. Take a note of your *Client ID* and *Client Secret*, or URL URI *https://open.spotify.com/* from the app's page
5. Open your terminal and run `git clone https://github.com/mastersamm-db/spotify-downloader` or optionally download the zip file
6. run `cd spotify-downloader`
7. run `$env:SPOTIPY_CLIENT_ID='<your-client-id>'` or `set SPOTIPY_CLIENT_ID='<your-client-id>'` 
8. run `$env:SPOTIPY_CLIENT_SECRET='<your-client-secret>'` or `set SPOTIPY_CLIENT_SECRET='<your-client-secret>'`
9. Finally, run `python project.py` and follow the instructions to download a song or a playlist from spotify

## Prerequisites
Run the following command in the terminal after navigating to the project's directory:
```
pip install -r requirements.txt
```
# =============================================================================================================================================
# Descargador de Spotify
# Español
#### Video de demostración: https://youtu.be/bp0aS67imes
#### Descripción: bifurcación de @Hosea174

## Acerca del proyecto

**Descargador de Spotify** es un programa CLI de Python que descarga canciones o incluso listas de reproducción completas de Spotify. Funciona buscando la URL de YouTube de la música y descargando el video usando una biblioteca llamada [pytube](https://github.com/pytube/pytube). Luego, después de convertir el video a mp3, el programa agrega diferentes metadatos de la canción (carátula del álbum, nombre del álbum, artistas, fecha de lanzamiento...) al archivo de audio descargado usando la biblioteca [mutagen](https://github.com/quodlibet/mutagen). Este programa también utiliza la biblioteca [spotipy](https://spotipy.readthedocs.io/en/2.21.0/) para interactuar con la API de Spotify

## Primeros pasos
1. Instale Python 3.x.x, descargue `https://www.python.org/downloads/` para Windows o Ubuntu (Linux) `sudo apt install python3`
2. Cree una [cuenta de desarrollador de Spotify](https://developer.spotify.com/dashboard/)
3. Cree una aplicación haciendo clic en *crear una aplicación* y dando un nombre y una descripción para la aplicación
4. Tome nota de su *ID de cliente* y *Secreto de cliente*, o URL URI *https://open.spotify.com/* de la página de la aplicación
5. Abra su terminal y ejecute `git clone https://github.com/mastersamm-db/spotify-downloader` u opcionalmente descargue el archivo zip
6. ejecute `cd spotify-downloader`
7. ejecuta `$env:SPOTIPY_CLIENT_ID='<your-client-id>'` o `set SPOTIPY_CLIENT_ID='<your-client-id>'`
8. ejecuta `$env:SPOTIPY_CLIENT_SECRET='<your-client-secret>'` o `set SPOTIPY_CLIENT_SECRET='<your-client-secret>'`
9. Por último, ejecuta `python project.py` y sigue las instrucciones para descargar una canción o una lista de reproducción de Spotify

## Requisitos previos
Ejecuta el siguiente comando en la terminal después de navegar al directorio del proyecto:
```
pip install -r requirements.txt
```