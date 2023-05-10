from typing import Optional
from pandas import DataFrame, to_datetime
from .data_readers import DataReader
from .enums import Headers


class DataProcessor:
    def __init__(self, reader: DataReader):
        self.data: Optional[DataFrame] = None
        self.reader: DataReader = reader

    def read_data(self):
        self.data = self.reader.read()

        # self.data = self.data.melt(id_vars=[Headers.DISTRICT.value],
        #                            var_name=Headers.DATE.value,
        #                            value_name=Headers.VALUE.value)
        #
        # self.data[Headers.DATE.value] = to_datetime(self.data[Headers.DATE.value], format='%d/%m/%Y')
        # self.data[Headers.VALUE.value] = self.data[Headers.VALUE.value] == 'Y'

    def data_processing(self, scenario):
        return scenario.execute(self)