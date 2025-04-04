# Backend Setup

## Initial Setup
### Only complete these steps the first time you open the project

### Virtual environment
After you clone the repository to your machine, create your virtual environment:
```shell
cd backend
python -m venv .venv
```

### Folders
Within *backend*, create a folder called *input* - this is where you should put your videos that you plan to use.
In *backend/app*, create a folder called *database* - this is where you will create your local SQLite database.

### SQLite
Follow these steps to download and install SQLite: https://www.youtube.com/watch?v=-bDwNR_C0dE
- Make sure you add your SQLite folder to your path variable

## Backend startup
From *backend*, activate your virtual environment and install dependencies:

```shell
.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

To start the server, run the following in *backend*:
```shell
uvicorn app.main:app --reload
```

# Frontend startup
Navigate to *frontend/track-vip* and start the frontend:

```shell
npm install
npm run dev
```

