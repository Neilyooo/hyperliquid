import logging

def setup_logger():
    """Configure the logger to output to both file and console."""
    logger = logging.getLogger('hyperliquid_monitor')
    logger.setLevel(logging.DEBUG)  # 设置为 DEBUG 级别以捕获更多信息
    
    # 文件处理器
    fh = logging.FileHandler('monitor.log')
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(fh_formatter)
    
    # 控制台处理器
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(ch_formatter)
    
    # 添加处理器
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
