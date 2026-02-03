from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import os

URL=os.getenv("DATABASE_URL")

engine =create_engine(URL)
sessionLocal=sessionmaker(autoflush=False , autocommit=False , bind=engine)

base=declarative_base()
