import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pushbullet import API
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
import schedule
from selenium.webdriver.support.ui import WebDriverWait

def run():
    treasure = []
    with open("conf.env") as sens:
        sens_itive = (sens.read()).split('\n')

    #push api details
    api_key: str = sens_itive[0]
    api = API()
    api.set_token(api_key)

    #login details
    lo_email: str = sens_itive[1]
    lo_pass: str = sens_itive[2]
    url: str = sens_itive[3]

    #Config headless option
    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Edge(options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 17)

    def get_find(how, target):
        if how == "css":
            res = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, target)))
            return res
        
        if how == "id":
            res = wait.until(EC.presence_of_element_located((By.ID, target)))
            return res

        elif how == "name":
            res = wait.until(EC.element_to_be_clickable((By.NAME, target)))
            return res
        
        elif how == "path":
            res = wait.until(EC.element_to_be_clickable((By.XPATH, target)))
            return res

        else:
            return "Enter a valid find method!"
        
    enter_email = get_find("name", "user[email]")
    enter_email.send_keys(lo_email)
    time.sleep(1)

    enter_password = get_find("name", "user[password]")
    enter_password.send_keys(lo_pass)
    enter_password.submit()
    time.sleep(3)

    # Get the total height of the page & Scroll down the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, arguments[0]);", total_height/2)

    try:
        table_projs = driver.find_element(By.CSS_SELECTOR, 'div[class="tw-py-16"]')
        print(table_projs.text)

    except:
        try:
            projs = driver.find_elements(By.CSS_SELECTOR, 'td[class="sc-fqkvVR cvoXuT tw-p-4 tw-text-size-table-body tw-text-black-90 undefined"]')

            for item in projs:
                if ( len(item.text) > 10 ) and ( '[QUALIFICATION]' not in item.text) and ( 'No matches for search conditions' not in item.text ):
                    treasure.append(item.text)
                    api.send_note("Good news!", f"Something you might like is here: {item.text}")

        except:
            pass


if __name__ == "__main__":
    run()
    schedule.every(10).minutes.do(run)

    while True:
        schedule.run_pending()
        time.sleep(300)  # Check for pending jobs every 5 minutes