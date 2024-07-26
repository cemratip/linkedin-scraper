import aiohttp
import asyncio
from bs4 import BeautifulSoup
import ssl
import time
from aiohttp import ClientTimeout
from asyncio import Semaphore

# Bypass bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

company_urls = [
    'https://www.linkedin.com/company/slate-capital-group/',
    'https://www.linkedin.com/company/askmariatodd/',
    'https://www.linkedin.com/company/arkoma/'
]*100

# Limit concurrency
CONCURRENT_REQUESTS = 10
SEMAPHORE = Semaphore(CONCURRENT_REQUESTS)

# Retry configuration
RETRY_LIMIT = 3
RETRY_DELAY = 2  # seconds

async def fetch(url, session):
    async with SEMAPHORE:
        for attempt in range(RETRY_LIMIT):
            try:
                async with session.get(url) as response:
                    response.raise_for_status()  # Raise an error for bad HTTP status codes
                    return await response.text()
            except Exception as e:
                if attempt < RETRY_LIMIT - 1:
                    print(f"Retrying {url} due to error: {e}")
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    print(f"Failed to fetch {url} after {RETRY_LIMIT} attempts: {e}")
                    return None

async def scrape_headcount(url, session):
    print(f"Fetching {url}")
    start_time = time.time()
    html_content = await fetch(url, session)
    
    if html_content:
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            element = soup.select_one('main section:nth-of-type(1) section div div:nth-of-type(2) div:nth-of-type(2) ul li div a')
            headcount = element.text if element else 'N/A'
            headcount = headcount.replace('View all ', '').replace(' employees', '').replace('View ', '').replace(' employee', '')
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
    async with aiohttp.ClientSession(headers=HEADERS, connector=aiohttp.TCPConnector(ssl=ssl_context), timeout=timeout) as session:
        tasks = []
        for url in company_urls:
            tasks.append(scrape_headcount(url, session))
            # Throttle requests: adjust delay as needed
            await asyncio.sleep(0.1)  # Adjust sleep to avoid overwhelming the server
        
        results = await asyncio.gather(*tasks)
        print(results)

# Run the main function
asyncio.run(main())
