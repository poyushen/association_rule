#!/usr/bin/env python3
import numpy as np
import csv
import math
import sys
import itertools
import time

def get_transactions(dataset):
    transactions = [[] for i in range(int(dataset[-1][0]))]
    category = []
    k = 0
    for i in range(int(dataset[-1][0])):
        while k<=len(dataset) - 1 and (int(dataset[k][0])-1) == i:
            if dataset[k][1] not in category and dataset[k][1] != 'NONE':
                category.append(dataset[k][1])
            transactions[i].append(dataset[k][1])
            if k<len(dataset): k += 1

    return transactions, category

def get_subsets(datalist, num):
    return list(itertools.combinations(datalist, num))

def get_itemsets(transactions, subsets, support):
    item_dict = dict.fromkeys(subsets, 0)
    for subset in subsets:
        for transaction in transactions:
            if set(subset).issubset(set(transaction)):
                item_dict[subset] += 1
    item_dict = {key: value for key, value in item_dict.items() if value >= support}

    return item_dict

def freq_itemset(transactions, category, support, method='apriori'):
    num = np.max(np.array([len(i) for i in transactions]))
    ans = {}
    ans[1] = get_itemsets(transactions, get_subsets(category, 1), support)
    for i in range(2, num+1):
        if method is "brute":
            sublist = list(itertools.combinations(category, i))
        else:
            sublist = list(dict.fromkeys(list(itertools.chain(*(ans[i-1].keys())))).keys())

        if get_itemsets(transactions, get_subsets(sublist, i), support):
            ans[i] = get_itemsets(transactions, get_subsets(sublist, i), support)
        else:
            break

    return ans

def gen_rules(ans_set, confidence, length):
    support_set = {}
    for i in range(len(list(ans_set.values()))):
        for k, v in list(ans_set.values())[i].items():
            support_set[frozenset(list(k))] = v/length

    confidence_list = []
    for key in support_set.keys():
        if len(key) > 1 :
            for i in range(1, len(key)):
                subset = list(itertools.combinations(list(key), i))
                for sub in subset:
                    sample = frozenset(set(sub))

                    target = set(key)
                    for j in list(sub):
                        target.remove(j)
                    target = frozenset(target)
                    cond = {'sample': sample, 'target': target, 'confidence': round((support_set[key] / support_set[sample]), 3)}
                    if cond['confidence'] >= confidence:
                        confidence_list.append(cond)

    return confidence_list

if '__main__' == __name__:
    if len(sys.argv) < 4:
        print('usage: $ python3 apriori.py [dataset] [support] [confidence]')
        print('\ne.g. $ python3 apriori.py kaggle 0.01')
        print('\nThe [dataset] can be `kaggle` or `ibm`')
        print('The [support] and [confidence] value is a `float less than 1` (ratio)')
        exit()

    if sys.argv[1] == 'kaggle':
        with open('./data/kaggle_data.csv') as f:
            data = np.array(list(csv.reader(f, delimiter=','))[1:])[:, 2:]

    if sys.argv[1] == 'ibm':
        with open('./data/ibm_data') as f:
            rawdata = f.readlines()
        data = []
        for i in range(len(rawdata)):
            data.append([int(rawdata[i][10:21]), int(rawdata[i][21:])])

    start_time = time.time()
    transactions, category = get_transactions(data)
    support = int(float(sys.argv[2]) * len(transactions))
    confidence = float(sys.argv[3])

    ans = freq_itemset(transactions, category, support)
    rule = gen_rules(ans, confidence, len(transactions))

    print('* Execution time : %f sec' %(time.time() - start_time))
    print('\n* Min support: ', sys.argv[2])
    print('* Frequent itemsets:\n')
    for i in range(len(list(ans.values()))):
        for k, v in list(ans.values())[i].items():
            print(list(k), ': ', round(v/len(transactions), 3))

    print('\n* Min confidence: ', confidence)
    print('* Association Rules:\n')
    for i in rule:
        print(list(i['sample']), '-->', list(i['target']), ': ', i['confidence'])
