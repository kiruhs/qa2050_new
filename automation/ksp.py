from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("user-data-dir=./chrome-profile")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-pipe")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://ksp.co.il/")
sleep(1)

# driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ENTER)
driver.find_element(By.CLASS_NAME, 'ksp-cc-btn').click()
sleep(1)

driver.find_element(By.XPATH, '//*[@id="site-header"]/div/div/div[1]/nav/button').click()
sleep(100)
first = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/header/div[3]/div/div/div[1]/nav/div/ul[1]/li[1]/a/div[2]/span')
                                         

ActionChains(driver).move_to_element(first).perform()

sleep(5)