# INSTALL.md

## Prerequisites

- Node.js (vXX+): [Download here](https://nodejs.org)
- Python 3.12.8
- pip (Python package manager)
- Git
- ngrok (optional but recommended for backend exposure)

## Step 1: Clone the Repo

```bash
git clone https://github.com/AhmedAl-Hayali/GenreGuru.git
cd GenreGuru
```

## Step 2 (Optional): Install and Run the Backend

This step is only required if server is not currently running

```bash
cd src/server
pip install -r requirements.txt
python server.py
```

## Step 3: Install and Run the Frontend

```bash
cd src/client/genre-guru
npm install
npm run dev
```

Note: Client must have valid API authentication credentials. Refer to src/client/genre-guru/README.md to set up.
