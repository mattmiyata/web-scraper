from bs4 import BeautifulSoup
import requests
import re  #regular expression

# with open('index.html', 'r') as f: 
#     doc = BeautifulSoup(f, 'html.parser')

# # print(doc.prettify())

# tags = doc.find_all('p')[0]

# print(tags.find_all('b'))

# url = "https://www.newegg.com/p/27N-008H-00001"

# result = requests.get(url)
# # print(result.text)
# doc = BeautifulSoup(result.text, 'html.parser')

# prices = doc.find_all(string='$')
# parent = prices[0].parent
# strong = parent.find('strong')
# print(strong.string)

##############################################################
# tag = doc.find('option')
# tag['value'] = 'new value'
# tag['color'] = 'blue'
# print(tag.attrs)
# print(tag)

# tags = doc.find_all(["p", "div", "li"])
# print(tags)
    
# tags = doc.find_all(['option'], string='Undergraduate')
# print(tags)

# tags = doc.find_all(class_='btn-item')
# print (tags)

# tags = doc.find_all(string=re.compile('\$.*'), limit=1)
# print(tags)
# for tag in tags:
#     print(tag.strip())
    
# tags = doc.find_all('input', type='text')
# for tag in tags:
#     tag['placeholder'] = 'I changed you!'
    
# with open('changed.html', 'w') as file: 
#     file.write(str(doc))

##############################################################

# url = 'https://coinmarketcap.com/'
# result = requests.get(url).text
# doc = BeautifulSoup(result, 'html.parser')

# tbody = doc.tbody
# trs = tbody.contents
# # print(trs[0].parent.name)

# # print(list(trs[0].children))

# prices = {}

# for tr in trs[:10]: 
#     name, price = tr.contents[2:4]
#     fixed_name = name.p.string
#     fixed_price = price.span.string

#     prices[fixed_name] = fixed_price


# print(prices)
    
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