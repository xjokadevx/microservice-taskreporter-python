import os
from exceptions import SaveFileException, DeleteDirectoryException


@staticmethod
def delete_local_dir(path_str: str):
    import shutil

    try:
        shutil.rmtree(path_str)
        return [True, f"Directory deleted :: {path_str}"]
    except Exception as ex:
        raise DeleteDirectoryException(f"{ex}")


@staticmethod
def save_file(content: str, output_path: str, filename: str, extension: str):
    try:
        with open(os.path.join(output_path, f"{filename}.{extension}"), "wb") as f:
            f.write(content)
            f.close()
        return [True, f"File saved as {filename}.{extension}"]
    except Exception as ex:
        raise SaveFileException(f"{ex}")
