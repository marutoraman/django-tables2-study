# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import timedelta as delta
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Boolean, func, update
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from pytz import timezone

from common.database import Base, get_ulid, session
from common.logger import set_logger
from common.utility import now_timestamp

CRAWL_INTERVAL = 3600

class User(Base):
    __tablename__ = 'users_user'
    mysql_charset = 'utf8mb4',
    mysql_collate = 'utf8mb4_unicode_ci'

    uuid = Column('uuid', UUIDType(binary=False), primary_key=True)
    account_id = Column('account_id', String(100), nullable=False)
    begin_crawle_at = Column('begin_crawle_at', DateTime, nullable=True)
    is_crawle = Column('is_crawle', Boolean, default=False)
    crawled_at = Column('crawled_at', DateTime, nullable=True)
