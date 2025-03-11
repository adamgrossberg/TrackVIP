from app.validation import *
from app.Organization import Organization
from app.local_objects.User import User

VALID_COMMANDS = {
    'list': 'list valid commands',
    'quit': 'close the system', 
    'save': 'save current organization configuration',
    'status': 'see the current organization configuration',
    'add athlete': 'add an athlete to your organization',
    'add run': 'add a run to your organization',
    'edit athlete': 'edit an athlete in your organization',
    'edit run': 'edit a run in your organization',
    'delete athlete': 'remove an athlete from your organization',
    'delete run': 'remove a run from your organization'
    }

def load_organization() -> Organization:
    org = Organization('gttrack', 'Georgia Tech Track')
    org.load_from_db()
    return org

def select_user(organization: Organization) -> User:
    user_id = input('User ID: ')
    if user_id in organization.users.keys():
        return organization.users[user_id]
    else:
        while user_id not in organization.users.keys():
            user_id = input('Invalid User ID. Try again: ')
        return organization.users[user_id]

def command_input() -> str:
    command = input('Enter a command: ')

    while command.lower() not in VALID_COMMANDS.keys():
        command = input('Invalid command. Enter a command (Type \'list\' to see valid commands): ')
    
    return command

def process_command(organization: Organization, command: str) -> str:
    
    match command:
        case 'list':
            result = ''
            for name, description in VALID_COMMANDS.items():
                result += f'{name}: {description}\n'
            return result

        case 'status':
            return str(organization)
        
        case 'save':
            path = f'.\\save_data'
            
            organization.save_to_db()

            return f'Organization data saved to database.'
        
        case 'add athlete':
            id = input('Athlete ID: ')
            first_name = input('First name: ')
            last_name = input('Last name: ')

            valid, message = add_athlete_is_valid(organization, id)
            if not valid:
                return message
            else:
                organization.create_athlete(id, first_name, last_name)
                return f'Athlete {first_name} {last_name} ({id}) added auccessfully.'
        
        case 'add run':
            id = input('Run ID: ')
            athlete_id = input('Athlete ID: ')
            video_path = input('Video file name: ')
            video_path = './input/' + video_path

            valid, message = add_run_is_valid(organization, id, athlete_id, video_path)
            if not valid:
                return message
            else:
                organization.create_run(id, athlete_id, video_path)
                return f'Run {id} added successfully.'
        
        case 'edit athlete':
            id = input('Athlete ID: ')
            first_name = input('First name: ')
            last_name = input('Last name: ')

            valid, message = edit_athlete_is_valid(organization, id)
            if not valid:
                return message
            else:
                organization.edit_athlete(id, first_name, last_name)
                return f'Athlete {first_name} {last_name} ({id}) edited auccessfully.'
        
        case 'edit run':
            id = input('Run ID: ')
            athlete_id = input('Athlete ID: ')
            valid, message = edit_run_is_valid(organization, id, id)
            if not valid:
                return message
            else:
                organization.edit_run(id, id)
                return f'Run {id} edited successfully.'
        
        case 'delete athlete':
            id = input('Athlete ID: ')

            valid, message = delete_athlete_is_valid(organization, id)

            if not valid:
                return message
            else:
                organization.delete_athlete(id)
                return f'Successfully deleted athlete {id}.'
        
        case 'delete run':
            id = input('Run ID: ')

            valid, message = delete_run_is_valid(organization, id)

            if not valid:
                return message
            else:
                organization.delete_run(id)
                return f'Successfully deleted run {id}.'

        case _:
            return ''