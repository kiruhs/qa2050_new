from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as WW
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.youtube.com/watch?v=voO12-fh-eU")

try:
    elem = WW(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="title"]/h1/yt-formatted-string'))
        )
except NoSuchElementException:
    print("Sorry, no such element on this site")
    quit(0)

body  = driver.find_element(By.TAG_NAME, 'body')

while True:
    try:
        body.send_keys(Keys.ARROW_DOWN)
        cnt = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]')
        print(f"There are {cnt.text} comments")
        break
    except NoSuchElementException:
        pass
sleep(1)

driver.execute_script("window.open('https://google.com', '_blank')")
sleep(1)
driver.switch_to.window(driver.window_handles[1])
driver.find_element(By.XPATH, '/html/body/div[2]/div[6]/form/div[1]/div/div[4]/center/input[2]').click()


sleep(5)