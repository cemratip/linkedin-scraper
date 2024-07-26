import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

proxies_list = [
    "http://aqroajvb:nidjeys54j7g@207.244.217.165:6712",
    "http://aqroajvb:nidjeys54j7g@134.73.69.7:5997",
    "http://aqroajvb:nidjeys54j7g@64.64.118.149:6732",
    "http://aqroajvb:nidjeys54j7g@157.52.253.244:6204",
    "http://aqroajvb:nidjeys54j7g@167.160.180.203:6754",
    "http://aqroajvb:nidjeys54j7g@166.88.58.10:5735",
    "http://aqroajvb:nidjeys54j7g@173.0.9.70:5653",
    "http://aqroajvb:nidjeys54j7g@204.44.69.89:6342",
    "http://aqroajvb:nidjeys54j7g@173.0.9.209:5792"
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
