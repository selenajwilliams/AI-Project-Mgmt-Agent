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
sheet = sheet.sheet1 # access first tab of the excel

# values_list = sheet.sheet1.row_values(1)
# values_list.extend(sheet.sheet1.row_values(2))
# print(values_list) 

## workflow:
## iniitial: read back end, populate front end

## starter code: reading in all info from the sheet
all_data = sheet.get_all_values()
header = all_data[0] if all_data else []
taskList = all_data[1:] if len(all_data) > 1 else []
print(header)
[print(task) for task in taskList]



def read_sheet():
    pass

def prioritize(tasks: list[list[str]]) -> list[list[str]]:
    """ Open API call to passing in the data with prompt to prioritize tasks 
        Returns prioritized task list
    """ 
    pass

def prioritize_sheet(tasks: list[list[str]]):
    """ Updates the sheet by re-ordering the tasks based on LLM determined priority
        Returns: nothing
    """ 
    pass

def update_task(task):
    """ Given a change to a single task, sends updated task info to the backend to update the sheet
    """

    def parse(task):
        """ Parses task from front-end format (maybe json?) to backend format (list of strings)
        """
        # TODO: fill this in
        return task
    
    
    def find_task_idx(task_name):
        """ Find's task index in the google sheet based on the task name
        """
        task_idx = None
        return task_idx

    task = parse(task)
    task_name = "" # TODO: Update this as needed! (task[0] or task[1]) task will be in order ID(?), Task, Description, Status, Priority, Due Date, Owner
    task_idx = find_task_idx(task)
    sheet.update(f'A{task_idx}', task)


# additional steps
## 1. back end changes --> UI updates
## 2. UI changes --> back end updates
##    if someone adds a task from the front end, it will trigger this 
## 3. stretch goal: ops plan changes --> back end changes
