import requests

def send_get_request(url, query_params):
    # Define the headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'http://94.237.63.109:36796/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i'
    }

    proxies = {
    'http': 'http://127.0.0.1:8080',  # Replace with your proxy's address
    'https': 'http://127.0.0.1:8080',  # Replace with your proxy's address
}

    # Send the GET request with query parameters
    response = requests.get(url, headers=headers, params=query_params, proxies=proxies)

    # Print the response
    print('Status Code:', response.status_code)
    print('Response Body:', response.text)

# Use the function
url = "http://94.237.63.109:36796/"
query_params = {'q[regex]/.*/': 'honey'}

send_get_request(url, query_params)
