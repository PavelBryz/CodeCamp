from enum import Enum
from types import MethodType
from typing import Optional, Callable, Union
import numpy as np
from numpy import datetime64

from pandas import DataFrame, read_csv, to_datetime, pivot_table
from abc import ABC, abstractmethod
from pathlib import Path, PurePath

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


class Headers(Enum):
    DISTRICT = "CFS District"
    DATE = "Date"
    VALUE = "Value"


class DataReader(ABC):
    @abstractmethod
    def read(self) -> DataFrame:
        pass


class CSVReader(DataReader):
    def __init__(self, file_path: PurePath):
        self.file_path = file_path

    def read(self) -> DataFrame:
        return read_csv(self.file_path, sep='\t')


class DataPrinter(ABC):
    @abstractmethod
    def print_data(self, df: Union[DataFrame, object]):
        pass


class ConsoleFormattedPrinter(DataPrinter):
    def print_data(self, df: DataFrame):
        red_color = '\033[31m'
        drop_format = '\033[0m'

        res = f"|{Headers.DISTRICT.value:^15}|{Headers.DATE.value:^15}|{Headers.VALUE.value:^7}|\n"
        for row in df.to_numpy():
            row_as_str = f"|{row[0]:^15}|{f'{row[1]:%d/%m/%Y}':^15}|{'Y' if row[2] else 'N':^7}|"
            if row[2]:
                res += red_color + row_as_str + drop_format
            else:
                res += row_as_str
            res += '\n'

        print(res)


class ConsolePrinter(DataPrinter):
    def print_data(self, df: object):
        print(df)


class DataProcessor:
    def __init__(self, reader: DataReader):
        self.data: Optional[DataFrame] = None
        self.reader: DataReader = reader

    def read_data(self):
        self.data = self.reader.read()

        self.data = self.data.melt(id_vars=[Headers.DISTRICT.value],
                                   var_name=Headers.DATE.value,
                                   value_name=Headers.VALUE.value)

        self.data[Headers.DATE.value] = to_datetime(self.data[Headers.DATE.value], format='%d/%m/%Y')
        self.data[Headers.VALUE.value] = self.data[Headers.VALUE.value] == 'Y'

    def data_processing(self, scenario):
        scenario.execute(self)


class Scenario(ABC):
    def __init__(self, printer: DataPrinter):
        self.printer = printer

    @abstractmethod
    def execute(self, caller: DataProcessor):
        pass


class PrintDataScenario(Scenario):
    def execute(self, caller: DataProcessor):
        df = caller.data.sort_values([Headers.DATE.value, Headers.DISTRICT.value, Headers.VALUE.value],
                                     ascending=[True, True, False])

        self.printer.print_data(df)
        # print(df.columns.names)

class PrintSumYScenario(Scenario):
    def execute(self, caller: DataProcessor):
        table = pivot_table(caller.data, values=Headers.VALUE.value, index=[Headers.DATE.value], aggfunc=np.sum)
        table = table.sort_index()
        table.index = table.index.strftime('%d/%m/%Y')

        self.printer.print_data(table)


class PrintThreeYScenario(Scenario):
    def execute(self, caller: DataProcessor):
        table = pivot_table(caller.data, values=Headers.VALUE.value, index=[Headers.DISTRICT.value], aggfunc=np.sum)
        table = table[table[Headers.VALUE.value] >= 3]
        table = table.sort_index()

        self.printer.print_data(table.index.values)


if __name__ == '__main__':
    csv_reader = CSVReader(BASE_DIR / "Fire Ban forecast for challenge.csv")
    data_processor = DataProcessor(csv_reader)
    data_processor.read_data()
    data_processor.data_processing(PrintDataScenario(ConsoleFormattedPrinter()))
    # data_processor.data_processing(PrintSumYScenario(ConsolePrinter()))
    # data_processor.data_processing(PrintThreeYScenario(ConsolePrinter()))

