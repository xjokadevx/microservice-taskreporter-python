from dotenv import load_dotenv
import keyring
from cryptography.fernet import Fernet
import os

load_dotenv()

local_hash = keyring.get_password("task-reporter", "hash")
fernet = Fernet(local_hash)

REPORTER_URI = fernet.decrypt(os.getenv("REPORTER_URI")).decode()
TASK_PATH = fernet.decrypt(os.getenv("TASK_PATH")).decode()
LOGIN_PATH = fernet.decrypt(os.getenv("LOGIN_PATH")).decode()
C_USR = fernet.decrypt(os.getenv("C_USR")).decode()
C_PD = fernet.decrypt(os.getenv("C_PD")).decode()
BASE_DIR = os.path.dirname(os.getcwd())


# TODO: PUT YOUR CREDENTIALS HERE LIKE LINES ABOVE
