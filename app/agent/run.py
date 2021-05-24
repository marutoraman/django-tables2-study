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
try:
    delete_backlog()  # 過去ログの削除
except:
    pass

SHUTDOWN_CMD = ["sudo", "shutdown", "-h", "now"]  # シャットダウンコマンド



def run(account_id:str=None):

    # クロール日時が最も古いユーザーを取得
    db: Session = SessionLocal()

    # モードに応じて処理を実施
    if account_id == None:
        # クロール中でないアカウントのうち、クロール完了日時が最も古いアカウントを処理する
        obj = db.query(User).filter(or_(User.is_crawle==False, User.is_crawle==None)).order_by(User.crawled_at.asc()).first()
        if obj == None:
            logger.info(f"[skip] mode:商品検索 対象アカウントなし")
            return False
    else:
        obj = db.query(User).filter_by(account_id=account_id).first()
    if obj == None:
        logger.error("ユーザー情報が取得できませんでした")
        return False
    logger.info(f"[begin] mode:商品検索 / account_id:{obj.account_id}")
    obj.is_crawle = True
    db.commit() # crawlステータスを更新
    
    try:
        manage = Manage(obj.account_id)
        manage.manage_fetch_items()
    except Exception as e:
        logger.error(f"商品検索エラー:{e}")
        
    obj.is_crawle = False
    obj.crawled_at = now_timestamp()
    db.commit()
    logger.info(f"[end] mode:商品検索 / account_id:{obj.account_id}")

    #if os.name == 'posix':  # Linux　➙　本番環境の場合の処理
        # IPを変える必要があるため、処理１回ごとにシャットダウンをかける
     #   time.sleep(120)  # すぐにシャットダウンすることを防ぐ
     #   subprocess.run(SHUTDOWN_CMD)

if __name__ == '__main__':
    account_id = None
    if len(sys.argv) >= 2:
        account_id = sys.argv[1]
    run(account_id)
