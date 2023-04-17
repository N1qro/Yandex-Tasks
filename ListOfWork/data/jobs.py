from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class Job(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = Column(Integer, autoincrement=True, primary_key=True)
    team_leader = Column(Integer, ForeignKey("users.id"))
    job = Column(String)
    work_size = Column(Integer)
    collaborators = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_finished = Column(Boolean)
