import requests
from db import engine, User, Counts
from sqlalchemy.orm import scoped_session, sessionmaker
import concurrent.futures
import threading
import time
import bigjson

db_session = scoped_session(sessionmaker(bind=engine))

if __name__ == "__main__":
    with open("user.json", "rb") as file:
        data = bigjson.load(file)
        for item in data:
            counts = Counts(**item['counts'])
            user = User(counts, **item)
            db_session.add(counts)
            db_session.add(user)
            db_session.commit()

