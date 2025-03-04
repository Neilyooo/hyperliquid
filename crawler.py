import requests
from bs4 import BeautifulSoup
import json

def crawl_address(address):
    """Crawl operations for a specific address."""
    url = f"https://app.hyperliquid.xyz/explorer/address/{address}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
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
        except FileNotFoundError:
            last_hashes = []
        
        # Find new operations
        new_operations = [op for op in operations if op['hash'] not in last_hashes]
        
        # Update last known hashes
        with open(f'last_hashes_{address}.json', 'w') as f:
            json.dump([op['hash'] for op in operations], f)
        
        return new_operations
    except Exception as e:
        print(f"Error crawling address {address}: {e}")
        return []

def crawl_hash(hash):
    """Crawl detailed information for a specific hash."""
    url = f"https://app.hyperliquid.xyz/explorer/tx/{hash}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        overview = soup.find('div', class_='overview')
        if not overview:
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
        return details
    except Exception as e:
        print(f"Error crawling hash {hash}: {e}")
        return {}
