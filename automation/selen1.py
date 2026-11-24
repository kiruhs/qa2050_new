from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import Select

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
sname = driver.find_element(By.ID, 'sname')
sname.click()
sname.send_keys("Rothshield")
phone = driver.find_element(By.ID, 'postfix')
phone.click()
phone.send_keys("054888888")
inv_phone = driver.find_element(By.ID, 'errorPhoneInvalid')
if inv_phone.is_displayed():
    print("the first test is passed")
else:
    print("the first test is failed")
year = Select(driver.find_element(By.CLASS_NAME, 'year'))
year.select_by_value("1998")
sleep(0.5)
month = Select(driver.find_element(By.CLASS_NAME, 'month'))
month.select_by_value("04")
sleep(0.7)
day = Select(driver.find_element(By.CLASS_NAME, 'day'))
day.select_by_value("15")
driver.find_element(By.ID, 'submit-button').click()
sleep(1)

driver.find_element(By.XPATH, '//label[text()=" נקבה"]/span').click()
# go to the parent tag - //label[text()=' נקבה']/parent::*
# //input[@id='gender-input-1']/parent::*/span
# //input[@id='gender-input-1']/following-sibling::*[1]

inv_gender = driver.find_element(By.ID, 'errorGenderInvalid')
inv_disclaimer = driver.find_element(By.ID, 'error-disclaimer')
if inv_gender.is_displayed() and inv_disclaimer.is_displayed():
    print("The second test failed")
else:
    print("The second test passed")
sleep(5)