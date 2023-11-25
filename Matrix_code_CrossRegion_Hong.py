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



#显示中文
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', size=25)

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
eastFilePaths, eastNorthFilePaths, centerFilePaths, westFilePaths = [], [], [], []
for filePath in txtFilePaths:
    if '江苏' in filePath or '浙江' in filePath or '上海' in filePath:
        eastFilePaths.append(filePath)
    elif '黑龙江' in filePath or '辽宁' in filePath or '沈阳' in filePath:
        eastNorthFilePaths.append(filePath)
    elif '安徽' in filePath or '湖南' in filePath or '山西' in filePath:
        centerFilePaths.append(filePath)
    elif '广西' in filePath or '内蒙' in filePath or '重庆' in filePath:
        westFilePaths.append(filePath)

eastWrodFrq = processSubFiles(eastFilePaths)
eastNorthWrodFrq = processSubFiles(eastNorthFilePaths)
centerWrodFrq = processSubFiles(centerFilePaths)
westWrodFrq = processSubFiles(westFilePaths)
#%%
commonKeys = set(eastWrodFrq.keys()) & set(eastNorthWrodFrq.keys()) & set(centerWrodFrq.keys()) & set(westWrodFrq.keys())

for key in commonKeys:
    if not key in eastWrodFrq:
        del eastWrodFrq[key]
    if not key in eastNorthWrodFrq:
        del eastNorthWrodFrq[key]
    if not key in centerWrodFrq:
        del centerWrodFrq[key]
    if not key  in westWrodFrq:
        del westWrodFrq[key]

allWord = {}

for key in commonKeys:
    allWord[key] = eastWrodFrq[key] + eastNorthWrodFrq[key] + centerWrodFrq[key] + westWrodFrq[key]

#%%

words = [['"工程"', '"完成"', '"重点"', '"项目"', '"改造"', '"农村"', '"公里"', '"建成"', '"万亩"', '"整治"'], ['"产业"', '"项目"', '"合作"', '"推动"', '"新"', '"企业"', '"投资"', '"国际"', '"国家"', '"经济"'], ['"农业"', '"改革"', '"农村"', '"试点"', '"农民"', '"综合"', '"深化"', '"农产品"', '"粮食"', '"促进"'], ['"就业"', '"教育"', '"基本"', '"提高"', '"农村"', '"工作"', '"社会"', '"城乡"', '"保障"', '"生活"'], ['"政府"', '"工作"', '"社会"', '"管理"', '"行政"', '"制度"', '"改革"', '"完善"', '"安全"', '"监督"'], ['"生态"', '"城市"', '"重庆"', '"创新"', '"提升"', '"经济"', '"推动"', '"绿色"', '"体系"', '"区域"'], ['"增长"', '"亿元"', '"年"', '"达到"', '"经济"', '"以上"', '"生产总值"', '"收入"', '"全省"', '"取得"'], ['"新"', '"经济"', '"工作"', '"全面"', '"坚持"', '"人民"', '"精神"', '"习近平"', '"代表"', '"五年"'], ['"文化"', '"创新"', '"科技"', '"产业"', '"旅游"', '"企业"', '"服务业"', '"培育"', '"一批"', '"现代"'], ['"企业"', '"经济"', '"消费"', '"市场"', '"支持"', '"政策"', '"改革"', '"投资"', '"促进"', '"融资"']]
words = [word.replace('"', '').replace('"', '') for sublist in words for word in sublist]

for word in words:
    if not word in eastWrodFrq:
        eastWrodFrq[word] = 0
    if not word in eastNorthWrodFrq:
        eastNorthWrodFrq[word] = 0
    if not word in centerWrodFrq:
        centerWrodFrq[word] = 0
    if not word  in westWrodFrq:
        westWrodFrq[word] = 0
#%%
for I in range(0, len(words), 10):
    values = words[I:I + 10]
    eastList, eastNorthList, centerList, westList = [], [], [], []
    for value in values:
        eastList.append(eastWrodFrq[value])
        eastNorthList.append(eastNorthWrodFrq[value])
        centerList.append(centerWrodFrq[value])
        westList.append(westWrodFrq[value])
    
    wordMatrix = np.array([eastList, eastNorthList, centerList, westList])
    plt.figure(figsize=(18, 14), dpi=100)
    plt.imshow(wordMatrix, cmap='gray_r', interpolation='nearest')
    plt.colorbar(shrink=0.43)
    plt.xticks(range(10), values)
    plt.yticks(range(4), ['东部', '东北', '中部', '西部'])
    plt.savefig(r'地区热力图\{}-{}'.format(I, I+10))
    plt.show()
    
    




