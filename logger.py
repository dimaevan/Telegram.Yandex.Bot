import logging

LOGGER_FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename="LOG.txt", filemode='w',
                    format=LOGGER_FORMAT, datefmt='[%H:%M:%S]')
log = logging.getLogger()
log.setLevel(logging.INFO)
