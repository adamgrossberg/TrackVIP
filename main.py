from control_utils import *

org = select_organization()

command = ''
while command != 'quit':
    command = command_input()
    command_result = process_command(org, command)
    print(command_result)