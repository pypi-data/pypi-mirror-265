from src.justogres.spreadsheets import SpreadSheets
import unittest

from datetime import datetime
import pandas as pd

class TestInsertDataFrame(unittest.TestCase):

    def test_insertDF(self):
        data = [[datetime.now(), "2402,57", 24123, 2402.57]]
        columns = ["date","str","int","float"]

        df = pd.DataFrame(data=data, columns=columns)

        spread_sheet_client = SpreadSheets("/Users/joseizam/Desktop/GitHub/justo-bi/sql-tables/utils/credentials.json")
        spreadsheet_id = '1ezD3tSpj6pT9YoGqn8MrVtL52aWlf60HVjQuOj1m7M0'
        worksheet_name = 'Test23'

        a = spread_sheet_client.append_dataframe(df, spreadsheet_id, worksheet_name)
        print(a, type(a))


if __name__ == '__main__':
    unittest.main()