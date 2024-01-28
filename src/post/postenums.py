from enum import Enum


class PostGroup(str, Enum):
    articles = 'articles'
    news = 'news'


class PostCategory(str, Enum):
    Development = 'Development'
    Administration = 'Administration'
    Design = 'Design'
    Management = 'Management'
    Marketing = 'Marketing'
    Science = 'Science'
