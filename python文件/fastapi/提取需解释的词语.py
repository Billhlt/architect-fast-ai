import requests
from typing import List
from 爬取公众号文章链接中的文章内容2 import wxarticles
from tqdm import tqdm
from prompt import 获取文章总结内容需要解释的词语提示词
from llm总结文章list import 总结内容list
import concurrent.futures
import ast
def process_article(idx: int, raw: str, endpoint: str) -> str:
    """处理单篇文章的函数，用于并发执行"""
    prompt = 获取文章总结内容需要解释的词语提示词 + f"\n{raw}"
    params = {
        "prompt": prompt,
        "chatId": str(idx+1000)  # 保持原有的chatId分配逻辑
    }
    resp = requests.post(endpoint, data=params, timeout=60)
    resp.raise_for_status()
    return resp.text.strip()

def optimize_articles(articles: List[str],
                      endpoint: str = "http://localhost:8081/ai/chat",
                      max_workers: int = 200) -> List[str]:
    """
    对 articles 列表中的每篇文章调用本地 LLM 获取需解释的词语。
    第 i 篇文章使用 chatId = i+1000（从 1 开始）。
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
        with tqdm(total=len(articles), desc="并发获取需解释词语") as pbar:
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    f=ast.literal_eval(future.result())
                    optimized[index] = f
                except Exception as e:
                    print(f"处理第{index+1}篇文章时出错: {str(e)}")
                    optimized[index] = ""  # 出错时返回空字符串
                pbar.update(1)
    
    return optimized

需解释词语列表 = optimize_articles(总结内容list)
# print(需解释词语列表)
# 现在 optimized_articles 就是优化后的字符串列表
# for art in optimized_articles:
#     print(art, "\n" + "-"*40)