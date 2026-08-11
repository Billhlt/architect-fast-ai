import requests
import json
import re
from bs4 import BeautifulSoup
import pprint    
import time
import datetime
from tqdm import tqdm
from datetime import datetime, timedelta


# 记录-->6月12日创业邦哔哩哔哩空间地址：https://space.bilibili.com/405261267    (+?spm_id_from=333.337.search-card.all.click)
# 记录-->6月12日周鸿祎哔哩哔哩空间地址：https://space.bilibili.com/627947058    (+?spm_id_from=333.337.search-card.all.click)

# token：2007767388
#################微信公众号网站（供传入print_wxoa()）
# 1.机器之心
机器之心 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzA3MzI4MjgzMw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"
# 2.量子位
量子位 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzIzNjc1NzUzMw%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"
# 3.创业邦
创业邦 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTAzMjc4MA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"
# 4.新智元
新智元 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzI3MTA0MTk1MA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"
# 5.XR Vision Pro
xrvision = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTY1ODgxMg==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"
# 6.阿里云开发者
阿里云开发者 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5OTY1ODgxMg==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"
# 7.APPSO
appso = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5MjAyNDUyMA==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"
# 8._36氪
_36氪 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzI2NDk5NzA0Mw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"
# 9.CodeSheep
codesheep = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzU4ODI1MjA3NQ==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"
# 10.智能涌现
智能涌现 = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&search_field=null&begin=0&count=5&query=&fakeid=MzkwMDQ2NDU2Nw==&type=101_1&free_publish_type=1&sub_action=list_ex&fingerprint=6f364151a7d28971c6feb6c8bd5f7650&token=2007767388&lang=zh_CN&f=json&ajax=1"


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@爬取微信公众号文章相关信息@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
def print_wxoa(url): # oa -> Official Account
    headers ={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    ,"Referer": "https://mp.weixin.qq.com/"
    ,"cookie" : "noticeLoginFlag=1; eas_sid=C1E7Y4T8Z3h4v9u3B7l2W3L6C7; pgv_pvid=9247808219; ua_id=egOd87dhTcHQEz6vAAAAAKfhcAjnu4Hv4isbJBP_lzg=; wxuin=49733519244516; mm_lang=zh_CN; yyb_muid=3534CD11B82067032834D8E1B9F2667C; RK=j/NAMJc7MV; ptcz=a418fbc06b82bf3957c4f72d10e4cc7d30a4460768091ad355e4529d9177f262; _ga=GA1.1.1992704597.1762070983; _ga_PF3XX5J8LE=GS2.1.s1762070982$o1$g0$t1762070992$j50$l0$h0; _qimei_uuid42=19b0210093510092ae636f3e598e04d7a3b14f3bcf; _qimei_fingerprint=cb8424c1c4448d1c39cfde47cc88a2aa; _qimei_i_3=4cc95383c70e57d29596fc365ad770b3f6bca0a21b0a078be088280a2095713a336337903989e2aad088; _qimei_h38=52f7f066ae636f3e598e04d709000003819b02; _qimei_i_1=74df6487970c578dc191f8610e8270e6a1edf1f41b535682b0db2f582f93206c6163349d3980b0dcd4f3dad5; rand_info=CAESICWsBJ5TW/TfEK4cZVOIiRWI6i/0x9ZGYziABUhSnuRD; slave_bizuin=3935680643; data_bizuin=3935680643; bizuin=3935680643; data_ticket=8p6/Vm3KIl/lc5eyK6ktzI7CFZ1akVZLLE+qI1qqMU2/ANU0soltLD/66zxXaoyZ; slave_sid=SU5DWUtvV1VPVmoxV2FVQTF0V0NXRXlhMXVybndoaVdnU0lYRDB2aHlzWUZhd0Y0SEk5OFpFZDFXMW9sWWNNWWp3WTRlWHJkM0FMYnMxSlBaQzBXU2cwNFJyWm05cWxZOFdnNHdZUDVqSFZyTHU2QTZmZmFBdU1iSEtnbUhOdW9pN21nWHdhUDNSeHpJRXBl; slave_user=gh_25b58f0685d7; xid=ae73847753dab0807f683762102eb7b2; poc_sid=HFoBCGmjF9wXROZumQEe-XzoAXhxkKLxEENGLON9; _clck=3935680643|1|g0r|0; _clsk=7qmb41|1762304943846|2|1|mp.weixin.qq.com/weheat-agent/payload/record"
    ,
    
    }
    param ={
    "search_field": "null",
    "begin": "0",
    "count": "5",
    "query": "",
    "fakeid": "Mz",
    "data": "sub: list",
    "IzNjc1NzUzMw==": "",
    "type": "101_1",
    "free_publish_type": "1",
    "sub_action": "list_ex",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1"
    }
    i="0"
    j="5"


    response = requests.get(url,headers=headers,params=param).text
    # print(response)

    pattern = r'create_time\\\\\\\":(\d{2,11}),\\\\\\\"is'
    timinfo = re.findall(pattern,response) 
    for i in range(len(timinfo)): 
        timinfo[i] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timinfo[i])))

    pattern = r'/s\\\\\\\\\\\\/(.{1,30})\\\\\\\",\\\\\\\"digest'# 提取文章链接  
    urlinfo = re.findall(pattern,response) # 提取文章链接 
    for i in range(len(urlinfo)): 
        urlinfo[i]='https://mp.weixin.qq.com/s/'+urlinfo[i]
        
        
    pattern = r'title\\\\\\\":\\\\\\\"(.{1,65})\\\\\\\",\\\\\\\"cover'
    titleinfo = re.findall(pattern,response) 
    

    for i in range(len(titleinfo)):
        print(str(i+1)+"."+titleinfo[i])
    print("------------------------------------------------------")    
    for i in range(len(titleinfo)):
        print(str(i+1)+"."+timinfo[i],"\t",urlinfo[i])



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@爬取bilibili热榜@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
def print_bilihot():
    # 以下为爬取app网页版b站热搜的代码
    url = "https://app.bilibili.com/x/v2/search/trending/ranking?csrf=45735bafe7cb3edcf0fddbd3a4e74e36&limit=30"
    headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
            
        }
    # 30+1个热搜，1为红色置顶新闻
    response = requests.get(url, headers=headers).text
    json_data=json.loads(response) 
    # print(response.status_code)


    # 以下为单次赋值并输出热搜名称和链接的代码
    # i=0
    # nameinfo = json_data['data']['list'][i]['show_name']
    # urlinfo = "https://search.bilibili.com/all?keyword="+nameinfo
    # print(nameinfo)
    # print(urlinfo)

###############循环打印热搜名称和链接###############

    print()
    print("#######################b站热搜榜#######################")
    for i in range(30):
        nameinfo = json_data['data']['list'][i]['show_name']
        urlinfo = "https://search.bilibili.com/all?keyword="+nameinfo
        print(nameinfo,'\t\t\t', urlinfo)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@爬取github热榜@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
def print_github():
    #三个url，分别是：https://kkgithub.com/trending、https://github.com/trending、https://github-zh.com/trending
    url = "https://github.com/trending"
    headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
            ,"Referer" : "https://www.baidu.com/"
            ,"Cookie" : "_gh_sess=3HN80ueYD7IPOkgZnwQCqVsd7660FBcjUGGFE26qhUZXCJh48vmB0F%2FVcY4g4yKk5vTdfekQcWiFmanpL1nkszCbJMzeT%2BpnQjGAYe6fSdbFh7sCqpceFxHBNujeTwU4MvREuk1g5Tm6JOmmc9sjU1Ixxw%2BDG5flGiEwFglNrd6snkqyiiGicjqWlLvS0hKok3Zgcs0gThNxfMAI7Pd2y%2BGurcTtPd88pkVbiaUc3HmnidHJysG587qppczr%2FbMwWYc7KqYle4fmrYMeN%2BlsKQ%3D%3D--M3TsIQFP7uvSEX4D--BQlBpDhtQt2HLxBooVUi7A%3D%3D; _octo=GH1.1.2058701624.1757464753; logged_in=no; cpu_bucket=xlg; preferred_color_mode=light; tz=Asia%2FShanghai"
        }
    respons = requests.get(url, headers=headers)
    response =respons.text
    #################github项目地址#################
    # 项目地址为github.com/项目作者/项目名称
    # 获取项目作者和名称
    pattern = r'<span data-view-component="true" class="text-normal">(.*?)</a>  </h2>'
    nameinfo = re.findall(pattern,response,re.DOTALL)
    # 使用 BeautifulSoup 清理内容
    ghname = []
    for item in nameinfo:
        # 解析HTML内容
        soup = BeautifulSoup(item, 'html.parser')
        # 提取纯文本内容并去除多余的空格和换行符
        clean_text = soup.get_text(strip=True)
        ghname.append(clean_text)

    # 获取项目描述
    pattern = r'</a>  </h2>(.*?)<div class="f6 color-fg-muted mt-2">'
    decripsioninfo = re.findall(pattern,response,re.DOTALL)
    # 使用 BeautifulSoup 清理内容
    ghdescri = []
    for item in decripsioninfo:
        # 解析HTML内容
        soup = BeautifulSoup(item, 'html.parser')
        # 提取纯文本内容并去除多余的空格和换行符
        clean_text = soup.get_text(strip=True)
        ghdescri.append(clean_text)


    # print(ghname)
    # print(ghdescri)
    display_gh=""
    for i in range(len(ghdescri)):
        display_gh+=f"@@@{i+1}.项目名：{ghname[i]}\n项目描述：{ghdescri[i]}\n"
    print(display_gh)







#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@爬取producthunt热榜（下午4点更新最新一天热榜）@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
def print_producthunt():
        # 获取昨天的日期
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    url = 'https://decohack.com/producthunt-daily-' + yesterday_str + '/'

    response = requests.get(url, timeout=20).text


    titles, slogans, intros, prod_links, ph_links, votes = [], [], [], [], [], []

    # 使用正则表达式提取标题
    title_pattern = r'<h2>.*?<a[^>]*>(.*?)</a></h2>'
    titles_raw = re.findall(title_pattern, response, re.DOTALL)
    for title in titles_raw:
        # 去掉前面的序号 "1. "、"2. "……
        clean_title = re.sub(r'^\d+\.\s*', '', title.strip())
        titles.append(clean_title)

    # 使用正则表达式提取产品块
    product_blocks = re.findall(r'<h2>.*?</h2>(.*?)<p><img', response, re.DOTALL)

    for block in product_blocks:
        # 标语
        slogan_match = re.search(r'<strong>标语</strong>：(.*?)<br />', block)
        slogan = slogan_match.group(1).strip() if slogan_match else ''
        slogans.append(slogan)
        
        # 介绍
        intro_match = re.search(r'<strong>介绍</strong>：(.*?)(?:<br/?>|<strong>)', block, re.DOTALL)
        intro = re.sub(r'<.*?>', '', intro_match.group(1)).strip() if intro_match else ''
        intros.append(intro)
        
        # 产品网站
        prod_match = re.search(r'<strong>产品网站</strong>: <a href="(.*?)"', block)
        prod_link = prod_match.group(1).strip() if prod_match else ''
        prod_links.append(prod_link)
        
        # Product Hunt 网站
        ph_match = re.search(r'<strong>Product Hunt</strong>: <a href="(.*?)"', block)
        ph_link = ph_match.group(1).strip() if ph_match else ''
        ph_links.append(ph_link)
        
    # 票数
    pattern = r'<strong>票数</strong>: 🔺(.*?)<br />'# 提取文章链接  
    votes = re.findall(pattern,response)
    display_ph = ""

    for i in range(30):
        display_ph+=f"@@@{i+1}.标题：{titles[i]}\n标语：{slogans[i]}\n介绍：{intros[i]}\n产品网站：{prod_links[i]}\nProduct Hunt 网站：{ph_links[i]}\n票数：{votes[i]}\n\n"
    print(display_ph)










榜单 = "000" # 榜单[0]和榜单[1]取值分别代表是否输出b站热搜和github热榜，“0”代表不输出，“1”代表输出
if 榜单[0] == "1":
    print_bilihot()
if 榜单[1] == "1":
    print_github()
if 榜单[2] == "1":
    print_producthunt()




work = "10" # work[0]和work[1]取值分别代表是否输出常更新和少更新的up主视频，公众号信息，“0”代表不输出，“1”代表输出
play = "00" #同变量work
if work[0] == "1":
    
    # print("####################### b站 metagpt 视频#######################")
    # print_up_video("metagpt")
    # print("####################### b站 周鸿祎 视频#######################")
    # print_up_video("周鸿祎")
    # print("####################### b站 创业邦 视频#######################")
    # print_up_video("创业邦")
    print("####################### wxoa 量子位 #######################")
    print_wxoa(量子位)
#    print("####################### wxoa 新智元 #######################")


if work[1] == "1":
    print("####################### b站 秋芝2046 视频#######################")
    print_up_video("秋芝2046")
    print("####################### b站 同济子豪兄 视频#######################")
    print_up_video("同济子豪兄")
    print("####################### b站 AI研究室-帆哥 视频#######################")
    print_up_video("AI研究室-帆哥")
    print("####################### b站 无处安放的小A 视频#######################")
    print_up_video("创业邦")
    print("####################### b站 小Lin说 视频#######################")
    print_up_video("小Lin说")
    print("####################### b站 ai产品观察 视频#######################")
    print_up_video("ai产品观察")
    print("####################### b站 metagpt 视频#######################")
    print_up_video("metagpt")





if play[0] == "1":
    print("####################### b站 柳冲冲 视频#######################")
    print_up_video("柳冲冲")
    print("####################### b站 我不是黄毛 视频#######################")
    print_up_video("我不是黄毛")    
 

if play[1] == "1":
    print("####################### b站 henry的小木屋 视频#######################")
    print_up_video("henry的小木屋")
    print("####################### b站 毕的二阶导 视频#######################")
    print_up_video("毕的二阶导")    





