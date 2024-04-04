import sys
from typing import List
from .classes.Collection import Collection
from .classes.Logger import Logger


def is_colab() -> bool:
    return 'google.colab' in sys.modules


def collection(items: List[any]):
    return Collection(items)


def danger(message: str) -> None:
    Logger.danger(message)
