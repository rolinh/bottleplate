from sqlalchemy.ext.declarative import declarative_base
import sys

sys.path = ['../../..'] + sys.path

Base = declarative_base()
Db_url = 'sqlite:///:memory:'
