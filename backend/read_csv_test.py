from pathlib import Path
from app.services.contract_import import validate_csv_file
from app.schemas.contract import ContractCSV
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "data" / "table1.csv"

valid, errors = validate_csv_file(csv_path)

print("\n Valid rows:")
for item in valid:
    print(item)

print("\n Error rows:")
for err in errors:
    print(f"Row {err['line']}: {err['error']}")
    print(f"  Data: {err['raw']}")