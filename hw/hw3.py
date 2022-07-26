import requests
import re
from operator import itemgetter
from bs4 import BeautifulSoup

import csv
import nltk
import numpy
from nltk.tokenize import sent_tokenize,word_tokenize


def parse(input_path,index1,index2):
    attributes=['sound','headphone','quality',
                'noise','bass','music','battery']

    def getGa(s):
        ga=set()
        f=open(s)
        for v in f:
            ga.add(v.strip())
        return ga

    ga=getGa( 'positive-words.txt')
    ba=getGa(  'negative-words.txt')

    f=open(input_path)
    reader=csv.reader(f)
    l=list(reader)
    p1=l[index1][0]
    p2=l[index2][0]

    def getM1(p1):

        m1={}

        sentences=sent_tokenize(p1)
        for sentence in sentences:
            nouns=set()
            count=0

            words=word_tokenize(sentence)
            tWords=nltk.pos_tag(words)
            for t in tWords:
                if t[1].startswith('NN'):
                    noun=t[0].lower()
                    nouns.add(noun)

                    if noun not in m1:
                        m1[noun]=[0,0]

            for t in tWords:
                if t[1]. startswith('JJ'):
                    if t [0] in ga:
                        count+=1
                    elif t[0] in ba:
                        count-=1
            if count>0:
                for noun in nouns: m1[noun][0]+=1
            elif count< 0 :
                for noun in nouns:m1[noun][1]+=1

        return m1

    m1=getM1(p1)
    m2=getM1(p2)

    r1=[]
    r2=[]
    for v in attributes:
        if v in m1:
            r1.append([v,m1[v],m1[v][1]-m1[v][0]])
        else:
            r1.append([v,[0,0],0])
        if v  in m2:
            r2.append([v,m2[v],m2[v][1]-m2[v][0]])
        else:
            r2.append([v,[0,0],0])

    r=[]
    for i in range(0,len(r1)):
        if r1[i][2] *r2[i] [2]<0:
            r.append(r1[i][0])


    # print(r1)
    # print(r2)
    return r

r=parse('amazonreviews.csv',9,12)
print(r)