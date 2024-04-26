from enum import StrEnum, auto


class PostGroup(StrEnum):
    articles = auto()
    news = auto()


class PostCategory(StrEnum):
    development = auto()
    administration = auto()
    design = auto()
    management = auto()
    marketing = auto()
    science = auto()
