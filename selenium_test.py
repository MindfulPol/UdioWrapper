from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

options = Options()
options.log.level = "trace"
service = Service(executable_path='/usr/bin/geckodriver')  
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://www.google.com/")

driver.implicitly_wait(500)



time.sleep(60)  

driver.quit()