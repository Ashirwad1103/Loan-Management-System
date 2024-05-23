import atexit
import json
import logging.config
import logging.handlers
import pathlib

def setup_logging():
    try:
        config_file = pathlib.Path("configs/log_config.json")
        with open(config_file) as f_in:
            config = json.load(f_in)

        logging.config.dictConfig(config)
    except Exception as e:
        logging.error(f"Error setting up logging: {e}")

 
# setup_logging()

if __name__ == "__main__":
    setup_logging()