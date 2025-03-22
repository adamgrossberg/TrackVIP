# Backend Setup

## Virtual Environment

After you clone the repository to your machine, create your virtual environment in the *backend* folder (you should only need to do this once, the first time you open the project):

**$ python -m venv .venv**

Activate your local environment (you must do this every time you work on the project):

**$ .venv/Scripts/Activate.ps1**

Once the environment is activated, install all the needed dependencies:

**$ pip install -r requirements.txt**

## Folders
**These folders are included in the .gitignore file**

Create a folder called *input* - this is where you should put your videos that you plan to use.

In the *app* directory, create a folder called *database* - this is where you will create your local SQLite database.

## SQLite

Follow these steps to download SQLite: https://www.youtube.com/watch?v=-bDwNR_C0dE
- Make sure you add your SQLite folder to your path variable

To start the FastAPI server, run the following from the backend folder:

**$ uvicorn app.main:app --reload**

# Frontend Setup
Navigate to frontend/track-vip

## React App Initialization

**$ npm install**
Install all necessary npm modules

### control f http:// and change the address to whatever url your fastapi backend is running on.

### change line 10 in main.py to whatever server your react app runs on


**$ npm run dev**
Run the application locally
