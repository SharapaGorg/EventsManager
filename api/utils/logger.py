import logging

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log', filemode='a', format=LOG_FORMAT)
logger = logging.getLogger()
