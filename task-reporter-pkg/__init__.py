import os
from config.env_vars import BASE_DIR, C_PD, C_USR, REPORTER_URI, TASK_PATH, LOGIN_PATH
from config.webdriver import WebDriver
from models.page_values import PageValue


class TaskReporter:
    def __init__(self):
        self.logs = ""
        self.driver_instance = {}

    def download_external_report(self):
        try:
            print("downloading...")
        except Exception as ex:
            self.logs += f"Error tryin downloading report :: {ex} \n"
            raise ex

    def logout(self):
        try:
            self.logs += "[INF] - Logout session...\n"
            do_action_res = self.driver_instance.do_action(
                "link", '//a[@id="btn_salir"]'
            )
            self.logs += f"{do_action_res[1]}\n"
        except Exception as ex:
            self.logs += f"[ERR] - Error logout :: {ex}\n"
            raise ex

    def fill_login_form(self):
        try:
            self.logs += "[INF] - Filling login form \n"
            login_values_arr = []
            login_values_arr.append(
                PageValue('//input[@id="MainContent_UserCorreo"]', C_USR)
            )

            login_values_arr.append(
                PageValue('//input[@id="MainContent_Password"]', C_PD)
            )
            set_values_result = self.driver_instance.set_values_in_page_xpath(
                login_values_arr
            )
            self.logs += f"{set_values_result[1]}\n"

            self.logs += "[INF] - Submiting login form\n"
            do_action_res = self.driver_instance.do_action(
                "submit", '//input[@type="submit"]'
            )
            self.logs += f"{do_action_res[1]}\n"
        except Exception as ex:
            self.logs += f"[ERR] - Error filling login form :: {ex}\n"
            raise ex

    def navigate_to_page(self, path_complement: str):
        try:
            self.logs += f"[INF] - Start navigation to {path_complement} \n"
            task_url = f"{REPORTER_URI}/{path_complement}"
            navigation_result = self.driver_instance.navigate_to(page_path=task_url)
            self.logs += f"{navigation_result[1]} \n"
        except Exception as ex:
            self.logs += f"[ERR] - Error navigate :: {ex} \n"
            raise ex

    def start(self):
        """
        Starts taskreporter function
        Returns:
          list: Indicates execution result [True, "Tasks has been uploaded"]
        """
        try:
            self.logs += "[INF] - Starting taskreporter ...\n"
            self.driver_instance = WebDriver()
            self.navigate_to_page(LOGIN_PATH)
            self.fill_login_form()
            self.navigate_to_page(TASK_PATH)
            self.logout()
        except Exception as ex:
            self.logs += f"[ERR] - Error tryin uploading task :: {ex} \n"
            print(self.logs)
        finally:
            # TODO: Create log files
            print(self.logs)


if __name__ == "__main__":
    TaskReporter().start()
