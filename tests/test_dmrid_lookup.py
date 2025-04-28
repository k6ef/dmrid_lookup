import os
import sys
from unittest.mock import patch, MagicMock

import pytest


# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dmrid_lookup import (
    get_dmr_ids,
    lookup_by_id,
    pretty_print,
    save_to_csv
)


@pytest.fixture
def mock_requests():
    with patch('dmrid_lookup.requests') as mock:
        yield mock


def test_get_dmr_ids_success(mock_requests):
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {"callsign": "TEST1", "id": 123456},
            {"callsign": "TEST2", "id": 789012}
        ]
    }
    mock_requests.get.return_value = mock_response

    results = get_dmr_ids("TEST")
    assert len(results) == 2
    assert results[0]["callsign"] == "TEST1"
    assert results[0]["dmr_id"] == 123456
    assert results[1]["callsign"] == "TEST2"
    assert results[1]["dmr_id"] == 789012


def test_get_dmr_ids_no_results(mock_requests):
    # Mock empty API response
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_requests.get.return_value = mock_response

    results = get_dmr_ids("NONE")
    assert len(results) == 0


def test_get_dmr_ids_error(mock_requests):
    # Mock API error
    mock_requests.get.side_effect = Exception("API Error")
    
    results = get_dmr_ids("ERROR")
    assert len(results) == 0


def test_lookup_by_id_success(mock_requests):
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{"callsign": "TEST1", "id": 123456}]
    }
    mock_requests.get.return_value = mock_response

    result = lookup_by_id(123456)
    assert result is not None
    assert result["callsign"] == "TEST1"
    assert result["id"] == 123456


def test_lookup_by_id_not_found(mock_requests):
    # Mock 406 response (not found)
    mock_response = MagicMock()
    mock_response.status_code = 406
    mock_requests.get.return_value = mock_response

    result = lookup_by_id(999999)
    assert result is None


def test_lookup_by_id_error(mock_requests):
    # Mock API error
    mock_requests.get.side_effect = Exception("API Error")
    
    result = lookup_by_id(123456)
    assert result is None


def test_save_to_csv(tmp_path):
    # Test CSV file creation
    results = [
        {"callsign": "TEST1", "dmr_id": 123456},
        {"callsign": "TEST2", "dmr_id": 789012}
    ]
    test_file = tmp_path / "test_results.csv"
    
    save_to_csv(results, str(test_file))
    
    assert test_file.exists()
    with open(test_file) as f:
        content = f.read()
        assert "callsign,dmr_id" in content
        assert "TEST1,123456" in content
        assert "TEST2,789012" in content


def test_pretty_print(capsys):
    # Test pretty print functionality
    results = [
        {"callsign": "TEST1", "dmr_id": 123456},
        {"callsign": "TEST2", "dmr_id": 789012}
    ]
    
    pretty_print(results)
    captured = capsys.readouterr()
    assert "TEST1" in captured.out
    assert "123456" in captured.out
    assert "TEST2" in captured.out
    assert "789012" in captured.out

def test_dmrid_lookup_initialization():
    lookup = DMRIDLookup()
    assert lookup is not None

def test_dmrid_lookup_get_callsign():
    lookup = DMRIDLookup()
    # Add more specific tests based on your implementation
    pass 