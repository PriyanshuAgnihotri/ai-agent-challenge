import argparse
import subprocess
import sys
from pathlib import Path

def run_tests(target: str) -> bool:
    """Run pytest for the target bank parser."""
    result = subprocess.run(
        ["pytest", f"tests/test_{target}_parser.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    return result.returncode == 0

def generate_parser(target: str):
    """Generate a parser file for the given bank."""
    parser_path = Path(f"custom_parsers/{target}_parser.py")

    code = '''import pdfplumber
import pandas as pd

def parse(pdf_path: str) -> pd.DataFrame:
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                # Skip header row
                for row in table[1:]:
                    rows.append(row)

    # Normalize rows into DataFrame
    df = pd.DataFrame(rows, columns=["Date", "Description", "Debit Amt", "Credit Amt", "Balance"])
    return df
'''
    parser_path.write_text(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    # self-correct loop
    for attempt in range(3):
        generate_parser(args.target)
        if run_tests(args.target):
            print("✅ Parser works correctly!")
            sys.exit(0)
        print(f"❌ Attempt {attempt+1} failed, retrying...")

    sys.exit(1)
