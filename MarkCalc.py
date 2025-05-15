import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


driver = webdriver.Firefox()

driver.get("https://id2.rtu.lv/openam/UI/Login?module=LDAP&locale=lv")

load_dotenv()

login_field = driver.find_element(By.ID, "IDToken1")
password_field = driver.find_element(By.ID, "IDToken2")
login_field.send_keys(os.environ.get("login_name"))
password_field.send_keys(os.environ.get("password"))
submit_button = driver.find_element(By.NAME, "Login.Submit")
submit_button.click()
driver.get("https://estudijas.rtu.lv/my/")
visible_course_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='course_div' and not(@style='display: none;')]")))
course_links = visible_course_div.find_elements(By.TAG_NAME, "a")

for link in course_links:
    course_url = link.get_attribute("href")
    driver.get(course_url)

#driver.quit()
