# 分词
import pandas as pd
import jieba

# 词频生成词云
import numpy as np
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image


# 读取
def read_excel():
    df = pd.read_excel("所有答案.xlsx")
    l = list(df["content"])
    return l


# 将原来的文件转换成只有必要信息的txt文件
def writeDown():
    list = read_excel()
    with open('所有答案.txt', 'w', encoding='utf-8') as f:
        for data in list:
            try:
                str = data + '\n'
                f.write(str)
            except Exception as e:
                print(e)


# 统计词频
def countDown():
    # 读取stopword,及各种没有意义的词语,以免影响词频分析
    with open('stopwords.txt', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
    with open('所有答案.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        words = jieba.lcut(text, cut_all=True)

        counts = {}
        for word in words:
            if word not in stopwords:
                # 不统计字数为一的词
                if len(word) == 1:
                    continue
                else:
                    counts[word] = counts.get(word, 0) + 1
                    # counts = {'a':7, 'b':14}
        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)
        return items, counts


# 绘制词云
def draw_cloud(dic):
    graph = np.zeros((400, 600, 3), dtype=np.int)
    # 参数分别是指定字体、背景颜色、最大的词的大小、使用给定图作为背景形状
    wc = WordCloud(font_path='simkai.ttf', background_color='black', max_words=200, mask=graph)
    wc.generate_from_frequencies(dic)  # 根据给定词频生成词云
    wc.to_file('所有答案.png')  # 图片命名


if __name__ == '__main__':
    writeDown()
    items, counts = countDown()
    # 绘制词云
    draw_cloud(counts)
    # 保存到新文件
    df = pd.DataFrame(items, columns = ["词语","频率"])
    df.to_excel("词频.xlsx", index=False)
