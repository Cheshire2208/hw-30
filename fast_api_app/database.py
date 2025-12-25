from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

engine = create_async_engine(DATABASE_URL, echo=True)
# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = async_sessionmaker(engine, expire_on_commit=False)
session = async_session()
Base = declarative_base()
