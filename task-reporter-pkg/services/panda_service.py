import pandas as pd
from config.exceptions import PandasReaderException


class PandaService:
    def __init__(self):
        self.dataframe = {}

    def get_xlsxdata_from_range(self, file_path: str):
        data_res = [True, []]
        try:
            dataframe = pd.read_excel(file_path)
            data_tuples = dataframe.itertuples()
            data_res[1] = data_tuples
            return data_res
        except Exception as ex:
            raise PandasReaderException(f"Error get dataframe {ex}")
