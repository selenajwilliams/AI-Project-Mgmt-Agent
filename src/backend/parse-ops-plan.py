""" This file will read & process the strategic operations plan from google docs.
    Main functionality includes:
    1. Read the strategic ops plan from google docs
    2. Parse text from ops plan to contain title, description, deadline, importance
       urgency, owner
    3. prioritize the tasks according to deadline, importance, urgency
    4. write the prioritized task list to a UI -- for now this will be a google sheet
       eventually I can build this out to be a front end
"""