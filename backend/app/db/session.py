from database import sessionLocal

async def get_db():
    async with sessionLocal() as db:
        yield db
