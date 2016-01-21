
# coding: utf-8

# In[ ]:

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from pdfminer.converter import PDFPageAggregator
import nltk
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import numpy as np
import lxml
import re
import pprint
import os
import copy
from nltk.stem.wordnet import WordNetLemmatizer
import csv
import unicodedata
import os
from os import listdir
from os.path import isfile, join


# In[ ]:

class IndexedText(object):

    def __init__(self, stemmer,lemmatizer, text):
        self._text = text
        self._stemmer = stemmer
        self._lemmatizer = lemmatizer
        self._index = nltk.Index((self._stem(word), i) for (i, word) in enumerate(text))
        #self._verbs = filter(lambda x: 'vb' in x[1].lower(), nltk.pos_tag(text))
        #self._stemVerbs = map(lambda x: self._stem(x[0]), self._verbs)

    def concordance(self, word):
        words = word.split(' ')
        keys = map(self._stem, words)              # words of context
        finded = []
        #if key in self._stemVerbs:
        allFound = True
        senInRow = False
        pos = 0
#        for key in keys:
#            if not self._index[key]:                
#                allFound = False
#            else:
#                pos = self._index[key]
        foundInd = []
        for key in keys:
            if not self._index[key]:                
                allFound = False
            else:
                foundInd.append(self._index[key])
                pos = self._index[key]
        if allFound and len(foundInd)>1:
            senInRow = False
            for i in foundInd[0]:
                found = True
                for j in range(len(foundInd)-1):
                    if not((i+1+j) in foundInd[j+1]):
                        found=False
                if found:
                    pos = [i+1+j]
                    senInRow = True
        else:
            senInRow = True
                
                    
            
#            found =[]
#            if not foundInd:
#                foundInd = self._index[key]
#            else:
#                nextInd = self._index[key]
#                for i in nextInd:
#                    if (i-1) in foundInd:
#                        found.append(i)
#                foundInd = found
        if allFound and senInRow:
            context = ' '.join(self._text)
            finded.append(context)
        return [finded, pos]

    def _stem(self, word):
        return self._lemmatizer.lemmatize(self._stemmer.stem(word).lower(), pos='v') 

def Searcher(texts,verbs):
    lemmatizer = WordNetLemmatizer()
    porter = nltk.PorterStemmer()
    searchRes = []
    for senNo,text in enumerate(texts):
        tokTest = nltk.word_tokenize(text)
        indexText = IndexedText(porter,lemmatizer, tokTest)
        for verb in verbs:
            con = indexText.concordance(verb)
            if con[0]:                
                for i in con[0]:
                    #found = False
                    #for j in range(len(searchRes)):
                    #    if i in searchRes[j][0]:
                    #        searchRes[j][1].append(verb)
                    #        found = True
                    #if not found:
                    #    searchRes.append([i,[verb]])
                    searchRes.append([senNo+1,i,verb,min(con[1]),max(con[1])])
    return searchRes               

def sentenceSplitter(texto):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentenses = sent_detector.tokenize(texto.strip())
    return sentenses

def normTextSplitTab(text):
    a = unicodedata.normalize('NFKD', unicode(text,'UTF-8'))
    a = a.encode('ascii','ignore')

    def regF(s):
        ss = s.group(0)
        return ss[0]+' '+ss[-1]
    a = re.sub('[a-z]\s*\n\n\s*\d\s*\n\n\s*[a-z]',regF,a)

    def regF(s):
        ss = s.group(0)
        return ss[0]+' . '+ss[-1]
    a = re.sub('[a-z]\s*\n\n\s*\d\s*\n\n\s*[A-Z]',regF,a)

    a = re.sub('\n\n','@SPLIT@',a)

    def regF(s):
        ss = s.group(0)
        return ss[0]+' '+ss[-1]
    a = re.sub('[a-z]\s*\n+\s*[a-z]',regF,a)

    def regF(s):
        ss = s.group(0)
        return ss[0]+' . '+ss[-1]
    a = re.sub('[a-z]\s*\n\n\s*[A-Z]',regF,a)

    def regF(s):
        ss = s.group(0)
        return ss[0]+' . '+ss[-1]
    a = re.sub('\d\s*\n+\s*[A-Z]',regF,a)

    def regF(s):
        ss = s.group(0)
        return ss[0]+' . '+ss[-1]
    a = re.sub('\)\s*\n*\s*[A-Z]',regF,a)

    def regF(s):
        ss = s.group(0)
        return ss[0]+ss[-1]
    a = re.sub('[a-z]-\s*\n*\s*[a-z]',regF,a)

    def regF(s):
        ss = s.group(0)
        return ' '+ss[-1]
    a = re.sub('@SPLIT@\s*\n*\s*[a-z]',regF,a)

    #a = re.sub('\n\n','{SPLIT}',a)
    a = re.sub('\n',' ',a)
    a = re.sub('\.',' . ',a)
    a = re.sub('\!',' ! ',a)
    a = re.sub('\?',' ? ',a)
    def regF(s):
        ss = s.group(0)
        return ss[0]+'.'+ss[-1]
    a = re.sub('\d\s*\.\s*\d',regF,a)
    #a = ' '.join(a.splitlines()).replace('.',' . ')
    a = a.replace("\x0c", "")
    a = re.sub(r'[^\w.@?!-]', ' ', a)

    a = re.sub(' +',' ',a)
    a = re.sub('(\. )+','. ',a)

    #def regF(s):
    #    return s.group(0).replace(' ','')
    #a = re.sub('\d\s*\.\s*\d',regF,a)
    a = re.sub('(@SPLIT@)+','@SPLIT@',a)
    tabSplit = a.split('@SPLIT@')
    return tabSplit  #Разделение по абзацам

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    prev=""
    text=[]
    for i, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages,password=password,caching=caching, check_extractable=True)):
        retstr.write("@SPLIT@")
        if page is not None:
            interpreter.process_page(page)
        #retstr.write("{END PAGE %d}" % i)
        #now = retstr.getvalue()
        #text.append(now.replace(prev,''))
        #prev = now
    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    fText = normTextSplitTab(text)
    
    return fText
def splitSen(text):
    sentenceSplit = []
    for tSpl in text:    
        sentenceSplit += sentenceSplitter(tSpl)
    return sentenceSplit #Разделение по предложениям

def unique(s):
    

    n = len(s)
    if n == 0:
        return []

   
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

   
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u



# In[ ]:

if __name__ == '__main__':


    onlyfiles = [f for f in listdir('./links/') if isfile(join('./links/', f))]

    #onlyfiles = onlyfiles[44:]


    mergeData_general1 = pd.DataFrame()
    general = []

    for f in onlyfiles:
        print f    
        currentPDF = convert_pdf_to_txt("links/" + f)
        currentPDF = splitSen(currentPDF)

        keywords = pd.read_csv('keywords.csv', sep=';', encoding = 'cp1252')
        tabRes = []
        for i in range(17):
            print i
            s = Searcher(currentPDF,keywords.ix[:,i].dropna())
            if len(s) > 0:
                tabRes.append(pd.DataFrame(data=np.array(s), columns=['pNo','text','word','minPos','maxPos']))
            else:
                tabRes.append(pd.DataFrame(columns=['pNo','text','word','minPos','maxPos']))


        mergeData = []
        for i in [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16]:
            mergeData.append(tabRes[10].merge(tabRes[i],'inner',on='pNo').drop('text_y',axis=1).rename(columns={'text_x':'text', 'word_x':'SDG11Word', 'word_y':'SDG'+str(i+1)+'Word'}))

        checkwords = pd.read_csv('checkwords.csv')
        for i in range(16):
            barrier = Searcher(mergeData[i]['text'],checkwords.ix[:,0].dropna())
            recomend =  Searcher(mergeData[i]['text'],checkwords.ix[:,1].dropna())
            mergeData[i]['common'] = 0
            mergeData[i]['constraint'] = 0
            mergeData[i]['recommendation'] = 0
            mergeData[i]['direction'] = ''
            for j in barrier:
                mergeData[i].loc[j[0]-1,'constraint'] = 1
            for j in recomend:
                mergeData[i].loc[j[0]-1,'recommendation'] = 1
            for j in range(len(mergeData[i])):
                if mergeData[i]['minPos_x'][j]>mergeData[i]['minPos_y'][j]:
                    mergeData[i].loc[j,'direction'] = 1
                else:
                    mergeData[i].loc[j,'direction'] = 2
                if mergeData[i]['constraint'][j]==0 and mergeData[i]['recommendation'][j]==0:
                    mergeData[i].loc[j,'common'] = 1
            mergeData[i] = mergeData[i].drop(['minPos_x','maxPos_x','minPos_y','maxPos_y'],axis=1)


        count = []
        count3 = []
        count4 = []
        count1 = []
        count2 = []
        type_3 = []
        type_4 = []
        type_1 = []
        type_2 = []
        for i in range(16):
                if i>=10:
                    j=i+2
                else:
                    j=i+1
                count.append([mergeData[i].columns[7], len(unique(mergeData[i].pNo.values))])
                type_1.append(mergeData[i][(mergeData[i]['common'] == 1)&(mergeData[i]['direction'] == 1)])
                type_2.append(mergeData[i][(mergeData[i]['common'] == 1)&(mergeData[i]['direction'] == 2)])
                type_3.append(mergeData[i][mergeData[i]['constraint'] == 1])
                type_4.append(mergeData[i][mergeData[i]['recommendation'] == 1])


        for i in range(16):   
                count1.append([type_1[i].columns[7], len(unique(type_1[i].pNo.values))])
                count2.append([type_2[i].columns[7], len(unique(type_2[i].pNo.values))])
                count3.append([type_3[i].columns[7], len(unique(type_3[i].pNo.values))])
                count4.append([type_4[i].columns[7], len(unique(type_4[i].pNo.values))])

        mergeData_general = mergeData[0]
        for i in xrange(1, len(mergeData)):
            mergeData_general = mergeData_general.append(mergeData[i])
        mergeData_general = mergeData_general.fillna('-0')

        mergeData_general1 = mergeData_general1.append(mergeData_general)

        general.append([f, count, count1, count2, count3, count4])

