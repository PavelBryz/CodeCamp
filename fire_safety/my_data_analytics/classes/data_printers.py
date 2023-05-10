from abc import ABC, abstractmethod
from typing import Union

import numpy as np
from numpy import ndarray

from .enums import Headers
from pandas import DataFrame


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


class WebPagePrinter(DataPrinter):
    def print_data(self, df: Union[DataFrame, ndarray]):
        if isinstance(df, DataFrame):
            return df.to_html()
        else:
            return str(df)


class WebFormattedPrinter(DataPrinter):
    def print_data(self, df: DataFrame):
        res = "<table><tr>"
        for c in df.columns:
            res += f'<td>{c}</td>'
        for r in df.iterrows():
            if r[1][2]:
                res += "<tr class='red-line'>"
            else:
                res += "<tr>"
            res += f'<td>{r[1][0]}</td>'
            res += f'<td>{r[1][1]:%d/%m/%Y}</td>'
            res += f'<td>{"Y" if r[1][2] else "N"}</td>'
            res += "</tr>"
        res += '</table>'

        return res
