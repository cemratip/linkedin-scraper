from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# TODO: Bypass bot detection
# SET A REFERRER
# CHANGE USER AGENT
# CHANGE IP ADDRESS

def get_new_driver():
    # Initialize Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode to speed up
    driver = webdriver.Chrome(options=options)
    return driver

company_urls = ['https://www.linkedin.com/company/slate-capital-group/',
                'https://www.linkedin.com/company/askmariatodd/', 'https://www.linkedin.com/company/arkoma/']

# Scrape headcount for each company
data = []
driver = get_new_driver()
for i, url in enumerate(company_urls):
    # if i % 2 == 0 and i != 0:
    #     print('changing driver')
    #     driver.quit()
    #     driver = get_new_driver()

    print(url)
    a = time.time()
    driver.delete_all_cookies()
    driver.get(url)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/main/section[1]/section/div/div[2]/div[2]/ul/li/div/a'))
        )
        headcount = element.text
        print(headcount.replace('View all ', '').replace(' employees', '').replace('View ', '').replace(' employee', ''))
    except:
        print('N/A')

    b = time.time()
    print(b - a)

driver.quit()
