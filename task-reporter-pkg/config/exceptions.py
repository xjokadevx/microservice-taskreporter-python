class NotExistsException(Exception):
    def __init__(self, msg):
        self.msg = f"Directory/path/something not exitst :: {msg}"
        super().__init__(msg)


class DownloadException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)


class SaveFileException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)


class ReadFileException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)


class DeleteDirectoryException(Exception):
    def __init__(self, msg):
        self.msg = f"Not posible delete directory :: {msg}"
        super().__init__(msg)


class WebDriverException(Exception):
    def __init__(self, msg):
        self.msg = f"WebDriver error :: {msg}"
        super().__init__(msg)
