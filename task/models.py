from sqlalchemy import Column, Integer, String, MetaData, Table, ForeignKey

metadata = MetaData()

theme = Table(
    "theme",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False)
)

task = Table(
    "task",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("solution", Integer, nullable=False),
    Column("name", String, nullable=False),
    Column("number", String, nullable=False),
    Column("difficulty", Integer, nullable=False),
    Column("url", String, nullable=False)
)

intersection = Table(
    "intersection",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task_id", Integer, ForeignKey("task.id")),
    Column("theme_id", Integer, ForeignKey("theme.id"))
)
