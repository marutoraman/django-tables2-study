from common.database import SessionLocal
from sqlalchemy.orm import sessionmaker,scoped_session,Session
from common.logger import set_logger, delete_backlog
from agent.models.syuppin_item import *
from agent.models.fetch_url import *
from agent.models.blacklist_seller import *
from agent.models.blacklist_word import *
from agent.engine.fetch_mercari_item import *
from agent.engine.fetch_rakuma_item import *
from agent.models.profit import *
from agent.models.search_word import *
from agent.models.replace_word import *
import ulid

logger = set_logger(__name__)

MAX_WORDS_COUNT = 20
MAX_URLS_COUNT = 1000

class Manage():
    def __init__(self,account_id:str):
        self.account_id = account_id
        self.db:Session=SessionLocal()
        self.replace_words = self.fetch_replace_words()
        self.is_alert_item = False
        
    def manage_fetch_items(self):
        '''
        各サイトからスクレイピングしてitemをDBに格納
        '''        
        # URLを取得
        logger.info("商品URL取得開始")
        url_objects = self.db.query(FetchUrl).filter_by(account_id=self.account_id, 
                                                         is_completed=False).limit(MAX_URLS_COUNT)
        mercari_urls = [obj.url for obj in url_objects if obj.url.find(MERCARI_BASE_URL) >= 0]
        rakuma_urls = [obj.url for obj in url_objects if obj.url.find(RAKUMA_ITEM_URL) >= 0]
        logger.info(f"mercari url:{len(mercari_urls)} 件")
        logger.info(f"rkauma url:{len(rakuma_urls)} 件")
        
        # URL指定スクレイピング
        items = []
        logger.info("URL指定スクレイピング開始")
        items.extend(FetchMercariItem.fetch_mercari_items(mercari_urls))
        logger.info(f"取得商品数(mercari):{len(items)}件")
        items.extend(FetchRakumaItem.fetch_items(rakuma_urls))
        logger.info(f"取得商品数累計(mercari+rakuma):{len(items)}件")
        
        # キーワード指定スクレイピング
        logger.info("キーワード指定スクレイピング開始")
        word_objects = self.db.query(SearchWord).filter_by(account_id=self.account_id, 
                                                           is_completed=False).limit(MAX_WORDS_COUNT)
        mercari_search_words = [obj.search_word for obj in word_objects if obj.search_site == "mercari"]
        rakuma_search_words = [obj.search_word for obj in word_objects if obj.search_site == "rakuma"]
        logger.info(f"mercari search word:{len(mercari_search_words)}件")
        logger.info(f"rakuma search word:{len(rakuma_search_words)}件")
        for word in mercari_search_words:
            items.extend(FetchMercariItem.fetch_keyword_searched_items(word))
        logger.info(f"取得商品数累計(mercari+rakuma+mercari_word):{len(items)}件")
        for word in rakuma_search_words:
            items.extend(FetchRakumaItem.fetch_keyword_searched_items(word))
        logger.info(f"取得商品数累計(mercari+rakuma+mercari_word+rakuma_word):{len(items)}件")
        
        logger.info(f"商品情報取得完了:{len(items)}件")
        
        # itemへの後処理(除外、出品価格計算)
        items = self.exclude_blacklist_items(items)
        items = self.calc_syuppin_price(items)
        logger.info(f"除外後商品数累計:{len(items)}件")
        
        # DB更新
        self.insert_items(items)
        
        # 完了フラグをセット
        for obj in url_objects:
            obj.is_completed = True
        for obj in word_objects:
            obj.is_completed = True
        self.db.commit()
        
        logger.info(f"商品情報更新完了:{len(items)}件")

        return items

    def insert_items(self, items:list):
        '''
        itemをDBに登録
        '''
        update_count = 0
        # １ページ分の更新データを全て処理する
        for item in items:
            if item.is_remove == False: # 除外フラグTrue(is_remove=True)はDBにインポートしない
                image_urls = item.image_urls
                for i in range(len(item.image_urls),10):
                    image_urls.append(None)
                self.is_alert_item = False # アラート状態をリセット
                self.db.add(
                    SyuppinItem(
                        account_id=self.account_id,
                        item_id = item.item_id,
                        item_name = self.replace_word(item.item_name), #置換処理対象
                        thumbnail_url=item.thumbnail_url,
                        image_url1=image_urls[0],
                        image_url2=image_urls[1],
                        image_url3=image_urls[2],
                        image_url4=image_urls[3],
                        image_url5=image_urls[4],
                        image_url6=image_urls[5],
                        image_url7=image_urls[6],
                        image_url8=image_urls[7],
                        image_url9=image_urls[8],
                        category = item.category,
                        description = self.replace_word(item.description), #置換処理対象
                        price = item.price,
                        brand = item.brand,
                        condition = item.condition,
                        shipping_payment = item.shipping_payment,
                        shipping_method = item.shipping_method,
                        shipping_prefecture = item.shipping_prefecture,
                        shipping_leadtime = item.shipping_leadtime,
                        seller_name = item.seller_name,
                        site = item.site,
                        url = item.url,
                        amazon_price = item.amazon_price,
                        item_sku = ulid.new().str,
                        is_alert = self.is_alert_item
                        )
                    )
                update_count += 1
            
        
        # 一括更新
        logger.info(f"bulk inport begine(update/total):{update_count} / {len(items)}")
        #self.db.bulk_save_objects(update_objects)
        self.db.commit()
        logger.info(f"bulk inport end")
            
    
    def exclude_blacklist_items(self, items:list):
        '''
        itemからブラックリストを除外(is_remove=Trueとする)
        '''
        # 除外リストを取得
        blacklist_seller_objects = self.db.query(BlacklistSeller).filter_by(account_id=self.account_id).all()
        blacklist_sellers = [obj.seller_name for obj in blacklist_seller_objects]
        blacklist_word_objects = self.db.query(BlacklistWord).filter_by(account_id=self.account_id).all()
        blacklist_words = [obj.blacklist_word for obj in blacklist_word_objects]
        
        # 除外処理(除外フラグを立てる)
        print(len(items))
        items = [item for item in items if item.seller_name not in blacklist_sellers]
        print(len(items))
        for item in items:
            for word in blacklist_words:
                if item.item_name.find(word) >= 0 or item.description.find(word) >= 0:
                    item.is_remove=True
                    break
            
        return items


    def calc_syuppin_price(self, items:list):
        profit_objects = self.db.query(Profit).filter_by(account_id=self.account_id).order_by("base_price").all()
        
        for item in items:
            for obj in profit_objects:
                if obj.base_price >= int(item.price):
                    #item.amazon_price = item.price + obj.profit # 現在価格＋設定した利益(円)
                    item.amazon_price = obj.profit # 現在価格は関係なく、設定した金額に設定（ご要望により仕様変更）
                    break
                
        return items
                
    
    def replace_word(self, target: str):
        if self.replace_words == None:
            return target
        for replace in self.replace_words:
            # 基準ワードが見つかったらITEMをアラート対象とする
            self.is_alert_item = True if target.find(replace.base_word) >= 0 and replace.is_alert else self.is_alert_item
            if replace.is_alert:
                replace.replace_word = "\u2757" + replace.base_word + "\u2757" 
            
            _replace_word = "" if replace.replace_word == None else replace.replace_word
            target = target.replace(replace.base_word, _replace_word)
            
        return target
    

    def fetch_replace_words(self):
        # 置換ワード取得
        replace_words = self.db.query(ReplaceWord).filter_by(
            account_id=self.account_id).all()
        
        return replace_words
