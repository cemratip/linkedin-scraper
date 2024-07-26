import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

proxies_list = [
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba08:ji6ncxkd45q9@proxy.oculus-proxy.com:31112",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba09:ji6ncxkd45q9@proxy.oculus-proxy.com:31113",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba0a:ji6ncxkd45q9@proxy.oculus-proxy.com:31114",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba0b:ji6ncxkd45q9@proxy.oculus-proxy.com:31111",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba0c:ji6ncxkd45q9@proxy.oculus-proxy.com:31112"
]

def get_proxy(index):
    return proxies_list[index % len(proxies_list)]


def request_with_retries(url, headers, proxies, max_retries=5, initial_delay=1, max_delay=60):
    retries = 0
    delay = initial_delay
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            return response
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            retries += 1
            if retries < max_retries:
                # Wait before retrying
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                # Increase the delay exponentially, up to max_delay
                delay = min(max_delay, delay * 2)
            else:
                print("Max retries reached. Moving to the next request.")
                return None


session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

# Load the CSV file
input_file = "test-file-short.csv"  # Adjust the file path as necessary
df = pd.read_csv(input_file)

# Extract company names from URLs (simple example, adjust as needed)
company_urls = df['truncate'].apply(lambda x: x.split('//')[-1].split('/')[0]).tolist()

# Find LinkedIn URLs
start = time.time()
linkedin_urls = []
proxy_index = 0

for company in company_urls:
    proxy = get_proxy(proxy_index)
    proxy_index += 1

    url = f'https://www.google.com/search?q={company} site:linkedin.com'
    proxies = {'http': proxy, 'https': proxy}

    response = request_with_retries(url, session.headers, proxies)

    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            url = link.get('href')
            if url and "https://www.linkedin.com/company/" in url:
                linkedin_urls.append(url)
                break
    else:
        print(f"Failed to retrieve results for company: {company}")

end = time.time()

print(linkedin_urls)
print(f"Time taken: {end - start} seconds")
