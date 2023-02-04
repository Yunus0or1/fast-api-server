import os
from dotenv import load_dotenv, find_dotenv
from currency.util.log import log

load_dotenv(find_dotenv())

ERROR_MESSAGE = "=> ERROR IN Loading Environment File in main.py. Please check if .env file exists and start the server again"


class Config:
    def __init__(self):
        try:
            self.PORT = int(os.environ.get("PORT"))
            self.DEBUG = os.environ.get("DEBUG")
        except Exception as error:
            log.error('Error in Config init => ', error)
            raise SystemExit(ERROR_MESSAGE)

    def verify(self):
        # Checking all the ENV variables exist or not
        if self.PORT == None:
            raise SystemExit(ERROR_MESSAGE)
        else:
            log.info('=> Loaded ENV Variables')
