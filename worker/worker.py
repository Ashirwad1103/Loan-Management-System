# from ..app.queue import consumer
from app.queue import consumer

if __name__ == "__main__":
    consumer.start_worker()