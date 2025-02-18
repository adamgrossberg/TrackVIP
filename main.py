from Run import Run

filename = input('Video filename: ')
path = f'./input/{filename}'

athlete_name = input('Athlete name: ')

testrun = Run(path, athlete_name)