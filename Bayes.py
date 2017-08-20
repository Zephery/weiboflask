'''
多类的朴素贝叶斯实现
'''
import os
import re

import jieba
import numpy as np

base_dir = os.path.dirname(__file__)
stop = [line.strip() for line in open(os.path.join(base_dir,'stop.txt'), 'r', encoding='utf-8').readlines()]  # 停用词


def build_word_array(line):
    line_cut = []
    temp = line.strip()
    try:
        sentence = temp.lstrip()  # 每条微博
        word_list = []
        sentence = str(sentence).replace('\u200b', '')
        for word in jieba.cut(sentence.strip()):
            p = re.compile(b'\w', re.L)
            result = p.sub(b"", bytes(word, encoding="utf-8")).decode("utf-8")
            if not result or result == ' ':  # 空字符
                continue
            word_list.append(word)
        word_list = list(set(word_list) - set(stop) - set('\u200b')
                         - set(' ') - set('\u3000') - set('️'))
        line_cut.append(word_list)
    except Exception:
        return None
    return line_cut


def build_key_word(path):  # 通过词频产生特征
    d = {}
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            for word in jieba.cut(line.strip()):
                p = re.compile(b'\w', re.L)
                result = p.sub(b"", bytes(word, encoding="utf-8")).decode("utf-8")
                if not result or result == ' ':  # 空字符
                    continue
                if len(word) > 1:  # 避免大量无意义的词语进入统计范围
                    d[word] = d.get(word, 0) + 1
    kw_list = sorted(d, key=lambda x: d[x], reverse=True)
    size = int(len(kw_list) * 0.2)  # 取最前的30%
    mood = set(kw_list[:size])
    return list(mood - set(stop))


def loadDataSet(path):  # 返回每条微博的分词与标签
    line_cut = []
    label = []
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            temp = line.strip()
            try:
                sentence = temp[2:].lstrip()  # 每条微博
                label.append(int(temp[:2]))  # 获取标注
                word_list = []
                sentence = str(sentence).replace('\u200b', '')
                for word in jieba.cut(sentence.strip()):
                    p = re.compile(b'\w', re.L)
                    result = p.sub(b"", bytes(word, encoding="utf-8")).decode("utf-8")
                    if not result or result == ' ':  # 空字符
                        continue
                    word_list.append(word)
                word_list = list(set(word_list) - set(stop) - set('\u200b')
                                 - set(' ') - set('\u3000') - set('️'))
                line_cut.append(word_list)
            except Exception:
                continue
    return line_cut, label  # 返回每条微博的分词和标注


def setOfWordsToVecTor(vocabularyList, moodWords):  # 每条微博向量化
    vocabMarked = [0] * len(vocabularyList)
    for smsWord in moodWords:
        if smsWord in vocabularyList:
            vocabMarked[vocabularyList.index(smsWord)] += 1
    return np.array(vocabMarked)


def setOfWordsListToVecTor(vocabularyList, train_mood_array):  # 将所有微博准备向量化
    vocabMarkedList = []
    for i in range(len(train_mood_array)):
        vocabMarked = setOfWordsToVecTor(vocabularyList, train_mood_array[i])
        vocabMarkedList.append(vocabMarked)
    return vocabMarkedList