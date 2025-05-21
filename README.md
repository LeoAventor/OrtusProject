# RTU eStudijas Datorsistēmas fakultātes atzīmju apstrādes rīks

## Projekta uzdevums

Šī Python programma ir izstrādāta, lai automatizētu Rīgas Tehniskās universitātes (RTU) e-studiju platformas studiju kursu gala vērtējumu iegūšanu, aprēķināšanu un analīzi.

Programmas mērķis ir:

- Automātiski pieslēgties eStudijas platformai, izmantojot Selenium bibliotēku;
- Nolasīt katra kursa vērtējumus, tos apstrādāt saskaņā ar kursa specifisko vērtēšanas loģiku;
- Aprēķināt gala atzīmes, pamatojoties uz kursa specifiskiem vērtēšanas kritērijiem;
- Saglabāt gala atzīmes strukturētā teksta failā.

Katrs kurss satur atšķirīgus vērtēšanas komponentus – kontroldarbi, laboratorijas darbi, eksāmeni u.c. –, un šis rīks ļauj tos novērtēt pēc svara, kā arī nodrošina vienotu gala atzīmes aprēķinu.

---

## Izmantotās Python bibliotēkas

| Bibliotēka          | Iemesls izmantošanai                                                                 |
|---------------------|--------------------------------------------------------------------------------------|
| `os`                | Lai piekļūtu `.env` failam un sistēmas mainīgajiem (lietotājvārds un parole).       |
| `statistics`        | Vidējo vērtību un gala atzīmju aprēķins pēc dažādiem svara koeficientiem.           |
| `re`                | Regulāro izteiksmju izmantošanai, piemēram, lai atrastu kursa kodu nosaukumā.       |
| `selenium`          | Automatizētai mijiedarbībai ar RTU e-studiju tīmekļa vietni.                        |
| `dotenv (load_dotenv)` | Drošai autentifikācijas datu uzglabāšanai ārpus koda.                           |

---

## Izmantotās datu struktūras

Projekta izveidē tika izmantotas sekojošas datu struktūras:

- **Klase `Course`**: Bāzes klase, kas satur vispārīgās metodes un atribūtus visiem kursiem – `id`, `classname`, `name`, `code`, `grades`, u.c.
- **Atvasinātās klases**: `DatuStrukturas`, `DiskretaMatematika`, `Fizika`, `Matematika`, `OOP`, `Vides_un_klimata_celvedis` – katrā klasē implementēta specifiska gala atzīmes aprēķināšanas loģika, kas atšķiras atkarībā no kursa prasībām.
- **Vārdnīcas (`dict`)**: Kursu atzīmes tiek glabātas kā atslēga-vērtība pāri, kur atslēga ir vērtēšanas uzdevuma nosaukums, bet vērtība – iegūtā atzīme.
- **Saraksti (`list`)**: Katrs vērtēšanas posms (piem., laboratorijas darbi, testi) tiek apkopots sarakstā, kuru pēc tam analizē statistiski.

> Katrai klasei (piemēram, `DatuStrukturas`, `DiskretaMatematika`) ir sava `calculate_final()` metode, kas atbilst RTU konkrētā kursa vērtēšanas struktūrai.

---

## Programmatūras izmantošana

Lai palaistu šo programmu:

1. Instalējiet nepieciešamās bibliotēkas:

    ```bash
    pip install -r requirements.txt
    ```

2. Izveidojiet `.env` failu tajā pašā direktorijā ar šādu saturu:

    ```dotenv
    login_name=JŪSU_LIETOTĀJVĀRDS
    password=JŪSU_PAROLE
    ```

3. Programma izpilda šādas darbības:

    - Atver Firefox pārlūku un pieslēdzas RTU eStudijas sistēmai.
    - Nolasa katra kursa lapu un saglabā atzīmes.
    - Aprēķina gala atzīmi, pamatojoties uz kursa īpašiem vērtēšanas kritērijiem.
    - Saglabā gala atzīmes failā `final_grades.txt`.

---

## Ievērībai

- Katra kursa vērtējumi tiek nolasīti no e-studiju portāla un tiek apstrādāti atbilstoši kursa struktūrai.
- Ja kāda atzīme nav pieejama, tiek uzskatīts, ka tā ir 0.
- Pēc kursu gala vērtējumu iegūšanas tiek aprēķināta arī kopējā vidējā atzīme.

---

## Faila struktūra

- **`Course` klase** – pamata datu struktūra, nodrošina kursa informācijas ielādi un vērtējumu nolasīšanu.
- Katrs kurss (piemēram, `Matematika`, `Fizika`) ir definēts kā atsevišķa klase ar savu aprēķinu loģiku.
- **`save_course_table()` funkcija** – saglabā gala atzīmes failā.
