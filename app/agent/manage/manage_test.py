from agent.manage.manage import *
from common.database import SessionLocal

def test_mercari():
    manage = Manage("takashi002013")
    items = manage.manage_fetch_items()
    
    print([item.item_name for item in items])
    

def test_mercari2():
    manage = Manage("takashi002013")
    items = manage.manage_fetch_items()
    items = manage.exclude_blacklist_items(items)
    
    print([item.is_remove for item in items])
    
    
def test_is_alert():
    manage = Manage("takashi002013")
    manage.replace_word("妖怪ウォッチのおもちゃ")
    assert manage.is_alert_item
    
    

def test_exclude_items():
    db=SessionLocal()
    manage = Manage("takashi002013")
    items = FetchMercariItem.fetch_keyword_searched_items("コマさん")
    print(len(items))
    items = manage.exclude_blacklist_items(items)
    print(len(items))
    manage.insert_items(items)
    