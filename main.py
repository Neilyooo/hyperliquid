import json
from apscheduler.schedulers.blocking import BlockingScheduler
from crawler import crawl_address, crawl_hash
from logger import setup_logger
from notifier import send_notification

def main():
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Setup logger
    logger = setup_logger()
    
    def job():
        """Monitoring job to run periodically."""
        for item in config['addresses']:
            name = item['name']
            address = item['address']
            new_operations = crawl_address(address)
            if new_operations:
                for op in new_operations:
                    # Log basic operation info
                    log_message = f"{name} ({address}): New operation - Hash: {op['hash']}, Action: {op['action']}, Time: {op['time']}"
                    logger.info(log_message)
                    
                    # Fetch and log hash details
                    details = crawl_hash(op['hash'])
                    if details:
                        detail_message = f"Details - Action: {details.get('action', 'N/A')}, Limit Price: {details.get('limit_price', 'N/A')}, Size: {details.get('size', 'N/A')}"
                        logger.info(detail_message)
                        full_message = log_message + "\n" + detail_message
                    else:
                        full_message = log_message
                    
                    # Send notification
                    send_notification(config['notification'], full_message)
    
    # Schedule the job
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=config['crawl_interval'])
    print("Starting Hyperliquid Monitor...")
    scheduler.start()

if __name__ == '__main__':
    main()
