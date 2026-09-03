from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
from sqlalchemy.orm import declarative_base
from core.config import Config

DatabaseUrl= Config.DATABASE_URL

engine =create_async_engine(DatabaseUrl)
sessionLocal=AsyncSession(bind=engine)

base=declarative_base()
