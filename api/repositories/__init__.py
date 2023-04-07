from models.article import Article
from models.user import User

from .article import ArticleRepository
from .user import UserRepository

user_repo = UserRepository(User)
article_repo = ArticleRepository(Article)
