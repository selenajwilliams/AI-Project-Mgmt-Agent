import gspread
from google.oauth2.service_account import Credentials

# code taken from this tutorial:
# YT: https://www.youtube.com/watch?v=zCEJurLGFRk
# github: https://github.com/techwithtim/Google-Sheets-API-Python/blob/main/main.py
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

SHEET_ID = "1Ajakctt9hGfP8Anwg3d7xiGS8cemBf5R3QyIcuq-fQA"
sheet = client.open_by_key(SHEET_ID)

values_list = sheet.sheet1.row_values(1)
print(values_list) 