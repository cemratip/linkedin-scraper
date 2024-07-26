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
    "http://ji6ncxkd45q9:ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-24111@proxy.oculus-proxy.com:31113",
    "http://ji6ncxkd45q9:ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-24112@proxy.oculus-proxy.com:31114",
    "http://ji6ncxkd45q9:ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-24113@proxy.oculus-proxy.com:31111",
    "http://ji6ncxkd45q9:ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-24114@proxy.oculus-proxy.com:31112",
    "http://ji6ncxkd45q9:ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-us-const-session-24115@proxy.oculus-proxy.com:31113"
]

company_urls = [
    'https://www.linkedin.com/company/slate-capital-group/',
    'https://www.linkedin.com/company/askmariatodd/',
    'https://www.linkedin.com/company/arkoma/',
    'https://www.linkedin.com/company/investment-management-partners/', 'https://www.linkedin.com/company/invest-in-turkey/', 'https://www.linkedin.com/company/investment-management-corporation-of-ontario/', 'https://www.linkedin.com/company/investment-bankers-forum/', 'https://www.linkedin.com/company/investment-planning-counsel/', 'https://www.linkedin.com/company/skills-investment-banking/', 'https://www.linkedin.com/company/barclays-investmentbank/', 'https://www.linkedin.com/company/axa-investment-managers/', 'https://www.linkedin.com/company/saudi-investment-bank/', 'https://www.linkedin.com/company/natixis-investment-managers/', 'https://www.linkedin.com/company/adia/', 'https://www.linkedin.com/company/lasalle-investment-management/', 'https://www.linkedin.com/company/uk-trade-&-investment/', 'https://www.linkedin.com/company/australian-trade-commission/', 'https://www.linkedin.com/company/gipc/', 'https://www.linkedin.com/company/triodos-investment-management-b.v./', 'https://www.linkedin.com/company/ubs-investment-bank/', 'https://www.linkedin.com/company/oman-investment-authority/', 'https://www.linkedin.com/company/children%27s-investment-fund-foundation-ciff-/', 'https://www.linkedin.com/company/sircsaudi/', 'https://www.linkedin.com/company/carnegie-investment-bank/', 'https://www.linkedin.com/company/flandersinvestmentandtrade/', 'https://www.linkedin.com/company/alberta-investment-management-corporation-aimco-/', 'https://www.linkedin.com/company/sharjah-investment-&-development-authority-shurooq-/', 'https://www.linkedin.com/company/insight-investment/', 'https://www.linkedin.com/company/angel-investment-network/', 'https://www.linkedin.com/company/marcellus-investment-managers/', 'https://www.linkedin.com/company/kuwait-investment-authority/', 'https://www.linkedin.com/company/tradeinvestqld/', 'https://www.linkedin.com/company/societegenerale-corporate-and-investment-banking/', 'https://www.linkedin.com/company/awqafinvestment/', 'https://www.linkedin.com/company/nn-investment-partners/', 'https://www.linkedin.com/company/european-investment-bank/', 'https://www.linkedin.com/company/asian-infrastructure-investment-bank-aiib-/', 'https://www.linkedin.com/company/natixis-corporate-investment-banking/', 'https://www.linkedin.com/company/investabudhabi/', 'https://www.linkedin.com/company/the-pri/', 'https://www.linkedin.com/company/british-international-investment/', 'https://www.linkedin.com/company/lombard-odier-investment-managers/', 'https://www.linkedin.com/company/norges-bank-investment-management/', 'https://www.linkedin.com/company/psinv/', 'https://www.linkedin.com/company/al-meezan-investment-management-limited/', 'https://www.linkedin.com/company/bidvbank/', 'https://www.linkedin.com/company/international-centre-for-settlement-of-investment-disputes/', 'https://www.linkedin.com/company/mfs-investment-management/', 'https://www.linkedin.com/company/ark-investment-management/', 'https://www.linkedin.com/company/fortress-investment-group/', 'https://www.linkedin.com/company/elliottinvestmentmanagementlp/', 'https://www.linkedin.com/company/k1im/', 'https://www.linkedin.com/company/hps-investment-partners-llc/', 'https://www.linkedin.com/company/psinv/', 'https://www.linkedin.com/company/al-meezan-investment-management-limited/', 'https://www.linkedin.com/company/bidvbank/', 'https://www.linkedin.com/company/international-centre-for-settlement-of-investment-disputes/', 'https://www.linkedin.com/company/mfs-investment-management/', 'https://www.linkedin.com/company/ark-investment-management/', 'https://www.linkedin.com/company/fortress-investment-group/', 'https://www.linkedin.com/company/elliottinvestmentmanagementlp/', 'https://www.linkedin.com/company/k1im/', 'https://www.linkedin.com/company/hps-investment-partners-llc/', 'https://www.linkedin.com/company/cdg-capital/', 'https://www.linkedin.com/company/project-a-ventures/', 'https://www.linkedin.com/company/amplifymeofficial/', 'https://www.linkedin.com/company/omrangroupom/', 'https://www.linkedin.com/company/cdc-group-plc/', 'https://www.linkedin.com/company/medallia-inc./', 'https://www.linkedin.com/company/shuaa-capital/', 'https://www.linkedin.com/company/norfund/', 'https://www.linkedin.com/company/insight--partners/', 'https://www.linkedin.com/company/balyasny-asset-management-l.p./']

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
