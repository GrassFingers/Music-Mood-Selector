import pytest
from unittest.mock import patch 
from MusicMoodSelector import analyse_tag 

def test_analyse_tag_logic_mood_map():
    from MusicMoodSelector import mood_map
    #test mood_map is configured correctly
    assert "happy" in mood_map["happy"]
    assert "sad" in mood_map["sad"]
    assert "chill" in mood_map["chill"]
    assert "gym" in mood_map["gym"]

def test_analyse_tag_lifefm_call():
    with patch('requests.get') as mock_get:
        #expected return values of mock
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "toptags" : {
                "tag" : [
                    {"name" : "happy"}, {"name" : "upbeat"}
                ]
            }
        }

        #call analyse_tag to test requests.get
        result = analyse_tag("FAKE KEY", "TRACK NAME", "ARTISTS", "happy")
        assert result == True

