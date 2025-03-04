import logging

def setup_logger():
    """Configure the logger to output to a file."""
    logger = logging.getLogger('hyperliquid_monitor')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('monitor.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
