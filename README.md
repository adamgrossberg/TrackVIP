# Environment Setup

## Virtual Environment

After you clone the repository to your machine, create your virtual environment (you should only need to do this once, the first time you open the project):

**$ python -m venv .venv**

To activate your local environment (you must do this every time you work on the project):

**$ .venv/Scripts/Activate.ps1**

Once the environment is activated, install all the needed dependencies:

**$ pip install -r requirements.txt**

## Folders
**These folders are included in the .gitignore file**

Create a folder called *input* - this is where you should put your videos that you plan to use.

Create a folder called *database* - this is where you will create your local SQLite database.

## SQLite

Follow these steps to download SQLite: https://www.youtube.com/watch?v=-bDwNR_C0dE
- Make sure you add your SQLite folder to your path variable

### Add system users

Run *main.py* once, then quit immediately. This will create your database. Open a command prompt in your *database* folder. Run the following command to enter your database:

**$ sqlite3 gttrack.db**

Within the SQLite CLI, insert your users using SQL:

**INSERT INTO USERS VALUES('<id>', '<name>')**