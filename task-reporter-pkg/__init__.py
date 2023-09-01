import os
from config.env_vars import BASE_DIR, C_PD, C_USR, REPORTER_URI, TASK_PATH, LOGIN_PATH
from config.webdriver import WebDriver
from services.panda_service import PandaService
from models.page_values import PageValue
import datetime
import math


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
                "link", '//div[@class="textos-usuario"]//a[@id="btn_salir"]'
            )
            self.logs += f"{do_action_res[1]}\n"
        except Exception as ex:
            self.logs += f"[ERR] - Error logout :: {ex}\n"
            raise ex

    def submit_login_form(self):
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

    def submit_taks_form(self, task_obj: object):
        try:
            # TODO: Manage actions as array
            # TODO: Change fielnames in code and report
            self.logs += f'[INF] - Uploading task ["{task_obj.Task}"]\n'

            taskform_values_arr = []

            # Seeking task day
            task_day = task_obj.Day.strftime("%d")
            task_day = task_day[1] if task_day.startswith("0") else task_day
            self.driver_instance.do_action("click", '//input[@id="dd_diaACA"]')
            self.driver_instance.do_action(
                "click",
                # f'//div[@class="datepicker-days"]//td[text()="{task_day}"]',
                f'//div[@class="datepicker-days"]//td[not(contains(@class, "old day")) and text()="{task_day}"]',
            )

            # "Cliente" field selection
            self.driver_instance.do_action("click", '//select[@id="clienteA"]')
            self.driver_instance.do_action(
                "click",
                # Other option: //select[@id="clienteA"]//option[contains(text(), "")]
                f'//select[@id="clienteA"]//option[text()="{task_obj.Customer}"]',
            )

            # "Proyecto" field selection
            self.driver_instance.do_action("click", '//select[@id="proyectoA"]')
            self.driver_instance.do_action(
                "click",
                # Other option: //select[@id="clienteA"]//option[contains(text(), "")]
                f'//select[@id="proyectoA"]//option[text()="{task_obj.Project}"]',
            )

            # "Act general" field selection
            self.driver_instance.do_action("click", '//select[@id="categoriaA"]')
            self.driver_instance.do_action(
                "click",
                # Other option: //select[@id="clienteA"]//option[contains(text(), "")]
                f'//select[@id="categoriaA"]//option[text()="{task_obj.Activity}"]',
            )

            # "Solicitado por" field set text
            taskform_values_arr.append(
                PageValue('//input[@id="persona_solA"]', task_obj.Requester)
            )
            # "Liga" field set text
            url_task = "" if f"{task_obj.Link}" == "nan" else task_obj.Link
            taskform_values_arr.append(PageValue('//input[@id="ligaW"]', url_task))

            # "Tareas" field set text
            taskform_values_arr.append(
                PageValue('//textarea[@id="tareasA"]', task_obj.Task)
            )

            # "Horas" field set text
            taskform_values_arr.append(
                PageValue('//input[@id="horasA"]', int(task_obj.Hour))
            )

            # "Minutos" field set text
            taskform_values_arr.append(
                PageValue('//input[@id="minutosA"]', int(task_obj.Min))
            )

            # "Comentarios" field set text
            comments = "" if math.isnan(task_obj.Comments) else task_obj.Comments
            taskform_values_arr.append(
                PageValue('//textarea[@id="coment_adicionalesA"]', comments)
            )

            self.driver_instance.set_values_in_page_xpath(taskform_values_arr)

            self.driver_instance.do_action(
                "click", '//button[@id="btnSave" and text() = "GUARDAR"]'
            )

            self.driver_instance.alerts_manage("Accept")
            print("uploaded")
            if self.driver_instance.element_is_exists(
                '//div[contains(@class, "swal2-show")]'
            ):
                self.driver_instance.alerts_manage("Ok", "swal")

            print("please wait")

        except Exception as ex:
            self.logs += f"[ERR] - Uploading task :: {ex}\n"
            raise ex

    def start(self):
        """
        Starts taskreporter function
        Returns:
          list: Indicates execution result [True, "Tasks has been uploaded"]
        """

        try:
            self.logs += "[INF] - Starting taskreporter ...\n"
            tasks_uploaded = []

            self.driver_instance = WebDriver()
            self.navigate_to_page(LOGIN_PATH)
            self.submit_login_form()
            self.navigate_to_page(TASK_PATH)

            file_path = os.path.join(
                "D:\\My Documents\\Projects\\Projects\\Repos\\python\\microservice-taskreporter-python\\temp",
                "report.xlsx",
            )
            # print(sys.path[0])
            panda_res = PandaService().get_xlsxdata_from_range(file_path)
            for item in panda_res[1]:
                self.logs += f"[INF] - Eval task :: {item}\n"
                if item.Status != "Pending":
                    print(f"{item} :: has been uploaded")
                    continue
                # if item.Day.strftime("%d/%m/%Y") == "27/07/2023":
                #     print(f"{item} :: skipped")
                #     continue
                print(f"Uploading :: {item}")
                self.submit_taks_form(item)
                tasks_uploaded.append(item.Task)
                # break

            # self.logout()

        except Exception as ex:
            self.logs += f"[ERR] - Error tryin uploading task :: {ex} \n"
            print(self.logs)
        finally:
            # TODO: Create log files
            with open("logs.txt", "w") as f:
                f.write(self.logs)


if __name__ == "__main__":
    TaskReporter().start()
