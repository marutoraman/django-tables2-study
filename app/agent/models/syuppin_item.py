# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import timedelta as delta
from sqlalchemy import Column, String,Text ,DateTime, Float, Integer, ForeignKey, Boolean, func, update
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from sqlalchemy.sql.type_api import STRINGTYPE
from sqlalchemy_utils import UUIDType
from pytz import timezone
import ulid

from common.database import Base, get_ulid, session
from common.logger import set_logger
from common.utility import now_timestamp


class SyuppinItem(Base):
    __tablename__ = 't_syuppin_item'
    mysql_charset = 'utf8mb4',
    mysql_collate = 'utf8mb4_unicode_ci'

    id = Column('id', Integer, primary_key=True)
    account_id = Column('account_id', String(100), nullable=False)
    item_sku = Column('item_sku', String(32), nullable=False,default=ulid.new().str)
    item_name = Column('item_name', String(256), nullable=False)
    item_id = Column('item_id', String(64), nullable=False)
    description = Column('description', String(4096), default="")
    price = Column('price', Integer, default=0)
    amazon_price = Column('amazon_price', Integer, default=0)
    category = Column('category', String(50), nullable=True)
    brand = Column('brand', String(50), nullable=True)
    thumbnail_url = Column('thumbnail_url', String(256), nullable=True)
    image_url1 = Column('image_url1', Text, nullable=True)
    image_url2 = Column('image_url2', Text, nullable=True)
    image_url3 = Column('image_url3', Text, nullable=True)
    image_url4 = Column('image_url4', Text, nullable=True)
    image_url5 = Column('image_url5', Text, nullable=True)
    image_url6 = Column('image_url6', Text, nullable=True)
    image_url7 = Column('image_url7', Text, nullable=True)
    image_url8 = Column('image_url8', Text, nullable=True)
    image_url9 = Column('image_url9', Text, nullable=True)
    is_image1_selected = Column('is_image1_selected', String(10), default="checked")
    is_image2_selected = Column('is_image2_selected', String(10), default="")
    is_image3_selected = Column('is_image3_selected', String(10), default="")
    is_image4_selected = Column('is_image4_selected', String(10), default="")
    is_image5_selected = Column('is_image5_selected', String(10), default="")
    is_image6_selected = Column('is_image6_selected', String(10), default="")
    is_image7_selected = Column('is_image7_selected', String(10), default="")
    is_image8_selected = Column('is_image8_selected', String(10), default="")
    is_image9_selected = Column('is_image9_selected', String(10), default="")
    is_image10_selected = Column('is_image10_selected', String(10), default="")
    condition = Column('condition', String(20), nullable=True)
    shipping_payment = Column('shipping_payment', String(20), nullable=True)
    shipping_method = Column('shipping_method', String(20), nullable=True)
    shipping_prefecture = Column('shipping_prefecture', String(20), nullable=True)
    shipping_leadtime = Column('shipping_leadtime', String(20), nullable=True)
    seller_name = Column('seller_name', String(50), nullable=True)
    is_export_completed = Column('is_export_completed', Boolean, default=False)
    is_alert = Column('is_alert', Boolean, default=False)
    site = Column('site', String(20), nullable=False)
    url = Column('url', Text)
    created_at = Column('created_at', DateTime, nullable=False,
                        default=current_timestamp())
    updated_at = Column('updated_at', DateTime, nullable=False,
                        default=current_timestamp(), onupdate=func.utc_timestamp())

