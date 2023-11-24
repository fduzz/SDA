# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 20:19:12 2023

@author: Lenovo
"""
# -*- coding: utf-8 -*-
"""

Get some chips

"""

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd
from collections import Counter
import os
import re
from tqdm import tqdm
import codecs
from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary

# 中文字体
plt.rcParams['font.sans-serif']=['KaiTi']
plt.rcParams['axes.unicode_minus'] = False


# 设置最上层文件夹
provinceFolder = r'Result'

# 获取省份文件夹
txtFolder = os.listdir(provinceFolder)

# 保存txt文件名
txtFilePaths = []

# 迭代文件名获取文件名
for folder in txtFolder:
    txtFolderPath = os.path.join(provinceFolder, folder)
    txtFileNames = os.listdir(txtFolderPath)
    for fileName in txtFileNames:
        txtFilePath = os.path.join(txtFolderPath, fileName)
        txtFilePaths.append(txtFilePath)

# 读入停用词
stopWordsFilePath = r'哈工大停用词.txt'
with open(stopWordsFilePath, 'r', encoding='utf-8') as file:
    stopWords = file.readlines()
    stopWords = [I.strip() for I in stopWords] 

# 去除最高频模糊政策词的干扰
feihuaList=["发展","建设","推进","加快","加强","实施"]

def removing(s):
    # 正式去除两类词语
    train=[]
    for i in s:
        if i not in stopWords and i not in feihuaList:
            train.append(i)
    return train
    
        
# 分行获取文本
wordList = []
allStr=""

# 读取txt文本
for txtFilePath in txtFilePaths:
    # 打开本文文件并逐行提取
    with open(txtFilePath, 'r', encoding='utf-8') as file:
        content = file.readlines()
        # 剔除换行符
        content = [I.strip() for I in content]
        for singleContent in content:
            if singleContent:
                allStr += singleContent
                chinesePunctuationPattern = re.compile("[\u3000\u3001\u3002\u3008-\u3011\u2014\uff01-\uff5e\u300e\u300f\u2018\u2019\u201c\u201d\u2026]")
                allStr = chinesePunctuationPattern.sub("", allStr)
                word = jieba.lcut(allStr)
                word = removing(word)
                wordList.append(word)
                allStr =""
            # 空字符不做操作
            else:
                pass

        
dictionary = corpora.Dictionary(wordList)
corpus = [ dictionary.doc2bow(text) for text in wordList]
lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=7,passes=20, random_state=100)

print(lda.print_topics(num_topics=7, num_words=6))

K=7
topicWordProbMat=lda.print_topics(K)
columns = (['Topics '+str(x) for x in range(1,7+1)])
df = pd.DataFrame(columns = columns)
df = pd.DataFrame(columns = columns)
pd.set_option('display.width', 1000)
# 20 need to modify to match the length of vocabulary 
zz = np.zeros(shape=(100,K))
last_number=0
DC={}
data = pd.DataFrame({columns[0]:""}, index=[0])
for x in range(100):
  for i in range(1,len(columns)):
    data[columns[i]] = ""
  df = df.append(data, ignore_index=True)
for line in topicWordProbMat: 
    tp, w = line
    probs=w.split("+")
    y=0
    for pr in probs:  
        a=pr.split("*")
        df.iloc[y,tp] = a[1]
        a[1] = a[1].strip()
        if a[1] in DC:
           zz[DC[a[1]]][tp]=a[0]
        else:
           zz[last_number][tp]=a[0]
           DC[a[1]]=last_number
           last_number=last_number+1
        y=y+1
print (df)
print (zz)
zz=np.resize(zz,(len(DC.keys()),zz.shape[1]))
plt.figure(figsize=(80,25))
for val, key in enumerate(DC.keys()):
        plt.text(-2.5, val + 0.5, key,
                 horizontalalignment='center',
                 verticalalignment='center'
                 )
#plt.imshow(zz, cmap='hot', interpolation='nearest')
plt.imshow(zz, cmap='rainbow', interpolation='nearest')
#plt.show()
plt.yticks([])
# plt.title("heatmap xmas song")
plt.savefig("heatmap_abstract.png", transparent = True, dpi=400)


     
