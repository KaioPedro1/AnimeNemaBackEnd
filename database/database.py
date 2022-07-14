from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utilidades import configuracao

SQLALCHEMY_DATABASE_URL = f'postgresql://{configuracao.settings.database_username}:{configuracao.settings.database_password}@{configuracao.settings.database_hostname}:{configuracao.settings.database_port}/{configuracao.settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()