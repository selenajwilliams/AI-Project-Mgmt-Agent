from openai import OpenAI
from api_keys import OPENAI_API_KEY
import sys
import pprint

client = OpenAI(api_key=OPENAI_API_KEY)
import os
from api_keys import OPENAI_API_KEY

# openai.api_key = os.getenv("OPENAI_API_KEY")

def prioritize(tasks: list[list[str]]) -> list[list[str]]:
    prompt = "Prioritize the following tasks from most to least important. Return only the ordered list of IDs:\n\n"
    for row in tasks:
        prompt += f"ID: {row[0]}, Task: {row[1]}, Status: {row[3]}, Priority: {row[4]}, Due: {row[5]}, Owner: {row[6]}\n"
    
    prompt += "\nList only the IDs in order (comma-separated):"

    messages=[{"role": "system", "content": "You are a task prioritization assistant."},
              {"role": "user", "content": prompt}]

    response = client.responses.create(
        model="gpt-4.1",
        input=messages
    )

    # pprint.pprint(f'******************\n{response}')
    # pprint.pprint(f'\n{response.output_text}')
    # sys.exit()

    id_order = response.output_text
    print(id_order)
    id_order = [id.strip() for id in id_order.split(',')] 
    # id_order = [id.strip() for id in id_order]
    pprint.pprint(f'cleaned ID order: {id_order}')

    id_to_task = {row[0]: row for row in tasks}
    pprint.pprint(f'id_to_task: {id_to_task}')
    return [id_to_task[i] for i in id_order if i in id_to_task]

if __name__ == "__main__":
    # unit testing prioritize tasks function given a data from a google sheet
    from sheet_utils import read_sheet
    header, tasks = read_sheet()
    ptasks = prioritize(tasks)
    print(f'\n\nfinalized prioritized tasks:')
    [print(t) for t in ptasks]

    # I have qualitatively tested that this achieves desired functionality


