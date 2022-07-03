from sqlalchemy import Column, Integer, String, Date

from db.database import Base


class Purchase(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    date = Column(Date)
    test = Column(String)

    def __repr__(self) -> str:
        return self.name
