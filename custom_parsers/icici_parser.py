import pdfplumber
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
