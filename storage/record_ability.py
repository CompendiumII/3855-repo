from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class RecordAbility(Base):
    __tablename__ = "ability_usage"

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, nullable=False)
    steam_id = Column(Integer, nullable=False)
    match_id = Column(Integer, nullable=False)
    game_version = Column(String(25), nullable=False)
    region = Column(String(25), nullable=False)
    hero_id = Column(Integer, nullable=False)
    hero_name = Column(String(100), nullable=False)
    ability_id = Column(Integer, nullable=False)
    ability_name = Column(String(100), nullable=False)
    ability_level = Column(Integer, nullable=False)
    used_in_game = Column(Integer, nullable=False)
    trace_id = Column(String(150), nullable=False)

    def __init__(self, steam_id, match_id, game_version, region, hero_id, hero_name, ability_id, ability_name, ability_level, used_in_game, trace_id):
        self.date_created = datetime.datetime.now()
        self.steam_id = steam_id
        self.match_id = match_id
        self.game_version = game_version
        self.region = region
        self.hero_id = hero_id
        self.hero_name = hero_name
        self.ability_id = ability_id
        self.ability_name = ability_name
        self.ability_level = ability_level
        self.used_in_game = used_in_game
        self.trace_id = trace_id

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['date_created'] = self.date_created
        dict['steam_id'] = self.steam_id
        dict['match_id'] = self.match_id
        dict['game_version'] = self.game_version
        dict['region'] = self.region
        dict['hero_id'] =self.hero_id
        dict['hero_name'] =self.hero_name
        dict['ability_id'] =self.ability_id
        dict['ability_name'] =self.ability_name
        dict['ability_level'] = self.ability_level
        dict['used_in_game'] = self.used_in_game
        dict['trace_id'] = self.trace_id
        return dict