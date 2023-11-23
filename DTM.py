import os
import re
import pandas as pd

from gensim import corpora
from collections import  defaultdict
from gensim.test.utils import common_corpus
from gensim.models import LdaSeqModel
from gensim.matutils import hellinger
import matplotlib.pyplot as plt
import jieba

os.chdir("/Users/zhou/Desktop/SDA/final") 

# create stop words list
stopWordsFilePath = r'/Users/zhou/Desktop/SDA/final/哈工大停用词.txt'
with open(stopWordsFilePath, 'r', encoding='utf-8') as file:   
    stopWords = file.readlines()
    stopWords = [I.strip() for I in stopWords]

def BasicCleanText(raw_text):
    cleantextprep = str(raw_text)
    
    # Tokenization
    tokens = jieba.cut(cleantextprep)
    tokens_list = list(tokens)

    # stop words and space
    texts_clean = [i.strip() for i in tokens_list if not i in stopWords]
    chinesePunctuationPattern = re.compile("[\\.\\%\u2002\u3000\u3001\u3002\u3008-\u3011\u2014\uff01-\uff5e\u300e\u300f\u2018\u2019\u201c\u201d\u20260-9a-z]")
    texts_clean = [chinesePunctuationPattern.sub("", i) for i in texts_clean]

    texts_clean = [i.strip() for i in texts_clean if i != '']

    return texts_clean


# load text
data = []
root_dir = '/Users/zhou/Desktop/SDA/final/Result'
for subdir in os.listdir(root_dir):

    if os.path.isdir(os.path.join(root_dir, subdir)):
        subdir_path = os.path.join(root_dir, subdir)

        for file in os.listdir(subdir_path):

            if file.endswith('.txt'):
                file_path = os.path.join(subdir_path, file)               
                year = file[-8:-4] 
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                cleaned_content = BasicCleanText(content)
                data.append({'Region': subdir, 'Year': year, 'Content': cleaned_content})

# create DataFrame
df = pd.DataFrame(data)

# time stamp and time slice
time_stamps = sorted(df['Year'].astype(int).unique())
time_stamps = list(time_stamps)

gp = df.groupby(by=['Year'])
total_yearly_list = list(gp.size())

# create dictionary
documents=list(df['Content'])
texts = [[word for word in document] for document in documents]

highfreq = ["发展","建设","推进","加快","加强","实施","年","新"]

# drop low frequency words
frequency = defaultdict(int)
for text in texts:
    for token in text:
        if token not in highfreq:
            frequency[token] += 1
texts = [[token for token in text if frequency[token] > 10] for text in texts]

# small sample
dict = ['产业', '创新', '农业', '推动', '提升', '全面', '工作', '坚持', '精神', '社会主义', '工程', '城市', '生态', '农村', '项目', '重点', '经济', '企业', '改革', '投资', '市场', '积极',
    '增长', '亿元', '就业', '达到', '年', '基本', '文化', '工作', '社会', '政府', '改革', '完善', '政府', '人民', '问题', '群众', '经济', '代表']
texts_sample = [[token for token in text if token in dict] for text in texts]

# big sample
top_tokens = sorted(frequency, key=frequency.get, reverse=True)[:200]
texts_bigsample = [[token for token in document if token in top_tokens] for document in documents]

# generate the dictionary
dictionary = corpora.Dictionary(texts)   
dictionary.compactify() 

# save dictionary and vocabulary
dictionary.save(os.path.join('dictionary.dict')) 

vocFile = open(os.path.join( 'vocabulary.dat'),'w')
for word in dictionary.values():
    vocFile.write(word+'\n')  
vocFile.close()

#Prevent storing the words of each document in the RAM
class MyCorpus(object):
     def __iter__(self):
         for document in documents:
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(document)

corpus_memory_friendly = MyCorpus()

multFile = open(os.path.join( 'foo-mult.dat'),'w')

for vector in corpus_memory_friendly: # load one vector into memory at a time
    multFile.write(str(len(vector)) + ' ')
    for (wordID, weigth) in vector:
        multFile.write(str(wordID) + ':' + str(weigth) + ' ')

    multFile.write('\n')
    
multFile.close()

#use LdaSeqModel to generate DTM results
ldaseq = LdaSeqModel(corpus=corpus_memory_friendly, id2word=dictionary, time_slice=total_yearly_list,
                      num_topics=5, passes=20)

# for given topic the word distribution over time
DTM_topic_0=ldaseq.print_topic_times(topic=0, top_terms=10)
DTM_topic_1=ldaseq.print_topic_times(topic=1, top_terms=10)
DTM_topic_2=ldaseq.print_topic_times(topic=2, top_terms=10)
DTM_topic_3=ldaseq.print_topic_times(topic=3, top_terms=10)
DTM_topic_4=ldaseq.print_topic_times(topic=4, top_terms=10)


def topic_time(DTM_topic,time_stamps):  
    for i in range(len(total_yearly_list)-1):
        if i==0:
            temp_a1=pd.DataFrame(DTM_topic[i])
            temp_a2=pd.DataFrame(DTM_topic[i+1])
            temp_a1.columns = ['words', time_stamps[i]]
            temp_a2.columns = ['words', time_stamps[i+1]]
            temp_a1=pd.merge(temp_a1,temp_a2)
        else:
            temp_a2=pd.DataFrame(DTM_topic[i+1])
            temp_a2.columns = ['words', time_stamps[i+1]]
            temp_a1=pd.merge(temp_a1,temp_a2)
    topic_words_time=temp_a1
    return topic_words_time
   
topic1_words_time=topic_time(DTM_topic_0,time_stamps)
topic2_words_time=topic_time(DTM_topic_1,time_stamps)
topic3_words_time=topic_time(DTM_topic_2,time_stamps)
topic4_words_time=topic_time(DTM_topic_3,time_stamps)
topic5_words_time=topic_time(DTM_topic_4,time_stamps)

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]

#plot the dynamic movement of topic 1
topic1_words=list(topic1_words_time['words'])
plt.figure()
for i in range(0,min(5,len(topic1_words))):
    plt.plot(time_stamps, topic1_words_time.iloc[i,1:],marker=".",label=str(topic1_words[i]))
#plt.xlim((-1, 2))
#plt.ylim((0, 0.02))
plt.legend(loc='best')
plt.title('Topic 1')
plt.savefig('Topic1.png',transparent=True)
plt.show()


#plot the dynamic movement of topic2
topic=topic2_words_time
topic_words=list(topic['words'])
plt.figure()
for i in range(0,min(5,len(topic_words))):
    plt.plot(time_stamps, topic.iloc[i,1:],marker=".",label=topic_words[i])
#plt.xlim((-1, 2))
#plt.ylim((0, 0.02))
plt.legend(loc='best')
plt.title('Topic 2')
plt.savefig('Topic2.png',transparent=True)
plt.show()


#plot the dynamic movement of topic3
topic=topic3_words_time
topic_words=list(topic['words'])
plt.figure()
for i in range(0,min(5,len(topic_words))):
    plt.plot(time_stamps, topic.iloc[i,1:],marker=".",label=topic_words[i])
#plt.xlim((-1, 2))
#plt.ylim((0, 0.02))
plt.legend(loc='best')
plt.title('Topic 3')
plt.savefig('Topic3.png',transparent=True)
plt.show()


#plot the dynamic movement of topic4
topic=topic4_words_time
topic_words=list(topic['words'])
plt.figure()
for i in range(0,min(5,len(topic_words))):
    plt.plot(time_stamps, topic.iloc[i,1:],marker=".",label=topic_words[i])
#plt.xlim((-1, 2))
#plt.ylim((0, 0.02))
plt.legend(loc='best')
plt.title('Topic 4')
plt.savefig('Topic4.png',transparent=True)
plt.show()


#plot the dynamic movement of topic5
topic=topic5_words_time
topic_words=list(topic['words'])
plt.figure()
for i in range(0,min(5,len(topic_words))):
    plt.plot(time_stamps, topic.iloc[i,1:],marker=".",label=topic_words[i])
#plt.xlim((-1, 2))
#plt.ylim((0, 0.02))
plt.legend(loc='best')
plt.title('Topic 5')
plt.savefig('Topic5.png',transparent=True)
plt.show()
