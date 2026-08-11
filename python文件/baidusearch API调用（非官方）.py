from baidusearch.baidusearch import search

results = search('今日美股和A股行情如何', num_results =100)
print(f"共找到 {len(results)} 条结果")
for result in results:
    print(f"标题: {result['title']} - 链接: {result['url']}")
