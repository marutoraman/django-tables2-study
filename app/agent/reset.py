import os
import sys
import subprocess
# 上位のBASEとなるフォルダをPATHに追加することで、モジュールの名前解決を可能とする
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm.session import Session
from sqlalchemy import or_
from common.logger import set_logger, delete_backlog
from agent.models.user import User
from agent.manage.manage import *
from common.database import SessionLocal


logger = set_logger(__name__)

def reset_is_crawle():
    logger.info("is_crawle リセット開始")
    db: Session = SessionLocal()
    db.query(User).update({User.is_crawle:False},synchronize_session=False)
    db.commit()
    logger.info("is_crawle リセット完了")
    
if __name__ == '__main__':
    reset_is_crawle()
