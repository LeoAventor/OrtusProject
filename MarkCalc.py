import os
import statistics
import re
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

#course_link = f"https://estudijas.rtu.lv/course/view.php?id={self.id}}"

#grade_links = f"https://estudijas.rtu.lv/grade/report/user/index.php?id={self.id}"

exams = {}
driver.get("https://ortus.rtu.lv/f/u108l1s22/normal/render.uP?pCt=rtu-eusso-studijas-info.u108l1n151")
driver.find_element(By.XPATH, f"//a[@href='/f/u108l1s22/p/rtu-eusso-studijas-info.u108l1n151/normal/action.uP?pP_action=info&pP_page=6']").click()
grade_table = driver.find_element(By.CLASS_NAME, "uportal-table")
subjects = grade_table.find_elements(By.TAG_NAME, "tr")
for subject in subjects:
    try:
        data_cells = subject.find_elements(By.TAG_NAME, "td")
        code = data_cells[0].text.strip()
        grade = float(data_cells[5].text.strip())
        exams[code] = grade
    except Exception as e:
        print(e)
#print(exams)

class Course:
    
    def __init__(self, id, classname):
        self.id = id
        self.classname = classname
        self.name = self.get_name()
        self.code = self.get_code()
        self.grades = self.get_grades()


    def get_name(self):
        driver.get("https://estudijas.rtu.lv/my/index.php")
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='https://estudijas.rtu.lv/course/view.php?id={self.id}']"))
        ).text
        return name
    
    def get_grades(self):
        driver.get(f"https://estudijas.rtu.lv/grade/report/user/index.php?id={self.id}")
        rows = driver.find_elements(By.CLASS_NAME, self.classname)
        
        grades = {}

        for row in rows:
            try:
                label = row.find_element(By.CLASS_NAME, "gradeitemheader").text.strip()
                grade_text = row.find_element(By.XPATH, ".//td[contains(@headers, 'grade')]").text.strip()
                if grade_text=="Ieskaitīts":
                    grade = 10.0
                else:
                    grade = float(grade_text.replace(',', '.')) if grade_text else 0.0
                grades[label] = grade
            except Exception as e:
                print(e)
        for exam in exams:
            if exam in self.code:
                grades["Eksāmens"] = exams[exam]
        return grades

    def formating(self): # formatēšanas metode priekš txt faila
        avg_grade = round(sum(self.grades.values()) / len(self.grades), 2) if self.grades else 0
        return f"{self.name:<25} | {avg_grade:<13}"
    
    def get_code(self):
        code = re.search(r"\([A-Z]{2}\d{4}\)", self.name)
        if code:
            code = code.group(0)
        else:
            code = "-"
        return code

class DatuStrukturas(Course):
    def calculate_final(self):
        #print(self.grades)
        L = [self.grades.get("Laboratorijas darbs Nr.1 (izpildīt klasē)", 0),
             self.grades.get("Uzdevums Nr.3 (Hash Table)", 0),
             self.grades.get("Patstavīgais darbs Nr.1", 0),
             self.grades.get("Laboratorijas darbs Nr.2 (atzīmes)", 0),
             self.grades.get("Paškontroles uzdevums Nr.3 (iesniegt TIKAI 1. un 2. grupai) (1. & 2. daļa, papilduzdevums; atzīmes)", 0)]
        Z = [self.grades.get("Zināšanu pārbaudes tests (18.03.2025)", 0),
             self.grades.get("2. Zināšanu pārbaude", 0),
             self.grades.get("Projekts (jāiesniedz GitHub saite un autoru vārdi)", 0)]
        E = self.grades.get("Eksāmens", 0)
        L = statistics.fmean(L)
        Z = statistics.fmean(Z)
        groups = [L, Z, E]
        weights = [0.3, 0.3, 0.4]
        final = statistics.fmean(groups, weights)
        return final


class DiskretaMatematika(Course):
    def calculate_final(self):
        K = [self.grades.get("Kontroldarbs Nr 1", 0),
             self.grades.get("Kontroldarbs Nr 2", 0),
             self.grades.get("Kontroldarbs Nr 3", 0)]
        M = self.grades.get("Mājasdarbi", 0)
        T = [self.grades.get("2025.g. Tests 1.1 \"Darbības ar kopām\" ( OBLIGĀTAIS ) - līdz 15.03.2025", 0),
             self.grades.get("Tests 2", 0),
             self.grades.get("Testi", 0),
             self.grades.get("Testi", 0)]
        E = self.grades.get("Eksāmens", 0)
        K = statistics.fmean(K)

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
        f.write(f"{'Course Name':<30} | {'Final Grade':<11}\n")
        f.write("-" * 60 + "\n")
        for course in courses:
            f.write(course.name  + " " * 10 + str(course.calculate_final()) + "\n")
        # Vidējā gala atzīme
        #avg_final = round(sum(c.calculate_final() for c in courses) / len(courses), 2) if courses else 0
        #f.write("\n")
        #f.write(f"Kopējā vidējā gala atzīme: {avg_final}\n")

courses = [
    DatuStrukturas(680502, "cat_579793")
    #DiskretaMatematika(695121, "cat_636085"),
    #Fizika(680310, "cat_579789"),
    #Matematika(680369, "cat_579791"),
    #OOP(680366, "cat_579790"),
    #Vides_un_klimata_celvedis(680306, "cat_579788"),
]
       
save_course_table(courses)


#driver.quit()

