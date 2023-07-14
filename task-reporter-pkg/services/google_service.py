class GoogleService:
    def __init__(self):
        self.service_name = "GoogleService"
        self.drive_instance = {}

    def download_file_from_drive(self, filename: str, drive_path: str, local_path: str):
        # TODO: Donwload file from drive
        pass

    def get_drive_connection(self):
        # TODO: With your credentials, get drive connection
        print("ok")
        self.drive_instance = {}


# Execute functions

g_instance = GoogleService()
g_instance.get_drive_connection()
