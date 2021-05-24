import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode
import time
import re

from agent.models.searched_item import *

HEADERS =  {"Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36}"}
RAKUMA_BASE_URL = "https://fril.jp/"
RAKUMA_ITEM_URL = "https://item.fril.jp/"
RAKUMA_SEARCH_URL = RAKUMA_BASE_URL + "s"
        
class FetchRakumaItem():
    
    @staticmethod
    def fetch_html(url:str) -> str:
        '''
        指定したurlのhtmlテキストを取得
        '''
        headers = HEADERS
        res = requests.get(url,headers=headers)
        if not(300 > res.status_code >= 200):
             raise Exception(f"リクエストエラー:{url} / status:{res.status_code}")
         
        return res.text 
    
    @staticmethod
    def fetch_items(urls:list):
        item_ids = []
        for url in urls:
            m = re.search(r"item.fril.jp/(.{32})", url)
            if m == None:
                continue
            item_ids.append(m.group(1))
        items = []
        for id in item_ids:
            try:
                items.append(FetchRakumaItem.fetch_item(RAKUMA_ITEM_URL + id, id))
            except Exception as e:
                print(f"HTTPアクセスエラー:{id}")
            #time.sleep(3) #可能な限り最速化
            
        return list(filter(None, items)) # Noneは除外
        
    @staticmethod
    def fetch_item(url:str, item_id:str):
        try:
            res_text = FetchRakumaItem.fetch_html(url)
            soup = bs(res_text,"html.parser")
            
            item_id = item_id
            item_name = soup.select_one(".item__name")
            description = soup.select_one(".item__description")
            table_th = soup.select(".item__details th")
            table_td = soup.select(".item__details td")
            images = soup.select(".sp-image")
            price = soup.select_one(".item__value")
            category = FetchRakumaItem.find_table_th_get_td(table_th, table_td, "カテゴリ")
            condition = FetchRakumaItem.find_table_th_get_td(table_th, table_td, "商品の状態")
            shipping_payment = FetchRakumaItem.find_table_th_get_td(table_th, table_td, "配送料の負担")
            shipping_method = FetchRakumaItem.find_table_th_get_td(table_th, table_td, "配送方法")
            shipping_prefecture = FetchRakumaItem.find_table_th_get_td(table_th, table_td, "発送元の地域")
            shipping_leadtime = FetchRakumaItem.find_table_th_get_td(table_th, table_td, "発送日の目安")
            seller_name =  soup.select_one(".header-shopinfo__shop-name span")
        except Exception as e:
            print(e)
            return None

        thumbnail_url = images[0].get("src") if len(images) != 0 else None
        image_urls = [image.get("src") for image in images]
        # カテゴリのパース
        _categories = category.split("›")
        _categories = [_cat.replace("\n","").strip() for _cat in _categories]
        category = "・".join(_categories)
        price = int(price.text.replace("￥","").replace(",",""))
        
        return SearchedItem(item_name=item_name.text, item_id=item_id, description=description.text, 
                           thumbnail_url=thumbnail_url, image_urls=image_urls, category=category, brand="", condition=condition,
                           shipping_payment=shipping_payment, shipping_method=shipping_method, 
                           shipping_prefecture=shipping_prefecture, shipping_leadtime=shipping_leadtime,
                           seller_name=seller_name.text, site="rakuma", url=url, price=int(price))
    
    @staticmethod
    def fetch_keyword_searched_item_urls(url:str):
        res_text = FetchRakumaItem.fetch_html(url)
        soup = bs(res_text,"html.parser")
        # ページが存在しない場合は空の配列を返す
        if soup.select_one(".nohit") != None:
            return []
        items = soup.select(".item-box__image-wrapper a")
        item_urls = [item.get("href") for item in items]
        
        return item_urls
    
    @staticmethod
    def fetch_keyword_searched_items(keyword:str, min_price:int=300, max_price:int=2000000, max_page_num:int=1):
        urls = []
        # 最大ページ数分をスクレピング
        for page in range(max_page_num):
            url = RAKUMA_SEARCH_URL + "?" + FetchRakumaItem.create_search_query(keyword,min_price,max_price,page)
            _urls = FetchRakumaItem.fetch_keyword_searched_item_urls(url)
            # ページが存在しない場合は終了
            if len(_urls) == 0:
                break 
            urls.extend(_urls)
        items = []
        for url in urls:
            m = re.search(r"item.fril.jp/(.{32})", url)
            if m == None:
                continue
            item = FetchRakumaItem.fetch_item(url,item_id=m.group(1))
            if item != None:
                items.append(item)

        return items
    
    @staticmethod
    def create_search_query(keyword:str, min_price:int=0, max_price:int=None, page:int=1):
        query_dict = {
            "query":keyword,
            "min":min_price,
            "max":max_price,
            "status":"new",
            "transaction":"selling",
            "page":page
        }
        return urlencode(query_dict)
    
    @staticmethod
    def find_table_th_get_td(th_list,td_list, target:str):
        for th,td in zip(th_list,td_list):
            if th.text.strip() == target: #余分な文字列が含まれる場合がある
                return td.text
        else:
            return None