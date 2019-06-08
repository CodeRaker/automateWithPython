from selenium import webdriver
import time
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "C:\\Users\\LoL\\Desktop\\chromedriver.exe"
driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome("C:\\Users\\LoL\\Desktop\\chromedriver.exe")
driver.get("https://google.com")
driver.get("https://facebook.com")
dir(driver)
loginButton = driver.find_element_by_id("loginbutton")
loginButton.click()
inputElement = driver.find_element_by_id("email_container")
inputElement.send_keys("hallo")
inputElement = driver.find_element_by_id("email")
inputElement.send_keys("hallo")
