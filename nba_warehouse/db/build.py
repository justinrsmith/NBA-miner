from sqlalchemy.orm import sessionmaker

from models import base, db


base.metadata.create_all(db)