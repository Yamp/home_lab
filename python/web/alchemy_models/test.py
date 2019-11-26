# from models import *
# from core import lolsession
from web.alchemy_models.core import lolsession
from web.alchemy_models.models import Game

session = lolsession()
df = Game.df_from_ids(session, ids)

print(df.columns)

session.close()
