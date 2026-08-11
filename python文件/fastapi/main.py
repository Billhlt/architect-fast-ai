import json
from fastapi import FastAPI
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
from shared_data import vue_content
import shared_data
from llm拆解搜索词 import optimize_text
from 爬取archdaily搜索界面 import fetch_archdaily_urls
from 爬取archdaily文章 import fetch_archdaily_articles
from tqdm import tqdm
from llm总结文章list import optimize_articles
# from llm总结文章list import 总结内容list
app = FastAPI()
# 允许所有来源跨域（生产环境建议限制）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/vue-data")
async def receive_vue_data(content: str = Body(...)):  # 使用Body接收请求体
    # print("前端传来的内容：", content)
    拆解完成词=optimize_text(content) #调用拆解用户搜索句的函数
    # print(拆解完成词)
    titles, adurls = fetch_archdaily_urls(拆解完成词)
    # print(titles,adurls)
    adarticles = []
    imgs = []
    for i in tqdm(adurls, desc="从链接提取archdaily文章和图片"):
        cleaned_text, img_links=fetch_archdaily_articles(i)
        adarticles.append(cleaned_text)
        imgs.append(img_links)
    
    # print(adarticles)
    print(imgs)
    总结内容list = optimize_articles(adarticles)
    for i in tqdm(range(len(总结内容list)), desc="补充文章链接至末尾"):
        总结内容list[i]+="\n文章链接为："
        总结内容list[i]+=adurls[i]
    with open("vue_data.json", "w", encoding="utf-8") as f:
        json.dump(总结内容list, f, ensure_ascii=False)
    with open("pics_data.json", "w", encoding="utf-8") as f:
        json.dump(imgs, f, ensure_ascii=False)
    return content
    
@app.get("/api/summary")
def get_summary():
    with open("vue_data.json", "r", encoding="utf-8") as f:
        content = json.load(f)  # 这里会自动将 JSON 数组转换为 

    return content

@app.get("/api/pics")
def get_pics_urls():
    with open("pics_data.json", "r", encoding="utf-8") as f:
        content = json.load(f)  # 这里会自动将 JSON 数组转换为 

    return content

# @app.get("/api/summary")
# def get_summary():
#     return vue_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)


