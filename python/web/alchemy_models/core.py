import pandas as pd
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def lolsession():
    engine = create_engine('postgresql://root:lol-math-pass-2018@54.93.112.189:5432/lol_math', echo=False)
    Session = sessionmaker(bind=engine)
    dbsession = Session()

    return dbsession


class LoLBase:
    @classmethod
    def get_df(cls, session) -> pd.DataFrame:
        d = list()
        with tqdm(total=100) as pbar:
            print('Making query...')

            objects = session.query(cls).all()

            pbar.update(100)

            for obj in objects:
                d.append(obj.__dict__)
            df = pd.DataFrame(d)
            df = df.drop('_sa_instance_state', axis=1)

            return df

