from dataclasses import dataclass
from typing import List


@dataclass
class BingoData:
    """Формат хранения данных для бинго"""

    title: str
    phrases: List[str]
