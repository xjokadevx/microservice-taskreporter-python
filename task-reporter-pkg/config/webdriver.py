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
            driver_path = os.path.join(BASE_DIR, "drivers", "chromedriver.exe")
            service = Service(driver_path)
            web_driver = webdriver.Chrome(service=service)
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
                f"Webdriver do_action error :: [action: {action}] :: {ex}"
            )

    def set_values_in_page_xpath(self, values_arr: list[PageValue]):
        try:
            for obj in values_arr:
                web_element = self.web_driver.find_element(By.XPATH, obj.xpath_query)
                web_element.send_keys(obj.value)
            return [True, "[OK] - The values change in page"]
        except Exception as ex:
            raise WebDriverException(f"Set Value in page ERROR {ex}")

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
