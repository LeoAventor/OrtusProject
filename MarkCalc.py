import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


courses={"Datu struktūras un algoritmi":{}, "Diskrētā matemātika":{}, "Fizika":{}, "Matemātika":{}, "Objektorientētā programmēšana":{}, "Vides un klimata ceļvedis":{}}

driver = webdriver.Firefox()

driver.get("https://id2.rtu.lv/openam/UI/Login?module=LDAP&locale=lv")

load_dotenv()

login_field = driver.find_element(By.ID, "IDToken1")
password_field = driver.find_element(By.ID, "IDToken2")
login_field.send_keys(os.environ.get("login_name"))
password_field.send_keys(os.environ.get("password"))
submit_button = driver.find_element(By.NAME, "Login.Submit")
submit_button.click()

course_link = ["https://estudijas.rtu.lv/course/view.php?id=680502",
                "https://estudijas.rtu.lv/course/view.php?id=695121",
                "https://estudijas.rtu.lv/course/view.php?id=680310",
                "https://estudijas.rtu.lv/course/view.php?id=680369",
                "https://estudijas.rtu.lv/course/view.php?id=680366",
                "https://estudijas.rtu.lv/course/view.php?id=680306"]

grade_links = ["https://estudijas.rtu.lv/grade/report/user/index.php?id=680502",
               "https://estudijas.rtu.lv/grade/report/user/index.php?id=695121",
               "https://estudijas.rtu.lv/grade/report/user/index.php?id=680310",
               "https://estudijas.rtu.lv/grade/report/user/index.php?id=680369",
               "https://estudijas.rtu.lv/grade/report/user/index.php?id=680366",
               "https://estudijas.rtu.lv/grade/report/user/index.php?id=680306"]

for link in grade_links:
    driver.get(link)
    atzimes=driver.find_elements(By.CLASS_NAME, "cat_579793")


#driver.quit()

class Course:
    def __init__(self, url, classname):
        self.url = url
        self.classname = classname
        self.name = self.get_name(url)
        self.grades = self.get_grades(classname)
        self.final_mark = self.get_final(self.grades, self.name)

    def get_grades(self, classname):
        grade_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, classname))
        )
        rows = grade_table.find_elements(By.CSS_SELECTOR, "tr")
        
        grades = {}
        for row in rows:
            try:
                label = row.find_element(By.CLASS_NAME, "gradeitemheader").text
                grade_text = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@headers='grade']"))
                )
                grade = float(grade_text.replace(',', '.')) if grade_text else 0.0
                grades[label] = grade
            except:
                continue
        return grades
    
    def get_final(self, grades, name):
        final = 0

    def get_name(self, url):
        driver.get("https://estudijas.rtu.lv/my/index.php")
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{url}']"))
        ).text
        return name

        