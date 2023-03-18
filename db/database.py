from sqlalchemy import create_engine, func
from sqlalchemy.sql import select, text
from .models import theme, task, intersection
from config import DB_PASS, DB_NAME, DB_USER, DB_PORT, DB_HOST
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True
        )
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
        task_id = select(task).where(
            task.c.name == data["name"] and task.c.number == data["number"]
        )
        theme_id = []

        for i in data["theme"]:
            theme_id.append(select(theme).where(theme.c.name == i))

        for j in theme_id:
            tk_id = self.session.execute(task_id).first()
            te_id = self.session.execute(j).first()
            self.session.execute(
                intersection.insert().values(task_id=tk_id[0], theme_id=te_id[0])
            )

        self.session.commit()

    async def get_data_theme(self):
        themes = []

        for i in self.session.query(theme).distinct().all():
            themes.append(i.name)

        return list(set(themes))

    async def get_data_solution(self, them):
        solution = []

        for i in self.session.execute(
            select(task)
            .join(intersection, task.c.id == intersection.c.task_id)
            .join(theme, theme.c.id == intersection.c.theme_id)
            .where(theme.c.name == them)
            .distinct()
        ):
            solution.append(i.solution)

        return list(set(solution))

    async def get_list_tasks(self, data):
        lst = []
        if data["theme"] and data["solution"]:
            for i in self.session.execute(
                text(
                    """select task.id, task.name, task.number, task.solution, task.url from task join intersection on task.id=intersection.task_id join theme on intersection.theme_id = theme.id 
where theme.name = :theme and task.solution >= :solution
group by task.id
having count(task.id) = 1
ORDER BY task.solution  DESC
LIMIT 10"""
                ),
                data,
            ):
                lst.append(
                    f"Task: {i.number}\nname: {i.name}\nsolution: {i.solution}\nurl: {i.url}"
                )
                lst.append("-" * 20)
            return lst
        else:
            return lst
