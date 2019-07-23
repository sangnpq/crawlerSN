from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


engine = create_engine("mysql+pymysql://root:root@localhost/gapo_crawl?charset=utf8mb4")
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    id = Column(Integer)
    id_chat = Column(String(255))
    username = Column(String(255))
    display_name = Column(String(2048))
    avatar =  Column(String(4096))
    cover = Column(String(4096))
    gender = Column(Integer)
    birthday = Column(String(255))
    location = Column(String(2048))
    counts_id = Column(Integer, ForeignKey('counts.id'))
    counts = relationship("Counts", backref=backref('counts', uselist=False))
    status = Column(Integer)
    create_time = Column(Integer)
    relation = Column(String(2048))
    status_verify = Column(Integer)
    data_source = Column(Integer)

    def __init__(self, counts_inp, **kwargs):
        self.counts = counts_inp
        for key in kwargs.keys():
            if hasattr(self, key):
                if key != 'counts':
                    setattr(self, key, kwargs[key])

class Counts(Base):
    __tablename__ = 'counts'

    id = Column(Integer, primary_key=True)
    post_count = Column(Integer)
    friend_count = Column(Integer)

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

if __name__ == "__main__":
    Base.metadata.create_all(engine)







