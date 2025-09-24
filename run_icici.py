from pathlib import Path
import subprocess
import sys

def run_tests() -> bool:
    """Run pytest for ICICI parser."""
    result = subprocess.run(
        ["pytest", "tests/test_icici_parser.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    return result.returncode == 0

def generate_icici_parser():
    """Generate ICICI parser with Debit/Credit auto-detection."""
    parser_dir = Path("custom_parsers")
    parser_dir.mkdir(parents=True, exist_ok=True)

    # ✅ make it a package
    init_file = parser_dir / "__init__.py"
    init_file.touch(exist_ok=True)

    parser_path = parser_dir / "icici_parser.py"

    code = '''import pdfplumber
import pandas as pd

def parse(pdf_path: str) -> pd.DataFrame:
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:
                    # Normalize Debit/Credit values (if one is missing, set to 0)
                    date, desc, debit, credit, balance = row
                    debit = float(debit) if debit not in (None, "", "-") else 0.0
                    credit = float(credit) if credit not in (None, "", "-") else 0.0
                    balance = float(balance) if balance not in (None, "", "-") else 0.0
                    rows.append([date, desc, debit, credit, balance])

    df = pd.DataFrame(rows, columns=["Date", "Description", "Debit Amt", "Credit Amt", "Balance"])
    return df
'''
    parser_path.write_text(code, encoding="utf-8")


def generate_icici_test():
    """Generate pytest for ICICI parser."""
    test_dir = Path("tests")
    test_dir.mkdir(parents=True, exist_ok=True)

    test_path = test_dir / "test_icici_parser.py"

    code = '''import sys
import pathlib
import pandas as pd

#  add project root to sys.path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from custom_parsers.icici_parser import parse

def test_icici_parser():
    pdf_path = "data/icici/icici sample.pdf"
    csv_path = "data/icici/result.csv"

    expected = pd.read_csv(csv_path)
    result = parse(pdf_path)

    # Align columns
    result.columns = expected.columns

    #  normalize: treat NaN and 0.0 as equal
    expected = expected.fillna(0.0)
    result = result.fillna(0.0)

    pd.testing.assert_frame_equal(result, expected, check_dtype=False)
'''
    test_path.write_text(code, encoding="utf-8")



if __name__ == "__main__":
    print("🚀 Generating ICICI parser and tests...")
    for attempt in range(3):
        generate_icici_parser()
        generate_icici_test()
        if run_tests():
            print("✅ ICICI parser works correctly!")
            sys.exit(0)
        print(f"❌ Attempt {attempt+1} failed, retrying...")

    sys.exit(1)
