from control_utils import *

org = load_organization()
print(f'Successfully loaded {org.name}')

user = select_user(org)
print(f'Welcome, {user.name}')

command = ''
while command != 'quit':
    print()
    command = command_input()
    command_result = process_command(org, command)
    print(command_result)