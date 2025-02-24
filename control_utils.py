from Organization import Organization
import os

VALID_COMMANDS = {
    'list': 'list valid commands',
    'quit': 'close the system', 
    'save': 'save current organization configuration',
    'status': 'see the current organization configuration',
    'add user': 'add a user to your organization',
    'add athlete': 'add an athlete to your organization',
    'add run': 'add a run to your organization',
    'edit user': 'edit a user in your organization',
    'edit athlete': 'edit an athlete in your organization',
    'edit run': 'edit a run in your organization',
    'delete user': 'remove a user from your organization',
    'delete athlete': 'remove an athlete from your organization',
    'delete run': 'remove a run from your organization'
    }

def select_organization():
    while True:
        org_id = input('Organization ID: ')
        if os.path.exists(f'./save_data/{org_id}'):
            org = Organization('', '')
            org.load_from_csv(org_id)
            break
        else:
            retry_prompt = input('No existing organization with that ID. Do you want to create a new organization? (y/n) ')
            if retry_prompt.lower() == 'y':
                org_name = input("New organization name: ")
                org = Organization(org_id, org_name)
    print(f'{org.name} ({org.id}) loaded.')
    return org

def command_input():
    command = input('Enter a command: ')

    while command.lower() not in VALID_COMMANDS.keys():
        command = input('Invalid command. Enter a command (Type \'list\' to see valid commands): ')
    
    return command

def process_command(organization: Organization, command: str):
    
    match command:
        case 'list':
            result = ''
            for name, description in VALID_COMMANDS.items():
                result += f'{name}: {description}\n'
            return result

        case 'status':
            return str(organization)
        
        case 'save':
            path = f'.\\save_data\\{organization.id}'
            
            organization.save_to_csv()

            return f'Organization data saved to {path}'

        case 'add user':
            id = input('User ID: ')
            name = input('User name: ')
            can_view = input('Can view (y/n): ').lower()
            can_add = input('Can add (y/n): ').lower()
            can_view = can_view == 'y'
            can_add = can_add == 'y'

            organization.add_user(id, name, can_view, can_add)
            
            return f'User with ID {id} added successfully.'
        
        case 'add athlete':
            id = input('Athlete ID: ')
            first_name = input('First name: ')
            last_name = input('Last name: ')

            organization.add_athlete(id, first_name, last_name)
        
            return f'Athlete {first_name} {last_name} ({id}) added auccessfully.'
        
        case 'add run':
            id = input('Run ID: ')
            athlete_id = input('Athlete ID: ')
            video_path = input('Video file name: ')
            video_path = './input/' + video_path

            organization.add_run(id, athlete_id, video_path)

            return f'Run {id} added successfully.'
        
        case 'edit user':
            id = input('User ID: ')
            name = input('User name: ')
            can_view = input('Can view (y/n): ').lower()
            can_add = input('Can add (y/n): ').lower()
            can_view = can_view == 'y'
            can_add = can_add == 'y'

            organization.edit_user(id, name, can_view, can_add)
            
            return f'User with ID {id} edited successfully.'
        
        case 'edit athlete':
            id = input('Athlete ID: ')
            first_name = input('First name: ')
            last_name = input('Last name: ')

            organization.edit_athlete(id, first_name, last_name)
        
            return f'Athlete {first_name} {last_name} ({id}) edited auccessfully.'
        
        case 'edit run':
            id = input('Run ID: ')
            athlete_id = input('Athlete ID: ')

            organization.edit_run(id, athlete_id)

            return f'Run {id} edited successfully.'
        
        case 'delete user':
            id = input('User ID: ')

            organization.delete_user(id)

            return f'Succefully deleted user {id}.'
        
        case 'delete athlete':
            id = input('Athlete ID: ')

            organization.delete_athlete(id)

            return f'Succefully deleted athlete {id}.'
        
        case 'delete run':
            id = input('Run ID: ')

            organization.delete_run(id)

            return f'Succefully deleted run {id}.'

        case _:
            return ''