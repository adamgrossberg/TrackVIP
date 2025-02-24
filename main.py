from Organization import Organization
from control_utils import *
import os
import numpy as np

org_id = input('Organization ID: ')

if os.path.exists(f'./save_data/{org_id}'):
    org = Organization('', '')
    org.load_from_csv(org_id)
else:
    org_name = input("No existing organization with that ID. New organization name: ")
    org = Organization(org_id, org_name)

command = command_input()

while command != 'quit':
    command_result = process_command(org, command)
    print(command_result)

    command = command_input()