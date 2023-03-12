from sqlalchemy import create_engine
from sqlalchemy.sql import select
from .models import theme, task, intersection
from config import DB_PASS, DB_NAME, DB_USER, DB_PORT, DB_HOST
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        self.engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

    async def insert_data_task(self, data):
        self.session.execute(task.insert().values(data))
        self.session.commit()

    async def insert_data_theme(self, data):
        for el in list(data):
            self.session.execute(theme.insert().values(name=str(el)))
        self.session.commit()

    async def insert_data_intersection(self, data):
        task_id = select(task).where(task.c.name == data['name'] and task.c.number == data['number'])
        theme_id = []

        for i in data['theme']:
            theme_id.append(select(theme).where(theme.c.name == i))

        for j in theme_id:
            tk_id = self.session.execute(task_id).first()
            te_id = self.session.execute(j).first()
            self.session.execute(intersection.insert().values(task_id=tk_id[0], theme_id=te_id[0]))

        self.session.commit()

