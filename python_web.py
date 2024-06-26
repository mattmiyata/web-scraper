from bs4 import BeautifulSoup
import requests
import re  #regular expression


    
search_term = input('What product do you want to search for?')

url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, 'html.parser')

page_text = doc.find(class_='list-tool-pagination-text').strong
print(page_text)
pages = int(str(page_text).split('/')[-2].split('>')[-1][:-1])

items_found = {}

for page in range(1, pages + 1): 
    url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')
    div = doc.find(class_='item-cells-wrap border-cells short-video-box items-grid-view four-cells expulsion-one-cell')

    items = div.find_all(string=re.compile(search_term))
    for item in items:
        parent = item.parent
        if parent.name != 'a':
            continue
        link = parent['href']
        try:
            next_parent = item.find_parent(class_='item-container')
            price = next_parent.find(class_='price-current').strong.string
        
            items_found[item] = {'price': int(price.replace(",", '')), 'link': link}
        except: 
            pass
sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items: 
    print(item[0])
    print(f'${item[1]['price']}')
    print(item[1]['link'])
    print('--------------------------------------------')
