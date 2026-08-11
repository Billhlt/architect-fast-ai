import requests
import re # 正则表达式模块
import json
from bs4 import BeautifulSoup
url = "https://www.gooood.cn/japan-pavilion-expo-2025-osaka-kansai-by-nikken-sekkei-ltd.htm"
headers = {    
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
   ,"Referer": "https://www.gooood.cn/"
}

response = requests.get(url, headers=headers)
# print(response.text)
data = response.text
garticleinfo = re.findall('window.__INITIAL_STATE__=(.*?)</script>',data)[0]
# print(garticleinfo)
json_data=json.loads(garticleinfo) # 将字符串转换为json格式(字典)

gdwordarticle_data = json_data['post']['content']# 获取混杂文章的内容
# print(gdwordarticle_data)

soup = BeautifulSoup(gdwordarticle_data, 'html.parser') # soup只含有需要的文章和文章对应的代码内容。
# print(soup)

html_str = str(soup)
pattern = re.compile(r'<p>▼(.*?)</p>', re.DOTALL)
matched_items = pattern.findall(html_str)
cleaned_content = pattern.sub('', html_str)
# print(cleaned_content)
# print(matched_items)



# 提取文本内容
cleaned = BeautifulSoup(cleaned_content, 'html.parser').get_text()   #干净的文本内容，缺点：（中文+英文）
print(cleaned)



# 使用列表推导式处理每个元素，而无需将整个matched_items列表转换为字符串后才能去除HTML标签
matched = [BeautifulSoup(item, 'html.parser').get_text() for item in matched_items]  #图片的配套说明文字组成的列表。len(matched)=len(img_links)
# print(matched)
# print(len(matched))



# 提取图片链接
img_links = [img['data-src'] for img in soup.find_all('img') if 'data-src' in img.attrs]  #图片链接组成的列表。len(matched)=len(img_links)
# print(len(img_links))
# print(img_links)



# # 提取链接
# links = [a['href'] for a in soup.find_all('a') if 'href' in a.attrs]
# print(links)



