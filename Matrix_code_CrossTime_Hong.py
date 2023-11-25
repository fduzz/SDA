# -*- coding: utf-8 -*-
"""

Get some chips

"""

import jieba
import matplotlib.pyplot as plt
from collections import Counter
import os
import re
from tqdm import tqdm
import numpy as np
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
        

def processSubFiles(subTxtFilePaths):
    # 拼接所有文本
    allStr = ''
    
    # 读取txt文本
    for txtFilePath in subTxtFilePaths:
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
                
    return dict(wordFreq)
#%%
before10Paths, after13FilePaths = [], []
for filePath in txtFilePaths:
    if '2000' in filePath or '2001' in filePath or '2003' in filePath or '2004' in filePath or '2005' in filePath \
        or '2006' in filePath or '2007' in filePath or '2008' in filePath or '2009' in filePath or '2010' in filePath:
        before10Paths.append(filePath)
    elif '2011' in filePath or '2012' in filePath or '2013' in filePath or '2014' in filePath or '2015' in filePath \
        or '2016' in filePath or '2017' in filePath or '2018' in filePath or '2019' in filePath or '2020' in filePath \
        or '2021' in filePath or '2022' in filePath or '2023' in filePath :
        after13FilePaths.append(filePath)

before10WrodFrq = processSubFiles(before10Paths)
after13WrodFrq = processSubFiles(after13FilePaths)

#%%
commonKeys = set(before10WrodFrq.keys()) & set(after13WrodFrq.keys())

for key in commonKeys:
    if not key in before10WrodFrq:
        del before10WrodFrq[key]
    if not key in after13WrodFrq:
        del after13WrodFrq[key]


allWord = {}

for key in commonKeys:
    allWord[key] = before10WrodFrq[key] + after13WrodFrq[key]
#%%

words = [['"工程"', '"完成"', '"重点"', '"项目"', '"改造"', '"农村"', '"公里"', '"建成"', '"万亩"', '"整治"'], ['"产业"', '"项目"', '"合作"', '"推动"', '"新"', '"企业"', '"投资"', '"国际"', '"国家"', '"经济"'], ['"农业"', '"改革"', '"农村"', '"试点"', '"农民"', '"综合"', '"深化"', '"农产品"', '"粮食"', '"促进"'], ['"就业"', '"教育"', '"基本"', '"提高"', '"农村"', '"工作"', '"社会"', '"城乡"', '"保障"', '"生活"'], ['"政府"', '"工作"', '"社会"', '"管理"', '"行政"', '"制度"', '"改革"', '"完善"', '"安全"', '"监督"'], ['"生态"', '"城市"', '"重庆"', '"创新"', '"提升"', '"经济"', '"推动"', '"绿色"', '"体系"', '"区域"'], ['"增长"', '"亿元"', '"年"', '"达到"', '"经济"', '"以上"', '"生产总值"', '"收入"', '"全省"', '"取得"'], ['"新"', '"经济"', '"工作"', '"全面"', '"坚持"', '"人民"', '"精神"', '"习近平"', '"代表"', '"五年"'], ['"文化"', '"创新"', '"科技"', '"产业"', '"旅游"', '"企业"', '"服务业"', '"培育"', '"一批"', '"现代"'], ['"企业"', '"经济"', '"消费"', '"市场"', '"支持"', '"政策"', '"改革"', '"投资"', '"促进"', '"融资"']]
words = [word.replace('"', '').replace('"', '') for sublist in words for word in sublist]

for word in words:
    if not word in before10WrodFrq:
        before10WrodFrq[word] = 0
    if not word in after13WrodFrq:
        after13WrodFrq[word] = 0

#%%
for I in range(0, len(words), 10):
    values = words[I:I + 10]
    before10List, after13List = [], []
    for value in values:
        before10List.append(before10WrodFrq[value])
        after13List.append(after13WrodFrq[value])

    
    wordMatrix = np.array([before10List, after13List])
    plt.figure(figsize=(18, 14), dpi=100)
    plt.imshow(wordMatrix, cmap='gray_r', interpolation='nearest')
    plt.colorbar(shrink=0.2)
    plt.xticks(range(10), values)
    plt.yticks(range(2), ['2010年及之前', '2013年及之后'])
    plt.savefig(r'时间热力图\{}-{}'.format(I, I+10))
    plt.show()
    
    




        