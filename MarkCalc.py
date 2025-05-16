import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


#courses={"Datu struktūras un algoritmi":{}, "Diskrētā matemātika":{}, "Fizika":{}, "Matemātika":{}, "Objektorientētā programmēšana":{}, "Vides un klimata ceļvedis":{}}

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

#driver.quit()

class Course:
    
    def __init__(self, url, classname):
        self.url = url
        self.classname = classname
        self.name = self.get_name()
        self.grades = self.get_grades()
        #self.final = self.get_final()
        self.final = 0


    def get_name(self):
        driver.get("https://estudijas.rtu.lv/my/index.php")
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{self.url}']"))
        ).text
        return name
    
    def get_grades(self):
        grade_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.classname))
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
    
    def get_final(self):
        self.final = 0

    def formating(self): # formatēšanas metode priekš txt faila
        avg_grade = round(sum(self.grades.values()) / len(self.grades), 2) if self.grades else 0
        return f"{self.name:<25} | {avg_grade:<13} | {self.final_grade:<11}"
    

class DatuStrukturas(Course):
    def calculate_final(self):
        L = self.grades.get("Laboratorijas darbi", 0)
        Z = self.grades.get("Zināšanas pārbaude", 0)
        E = self.grades.get("Eksāmens", 0)
        self.final_grade = round(0.3 * L + 0.3 * Z + 0.4 * E, 2)


class DiskretaMatematika(Course):
    def calculate_final(self):
        K1 = self.grades.get("Kontroldarbs Nr 1", 0)
        K2 = self.grades.get("Kontroldarbs Nr 2", 0)
        K3 = self.grades.get("Kontroldarbs Nr 3", 0)
        M = self.grades.get("Mājasdarbi", 0)
        T = self.grades.get("Testi", 0)
        E = self.grades.get("Eksāmens", 0)
        K = (K1 + K2 + K3) / 3 if (K1 and K2 and K3) else 0

        if K1 < 4 or K2 < 4 or K3 < 4:
            self.final_grade = round(0.5 * E + 0.3 * K + 0.1 * M + 0.1 * T, 2)
        else:
            self.final_grade = round(0.3 * K1 + 0.2 * K2 + 0.3 * K3 + 0.1 * M + 0.1 * T, 2)

class Fizika(Course):
    def calculate_final(self):
        LB = self.grades.get("Laboratorijas darbi", 0)
        KD = self.grades.get("Kontroldarbi", 0)
        Eks = self.grades.get("Eksāmens", 0)
        # pārbaudām vai ir kāda zem 4
        low_score = any(g < 4 for g in [LB, KD, Eks] if g > 0)
        if low_score:
            self.final_grade = round(0.25 * LB + 0.25 * KD + 0.5 * Eks, 2)
        else:
            KDteor = self.grades.get("KD teorētiskie", 0)
            KDprakt = self.grades.get("KD praktiskie", 0)
            LD = self.grades.get("LD", 0)
            self.final_grade = round((KDteor + KDprakt + LD) / 3, 2)

class Matematika(Course):
    def calculate_final(self):
        E = self.grades.get("Eksāmens", 0)
        K = self.grades.get("Kontroldarbi", 0)
        M = self.grades.get("Mājasdarbi", 0)
        L = self.grades.get("Laboratorijas darbi", 0)
        T = self.grades.get("Testi", 0)
        self.final_grade = round(0.5 * E + 0.25 * K + 0.1 * M + 0.1 * L + 0.05 * T, 2)

class OOP(Course):
    def calculate_final(self):
        E = self.grades.get("Eksāmens", 0)
        L = self.grades.get("Laboratorijas darbi", 0)
        K = self.grades.get("Kontroldarbs", 0)
        B = 1
        # ja kāds mājasdarbs zem 4, tad bonuss = 0
        for k,v in self.grades.items():
            if "Mājasdarbs" in k and v < 4:
                B = 0
                break
        self.final_grade = round(0.3 * E + 0.4 * L + 0.25 * K + B, 2)

class Vides_un_klimata_celvedis(Course):
    def calculate_final(self):
        T = self.grades.get("Testi", 0)
        LS = self.grades.get("Lomu spēle", 0)
        E = self.grades.get("Eksāmens", 0)
        self.final_grade = round(0.45 * T + 0.25 * LS + 0.3 * E, 2)


def save_course_table(courses, filename="final_grades.txt"):
    with open(filename, "w", encoding='utf-8') as f:
        f.write(f"{'Course Name':<30} | {'Average Grade':<13} | {'Final Grade':<11}\n")
        f.write("-" * 60 + "\n")
        for course in courses:
            f.write(course.to_row() + "\n")
        # Vidējā gala atzīme
        avg_final = round(sum(c.final_grade for c in courses) / len(courses), 2) if courses else 0
        f.write("\n")
        f.write(f"Kopējā vidējā gala atzīme: {avg_final}\n")

def main():
    courses = [
        DatuStrukturas("https://estudijas.rtu.lv/grade/report/user/index.php?id=680502", "cat_579793"),
        DiskretaMatematika("https://estudijas.rtu.lv/grade/report/user/index.php?id=695121", "cat_636085"),
        Fizika("https://estudijas.rtu.lv/grade/report/user/index.php?id=680310", "cat_579789"),
        Matematika("https://estudijas.rtu.lv/grade/report/user/index.php?id=680369", "cat_579791"),
        OOP("https://estudijas.rtu.lv/grade/report/user/index.php?id=680366", "cat_579790"),
        Vides_un_klimata_celvedis("https://estudijas.rtu.lv/grade/report/user/index.php?id=680306", "cat_579788"),
    ]
       
    save_course_table(courses)







        
        