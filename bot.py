from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from time import sleep
import requests
from bs4 import BeautifulSoup

REGISTERED = False

def doIt():
    # Replace with proper creds here
    CREDS = ("username", "password")

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\phant\\AppData\\Local\\Temp\\scoped_dir10980_1046497543\\Default")

    # Go to Northeastern reg
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://nubanner.neu.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=registration")

    # Log in to registration
    driver.find_element_by_id("registerLink").click()
    driver.find_element_by_id("username").send_keys(CREDS[0])
    driver.find_element_by_id("password").send_keys(CREDS[1])
    driver.find_element_by_name("_eventId_proceed").click()

    # Select term
    sleep(0.5)
    WebDriverWait(driver, 10).until(EC.title_is("Banner"))
    driver.find_element_by_id("select2-chosen-1").click()
    driver.implicitly_wait(10)
    driver.find_element_by_id("202210").click()
    driver.implicitly_wait(10)
    driver.find_element_by_id("term-go").click()

    # Find DS 3000
    driver.implicitly_wait(10)
    driver.find_element_by_id("enterCRNs-tab").click()
    driver.find_element_by_id("txt_crn1").send_keys("15065")
    driver.find_element_by_id("addCRNbutton").click()

    # Drop remote DS 3000
    sleep(3)
    driver.find_element_by_id("s2id_action-19413-ddl").click()
    sleep(0.5)
    driver.find_elements_by_xpath("//ul[@role='listbox']/li")[1].click()

    # Conditional drop and submit

    driver.find_element_by_id("conditionalAddDrop").click()
    sleep(0.5)
    driver.find_element_by_id("saveButton").click()

    # Check if it worked

    sleep(0.5)
    found = driver.find_elements_by_xpath("//*[text()='Unable to make requested changes so your schedule was not changed.']")

    if len(found) > 0:
        print("[SEVERE] Unable to register for DS 3000")
    else:
        print("[INFO] Successfully registered for DS 3000")
        REGISTERED = True

    sleep(5)

    driver.close()

def check_banner():
    url = "https://wl11gp.neu.edu/udcprod8/bwckschd.p_disp_detail_sched?term_in=202210&crn_in=15065"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    tables = soup.find_all('table', class_="datadisplaytable")

    # This is the one with the class capacity
    table = tables[1]

    remaining = table.findChildren('td', class_="dddefault")[2].text

    print(remaining + " seats remaining.")

    if int(remaining) > 0:
        doIt()

def main():
    print("NEU Course Bot")
    counter = 0
    while not REGISTERED:
        try:
            print("CHECK #" + str(counter))
            check_banner()
            counter = counter + 1
            sleep(5)
        except:
            print("Trying again")
            pass

    print("Exiting. Checked " + str(counter) + "times.")
    input("Press any key...")

    

if __name__ == "__main__":
    main()