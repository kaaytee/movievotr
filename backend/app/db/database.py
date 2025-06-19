from peewee import *
from playhouse.db_url import connect
from app.core.config import settings


db = connect(settings.DATABASE_URL)

def init_db():
    """
    Initializes the database by connecting and creating tables.
    """
    from app.models.model import TABLES_TO_CREATE, User
    from app.core.security import get_password_hash
    db.connect(reuse_if_open=True)
    # db.drop_tables(TABLES_TO_CREATE)
    db.create_tables(TABLES_TO_CREATE, safe=True)

    admin_username = settings.ADMIN_USERNAME
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD    

    if not User.select().where(User.username == admin_username).exists():
        User.create(
            username=admin_username,
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            is_superuser=True
        )

    db.create_tables(TABLES_TO_CREATE)