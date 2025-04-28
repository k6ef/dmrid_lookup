import os
import sys
from unittest.mock import patch, MagicMock
import requests.exceptions
import pytest
from rich.table import Table
from rich.console import Console
import dmrid_lookup

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
    with patch('requests.get') as mock:
        yield mock


@pytest.fixture
def mock_rich():
    with patch('rich.table.Table') as mock_table, \
         patch('rich.console.Console') as mock_console:
        yield mock_table, mock_console


def test_get_dmr_ids_success(mock_requests):
    mock_requests.return_value.json.return_value = {'results': [{'id': 123456}]}
    result = get_dmr_ids()
    assert result == {'results': [{'id': 123456}]}
    mock_requests.assert_called_once_with('https://api.radioid.net/api/dmr/user/')


def test_get_dmr_ids_no_results(mock_requests):
    mock_requests.return_value.json.return_value = {'results': []}
    result = get_dmr_ids()
    assert result == {'results': []}


def test_get_dmr_ids_error(mock_requests):
    mock_requests.side_effect = requests.exceptions.RequestException('API Error')
    result = get_dmr_ids()
    assert result is None


def test_lookup_by_id_success(mock_requests):
    mock_requests.return_value.json.return_value = {'results': [{'id': 123456}]}
    result = lookup_by_id(123456)
    assert result == {'results': [{'id': 123456}]}
    mock_requests.assert_called_once_with(
        'https://api.radioid.net/api/dmr/user/?id=123456'
    )


def test_lookup_by_id_error(mock_requests):
    mock_requests.side_effect = requests.exceptions.RequestException('API Error')
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


def test_pretty_print(mock_rich):
    mock_table, mock_console = mock_rich
    mock_table_instance = MagicMock()
    mock_table.return_value = mock_table_instance
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    data = {'id': 123456, 'name': 'Test User'}
    pretty_print(data)

    mock_table.assert_called_once_with(title="DMR ID Information")
    assert mock_table_instance.add_column.call_count == 2
    mock_table_instance.add_row.assert_called_with('id', '123456')
    mock_console_instance.print.assert_called_once_with(mock_table_instance)

    assert mock_requests.called
    assert mock_requests.call_args[0][0] == f"https://radioid.net/api/dmr/user/?id={dmr_id}"
    assert mock_requests.call_args[1]["headers"] == {"Accept": "application/json"}
    assert mock_requests.call_args[1]["timeout"] == 10 