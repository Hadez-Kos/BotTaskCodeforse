from sqlalchemy import create_engine
from .models import theme, task, intersection
from config import DB_PASS, DB_NAME, DB_USER, DB_PORT, DB_HOST


class Database:
    def __init__(self):
        self.engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True)

    async def insert_data_task(self, data):
        with self.engine.connect() as conn:
            query_task = task.insert().values(data).returning(task)

            dt = conn.execute(query_task).fetchall()

    async def insert_data_theme(self, data):
        with self.engine.connect() as conn:
            query_theme = theme.insert().values(data).returning(theme)

            dt = conn.execute(query_theme).fetchall()

