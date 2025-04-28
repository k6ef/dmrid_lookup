"""
DMR ID Lookup Tool

A Python package for looking up DMR IDs from radioid.net
"""

__version__ = "1.0.14"

import requests
from rich.console import Console
from rich.table import Table


def get_dmr_ids():
    """Fetch all DMR IDs from the API."""
    try:
        response = requests.get(
            "https://radioid.net/api/dmr/user/",
            headers={"Accept": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching DMR IDs: {e}")
        return None


def lookup_by_id(dmr_id):
    """Look up a specific DMR ID."""
    try:
        response = requests.get(
            f"https://radioid.net/api/dmr/user/?id={dmr_id}",
            headers={"Accept": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error looking up DMR ID: {e}")
        return None


def pretty_print(data):
    """Format and display the DMR ID data in a table."""
    if not data:
        return

    table = Table(title="DMR ID Information")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    for key, value in data.items():
        table.add_row(str(key), str(value))

    console = Console()
    console.print(table) 