from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ARRAY, BigInteger, Boolean, Column, DateTime, ForeignKey, Index, Integer, JSON, Numeric, \
    SmallInteger, Text, text, String

from web.alchemy_models.core import LoLBase
import pandas as pd

Base = declarative_base(cls=LoLBase)
metadata = Base.metadata


class Champion(Base):
    __tablename__ = 'champions'

    id = Column(Integer, primary_key=True, server_default=text("nextval('champions_id_seq'::regclass)"))
    name = Column(Text, nullable=True)
    riot_id = Column(Integer, nullable=False)


class EventType(Base):
    __tablename__ = 'event_types'

    id = Column(Integer, primary_key=True, server_default=text("nextval('event_types_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    fields = Column(Text, nullable=False)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, server_default=text("nextval('items_id_seq'::regclass)"))
    riot_id = Column(BigInteger, nullable=False)
    name = Column(Text, nullable=True)


class League(Base):
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True, server_default=text("nextval('leagues_id_seq'::regclass)"))
    slug = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    region = Column(Text, nullable=False)


class MatchType(Base):
    __tablename__ = 'match_types'

    id = Column(Integer, primary_key=True, server_default=text("nextval('match_types_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    best_of = Column(Integer, nullable=True)


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, server_default=text("nextval('players_id_seq'::regclass)"))
    name = Column(Text, nullable=False)


class Spell(Base):
    __tablename__ = 'spells'

    id = Column(Integer, primary_key=True, server_default=text("nextval('spells_id_seq'::regclass)"))
    name = Column(Text, nullable=True)
    riot_id = Column(Integer, nullable=True)


class Team(Base):
    __tablename__ = 'teams'

    __table_args__ = (
        Index('riot_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('teams_id_seq'::regclass)"))
    riot_id = Column(Integer, nullable=True)
    league_id = Column(ForeignKey('leagues.id'), nullable=False)
    slug = Column(Text, nullable=False)
    acronym = Column(Text, nullable=False)
    name = Column(Text, nullable=False)

    league = relationship('League')


class Tournament(Base):
    __tablename__ = 'tournaments'

    __table_args__ = (
        Index('riot_id', unique=False),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('tournaments_id_seq'::regclass)"))
    league_id = Column(ForeignKey('leagues.id'), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    riot_id = Column(Text, nullable=True)

    league = relationship('League')


class Match(Base):
    __tablename__ = 'matches'

    __table_args__ = (
        Index('riot_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('matches_id_seq'::regclass)"))
    datetime = Column(DateTime, nullable=True)
    riot_id = Column(Text, nullable=True)
    type_id = Column(ForeignKey('match_types.id'), nullable=True)
    tournament_id = Column(ForeignKey('tournaments.id'), nullable=True)
    bracket_id = Column(Text, nullable=True)
    type_is_incorrect = Column(Boolean, nullable=False, server_default=text("false"))
    team_1_id = Column(ForeignKey('teams.id'), nullable=True)
    team_2_id = Column(ForeignKey('teams.id'), nullable=True)
    first_choice = Column(SmallInteger)
    status = Column(Text, nullable=True)
    score_1 = Column(SmallInteger, nullable=True)
    score_2 = Column(SmallInteger, nullable=True)

    team_1 = relationship('Team', primaryjoin='Match.team_1_id == Team.id')
    team_2 = relationship('Team', primaryjoin='Match.team_2_id == Team.id')
    tournament = relationship('Tournament')
    type = relationship('MatchType')


class Game(Base):
    __tablename__ = 'games'
    __table_args__ = (
        Index('games_main_key', 'realm_id', 'game_id', 'game_hash', unique=False),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('games_id_seq'::regclass)"))
    riot_id = Column(Text, nullable=False)
    league_id = Column(ForeignKey('leagues.id'), nullable=False)
    match_id = Column(ForeignKey('matches.id'), nullable=False)
    datetime = Column(DateTime, nullable=True)
    num = Column(SmallInteger, nullable=False)
    realm_id = Column(Text, nullable=False)
    game_id = Column(BigInteger, nullable=False)
    game_hash = Column(Text, nullable=False)
    team_1_id = Column(ForeignKey('teams.id'), nullable=False)
    team_2_id = Column(ForeignKey('teams.id'), nullable=False)
    score = Column(Text, nullable=True)
    reddit = Column(Text, nullable=True)
    vods = Column(JSON, nullable=True)
    mh = Column(Text, nullable=True)
    mvp = Column(Text, nullable=True)
    team_1_picks = Column(ARRAY(Text()), nullable=True)
    team_2_picks = Column(ARRAY(Text()), nullable=True)
    team_1_bans = Column(ARRAY(Text()), nullable=True)
    team_2_bans = Column(ARRAY(Text()), nullable=True)
    player_1_id = Column(ForeignKey('players.id'), nullable=False)
    player_2_id = Column(ForeignKey('players.id'), nullable=False)
    player_3_id = Column(ForeignKey('players.id'), nullable=False)
    player_4_id = Column(ForeignKey('players.id'), nullable=False)
    player_5_id = Column(ForeignKey('players.id'), nullable=False)
    player_6_id = Column(ForeignKey('players.id'), nullable=False)
    player_7_id = Column(ForeignKey('players.id'), nullable=False)
    player_8_id = Column(ForeignKey('players.id'), nullable=False)
    player_9_id = Column(ForeignKey('players.id'), nullable=False)
    player_10_id = Column(ForeignKey('players.id'), nullable=False)
    patch = Column(Text, nullable=False)
    season_id = Column(Integer, nullable=True)
    game_duration = Column(BigInteger, nullable=True)
    win = Column(Integer, nullable=False)
    count = Column(Text, nullable=False)

    league = relationship('League')
    match = relationship('Match', backref="games")
    player_1 = relationship('Player', primaryjoin='Game.player_1_id == Player.id')
    player_2 = relationship('Player', primaryjoin='Game.player_2_id == Player.id')
    player_3 = relationship('Player', primaryjoin='Game.player_3_id == Player.id')
    player_4 = relationship('Player', primaryjoin='Game.player_4_id == Player.id')
    player_5 = relationship('Player', primaryjoin='Game.player_5_id == Player.id')
    player_6 = relationship('Player', primaryjoin='Game.player_6_id == Player.id')
    player_7 = relationship('Player', primaryjoin='Game.player_7_id == Player.id')
    player_8 = relationship('Player', primaryjoin='Game.player_8_id == Player.id')
    player_9 = relationship('Player', primaryjoin='Game.player_9_id == Player.id')
    player_10 = relationship('Player', primaryjoin='Game.player_10_id == Player.id')
    team_1 = relationship('Team', primaryjoin='Game.team_1_id == Team.id')
    team_2 = relationship('Team', primaryjoin='Game.team_2_id == Team.id')

    @classmethod
    def get_by_ids(cls, session, ids):
        return session.query(cls).filter(cls.id.in_(ids)).all()

    # @classmethod
    # def get_related(cls, games, session, names):
    #     for game in games:
    #         objects = session.query(cls).filter(cls.id.in_(ids)).all()

    @classmethod
    def df_from_ids(cls, session, ids) -> pd.DataFrame:
        objects = session.query(cls).filter(cls.id.in_(ids)).all()

        dicts = []
        for obj in objects:
            dicts.append(obj.__dict__)
        df = pd.DataFrame(dicts)
        df = df.drop('_sa_instance_state', axis=1)

        return df


class MatchOdd(Base):
    __tablename__ = 'match_odds'

    id = Column(Integer, primary_key=True, server_default=text("nextval('match_odds_id_seq'::regclass)"))
    match_id = Column(ForeignKey('matches.id'), nullable=True)
    full_time = Column(JSON, nullable=True)
    first_set = Column(JSON, nullable=True)
    second_set = Column(JSON, nullable=True)
    third_set = Column(JSON, nullable=True)
    ft_including_ot = Column(JSON, nullable=True)

    match = relationship('Match')


class GamePlayerTimeline(Base):
    __tablename__ = 'game_player_timeline'

    id = Column(Integer, primary_key=True, server_default=text("nextval('game_player_timeline_id_seq'::regclass)"))
    game_id = Column(ForeignKey('games.id'), nullable=False)
    team_id = Column(ForeignKey('teams.id'), nullable=False)
    player_num = Column(SmallInteger, nullable=False)
    player_id = Column('player ', ForeignKey('players.id'), nullable=False)
    secs = Column(Numeric(9, 3), nullable=False)

    game = relationship('Game')
    player = relationship('Player')
    team = relationship('Team')


class GameTeamStat(Base):
    __tablename__ = 'game_team_stats'

    id = Column(Integer, primary_key=True, server_default=text("nextval('game_team_stats_id_seq'::regclass)"))
    game_id = Column(ForeignKey('games.id'), nullable=False)
    team_id = Column(ForeignKey('teams.id'), nullable=False)
    team_num = Column(SmallInteger, nullable=False)
    first_blood = Column(Boolean, nullable=False)
    first_tower = Column(Boolean, nullable=False)
    first_inhibitor = Column(Boolean, nullable=False)
    first_baron = Column(Boolean, nullable=False)
    first_dragon = Column(Boolean, nullable=False)
    first_rift_herald = Column(Boolean, nullable=True)
    tower_kills = Column(SmallInteger, nullable=False)
    inhibitor_kills = Column(SmallInteger, nullable=False)
    baron_kills = Column(SmallInteger, nullable=False)
    dragon_kills = Column(SmallInteger, nullable=False)
    vilemaw_kills = Column(SmallInteger, nullable=False)
    rift_herald_kills = Column(SmallInteger, nullable=True)

    game = relationship('Game', uselist=False)
    team = relationship('Team')


class GameTeamTimeline(Base):
    __tablename__ = 'game_team_timeline'

    id = Column(Integer, primary_key=True, server_default=text("nextval('game_team_timeline_id_seq'::regclass)"))
    game_id = Column(ForeignKey('games.id'), nullable=False)
    team_id = Column(ForeignKey('teams.id'), nullable=False)
    team_num = Column(SmallInteger, nullable=False)
    secs = Column(Numeric(9, 3), nullable=False)

    game = relationship('Game')
    team = relationship('Team')


class GameTimeline(Base):
    __tablename__ = 'game_timeline'

    id = Column(Integer, primary_key=True, server_default=text("nextval('game_timeline_id_seq'::regclass)"))
    game_id = Column(ForeignKey('games.id'), nullable=False)
    secs = Column(Numeric(9, 3), nullable=False)

    game = relationship('Game')


class GameEvent(Base):
    __tablename__ = 'game_events'

    id = Column(Integer, primary_key=True, server_default=text("nextval('game_events_id_seq'::regclass)"))
    timeline_id = Column(ForeignKey('game_timeline.id'), nullable=False)
    game_id = Column(ForeignKey('games.id'), nullable=False)
    secs = Column(Numeric(9, 3), nullable=False)
    type_id = Column(ForeignKey('event_types.id'), nullable=False)
    data = Column(JSON, nullable=False)

    game = relationship('Game')
    timeline = relationship('GameTimeline')
    type = relationship('EventType')


class GamePlayerStat(Base):
    __tablename__ = 'game_player_stats'

    id = Column(Integer, primary_key=True, server_default=text("nextval('game_player_stats_id_seq'::regclass)"))
    game_id = Column(ForeignKey('games.id'), nullable=False)
    player_num = Column(SmallInteger, nullable=True)
    player_id = Column(ForeignKey('players.id'), nullable=True)
    team_id = Column(ForeignKey('teams.id'), nullable=True)
    team_num = Column(SmallInteger, nullable=True)
    team_stat_id = Column(ForeignKey('game_team_stats.id'), nullable=True)
    champion_id = Column(ForeignKey('champions.id'), nullable=True)
    spell_1_id = Column(ForeignKey('spells.id'), nullable=True)
    spell_2_id = Column(ForeignKey('spells.id'), nullable=True)
    masteries = Column(JSON, nullable=True)
    runes = Column(JSON, nullable=True)
    item_0_id = Column(ForeignKey('items.id'), nullable=True)
    item_1_id = Column(ForeignKey('items.id'), nullable=True)
    item_2_id = Column(ForeignKey('items.id'), nullable=True)
    item_3_id = Column(ForeignKey('items.id'), nullable=True)
    item_4_id = Column(ForeignKey('items.id'), nullable=True)
    item_5_id = Column(ForeignKey('items.id'), nullable=True)
    item_6_id = Column(ForeignKey('items.id'), nullable=True)
    kills = Column(Integer, nullable=True)
    deaths = Column(Integer, nullable=True)
    assists = Column(Integer, nullable=True)
    largest_killing_spree = Column(Integer, nullable=True)
    largest_multi_kill = Column(Integer, nullable=True)
    killing_sprees = Column(Integer, nullable=True)
    longest_time_spent_living = Column(Integer, nullable=True)
    double_kills = Column(Integer, nullable=True)
    triple_kills = Column(Integer, nullable=True)
    quadra_kills = Column(Integer, nullable=True)
    penta_kills = Column(Integer, nullable=True)
    unreal_kills = Column(Integer, nullable=True)
    total_damage_dealt = Column(Integer, nullable=True)
    magic_damage_dealt = Column(Integer, nullable=True)
    physical_damage_dealt = Column(Integer, nullable=True)
    true_damage_dealt = Column(Integer, nullable=True)
    largest_critical_strike = Column(Integer, nullable=True)
    total_damage_dealt_to_champions = Column(Integer, nullable=True)
    magic_damage_dealt_to_champions = Column(Integer, nullable=True)
    physical_damage_dealt_to_champions = Column(Integer, nullable=True)
    true_damage_dealt_to_champions = Column(Integer, nullable=True)
    total_heal = Column(Integer, nullable=True)
    total_units_healed = Column(Integer, nullable=True)
    damage_self_mitigated = Column(Integer, nullable=True)
    damage_dealt_to_objectives = Column(Integer, nullable=True)
    damage_dealt_to_turrets = Column(Integer, nullable=True)
    vision_score = Column(Integer, nullable=True)
    time_c_cing_others = Column(Integer, nullable=True)
    total_damage_taken = Column(Integer, nullable=True)
    magical_damage_taken = Column(Integer, nullable=True)
    physical_damage_taken = Column(Integer, nullable=True)
    true_damage_taken = Column(Integer, nullable=True)
    gold_earned = Column(Integer, nullable=True)
    gold_spent = Column(Integer, nullable=True)
    turret_kills = Column(Integer, nullable=True)
    inhibitor_kills = Column(Integer, nullable=True)
    total_minions_killed = Column(Integer, nullable=True)
    neutral_minions_killed = Column(Integer, nullable=True)
    neutral_minions_killed_team_jungle = Column(Integer, nullable=True)
    neutral_minions_killed_enemy_jungle = Column(Integer, nullable=True)
    total_time_crowd_control_dealt = Column(Integer, nullable=True)
    champ_level = Column(Integer, nullable=True)
    vision_wards_bought_in_game = Column(Integer, nullable=True)
    sight_wards_bought_in_game = Column(Integer, nullable=True)
    wards_placed = Column(Integer, nullable=True)
    wards_killed = Column(Integer, nullable=True)
    first_blood_kill = Column(Boolean, nullable=True)
    first_blood_assist = Column(Boolean, nullable=True)
    first_tower_kill = Column(Boolean, nullable=True)
    first_tower_assist = Column(Boolean, nullable=True)
    first_inhibitor_kill = Column(Boolean, nullable=True)
    first_inhibitor_assist = Column(Boolean, nullable=True)
    creeps_per_min_deltas = Column(JSON, nullable=True)
    xp_per_min_deltas = Column(JSON, nullable=True)
    gold_per_min_deltas = Column(JSON, nullable=True)
    cs_diff_per_min_deltas = Column(JSON, nullable=True)
    xp_diff_per_min_deltas = Column(JSON, nullable=True)
    damage_taken_per_min_deltas = Column(JSON, nullable=True)
    damage_taken_diff_per_min_deltas = Column(JSON, nullable=True)

    champion = relationship('Champion')
    game = relationship('Game')
    item0 = relationship('Item', primaryjoin='GamePlayerStat.item_0_id == Item.id')
    item1 = relationship('Item', primaryjoin='GamePlayerStat.item_1_id == Item.id')
    item2 = relationship('Item', primaryjoin='GamePlayerStat.item_2_id == Item.id')
    item3 = relationship('Item', primaryjoin='GamePlayerStat.item_3_id == Item.id')
    item4 = relationship('Item', primaryjoin='GamePlayerStat.item_4_id == Item.id')
    item5 = relationship('Item', primaryjoin='GamePlayerStat.item_5_id == Item.id')
    item6 = relationship('Item', primaryjoin='GamePlayerStat.item_6_id == Item.id')
    player = relationship('Player')
    spell_1 = relationship('Spell', primaryjoin='GamePlayerStat.spell_1_id == Spell.id')
    spell_2 = relationship('Spell', primaryjoin='GamePlayerStat.spell_2_id == Spell.id')
    team = relationship('Team')
    team_stat = relationship('GameTeamStat')


class CalculationResult(Base):
    __tablename__ = 'calculation_result'

    id = Column(Integer, primary_key=True, server_default=text("nextval('game_events_id_seq'::regclass)"))
    game_id = Column(ForeignKey('games.id'), nullable=True)
    timeline_id = Column(ForeignKey('game_timeline.id'), nullable=True)
    service = Column(String(128), nullable=True)
    name = Column(String(128), nullable=True)
    tag = Column(String(128), nullable=True)
    value = Column(String(), nullable=True)

    game = relationship('Game')
    timeline = relationship('GameTimeline')
