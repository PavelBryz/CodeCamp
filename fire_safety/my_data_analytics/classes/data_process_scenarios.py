from abc import ABC, abstractmethod
import numpy as np
from .data_processors import DataProcessor
from .enums import Headers
from .data_printers import DataPrinter
from pandas import pivot_table


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

        return self.printer.print_data(df)


class PrintSumYScenario(Scenario):
    def execute(self, caller: DataProcessor):
        table = pivot_table(caller.data, values=Headers.VALUE.value, index=[Headers.DATE.value], aggfunc=np.sum)
        table = table.sort_index()
        table.index = table.index.strftime('%d/%m/%Y')

        return self.printer.print_data(table)


class PrintThreeYScenario(Scenario):
    def execute(self, caller: DataProcessor):
        table = pivot_table(caller.data, values=Headers.VALUE.value, index=[Headers.DISTRICT.value], aggfunc=np.sum)
        table = table[table[Headers.VALUE.value] >= 3]
        table = table.sort_index()

        return self.printer.print_data(table.index.values)
