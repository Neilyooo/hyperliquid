import json
from apscheduler.schedulers.blocking import BlockingScheduler
from crawler import crawl_address, crawl_hash
from logger import setup_logger
from notifier import send_notification
import time

logger = setup_logger()

def main():
    # Load configuration
    logger.info("Starting Hyperliquid Monitor...")
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        logger.debug(f"Loaded configuration: {config}")
    except Exception as e:
        logger.error(f"Failed to load config.json: {str(e)}")
        return
    
    # Extract crawl interval
    crawl_interval = config.get('crawl_interval', 30)  # Default to 30 seconds if not specified
    
    def job():
        """Monitoring job to run periodically."""
        logger.info(f"Starting monitoring job at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        start_time = time.time()
        
        for item in config['addresses']:
            name = item['name']
            address = item['address']
            logger.debug(f"Processing address: {name} ({address})")
            new_operations = crawl_address(address)
            if new_operations:
                for op in new_operations:
                    # Log basic operation info
                    log_message = f"{name} ({address}): New operation - Hash: {op['hash']}, Action: {op['action']}, Time: {op['time']}"
                    logger.info(log_message)
                    
                    # Fetch and log hash details
                    logger.debug(f"Fetching details for hash: {op['hash']}")
                    details = crawl_hash(op['hash'])
                    if details:
                        detail_message = f"Details - Action: {details.get('action', 'N/A')}, Limit Price: {details.get('limit_price', 'N/A')}, Size: {details.get('size', 'N/A')}"
                        logger.info(detail_message)
                        full_message = log_message + "\n" + detail_message
                    else:
                        full_message = log_message
                    
                    # Send notification
                    logger.debug(f"Sending notification for operation: {full_message}")
                    send_notification(config['notification'], full_message)
            else:
                logger.debug(f"No new operations found for address {address}")
        
        end_time = time.time()
        logger.debug(f"Job completed in {end_time - start_time} seconds")
    
    # Schedule the job
    logger.debug(f"Scheduling job with interval: {crawl_interval} seconds")
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=crawl_interval, max_instances=1)
    logger.info(f"Scheduled job to run every {crawl_interval} seconds")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Shutting down Hyperliquid Monitor...")
        scheduler.shutdown()

if __name__ == '__main__':
    main()
