from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeMeta
from sqlalchemy.ext.declarative import as_declarative
from settings import DB_HOST, DB_NAME, DB_PASS, DB_USER

engine = create_engine(f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4", echo=True)

metadata = MetaData(bind=engine)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)


@as_declarative(metadata=metadata)
class Base:
    pass
