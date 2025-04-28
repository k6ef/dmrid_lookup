import os
import sys
from unittest.mock import patch, MagicMock
import requests.exceptions
import pytest
from rich.table import Table
from rich.console import Console

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dmrid_lookup import (
    get_dmr_ids,
    lookup_by_id,
    pretty_print,
    save_to_csv,
    main
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
    mock_response = MagicMock()
    mock_response.json.return_value = {'results': [{'id': 123456}]}
    mock_requests.return_value = mock_response
    result = get_dmr_ids()
    assert result == {'results': [{'id': 123456}]}
    mock_requests.assert_called_once_with(
        'https://radioid.net/api/dmr/user/',
        headers={'Accept': 'application/json'},
        timeout=10
    )


def test_get_dmr_ids_no_results(mock_requests):
    mock_response = MagicMock()
    mock_response.json.return_value = {'results': []}
    mock_requests.return_value = mock_response
    result = get_dmr_ids()
    assert result == {'results': []}


def test_get_dmr_ids_error(mock_requests):
    mock_requests.side_effect = requests.exceptions.RequestException('API Error')
    result = get_dmr_ids()
    assert result is None


def test_lookup_by_id_success(mock_requests):
    mock_response = MagicMock()
    mock_response.json.return_value = {'id': 123456, 'name': 'Test User'}
    mock_requests.return_value = mock_response
    result = lookup_by_id(123456)
    assert result == {'id': 123456, 'name': 'Test User'}
    mock_requests.assert_called_once_with(
        'https://radioid.net/api/dmr/user/?id=123456',
        headers={'Accept': 'application/json'},
        timeout=10
    )


def test_lookup_by_id_error(mock_requests):
    mock_requests.side_effect = requests.exceptions.RequestException('API Error')
    result = lookup_by_id(123456)
    assert result is None


def test_save_to_csv(tmp_path):
    data = {'id': 123456, 'name': 'Test User'}
    filename = tmp_path / "test.csv"
    save_to_csv(data, str(filename))
    assert filename.exists()
    with open(filename) as f:
        content = f.read()
        assert 'id,123456' in content
        assert 'name,Test User' in content


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
    mock_console_instance.print.assert_called_once_with(mock_table_instance)


def test_main_with_id(mock_requests):
    mock_response = MagicMock()
    mock_response.json.return_value = {'id': 123456, 'name': 'Test User'}
    mock_requests.return_value = mock_response
    with patch('sys.argv', ['script.py', '--id', '123456']):
        assert main() == 0


def test_main_with_id_and_csv(mock_requests, tmp_path):
    mock_response = MagicMock()
    mock_response.json.return_value = {'id': 123456, 'name': 'Test User'}
    mock_requests.return_value = mock_response
    csv_file = tmp_path / "test.csv"
    with patch('sys.argv', ['script.py', '--id', '123456', '--csv', str(csv_file)]):
        assert main() == 0
    assert csv_file.exists()


def test_main_no_id():
    with patch('sys.argv', ['script.py']), \
         patch('sys.exit') as mock_exit:
        main()
        mock_exit.assert_called_once_with(1) 