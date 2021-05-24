from agent.engine.fetch_mercari_item import *


def test_fetch_item():
    item = FetchItem.fetch_mercari_item("https://www.mercari.com/jp/items/m29504875027/")
    print(item.__dict__)
    
    assert item.item_name
    assert item.condition
    

def test_fetch_items():
    item = FetchItem.fetch_mercari_items(["https://www.mercari.com/jp/items/m29504875027/","https://www.mercari.com/jp/items/m20942656719/"])
    print(item.__dict__)
    
    assert item.item_name
    assert item.condition
        

def test_fetch_item_urls():
    urls = FetchItem.fetch_keyword_searched_item_urls("https://www.mercari.com/jp/search/?sort_order=&keyword=%E3%81%93%E3%81%BE%E3%81%95%E3%82%93&category_root=&brand_name=&brand_id=&size_group=&price_min=1000&price_max=3000&item_condition_id%5B1%5D=1&status_on_sale=1")
    print(urls)
    
def test_fetch_keyword():
    items = FetchMercariItem.fetch_keyword_searched_items("こまさん",300,3000,5)
    
    for item in items:
        assert item.item_name
        assert item.condition
        assert len(item.image_urls) >= 1
        
    print(len(items))
    