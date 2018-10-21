#!/usr/bin/env python3
import numpy as np
import csv
import sys
import itertools
import operator
sys.path.append('./apriori')
from apriori import get_transactions, get_subsets, get_itemsets

class node:
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.link = None
        self.child = {}

    def increment(self, count):
        self.count += count

    def display(self, ind=1):
        print('    '*ind, self.name, '  ', self.count)
        for child in self.child.values():
            child.display(ind+1)

def create_dataset(data):
    dataset = {}
    for i in data:
        if frozenset(i) not in dataset.keys():
            dataset[frozenset(i)] = 1
        else:
            dataset[frozenset(i)] += 1
    return dataset

def create_tree(dataset, support):
    header = {}
    for trans in dataset:
        for item in trans:
            header[item] = header.get(item, 0) + dataset[trans]
    for i in list(header.keys()):
        if header[i]<support or i=='NONE':
            del(header[i])
        else:
            header[i] = [header[i], None]
    freq_item_set = list(header.keys())
    if len(freq_item_set) == 0:
        return None, None

    tree = node(name = 'Root', count = 1, parent = None)

    for trans, count in dataset.items():
        trans_with_count = {}
        for item in trans:
            if item in freq_item_set:
                trans_with_count[item] = header[item][0]
        if len(trans_with_count) > 0:
            sorted_trans = [i[0] for i in sorted(trans_with_count.items(), key=lambda k:k[1], reverse=True)]
            update_tree(sorted_trans, tree, header, count)
    return tree, header

def update_tree(transaction, tree, header, count):
    if transaction[0] in tree.child:
        tree.child[transaction[0]].increment(count)
    else:
        tree.child[transaction[0]] = node(transaction[0], count, tree)
        if header[transaction[0]][1] == None:
            header[transaction[0]][1] = tree.child[transaction[0]]
        else:
            update_header(header[transaction[0]][1], tree.child[transaction[0]])

    if len(transaction)>1:
        update_tree(transaction[1:], tree.child[transaction[0]], header, count)

def update_header(oldnode, newnode):
    while oldnode.link != None:
        oldnode = oldnode.link
    oldnode.link = newnode

def get_prev_path(item, node):
    prev_path = {}
    while node != None:
        tmp = []
        get_parent_tree(node, tmp)
        if len(tmp) > 1:
            prev_path[frozenset(tmp[:-1])] = node.count
        node = node.link
    return prev_path

def get_parent_tree(node, path):
    if node.parent != None:
        path.append(node.parent.name)
        get_parent_tree(node.parent, path)

def fptree(tree, header, support, prev_set, freq_itemsets):
    items = [i[0] for i in sorted(header.items(), key=lambda k: k[1][0])]
    for item in items:
        new_freq_itemset = prev_set.copy()
        new_freq_itemset.add(item)
        freq_itemsets.append(new_freq_itemset)

        prev_path = get_prev_path(item, header[item][1])
        tmp_tree, tmp_header = create_tree(prev_path, support)

        if tmp_header != None:
            fptree(tmp_tree, tmp_header, support, new_freq_itemset, freq_itemsets)

if '__main__' == __name__:
    if len(sys.argv) == 1:
        print('usage: $ python3 fpgrowth.py [support]')
        print('\nThe support value can be a `float less than 1` or an `integer`')
        exit()

    with open('./dataset.csv') as f:
        data = np.array(list(csv.reader(f, delimiter=','))[1:])[:, 2:]
    transactions, category = get_transactions(data)
    dataset = create_dataset(transactions)
    if float(sys.argv[1]) < 1:
        support = int(float(sys.argv[1]) * len(transactions))
    else:
        support = int(sys.argv[1])
    tree, header = create_tree(dataset, support)
    freq_itemsets = []
    prev_set = set([])
    fptree(tree, header, support, prev_set, freq_itemsets)

    max_len = max([len(i) for i in freq_itemsets])

    print('min support: %d' %support)
    for i in range(1, max_len + 1):
        print('\n%d frequent itemsets:' %i)
        for item in freq_itemsets:
            if len(item) == i:
                print(list(item))
