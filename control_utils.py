from Organization import Organization

def command_input():
    command = input('Enter a command: ')

    while command.lower() not in ['quit', 'save', 'load', 'status', 'add user', 'add athlete', 'add run']:
        command = input('Invalid command. Enter a command: ')
    
    return command

def process_command(organization: Organization, command: str):
    
    match command:
        case 'status':
            return str(organization)
        
        case 'save':
            path = f'.\\save_data\\{organization.id}'
            
            organization.save_to_csv()

            return f'Organization data saved to {path}'

        case 'load':
            id = input('Organization ID: ')

            organization.load_from_csv(id)

            return f'Organization {organization.name} ({organization.id}) loaded successfully.'

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
        
        case _:
            return ''