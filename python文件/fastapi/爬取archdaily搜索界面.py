import requests
import re  # 正则表达式模块
import json
from bs4 import BeautifulSoup
from tqdm import tqdm  # 导入tqdm模块

def fetch_archdaily_urls(search_term: str):
    """
    从ArchDaily搜索并获取文章标题和链接

    参数:
        search_term (str): 搜索关键词，将用于构建搜索URL

    返回:
        tuple: (文章标题列表, 文章链接列表)
    """
    ur = "https://www.archdaily.cn/search/api/v1/cn/projects?q= "
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Referer": "https://www.archdaily.cn/"
    }

    url = ur + search_term
    response = requests.get(url, headers=headers)
    data = response.text
    json_data = json.loads(data)  # 将字符串转换为json格式(字典)

    adtitles = []  # 存储文章标题
    adurls = []  # 存储文章链接
    
    # 使用tqdm显示进度条
    for i in tqdm(range(len(json_data['results'])), desc="正在获取文章标题和链接"):
        adtitles.append(json_data['results'][i]['title'])   # 添加文章标题
        adurls.append(json_data['results'][i]['url'])       # 添加文章链接

    return adtitles, adurls





# 示例使用
if __name__ == "__main__":
    titles, urls = fetch_archdaily_urls("建筑 兰")
    print(titles)
    print(urls)