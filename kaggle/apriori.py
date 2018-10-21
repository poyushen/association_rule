#!/usr/bin/env python3
import numpy as np
import csv
import math
import sys
import itertools

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
    if support < 1:
        support = int(support * len(transactions))
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

if '__main__' == __name__:
    if len(sys.argv) == 1:
        print('usage: $ python3 apriori.py [support]')
        print('\nThe support value can be a `float less than 1` or an `integer`')
        exit()

    with open('./dataset.csv') as f:
        dataset = np.array(list(csv.reader(f, delimiter=','))[1:])[:, 2:]

    transactions, category = get_transactions(dataset)
    if float(sys.argv[1]) < 1:
        support = int(float(sys.argv[1]) * len(transactions))
    else:
        support = int(sys.argv[1])

    ans = freq_itemset(transactions, category, support)

    print("min support: %d" %support)
    for i in range(len(ans)):
        print("\n%d frequent itemsets :" %(i+1))
        for j in range(len(list(ans[i+1].keys()))):
            print(list(list(ans[i+1].keys())[j]))
