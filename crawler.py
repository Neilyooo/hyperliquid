import requests
from bs4 import BeautifulSoup
import json
import logging

logger = logging.getLogger('hyperliquid_monitor')

def crawl_address(address):
    """Crawl operations for a specific address."""
    logger.debug(f"Starting to crawl address: {address}")
    url = f"https://app.hyperliquid.xyz/explorer/address/{address}"
    try:
        logger.debug(f"Sending GET request to {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.debug(f"Successfully fetched data from {url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            logger.warning(f"No table found for address {address}")
            return []
        rows = table.find_all('tr')
        operations = []
        for row in rows[1:]:  # Skip header
            cols = row.find_all('td')
            if len(cols) >= 4:
                hash = cols[0].text.strip()
                action = cols[1].text.strip()
                time = cols[3].text.strip()
                operations.append({'hash': hash, 'action': action, 'time': time})
        
        # Load last known hashes
        try:
            with open(f'last_hashes_{address}.json', 'r') as f:
                last_hashes = json.load(f)
            logger.debug(f"Loaded last hashes for {address}: {last_hashes}")
        except FileNotFoundError:
            last_hashes = []
            logger.debug(f"No previous hashes found for {address}")
        
        # Find new operations
        new_operations = [op for op in operations if op['hash'] not in last_hashes]
        logger.debug(f"Found {len(new_operations)} new operations for {address}")
        
        # Update last known hashes
        with open(f'last_hashes_{address}.json', 'w') as f:
            json.dump([op['hash'] for op in operations], f)
        logger.debug(f"Updated last hashes file for {address}")
        
        return new_operations
    except Exception as e:
        logger.error(f"Error crawling address {address}: {str(e)}")
        return []

def crawl_hash(hash):
    """Crawl detailed information for a specific hash."""
    logger.debug(f"Starting to crawl hash: {hash}")
    url = f"https://app.hyperliquid.xyz/explorer/tx/{hash}"
    try:
        logger.debug(f"Sending GET request to {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.debug(f"Successfully fetched data for hash {hash}")
        soup = BeautifulSoup(response.text, 'html.parser')
        overview = soup.find('div', class_='overview')
        if not overview:
            logger.warning(f"No overview found for hash {hash}")
            return {}
        details = {}
        for item in overview.find_all('div', class_='detail-item'):
            label = item.find('span', class_='label')
            value = item.find('span', class_='value')
            if label and value:
                label_text = label.text.strip()
                value_text = value.text.strip()
                if label_text == 'Action':
                    details['action'] = value_text
                elif label_text == 'Limit Price':
                    details['limit_price'] = value_text
                elif label_text == 'Size':
                    details['size'] = value_text
        logger.debug(f"Parsed details for hash {hash}: {details}")
        return details
    except Exception as e:
        logger.error(f"Error crawling hash {hash}: {str(e)}")
        return {}
