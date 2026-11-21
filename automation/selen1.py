from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
driver = webdriver.Chrome()
driver.maximize_window()
# url = "https://google.com"
url = "https://www.walla.co.il/"
driver.get(url)
search = driver.find_element(By.CLASS_NAME, 'styles_mailTitle__k3w_B')
search.click()
sleep(1)
driver.find_element(By.XPATH, '/html/body/app-root/div/div/div[1]/main/div[1]/app-login/div/div/section/fieldset/a').click()
sleep(1)
user = driver.find_element(By.ID, 'username')
user.click()
user.send_keys("test2050")
pswd = driver.find_element(By.CLASS_NAME, 'password-field')
pswd.click()
pswd.send_keys('zxpQ45#00')
fname = driver.find_element(By.ID, 'fname')
fname.click()
fname.send_keys('Alexander')
sleep(5)