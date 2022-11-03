import pytest

from project import get_playlist_info, get_track_info, validate_url


def test_validate_url():
    with pytest.raises(ValueError) as e:
        validate_url("www.youtube.com/watch?=xxxxxxxx")
    assert "Invalid Spotify URL" in str(e.value)

    with pytest.raises(ValueError) as e:
        validate_url(
            "https://open.spotify.com/37i9dQZF1DXcBWIGoYBM5M?si=d215a681aedb41b6"
        )
    assert "Invalid Spotify URL" in str(e.value)

    with pytest.raises(ValueError) as e:
        validate_url(
            "https://spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=d215a681aedb41b6"
        )
    assert "Invalid Spotify URL" in str(e.value)


def test_get_track_info():
    with pytest.raises(ValueError) as e:
        get_track_info("https://open.spotify.com/track/xxxxxxxxx")
    assert "Invalid Spotify track URL" in str(e.value)

    with pytest.raises(ValueError) as e:
        get_track_info("https://open.spotify.com/track/invlaidurl")
    assert "Invalid Spotify track URL" in str(e.value)


def test_get_playlist_info():
    with pytest.raises(ValueError) as e:
        get_playlist_info("https://open.spotify.com/playlist/xxxxxxxxx")
    assert "Invalid Spotify playlist URL" in str(e.value)

    with pytest.raises(ValueError) as e:
        get_playlist_info("https://open.spotify.com/playlist/invlaidurl")
    assert "Invalid Spotify playlist URL" in str(e.value)

    with pytest.raises(ValueError) as e:
        get_playlist_info(
            "https://open.spotify.com/playlist/164xV2xrlcgk3U0pmYH513?si=74bcd8ec8d5b4f9a"
        )
    assert "Can't download private playlists." in str(e.value)
