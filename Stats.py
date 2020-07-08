import requests
import json
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
import math

################################################
# 读取文本
################################################
with open("./old.txt", 'r', encoding='utf-8') as txt:
    oldText = txt.read()
oldText = oldText.strip()
maxInterval = 15000
maxIndex = math.ceil(len(oldText) / maxInterval)

################################################
# 调用api进行分词
################################################
url = "http://27.221.81.242:3333/HanlpApi"
res_list = []
for i in range(0, maxIndex):
    payload = {
        'text':'海是蓝色的',
        # 'text':oldText,     # 太长了，api限制，会失败
        # 'text': oldText[maxInterval * i:maxInterval * (i + 1)],
        'apiKey': '054351a823654192abd7ee815fdbe70d',
    }
    response = requests.post(url, data=payload)
    res = json.loads(response.text)["data"]
    res_list += list(map(lambda item: item["word"], res))

################################################
# 词频统计
################################################
stop_words = []
with open("./cn_stopwords.txt", 'r', encoding='utf-8') as txt:
    stop_words = txt.read().split('\n')
counter = {}
for word in res_list:
    if len(word) < 2:
        continue
    if word in stop_words:
        continue
    try:
        counter[word] += 1
    except:
        counter[word] = 1
wordcloud_data = list(
    map(lambda item: (item, counter[item]), counter))  # 两种遍历方式，对应两种不同写法；上面是遍历key值，下面是遍历各项，其中0取key，1取value
# wordcloud_data = list(map(lambda item: (item[0], item[1]), counter.items()))


################################################
# 词云
################################################
words = sorted(wordcloud_data, key=lambda d: d[1], reverse=True)
# words = wordcloud_data[:20]
# WordCloud模块，链式调用配置，最终生成html文件
c = (
    WordCloud()
        .add("", words[:50], word_size_range=[20, 100], shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title="老人与海"))
        .render("老人与海_词云展示.html")
)
