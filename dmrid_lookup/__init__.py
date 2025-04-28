import requests
from rich.console import Console
from rich.table import Table

def get_dmr_ids():
    """Get all DMR IDs from the API."""
    try:
        response = requests.get('https://api.radioid.net/api/dmr/user/')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching DMR IDs: {e}")
        return None

def lookup_by_id(dmr_id):
    """Look up a specific DMR ID from the API."""
    try:
        response = requests.get(f'https://api.radioid.net/api/dmr/user/?id={dmr_id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error looking up DMR ID: {e}")
        return None

def pretty_print(data):
    """Pretty print the DMR ID data using rich."""
    if not data:
        return

    table = Table(title="DMR ID Information")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in data.items():
        table.add_row(str(key), str(value))

    console = Console()
    console.print(table) 