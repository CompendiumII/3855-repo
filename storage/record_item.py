from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class RecordItem(Base):
    __tablename__ = "item_usage"

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, nullable=False)
    steam_id = Column(Integer, nullable=False)
    match_id = Column(Integer, nullable=False)
    game_version = Column(String(25), nullable=False)
    region = Column(String(25), nullable=False)
    item_id = Column(Integer, nullable=False)
    item_name = Column(String(100), nullable=False)
    item_type = Column(String(100), nullable=False)
    item_cost = Column(Integer, nullable=False)
    obtain_status = Column(String(100), nullable=False)
    used_in_game = Column(Integer, nullable=False)
    trace_id = Column(String(150), nullable=False)

    def __init__(self, steam_id, match_id, game_version, region, item_id, item_name, item_type, item_cost, obtain_status, used_in_game, trace_id):
        self.date_created = datetime.datetime.now()
        self.steam_id = steam_id
        self.match_id = match_id
        self.game_version = game_version
        self.region = region
        self.item_id = item_id
        self.item_name = item_name
        self.item_type = item_type
        self.item_cost = item_cost
        self.obtain_status = obtain_status
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
        dict['item_id'] =self.item_id
        dict['item_name'] =self.item_name
        dict['item_type'] =self.item_type
        dict['item_cost'] =self.item_cost
        dict['obtain_status'] = self.obtain_status
        dict['used_in_game'] = self.used_in_game
        dict['trace_id'] = self.trace_id
        return dict