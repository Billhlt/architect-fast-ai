import requests, re
from bs4 import BeautifulSoup
header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
       ,"Cookie": "eas_sid=C1E7Y4T8Z3h4v9u3B7l2W3L6C7; pgv_pvid=9247808219; ua_id=egOd87dhTcHQEz6vAAAAAKfhcAjnu4Hv4isbJBP_lzg=; wxuin=49733519244516; mm_lang=zh_CN; yyb_muid=3534CD11B82067032834D8E1B9F2667C; _clck=3935680643|1|fy4|0; rand_info=CAESIC+LHuZiu2piMcraUI87LjWOzNfvC676Kwp2FwuhABPp; slave_bizuin=3935680643; data_bizuin=3935680643; bizuin=3935680643; data_ticket=hY+Xbi1/eA16LtuP0mAvGXYZoaO0qHscCE+woiMYDL9O9jrVNqqf/F7P2MM7d7g3; slave_sid=ZEtvVDhFWmtaM0NIYkZKbjRyQ21uZWJaREhveVkwazdBSUtKV3pGaDU0TWIzRXZYVW1oaGpaaks2NHA4c1puSERjalVwOTRETGtEdWJyeWEyb3VzNlQ0S2VLbVBHbTBQQkQ0U2xFZWNVRThOVXhNdjh5VVBJSEJFR3JlbWx1eDdxTE9RdzdIbGtoY09la2tp; slave_user=gh_25b58f0685d7; xid=63b76499cce0c5ca569a4871574c1332; _clsk=mk0we5|1754127625085|3|1|mp.weixin.qq.com/weheat-agent/payload/record; poc_sid=HKPIjmijKPVzWNIQHLCY2TsxCTFVCrpYEBFu5vRp; rewardsn=; wxtokenkey=777"              
       
    }
def extract_text(url):
    headers = header
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    r.encoding = 'utf-8'
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

if __name__ == '__main__':
    print(extract_text('https://mp.weixin.qq.com/s/tVAOdjL7WVGwXyE2rXyusA'))
# import requests
# from gne import GeneralNewsExtractor

# url = 'https://blog.csdn.net/JouJz/article/details/149388471?spm=1000.2115.3001.10524'      # 任意文章页
# header = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                       "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#     }
# html = requests.get(url, headers=header).text
# info  = GeneralNewsExtractor().extract(html)
# print(info['title'])      # 标题
# print(info['publish_time'])  # 发布时间
# print(info['content'])   # 纯正文
