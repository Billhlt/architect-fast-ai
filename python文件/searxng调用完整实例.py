import requests, re
import json
from bs4 import BeautifulSoup






#################以下代码实现调用搜索api获取返回的搜索url，title简单集合#################
header = {
          
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    
}
# question = input("What is your question? ")
url = "http://localhost:8080/search?q="+"今日新闻"+"&format=json&pageno=1"
response = requests.get(url, headers=header).text
jsondata=json.loads(response) 

results_count = len(jsondata['results'])
urls = [result['url'] for result in jsondata['results']]
titles = [result['title'] for result in jsondata['results']]
#################输出集合url，集合title的值#################
# print("URLs:", urls)
# print("titles:", titles)
#################获取集合urls，集合titles的元素数量和搜索结果的数量#################
# print(len(urls))
# print(len(titles))
# print(results_count)






#################以下代码实现从搜索url集合中爬取对应的文章#################
def extract_text(url):
    headers = header
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')

    # 1. 去噪：删除明显不相关的标签
    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
        tag.decompose()

    # 2. 取最长 <p> 父节点作为正文容器（经验规则）
    p_nodes = soup.find_all('p')
    if not p_nodes:
        return soup.get_text(' ', strip=True)    # 兜底
    parent = max(set(p.parent for p in p_nodes), key=lambda x: len(x.get_text()))
    text = parent.get_text(separator='\n', strip=True)

    # 3. 合并空行
    return re.sub(r'\n{2,}', '\n\n', text)
#################集合urls中的文章内容集合#################
articles = [extract_text(url) for url in urls]
print(articles)
