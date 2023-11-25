# -*- coding: utf-8 -*-
"""

Get some chips

"""

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from collections import Counter
import os
import re
from tqdm import tqdm

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
        
        
# 拼接所有文本
allStr = ''

# 读取txt文本
for txtFilePath in txtFilePaths:
    # 打开本文文件
    with open(txtFilePath, 'r', encoding='utf-8') as file:
        content = file.readlines()
        # 剔除换行符
        content = [I.strip() for I in content]
        for singleContent in content:

            if singleContent:
                allStr += singleContent
            # 空字符不做操作
            else:
                pass
            
# 正则表达式去除标点符号
chinesePunctuationPattern = re.compile("[\u3000\u3001\u3002\u3008-\u3011\u2014\uff01-\uff5e\u300e\u300f\u2018\u2019\u201c\u201d\u2026]")
allStr = chinesePunctuationPattern.sub("", allStr)

# 使用jieba分词处理文本
segList = jieba.cut(allStr)
wordFreq = Counter(segList)

# 读入停用词
stopWordsFilePath = r'哈工大停用词.txt'
with open(stopWordsFilePath, 'r', encoding='utf-8') as file:
    
    stopWords = file.readlines()
    stopWords = [I.strip() for I in stopWords]
    for stopWord in tqdm(stopWords):
        if stopWord in wordFreq:
            del wordFreq[stopWord]

    
del wordFreq['中']
del wordFreq['方面']
del wordFreq['区']
del wordFreq['万人']
del wordFreq['上']

mask = np.array(Image.open(r'maskImage.jpg'))

wordcloud = WordCloud(width=800,
                      height=500,
                      font_path="STKAITI.TTF",
                      background_color='white',
                      max_font_size=80,
                      min_font_size=10,
                      mask=mask,
                      )

wordcloud.generate_from_frequencies(wordFreq)

# 显示词云图像
plt.figure(figsize=(10, 10), dpi=200)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")  # 隐藏坐标轴
plt.show()



        