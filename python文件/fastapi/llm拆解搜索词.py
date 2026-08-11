import random
import requests
from tqdm import tqdm   # 新增
from prompt import 拆解请求提示词


def process_text(text: str, endpoint: str, pbar: tqdm) -> str:
    """处理单个文本的函数（内部带进度条更新）"""
    prompt = 拆解请求提示词 + f"\n{text}"
    tqdm.write(prompt)          # 用 tqdm.write 避免冲掉进度条

    params = {
        "prompt": prompt,
        "chatId": str(random.randint(1, 1_000_000_000))
    }
    resp = requests.post(endpoint, data=params, timeout=60)
    resp.raise_for_status()

    pbar.update(1)              # 关键：每完成一次请求就更新进度
    return resp.text.strip()


def optimize_text(text: str,
                  endpoint: str = "http://localhost:8081/ai/chat") -> str:
    """对单个文本调用本地 LLM 进行优化。"""
    try:
        # 单个文本也包一层 tqdm，保持接口一致
        with tqdm(total=1, desc="LLM 请求进度") as pbar:
            return process_text(text, endpoint, pbar)
    except Exception as e:
        print(f"处理文本时出错: {e}")
        return ""


# —— 可选：批量接口 ——
def optimize_text_list(text_list: list[str],
                       endpoint: str = "http://localhost:8081/ai/chat") -> list[str]:
    """批量优化，带总进度条"""
    results = []
    with tqdm(total=len(text_list), desc="总进度") as pbar:
        for t in text_list:
            results.append(process_text(t, endpoint, pbar))
    return results

