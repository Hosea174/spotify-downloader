TODO

- Get a spotify link (playlist or track) as an input
- make sure the link is a valid spotify link and is either a playlist or a track
- if the link is a track
    - get the name and other metadata of the song
        * a function that takes in a spotify uri of a track
        * the function returns the name(and other metadeta in the future) of the track
- elif the link is a playlist
    - get the names of all songs in the playlist
    - call the function get_song_info() on each item of the playlist  
- Search that song on youtube and download it query="{artist_name} {track_name} audio"