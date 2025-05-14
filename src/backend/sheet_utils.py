import gspread
from google.oauth2.service_account import Credentials
import os

# === GOOGLE SHEET CONFIG ===
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


credentials_path = "/etc/secrets/credentials.json"
if not os.path.exists(credentials_path):
    raise RuntimeError(f"Missing secret file at {credentials_path}")
CREDS = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
# CREDS = Credentials.from_service_account_file("/etc/secrets/credentials.json", scopes=SCOPES)

CLIENT = gspread.authorize(CREDS)
SHEET_ID = os.environ["SHEET_ID"]


SHEET = CLIENT.open_by_key(SHEET_ID).sheet1

def read_sheet():
    data = SHEET.get_all_values()
    header = data[0]
    rows = data[1:]
    return header, rows

def update_task(task_id, updated_row):
    all_data = SHEET.get_all_values()
    for i, row in enumerate(all_data[1:], start=2):  # start=2 to account for header + 1-indexing
        if row[0] == str(task_id):
            SHEET.update(f'A{i}:G{i}', [updated_row])
            return True
    return False

def prioritize_sheet(prioritized_tasks):
    SHEET.batch_update([{
        'range': f'A2:G{len(prioritized_tasks)+1}',
        'values': prioritized_tasks
    }])


if __name__ == "__main__":
    # unit testing read_sheet 
    header, rows = read_sheet()
    print(header)
    [print(row) for row in rows]
