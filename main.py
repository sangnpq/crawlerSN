import requests
from db import engine, User, Counts
from sqlalchemy.orm import scoped_session, sessionmaker
import concurrent.futures
import threading
import time
import json


thread_local = threading.local()
# define db
db_session = scoped_session(sessionmaker(bind=engine))

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {json.loads(response.text)} from {url}")
        counts = Counts(**response[0]['counts'])
        user = User(counts, **response)
        db_session.add(counts)
        db_session.add(user)
        db_session.commit()

def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)

if __name__ == "__main__":
    url = "https://api.gapo.vn/main/v1.0/user?id=%d"
    limit = 5
    sites = [ url %(i + 1) for i in range(0, limit) ]

    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")