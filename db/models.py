from sqlalchemy import Column, Integer, String, Date

from db.database import Base


class Purchase(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    date = Column(Date)

    def __repr__(self) -> str:
        return self.name


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    title = Column(Integer)
    tag = Column(Integer)
    date = Column(Date)

    def __repr__(self) -> str:
        return self.title
