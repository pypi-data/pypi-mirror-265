# entry should not be blank is the check

import pandas as pd


def missing_data_check(column_df):

    missing_data = column_df[column_df == ""]
    missing_rows = missing_data.index.tolist()

    if len(missing_rows) == 0:
        return True

    missing_count = len(missing_data)

    missing_rows = [x + 2 for x in missing_rows]

    return {"no of rows missing": missing_count,
            "rows_which_failed": missing_rows
            }
