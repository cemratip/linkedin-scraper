import requests

test_proxies = [
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba08:ji6ncxkd45q9@proxy.oculus-proxy.com:31112",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba09:ji6ncxkd45q9@proxy.oculus-proxy.com:31113",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba0a:ji6ncxkd45q9@proxy.oculus-proxy.com:31114",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba0b:ji6ncxkd45q9@proxy.oculus-proxy.com:31111",
    "http://ba13396172373555b0b863c3af19140f1c50faec8d488802c91af43e969e797d015ab7eda42fcc9e52c91f64a3c28ca3-country-se-const-session-6ba0c:ji6ncxkd45q9@proxy.oculus-proxy.com:31112"
]

def test_proxy(proxy):
    try:
        response = requests.get('http://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Proxy test failed: {proxy} - {e}")
        return False

for proxy in test_proxies:
    if test_proxy(proxy):
        print(f"Proxy working: {proxy}")
    else:
        print(f"Proxy not working: {proxy}")
