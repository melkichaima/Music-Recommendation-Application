from project import get_artist_id,get_recommendations,open_url
import pytest

def test_get_artist_id():
    """ Testing get_artist_id function"""
    assert get_artist_id("") == ""
    assert get_artist_id(["bts","One direction"]) == "3Nrfpe0tUJi4K4DXYWgMUX,4AK6F7OLvEQ5QYCBNiQWHq"

def test_get_recommendations():
    '''Tests arguments to get_recommendation function'''
    with pytest.raises(ValueError):
        get_recommendations("gwshjf,,fiujhf4","happy","aucastic")
    with pytest.raises(TypeError):
        get_recommendations(["jhjhHJ8","hgyhfy8"],"happy","aucastic")


def test_open_url():
    '''Testing spotify track urls'''
    with pytest.raises(ValueError):
        open_url("https://open.spotify.com/track/")
        open_url("http:/open.spotify.com/track/2rCPeuzBY9NEX9VNshkjmH")
        open_url("https://open.spotifycom/track/2rCPeuzBY9NEX9VNshkjmH")
