from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chromedriver_path = 'C:/Users/nikit/Desktop/bsuir/Practice/Internet/selenium/chromedriver.exe'

options = webdriver.ChromeOptions()
options.binary_location = r'C:/Users/nikit/Downloads/chrome-win32/chrome-win32/chrome.exe'

service = webdriver.chrome.service.Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.google.com')

# Cookie
driver.add_cookie({'name': 'test_cookie_key', 'value': 'test_cookie_value'})
cookie = driver.get_cookie('test_cookie_key')
print(f"Cookie value: {cookie['value']}")
driver.delete_cookie('test_cookie_key')
cookie = driver.get_cookie('test_cookie_key')
print(f"Cookie value after deletion: {cookie}")

# LocalStorage
driver.execute_script("localStorage.setItem('test_key', 'test_value');")
value = driver.execute_script("return localStorage.getItem('test_key');")
print(f"LocalStorage value: {value}")
driver.execute_script("localStorage.removeItem('test_key');")
value = driver.execute_script("return localStorage.getItem('test_key');")
print(f"LocalStorage value after removal: {value}")

driver.quit()
