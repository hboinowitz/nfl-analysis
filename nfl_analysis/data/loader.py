import pandas as pd
import os


def load(table_name: str) -> pd.DataFrame:
    path = os.path.dirname(os.path.realpath(__file__))
    try:
        table = pd.read_parquet(os.path.join(path, f"{table_name}.parquet"))
        return table
    except FileNotFoundError:
        raise ValueError("The table with the given `table_name` does not exist.")
