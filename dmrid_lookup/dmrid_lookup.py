"""
DMR ID Lookup Tool core functionality
"""

import sys
import argparse
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


def ensure_venv():
    """Ensure we're running in a virtual environment."""
    if not hasattr(sys, 'real_prefix') and not hasattr(sys, 'base_prefix'):
        print("Warning: Not running in a virtual environment!")


def save_to_csv(data, filename):
    """Save DMR ID data to a CSV file."""
    import csv
    if not data:
        return

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Field', 'Value'])
        for key, value in data.items():
            writer.writerow([key, value])


def main():
    """Main function to run the DMR ID lookup tool."""
    ensure_venv()
    console = Console()

    parser = argparse.ArgumentParser(description="DMR ID Lookup Tool")
    parser.add_argument("--id", type=int, help="DMR ID to look up")
    parser.add_argument("--csv", type=str, help="Save output to CSV file")
    args = parser.parse_args()

    if args.id:
        data = lookup_by_id(args.id)
        if data:
            if args.csv:
                save_to_csv(data, args.csv)
                console.print(f"Data saved to {args.csv}")
            else:
                pretty_print(data)
        else:
            console.print("No data found for the specified DMR ID", style="red")
            sys.exit(1)
    else:
        console.print("Please provide a DMR ID using --id", style="yellow")
        sys.exit(1)

    return 0


if __name__ == "__main__":
    sys.exit(main()) 