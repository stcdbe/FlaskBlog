from enum import Enum


class UserStatus(str, Enum):
    Default = 'Default'
    Author = 'Author'
    Admin = 'Admin'


class PostType(str, Enum):
    article_post = 'article_post'
    news_post = 'news_post'


class PostCategory(str, Enum):
    Development = 'Development'
    Administration = 'Administration'
    Design = 'Design'
    Management = 'Management'
    Marketing = 'Marketing'
    Science = 'Science'
