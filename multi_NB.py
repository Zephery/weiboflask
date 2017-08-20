'''
使用机器学习库sklearn处理多分类问题
'''

import random
import os
import json
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import zero_one_loss
from sklearn.naive_bayes import MultinomialNB

import Bayes as bayes

base_dir = os.path.dirname(__file__)

n_estimators = 500
learning_rate = 1.
vocabList = bayes.build_key_word(os.path.join(base_dir, "train.txt"))
line_cut, label = bayes.loadDataSet(os.path.join(base_dir, "train.txt"))
train_mood_array = bayes.setOfWordsListToVecTor(vocabList, line_cut)
test_word_array = []
test_word_arrayLabel = []
testCount = 100  # 从中随机选取100条用来测试，并删除原来的位置
for i in range(testCount):
    try:
        randomIndex = int(random.uniform(0, len(train_mood_array)))
        test_word_arrayLabel.append(label[randomIndex])
        test_word_array.append(train_mood_array[randomIndex])
        del (train_mood_array[randomIndex])
        del (label[randomIndex])
    except Exception as e:
        print(e)
multi = MultinomialNB()
ada_real = AdaBoostClassifier(
    base_estimator=multi,
    learning_rate=learning_rate,
    n_estimators=n_estimators,
    algorithm="SAMME.R")
ada_real.fit(train_mood_array, label)
ada_real_err = np.zeros((n_estimators,))  # 变成一个一维的矩阵，长度为n
for i, y_pred in enumerate(ada_real.staged_predict(test_word_array)):  # 测试
    ada_real_err[i] = zero_one_loss(y_pred, test_word_arrayLabel)  # 得出不同的，然后除于总数
ada_real_err_train = np.zeros((n_estimators,))
for i, y_pred in enumerate(ada_real.staged_predict(train_mood_array)):  # 训练样本对训练样本的结果
    ada_real_err_train[i] = zero_one_loss(y_pred, label)


def test(word):
    word_array = bayes.build_word_array(word)
    asfaiajioaf = bayes.setOfWordsListToVecTor(vocabList, word_array)
    return ada_real.predict(asfaiajioaf)[0]


def testandscore(word):
    word_array = bayes.build_word_array(word)
    asfaiajioaf = bayes.setOfWordsListToVecTor(vocabList, word_array)
    aa, bb = ada_real.predict(asfaiajioaf)[0], ada_real.predict_proba(asfaiajioaf)[0]
    total = {}
    total["type"] = int(aa)  # 需要转化一下int跟int32是不同的，int32不能序列化
    temp = []
    ggg = {}
    ccc = {}
    ddd = {}
    ggg["key"] = "正向"
    ggg["value"] = float('%.5f' % bb[0])
    ccc["key"] = "负向"
    ccc["value"] = float('%.5f' % bb[1])
    ddd["key"] = "客观"
    ddd["value"] = float('%.5f' % bb[2])
    temp.append(ggg)
    temp.append(ccc)
    temp.append(ddd)
    total["data"] = temp
    return total


if __name__ == '__main__':
    word = "高兴，开心，非常开心，愉快"
    tt = testandscore(word)
    print(json.dumps(tt))
