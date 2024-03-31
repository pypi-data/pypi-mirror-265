import os
import json
from unittest.mock import patch, mock_open, Mock


cute_exp_html_start = """\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>How cute?</title>
  </head>
"""


def test_exp_cute_index(client):
    response = client.get("/exp_cute/")
    assert response.status_code == 200
    assert response.text[:100] == cute_exp_html_start


def test_save_data_json1(client):
    example_data = {
        "participantID": "debug_1",
        "condition": "1",
        "experiment1": [2, 59, 121, 256],
    }
    mock_open_exp_data = mock_open()
    mock_datetime = Mock()
    mock_datetime.now = Mock(return_value="2023-11-02_01:49:39.905657")
    with (
        patch("psyserver.main.open", mock_open_exp_data, create=False),
        patch("psyserver.main.datetime", mock_datetime),
    ):
        response = client.post("/exp_cute/save", json=example_data)
    assert response.status_code == 200
    assert response.json() == {"success": True}
    written_data = "".join(
        [_call.args[0] for _call in mock_open_exp_data.mock_calls[2:-1]]
    )
    assert written_data == json.dumps(example_data)
    mock_open_exp_data.assert_called_once_with(
        "data/studydata/exp_cute/debug_1_2023-11-02_01-49-39.json", "w"
    )


def test_save_data_json2(client):
    """no id, saving with timestamp instead."""
    example_data = {
        "participant_id": "debug_1",
        "condition": "1",
        "experiment1": [2, 59, 121, 256],
    }
    mock_open_exp_data = mock_open()
    mock_datetime = Mock()
    mock_datetime.now = Mock(return_value="2023-11-02_01:49:39.905657")
    with (
        patch("psyserver.main.open", mock_open_exp_data, create=False),
        patch("psyserver.main.datetime", mock_datetime),
    ):
        response = client.post("/exp_cute/save", json=example_data)
    assert response.status_code == 200
    assert response.json()["success"]

    written_data = "".join(
        [_call.args[0] for _call in mock_open_exp_data.mock_calls[2:-1]]
    )
    assert written_data == json.dumps(example_data)
    mock_open_exp_data.assert_called_once_with(
        "data/studydata/exp_cute/2023-11-02_01-49-39.json", "w"
    )
