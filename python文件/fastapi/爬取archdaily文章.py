import requests
import re
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

headers = {    
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Referer": "https://www.archdaily.cn/"
}

def fetch_archdaily_articles(url: str):
    try:
        # 获取页面内容
        print("正在获取页面内容...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        # 提取文章信息
        print("正在解析文章内容...")
        data = response.text
        adarticleinfo = re.findall(r'<span class="afd-specs__value">([\s\S]*?)<h2 class=\'afd-post-content-h2 article__subtitle\'>项目图库</h2>', data)[0]
        
        # 使用BeautifulSoup解析
        soup = BeautifulSoup(adarticleinfo, 'html.parser')
        cleaned_text = soup.get_text()
        
        # 提取图片链接并显示进度
        print("正在提取图片链接...")
        img_tags = soup.find_all('img')
        img_links = []
        
        # 使用tqdm显示进度条
        for img in tqdm(img_tags, desc="处理图片链接"):
            if 'data-src' in img.attrs:
                img_links.append(img['data-src'])
            elif 'src' in img.attrs:
                img_links.append(img['src'])
            time.sleep(0.01)  # 添加小延迟以便观察进度条
        
        print(f"成功提取 {len(img_links)} 张图片链接")
        return cleaned_text, img_links
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None, None


# 以下为测试用例
# adarticles=[]
# imgs=[]
# adurls=['https://www.archdaily.cn/cn/1034494/ba-sai-er-helvetia-yuan-qu-he-er-zuo-ge-and-de-mei-long-jian-zhu-shi-wu-suo?ad_source=search&ad_medium=projects_tab']
# for i in tqdm(adurls, desc="从链接提取archdaily文章和图片"):
#     cleaned_text, img_links=fetch_archdaily_articles(i)
#     adarticles.append(cleaned_text)
#     imgs.append(img_links)
# print(adarticles)
# print(imgs)



# img_links = [img['data-src'] for img in soup.find_all('img') if 'data-src' in img.attrs]  #图片链接组成的列表。len(matched)=len(img_links)
# print(len(img_links))
# print(img_links)


# html_str = str(soup)
# pattern = re.compile(r'<p>▼(.*?)</p>', re.DOTALL)
# matched_items = pattern.findall(html_str)
# cleaned_content = pattern.sub('', html_str)
# # print(cleaned_content)
# # print(matched_items)



# 提取文本内容
# cleaned = BeautifulSoup(soup, 'html.parser').get_text()   #干净的文本内容，缺点：（中文+英文）
# print(cleaned)



# # 使用列表推导式处理每个元素，而无需将整个matched_items列表转换为字符串后才能去除HTML标签
# matched = [BeautifulSoup(item, 'html.parser').get_text() for item in matched_items]  #图片的配套说明文字组成的列表。len(matched)=len(img_links)
# # print(matched)
# # print(len(matched))



# # 提取图片链接
# img_links = [img['data-src'] for img in soup.find_all('img') if 'data-src' in img.attrs]  #图片链接组成的列表。len(matched)=len(img_links)
# # print(len(img_links))
# # print(img_links)



# # 提取链接
# links = [a['href'] for a in soup.find_all('a') if 'href' in a.attrs]
# print(links)


# <div id="ads-single-mobile-banner">
# <h2 class='afd-post-content-h2 article__subtitle'>项目图库</h2>

