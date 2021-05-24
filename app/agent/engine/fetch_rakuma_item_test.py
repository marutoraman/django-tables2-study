from agent.engine.fetch_rakuma_item import *


def test_fetch_item():
    item = FetchRakumaItem.fetch_item("https://item.fril.jp/dc7f0a91546c0e82fbfe8b031d1db920","eaa62f927bd6c76fffc1a5c0f425b4e0")
    print(item.__dict__)
    
    assert item.item_name
    assert item.condition

def test_fetch_items():
    items = FetchRakumaItem.fetch_items(["https://item.fril.jp/eaa62f927bd6c76fffc1a5c0f425b4e0","https://item.fril.jp/b80eaefbff28c31ba1425a939eb54f0b","https://item.fril.jp/ee64709d25f9f599bf14f2d478a4266b"])
    
    for item in items:
        assert item.item_name
        assert item.condition

def test_fetch_search_items():
    items = FetchRakumaItem.fetch_keyword_searched_items("コマさん",300,1000,max_page_num=5)
    
    for item in items:
        assert item.item_name
        assert item.condition
        
    print(len(items))