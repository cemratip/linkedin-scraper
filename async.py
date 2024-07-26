import aiohttp
import asyncio
from bs4 import BeautifulSoup
import ssl
import time

# Bypass bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

company_urls = [
    'https://www.linkedin.com/company/slate-capital-group/',
    'https://www.linkedin.com/company/askmariatodd/',
    'https://www.linkedin.com/company/arkoma/'
]


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def scrape_headcount(url, session):
    print(f"Fetching {url}")
    start_time = time.time()
    try:
        html_content = await fetch(url, session)
        soup = BeautifulSoup(html_content, 'html.parser')

        element = soup.select_one(
            'main section:nth-of-type(1) section div div:nth-of-type(2) div:nth-of-type(2) ul li div a')
        headcount = element.text if element else 'N/A'

        headcount = headcount.replace('View all ', '').replace(' employees', '').replace('View ', '').replace(
            ' employee', '')
        print(headcount)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        headcount = 'N/A'

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return headcount


async def main():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(headers=HEADERS, connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        tasks = []
        for url in company_urls:
            tasks.append(scrape_headcount(url, session))

        results = await asyncio.gather(*tasks)
        print(results)


# Run the main function
asyncio.run(main())
