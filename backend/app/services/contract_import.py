
import csv
from pathlib import Path
from typing import List, Tuple

from pydantic import ValidationError

from app.schemas.contract import ContractCSV

def validate_csv_file(path: Path) -> Tuple[List[ContractCSV], list]:
    """
    Read and validate a CSV file of contracts.

    Return: 
        - a list of valid ContractCSV objects
        - a list of error dictionaries describing validation issues
    """
    results: List[ContractCSV] = []
    errors: list = []

    # Open the CSV file for reading
    with path.open("r", encoding="utf-8", newline="") as f:
        # DictReader reads the first row as header and returns each subsequent
        # row as a dict mapping column names to values.
        reader = csv.DictReader(f, delimiter=",")

        # Enumerate the rows starting from line 2, because line 1 is the header.
        for line_number, row in enumerate(reader, start=2):
            try:
                # Create a Pydantic model instance from the CSV row.
                # ContractCSV will validate the types.
                contract = ContractCSV(
                    contract_number=row["Vertragsnummer"],
                    start_date=row["Vertragsbeginn"],
                    end_date=row["Vertragsende"] or None,
                    status=row["Vertragsstatus"],
                )
                # Add the validated contract to the results list.
                results.append(contract)
                

            except ValidationError as e:
                # If Pydantic validation fails, collect all error messages.
                error = "; ".join([err["msg"] for err in e.errors()])
                errors.append({
                    "line": line_number, # line numer in the CSV file
                    "contract_number": row["Vertragsnummer"],
                    "error": error,
                })
                # Skip to the next row
                continue
            except KeyError as e: 
                # KeyError means a required column header is missing or misspelled.
                errors.append({
                    "error": f"Die Spalte '{e.args[0]}' ist fehlerhaft / fehlt."
                })
                # Stop processing further rows because the structure is invalid.
                break

    # Returns both valid contracts and all collected errors.
    return results, errors