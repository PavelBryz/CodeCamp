from abc import abstractmethod, ABC
from io import BytesIO
from pathlib import PurePath

from django.db.models import QuerySet
from pandas import DataFrame, read_csv, to_datetime, pivot_table
from django_pandas.io import read_frame

from .enums import Headers


class DataReader(ABC):
    @abstractmethod
    def read(self) -> DataFrame:
        pass


class CSVReader(DataReader):
    def __init__(self, file_path: PurePath):
        self.file_path = file_path

    def read(self) -> DataFrame:
        data = read_csv(self.file_path, sep='\t')
        data = data.melt(id_vars=[Headers.DISTRICT.value],
                         var_name=Headers.DATE.value,
                         value_name=Headers.VALUE.value)

        data[Headers.DATE.value] = to_datetime(data[Headers.DATE.value], format='%d/%m/%Y')
        data[Headers.VALUE.value] = data[Headers.VALUE.value] == 'Y'
        return data


class BitesIOReader(DataReader):
    def __init__(self, file_bytes: BytesIO):
        self.file_bytes = file_bytes

    def read(self) -> DataFrame:
        data = read_csv(self.file_bytes, sep='\t')
        data = data.melt(id_vars=[Headers.DISTRICT.value],
                         var_name=Headers.DATE.value,
                         value_name=Headers.VALUE.value)

        data[Headers.DATE.value] = to_datetime(data[Headers.DATE.value], format='%d/%m/%Y')
        data[Headers.VALUE.value] = data[Headers.VALUE.value] == 'Y'
        return data


class DatabaseReader(DataReader):
    def __init__(self, data: QuerySet, rename=True):
        self.data = data
        self.rename = rename

    def read(self) -> DataFrame:
        df = read_frame(self.data)
        if self.rename:
            df = df.rename(columns={'date': Headers.DATE.value,
                                    'id_cfsdistrict': Headers.DISTRICT.value,
                                    'total': Headers.VALUE.value})

        return df
