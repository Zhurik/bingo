import win32com.client as win32
import os
from math import sqrt
from datetime import datetime
from random import shuffle

from bingo_data import BingoData

from typing import List


class BingoGenerator:
    """
    Гененрирует бинго по заданным данным
    """

    # Количество ячеек в бинго
    SMALL = 16
    NORMAL = 25

    TEMPLATES_PATH = "./Templates/"

    TEMPLATES = {
        SMALL: "Bingo_16.docx",
        NORMAL: "Bingo_25.docx"
    }

    SAVE_PATH = "./"

    BOOKMARK_TITLE = "TITLE"
    BOOKMARK_DATE = "DATE"
    BOOKMARK_TABLE = "TABLE"

    MONTHS = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря"
    }

    def __init__(
        self,
        bingo: BingoData
    ) -> None:
        self.title = bingo.title.upper()
        self.phrases = bingo.phrases

        if len(self.phrases) <= self.SMALL:
            self._set_table_variables(self.SMALL)
        else:
            self._set_table_variables(self.NORMAL)

    def _set_table_variables(
        self,
        template_size: int
    ) -> None:
        """Задаем путь до шаблона и размер таблицы"""
        self._template = self.TEMPLATES_PATH + self.TEMPLATES[template_size]
        self._max_words = template_size
        self._table_size = int(sqrt(template_size))

    def _generate_new_filename(self) -> str:
        """
        Собираем уникальное имя файла

        Для этого берём текущий заголовок бинго, дату и микросекунды
        """
        return os.path.join(
            os.getcwd(),
            self.SAVE_PATH,
            self.title +
            " " +
            str(datetime.now().date()) +
            " - " +
            str(datetime.now().microsecond) +
            ".docx"
        )

    def _fill_date(self) -> None:
        """Оформляем дату в закладке с русским названием месяца"""
        today = datetime.now().date()

        day = str(today.day)
        month = self.MONTHS[today.month]
        year = str(today.year)

        date = " ".join((day, month, year))

        self._new_doc_file.Bookmarks(self.BOOKMARK_DATE).Range.Text = date

    def _fill_bookmarks(self) -> None:
        """Заполняем закладки в открытом файле"""

        self._new_doc_file.Bookmarks(
            self.BOOKMARK_TITLE
        ).Range.Text = self.title

        self._fill_date()

        table = self._new_doc_file.Bookmarks(
            self.BOOKMARK_TABLE
        ).Range.Tables(1)

        shuffle(self.phrases)

        # Делаем +1, потому что VBA считает с единицы
        for i, string in enumerate(self.phrases[:self._max_words]):
            table.Cell(
                i // self._table_size + 1,
                i % self._table_size + 1
            ).Range.Text = string

    def generate_bingo(self) -> None:
        """Создать бинго из шаблона"""

        try:
            word_app = win32.dynamic.Dispatch("Word.Application")
            word_app.Visible = False

            self._new_doc_file = word_app.Documents.Open(
                os.path.abspath(self._template)
            )

            self._fill_bookmarks()

            self._new_doc_file.SaveAs(self._generate_new_filename())

        except:
            # TODO Сделать нормальную обработку ошибок
            pass

        finally:
            self._new_doc_file.Close()
            word_app.Quit()

    def generate_n_bingos(
        self,
        n: int
    ) -> None:
        """Создать n бинго в одном файле"""
        # TODO сделать
        raise NotImplementedError
