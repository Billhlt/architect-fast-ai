import requests
from typing import List
from tqdm import tqdm
from prompt import 建筑师文章阅读
import concurrent.futures
# from prompt import 建筑测试长新闻文章
# from github热榜 import display_gh
# from 爬取producthunt热榜 import display_ph
def process_article(idx: int, raw: str, endpoint: str) -> str:
    """处理单篇文章的函数，用于并发执行"""
    prompt = 建筑师文章阅读 + f"\n{raw}"
    print(prompt)
    params = {
        "prompt": prompt,
        "chatId": str(idx)
    }
    resp = requests.post(endpoint, data=params, timeout=60)
    resp.raise_for_status()
    return resp.text.strip()

def optimize_articles(articles: List[str],
                      endpoint: str = "http://localhost:8081/ai/chat",
                      max_workers: int = 200) -> List[str]:
    """ 
    对 articles 列表中的每篇文章调用本地 LLM 进行优化。
    第 i 篇文章使用 chatId = i（从 1 开始）。
    返回与输入顺序一一对应的优化后文章列表。
    使用线程池实现并发请求。
    """
    optimized = [None] * len(articles)  # 预分配结果列表
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_index = {
            executor.submit(process_article, idx, raw, endpoint): idx-1
            for idx, raw in enumerate(articles, start=1)
        }
        
        # 使用tqdm显示进度
        with tqdm(total=len(articles), desc="并发总结提取wx文章内容") as pbar:
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    optimized[index] = future.result()
                except Exception as e:
                    print(f"处理第{index+1}篇文章时出错: {str(e)}")
                    optimized[index] = ""  # 出错时返回空字符串
                pbar.update(1)
    
    return optimized

# print(optimize_articles(建筑测试长新闻文章))
# wxarticles为正式使用，测试文章为测试使用
# 总结内容list = optimize_articles(wxarticles)
# for i in tqdm(range(len(总结内容list)), desc="补充文章链接至末尾"):
#     总结内容list[i]+="\n文章链接为："
#     总结内容list[i]+=wxurl[i]
# 总结内容list.append(display_ph)
# 总结内容list.append(display_gh)


# print(总结内容list)
# 现在 optimized_articles 就是优化后的字符串列表
# for art in optimized_articles:
#     print(art, "\n" + "-"*40)
