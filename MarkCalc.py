import os
import statistics
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv


firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)

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
    
    def get_code(self):
        code = re.search(r"\([A-Z]{2}\d{4}\)", self.name)
        if code:
            code = code.group(0)
        else:
            code = "-"
        return code

class DatuStrukturas(Course):
    def calculate_final(self):
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
        K1 = self.grades.get("1. starpeksāmens - Kopas, attēlojumi, attieksmes.", 0)
        K2 =self.grades.get("2. starpeksāmens - Kombinatorika.", 0)
        K3 = self.grades.get("3. starpeksāmens - Būla funkcijas.", 0)
        M = [self.grades.get("MD \"Matemātiskā indukcija\"", 0),
             self.grades.get("MD \"Stingra sakārtojuma algoritms\"", 0),
             self.grades.get("MD \"Būla funkcijas\"", 0)]
        T = [self.grades.get("2025.g. Tests 1.1 \"Darbības ar kopām\" ( OBLIGĀTAIS ) - līdz 15.03.2025", 0),
             self.grades.get("2025.g. Tests 1.2 \"Kopu attēlojumi un attieksmes\" ( OBLIGĀTAIS ) - līdz 15.03.2025", 0),
             self.grades.get("2025.g. Teorijas tests \"Kopu teorija\" ( OBLIGĀTAIS ) - līdz 15.Mar.2025", 0),
             self.grades.get("Teorijas tests \"Kombinatorika\" ( OBLIGĀTAIS ) - līdz 23.Apr.2025", 0),
             self.grades.get("2.2. Izlases ( OBLIGĀTAIS ) - līdz 23.04.2025", 0),
             self.grades.get("7. Pilnās sistēmas ( OBLIGĀTAIS ) - līdz 21.05.2025", 0),
             self.grades.get("Teorijas tests \"Matemātiskā loģika\" ( OBLIGĀTAIS ) - līdz 29.05.2025", 0)]
        M = statistics.fmean(M)
        T = statistics.fmean(T)

        if K1 >= 4 and K2 >= 4 and K3 >= 4:
            groups = [ K1, K2, K3 ,M, T,]
            weights= [0.3, 0.2, 0.3, 0.1, 0.1]
        else:
            E = self.grades.get("Eksāmens", 0)
            groups = [K1, K2, K3, M, T, E ]
            weights= [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]

        final = statistics.fmean(groups,weights)
        return final
    

class Fizika(Course):
    def calculate_final(self):

        LD = self.grades.get("Lab. Darbi", 0)
        K = [self.grades.get("I teorijas KD", 0),
             self.grades.get("II teorijas KD", 0),
             self.grades.get("P KD I", 0),
             self.grades.get("P KD II", 0)]
        if LD >= 4 and min(K) >= 4:
            K = statistics.fmean(K)
            if statistics.fmean([LD,K]) >= 5.5:
                groups = [K, LD]
                weights = [2/3, 1/3]
                final = statistics.fmean(groups, weights)
                return final
        E = self.grades.get("Eksāmens", 0)
        K = statistics.fmean(K)
        groups = [LD, K, E]
        weights = [0.25, 0.25, 0.5]
        final = statistics.fmean(groups, weights)
        return final

class Matematika(Course):
    def calculate_final(self):
        K = [self.grades.get("1.kontroldarba \"Integrēšanas ābece\" rezultāti", 0),
            self.grades.get("2.kontroldarba \"Integrēšanas metodes\" rezultāti", 0),
            self.grades.get("3.kontroldarba \"Noteiktais un neīstais integrālis\" rezultāti", 0),
            self.grades.get("4.kontroldarba \"Diferenciālvienādojumi\" rezultāti", 0),
            self.grades.get("5.kontroldarba \"Rindas\" rezultāti", 0)]

        M = [self.grades.get("1.mājasdarba \"Nenoteiktais integrālis\" rezultāti", 0),
             self.grades.get("2.mājasdarba \"Noteiktais integrālis, tā pielietojumi, neīstie integrāļi\" rezultāti", 0),
             self.grades.get("3.mājasdarba \"Diferenciālvienādojumi\" rezultāti", 0),
             self.grades.get("4.mājasdarba \"Rindas\" rezultāti", 0)]

        L = [self.grades.get("1.laboratorijas darba rezultāti", 0),
             self.grades.get("2.laboratorijas darba rezultāti", 0),
             self.grades.get("3.laboratorijas darba rezultāti", 0)]

        T = [self.grades.get("Tests 2.1. Noteiktā integrāļa aprēķināšana", 0),
             self.grades.get("Tests 2.2 Plaknes figūras laukuma aprēķināšana", 0),
             self.grades.get("Tests 2.3 Neīstie integrāļi", 0),
             self.grades.get("1. teorijas tests", 0),
             self.grades.get("2. teorijas tests", 0)]
        
        S = [self.grades.get("1.starpeksāmena rezultāti", 0),
             self.grades.get("2.starpeksāmena rezultāti", 0)]

        K=statistics.fmean(K)
        M=statistics.fmean(M)
        L=statistics.fmean(L)
        T=statistics.fmean(T)
        
        if min(S) >= 4:
            E=statistics.fmean(S)
        else:
            E = self.grades.get("Eksāmens", 0)
        groups = [E, K, M, L, T]
        weights = [0.5, 0.25, 0.1, 0.1, 0.05]
        final = statistics.fmean(groups, weights)
        return final

class OOP(Course):
    def calculate_final(self):
        L = [self.grades.get("1. Laboratorijas darbs", 0),
             self.grades.get("2. Laboratorijas darbs", 0),
             self.grades.get("3. Laboratorijas darbs", 0),
             self.grades.get("4. Laboratorijas darbs", 0),
             self.grades.get("5. Laboratorijas darbs", 0),
             self.grades.get("6. Laboratorijas darbs", 0),
             self.grades.get("7. Laboratorijas darbs", 0)]
        K = [self.grades.get("1. kontroldarbs 17.03.2025. Seanss 8.20", 0),
             self.grades.get("2. kontroldarbs 19.05.2025. Seanss 8.20", 0)]
        M = [self.grades.get("Mājas darbs 1", 0),
             self.grades.get("Mājas darbs 2", 0),
             self.grades.get("Mājas darbs 4", 0),
             self.grades.get("Mājas darbs 7", 0)]
        E = self.grades.get("Eksāmens", 0)

        if min(M) >= 4:
            B = 1
        else:
            B = 0
        L=statistics.fmean(L)
        K=statistics.fmean(K)

        groups = [E, L, K, 0]
        weights = [0.3, 0.4, 0.25, 0.05]
        final = statistics.fmean(groups, weights)
        final += B*0.1
        if final > 10:
            final = 10
        return final
      

class Vides_un_klimata_celvedis(Course):
    def calculate_final(self):
        T = [self.grades.get("Uzdevums \"Elektronikas aprite\"_2", 0),
             self.grades.get("Tests 2 - Indikatori_2", 0),
             self.grades.get("Atjaunojamie energoresursi un viedās energosistēmas_praktiskie darbi_2", 0),
             self.grades.get("Uzdevums \"Elektronikas aprite\"_2", 0),
             self.grades.get("Tests - aprites cikla analīze un ekodizains_0", 0),
             self.grades.get("Tests - aprites cikla analīze un ekodizains_1", 0),
             self.grades.get("Tests - aprites cikla analīze un ekodizains_2", 0),
             self.grades.get("Tests - aprites cikla analīze un ekodizains_3", 0),
             self.grades.get("Tests 1_Aprites ekonomikas pamatprincipi _2", 0),
             self.grades.get("Tests2_Biotehnoloģijas priekšrocības un trūkumi_2", 0),
             self.grades.get("Ilgtspējīga mobilitāte_2", 0),
             self.grades.get("Uzdevums_pozitīvās enerģijas pilsēta_2", 0),
             self.grades.get("Tests1_Biotehnoloģijas_2", 0),
             self.grades.get("Noslēguma eksāmens_2", 0)]
        LS = self.grades.get("Tests_Lomu spēle_2", 0)
        E = self.grades.get("Eksāmens", 0)
        T=statistics.fmean(T)

        groups = [T, LS, E]
        weights = [0.45, 0.25, 0.3]
        final = statistics.fmean(groups, weights)
        return final


def save_course_table(courses, filename="final_grades.txt"):
    rounded = []
    exact = []
    with open(filename, "w", encoding='utf-8') as f:
        f.write(f"{'Kursa nosaukums':<45} | {'Gala atzīme':<11}\n")
        f.write("-" * 60 + "\n")
        for course in courses:
            final = round(course.calculate_final(), 2)
            rounded.append(round(final))
            exact.append(final)
            f.write(f"{course.name:<45} | {str(final):<11}\n")

        avg_final_exact = round(statistics.fmean(exact), 1)
        avg_final_rounded = round(statistics.fmean(rounded))
        f.write("-"*59+"\n")
        f.write(f"{'Kopējā vidējā gala atzīme: ':<45} | {avg_final_exact:<11}\n")
        f.write("-"*59+"\n")
        f.write(f"{'Atzīme pēc noapaļotām vērtībām: ':<45} | {avg_final_rounded}\n")

courses = [
    DatuStrukturas(680502, "cat_579793"),
    DiskretaMatematika(695121, "cat_636085"),
    Fizika(680310, "cat_579789"),
    Matematika(680369, "cat_579791"),
    OOP(680366, "cat_579790"),
    Vides_un_klimata_celvedis(680306, "cat_579788"),
]
       
save_course_table(courses)

driver.quit()

