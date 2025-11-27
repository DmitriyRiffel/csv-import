
import csv
from pathlib import Path
from typing import List, Tuple

from app.schemas.contract import ContractCSV

def validate_csv_file(path: Path) -> Tuple[List[ContractCSV], list]:
    results: List[ContractCSV] = []
    errors: list = []

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=",")

        for line_number, row in enumerate(reader, start=2):
            try:
                contract = ContractCSV(
                    contract_number=row["Vertragsnummer"],
                    start_date=row["Vertragsbeginn"],
                    end_date=row["Vertragsende"] or None,
                    status=row["Vertragsstatus"],
                )
                results.append(contract)
                
            except Exception as e:
                error = "; ".join([err["msg"] for err in e.errors()])
                errors.append({
                    "line": line_number,
                    "contract_number": row["Vertragsnummer"],
                    "error": error,
                })

    return results, errors