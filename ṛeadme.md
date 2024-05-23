## Setup and running steps
1. Clone the repository: `git clone <repo_url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the API server: `uvicorn main:app --reload`
4. set PYTHONPATH={path to root}
5. Start the message consumer: `python worker/worker.py`
6. Submit applications via API .

## Testing
Run tests using: when in root `python -m pytest`