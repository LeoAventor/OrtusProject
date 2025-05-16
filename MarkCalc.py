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
#visible_course_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='course_div' and not(@style='display: none;')]")))
course_links = ["https://estudijas.rtu.lv/course/view.php?id=680502",
                "https://estudijas.rtu.lv/course/view.php?id=695121",
                "https://estudijas.rtu.lv/course/view.php?id=680310",
                "https://estudijas.rtu.lv/course/view.php?id=680369",
                "https://estudijas.rtu.lv/course/view.php?id=680366", 
                "https://estudijas.rtu.lv/course/view.php?id=680306" ]

for link in course_links:
    driver.get(link)

#driver.quit()


# Datu struktūras un algoritmi: https://estudijas.rtu.lv/course/view.php?id=680502
# Diskrētā matemātika: https://estudijas.rtu.lv/course/view.php?id=695121
# Fizika: https://estudijas.rtu.lv/course/view.php?id=680310
# Matemātika: https://estudijas.rtu.lv/course/view.php?id=680369
# OOP: https://estudijas.rtu.lv/course/view.php?id=680366
# Vides un klimata ceļvedis: https://estudijas.rtu.lv/course/view.php?id=680306
