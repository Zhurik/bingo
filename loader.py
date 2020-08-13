import json

from bingo_data import BingoData

from typing import List


class Loader:
    """Базовый класс для подгрузки данных"""

    def load_data(self) -> List[BingoData]:
        """
        Основной метод, который должен
        быть реализован в каждом из дочерних классов
        """

        raise NotImplementedError


class JSONLoader(Loader):
    """Класс для подгрузки записей из json"""

    PHRASES_FILE = "./phrases.json"

    def __init__(
        self,
        json_path: str=PHRASES_FILE
    ) -> None:
        self.json_path = json_path

    def load_data(self) -> List[BingoData]:
        """Подгружает данные из файла"""

        bingos = []

        with open(self.json_path, "r", encoding="utf-8") as json_file:
            raw_data = json.load(json_file)

        for item in raw_data:
            bingos.append(
                BingoData(
                    item["title"],
                    item["phrases"]
                )
            )

        return bingos


class SQLiteLoader(Loader):
    """Класс для подгрузки записей из SQLite"""

    # TODO реализовать, если не лень)))

    def __init__(self) -> None:
        raise NotImplementedError
