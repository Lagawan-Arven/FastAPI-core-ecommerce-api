from slowapi import Limiter
from slowapi.util import get_remote_address
import logging,sys

'''
LIMITER CONFIGURATION
'''
limiter = Limiter(key_func=get_remote_address)

'''
LOGGING CONFIGURATION
'''
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

def setup_logging():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[logging.StreamHandler(sys.stdout)])

