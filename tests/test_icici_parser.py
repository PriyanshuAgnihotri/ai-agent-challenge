import sys
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
