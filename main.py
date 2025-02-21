from Organization import Organization
from control_utils import *

org = Organization('vip', 'GT Track VIP')

command = command_input()

while command != 'quit':
    command_result = process_command(org, command)
    print(command_result)
    
    command = command_input()