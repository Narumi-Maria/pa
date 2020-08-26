#分词
import csv
import jieba

#词频生成词云
import numpy as np
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image

#读取csv文件
def read_csv(filename):
    dict_made=[]
    with open(filename,'r',newline='',encoding='utf-8') as f:
        reader= csv.DictReader(f,delimiter = ',',quotechar='"')
        for row in reader:
            dict_made.append(dict(row))
    return dict_made
    
#将原来的csv文件转换成只有必要信息的txt文件
def writeDown(file):
    list = read_csv(file+'.csv')
    with open(file+'.txt','w',encoding='utf-8') as f:
        for data in list:
            str = data['title'] + ':' + data['review'] + '\n'
            f.write(str)

#统计词频
def countDown(file):   
    #读取stopword,及各种没有意义的词语,以免影响词频分析
    with open('stopwords.txt',encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
    with open(file+'.txt','r',encoding='utf-8') as f:
        text = f.read()
        words = jieba.lcut(text, cut_all=True)
        
        counts = {}
        for word in words:
            if word not in stopwords:  
                #不统计字数为一的词  
                if len(word) == 1:  
                    continue  
                else:  
                    counts[word] = counts.get(word,0) + 1  
                    
        #counts = {'a':7, 'b':14}
        items = list(counts.items())
        items.sort(key=lambda x:x[1], reverse=True)
        return items,counts
        
        
#绘制词云
def draw_cloud(dic,file):
    graph = np.zeros((400,600,3),dtype=np.int)
    # 参数分别是指定字体、背景颜色、最大的词的大小、使用给定图作为背景形状
    wc = WordCloud(font_path='simkai.ttf', background_color='black', max_words=200, mask=graph)
    wc.generate_from_frequencies(dic)  # 根据给定词频生成词云
    wc.to_file(file+'.png')  # 图片命名
    
    
if __name__ == '__main__':
    for file in ['summary', 'summaryYear']:#两个文件分别统计
        writeDown(file)
        items,counts = countDown(file)
        #绘制词云
        draw_cloud(counts,file)
        #保存到新的csv文件
        with open(file+'_count.csv','w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f, delimiter = ',', quotechar='"')
            writer.writerows(items)
        
            