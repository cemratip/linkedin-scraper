import aiohttp
import asyncio
from bs4 import BeautifulSoup
import ssl
import time
import random
from aiohttp import ClientTimeout

# Bypass bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

# List of proxies
proxies = [
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-206d:ji6ncxkd45q9@proxy.oculus-proxy.com:31111",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-206e:ji6ncxkd45q9@proxy.oculus-proxy.com:31112",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-206f:ji6ncxkd45q9@proxy.oculus-proxy.com:31113",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-2070:ji6ncxkd45q9@proxy.oculus-proxy.com:31114",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-2071:ji6ncxkd45q9@proxy.oculus-proxy.com:31111"
]

company_urls = [
    'https://www.linkedin.com/company/slate-capital-group/',
    'https://www.linkedin.com/company/askmariatodd/',
    'https://www.linkedin.com/company/arkoma/',
    'https://www.linkedin.com/company/investment-management-partners/',
    'https://www.linkedin.com/company/invest-in-turkey/'
]

# Retry configuration
RETRY_LIMIT = 5
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 60  # seconds

proxy_index = 0
request_count = 0


def get_next_proxy():
    global proxy_index, request_count
    if request_count >= 3:
        proxy_index = (proxy_index + 1) % len(proxies)
        request_count = 0
    request_count += 1
    return proxies[proxy_index]


async def fetch(url, session, semaphore):
    async with semaphore:
        retry_delay = INITIAL_RETRY_DELAY
        for attempt in range(RETRY_LIMIT):
            proxy = get_next_proxy()
            try:
                async with session.get(url, proxy=proxy) as response:
                    if response.status == 429:
                        # Handle rate limiting
                        retry_after = response.headers.get('Retry-After')
                        if retry_after:
                            retry_delay = int(retry_after)
                        else:
                            retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)
                        print(f"Rate limit exceeded for {url}. Retrying in {retry_delay} seconds.")
                        await asyncio.sleep(retry_delay)
                    else:
                        response.raise_for_status()  # Raise an error for bad HTTP status codes
                        return await response.text()
            except Exception as e:
                if attempt < RETRY_LIMIT - 1:
                    retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)
                    print(f"Retrying {url} due to error: {e}. Retrying in {retry_delay} seconds.")
                    await asyncio.sleep(retry_delay + random.uniform(0, 1))  # Add a small random delay
                else:
                    print(f"Failed to fetch {url} after {RETRY_LIMIT} attempts: {e}")
                    return None


async def scrape_headcount(url, session, semaphore):
    print(f"Fetching {url}")
    start_time = time.time()
    html_content = await fetch(url, session, semaphore)

    if html_content:
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            element = soup.select_one(
                'main section:nth-of-type(1) section div div:nth-of-type(2) div:nth-of-type(2) ul li div a')
            headcount = element.text if element else 'N/A'
            headcount = headcount.replace('View all ', '').replace(' employees', '').replace('View ', '').replace(
                ' employee', '')
            print(headcount)
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            headcount = 'N/A'
    else:
        headcount = 'N/A'

    end_time = time.time()
    print(f"Time taken for {url}: {end_time - start_time} seconds")
    return headcount


async def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    timeout = ClientTimeout(total=60)
    semaphore = asyncio.Semaphore(5)  # Adjust based on server tolerance

    async with aiohttp.ClientSession(headers=HEADERS, connector=aiohttp.TCPConnector(ssl=ssl_context),
                                     timeout=timeout) as session:
        tasks = [scrape_headcount(url, session, semaphore) for url in company_urls]
        results = await asyncio.gather(*tasks)
        print(results)


# Run the main function within the event loop
if __name__ == "__main__":
    asyncio.run(main())
