import os
from dotenv import load_dotenv, find_dotenv
from currency.util.log import log

load_dotenv(find_dotenv())


PORT = int(os.environ.get("PORT"))
DEBUG = os.environ.get("DEBUG")
CONVERTER_API = os.environ.get("CONVERTER_API")
CONVERTER_API_KEY = os.environ.get("CONVERTER_API_KEY")

ERROR_MESSAGE = "=> ERROR IN Loading Environment File in main.py. Please check if .env file exists and start the server again"
def verify():
    pass
    # Checking all the ENV variables exist or not
    if PORT == None or CONVERTER_API == None or CONVERTER_API_KEY == None:
        raise SystemExit(ERROR_MESSAGE)
    else:
        log.info('=> Loaded ENV Variables')
