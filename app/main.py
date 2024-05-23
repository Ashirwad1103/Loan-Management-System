from fastapi import FastAPI
from .api.api import router
from .db.session import init_db
from setup_logging import setup_logging
from .middlewares.execution_time_middleware import ExecutionTimeMiddleware
from dotenv import load_dotenv

app = FastAPI()

app.include_router(router)

app.add_middleware(ExecutionTimeMiddleware)
@app.on_event("startup")
def on_startup():
    load_dotenv()
    init_db()
    setup_logging()
