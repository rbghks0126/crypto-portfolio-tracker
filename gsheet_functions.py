from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd


def get_gsheet_df(sheet_name):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'banterbuylowcrypto-f5c9f0d4f197.json', scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name)
    gsheet_instance = sheet.get_worksheet(0)

    # get all the records of the data
    records_data = gsheet_instance.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)
    return gsheet_instance, records_df


def update_gsheet(gsheet_instance, update_info):
    gsheet_instance.batch_update([{
        'range': 'A2:J71',
        'values': update_info,
    }])
