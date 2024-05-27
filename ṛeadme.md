## Setup and running steps
1. Clone the repository: `git clone <repo_url>`
2. create a virutal env 
    command - python3 -m venv venv
3. Install dependencies: `pip install -r requirements.txt`
4. Start the API server: `uvicorn main:app --reload`
5. set PYTHONPATH={path to root}
6. Start the message consumer: `python worker/worker.py`
7. Submit applications via API .

## Testing
Run tests using: when in root `python -m pytest`