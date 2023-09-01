import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .exceptions import WebDriverException
from .env_vars import BASE_DIR
from models.page_values import PageValue


class WebDriver:
    def __init__(self):
        self.web_driver = {}
        try:
            driver_path = os.path.join(
                BASE_DIR,
                "microservice-taskreporter-python",
                "drivers",
                "chromedriver.exe",
            )
            print(driver_path)
            service = Service(driver_path)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = (
                "C:/Program Files/Google/Chrome Dev/Application/chrome.exe"
            )
            chrome_options.add_argument("--incognito")

            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.binary_location = (
            #     "C:\Program Files\Google\Chrome Dev\Application"
            # )
            # Configura las opciones del navegador
            # chrome_options.add_experimental_option(
            #     "debuggerAddress", "localhost:9222"
            # )  # Conecta a una instancia de Chrome abierta

            # Inicializa el navegador
            # driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

            web_driver = webdriver.Chrome(service=service, options=chrome_options)
            self.web_driver = web_driver
        except Exception as ex:
            raise WebDriverException(f"Setup error WebDriver {ex}")

    def navigate_to(self, page_path: str):
        try:
            self.web_driver.get(page_path)
            return [True, f"[OK] - Succes navigation to {page_path}"]
        except Exception as ex:
            raise WebDriverException(
                f"Webdriver navigation error :: [path: {page_path}] :: {ex}"
            )

    def do_action(self, action: str, xpath_query: str):
        from selenium.webdriver.support import expected_conditions as EC

        try:
            element = WebDriverWait(self.web_driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, xpath_query))
            )
            if action.endswith(("click", "submit", "link")):
                element.click()

            return [True, f"[OK] - Action {action} done"]
        except Exception as ex:
            raise WebDriverException(
                f"Webdriver do_action error :: [action: {action}, path: {xpath_query}] :: {ex}"
            )

    def alerts_manage(self, action: str, type_alert="alert"):
        from selenium.webdriver.common.alert import Alert

        try:
            alert = Alert(self.web_driver)
            if action == "Accept" and type_alert == "alert":
                alert.accept()
            if action == "Close" and type_alert == "alert":
                alert.dismiss()
            if action == "Close" and type_alert == "swal":
                self.web_driver.execute_script("Swal.close();")
            if action == "Ok" and type_alert == "swal":
                self.web_driver.execute_script("Swal.clickConfirm();")

            return [True, "[OK] - The Alert dialog has been checked"]
        except Exception as ex:
            raise WebDriverException(f"Manage Alert ERROR {ex}")

    def set_values_in_page_xpath(self, values_arr: list[PageValue]):
        try:
            for obj in values_arr:
                web_element = self.web_driver.find_element(By.XPATH, obj.xpath_query)
                web_element.clear()
                web_element.send_keys(obj.value)
            return [True, "[OK] - The values change in page"]
        except Exception as ex:
            raise WebDriverException(f"Set Value in page ERROR {ex}")

    def element_is_exists(self, xpath_query: str):
        result = False
        try:
            element = self.web_driver.find_element(By.XPATH, xpath_query)
            print(f"Element found :: {element}")
            result = True
        except Exception as ex:
            print(f"No suche element :: {ex}")
        return result

    def get_value_by_xpath(self, xpath_query: str):
        try:
            element = self.web_driver.find_element(By.XPATH, xpath_query)
            return [True, element.text]
        except Exception as ex:
            raise WebDriverException(f"Get Value by element ERROR {ex}")

    def close(self):
        try:
            self.web_driver.quit()
            return [True, "WebDriver closed"]
        except Exception as ex:
            raise WebDriverException(f"Error trying close action in webDriver {ex}")
