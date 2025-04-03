from app.control_utils import *
from fastapi import FastAPI
from app.routes import athletes, runs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(athletes.router, prefix="/athletes", tags=["Athletes"])
app.include_router(runs.router, prefix="/runs", tags=["Runs"])

# print(f'Successfully loaded {org.name}')

# user = select_user(org)
# print(f'Welcome, {user.name}')

# command = ''
# while command != 'quit':
#     print()
#     command = command_input()
#     command_result = process_command(org, command)
#     print(command_result)