## association_rule
This is a repository for assiciation_rule.

* There are two datasets:
  * Select from kaggle.com: 
    Transactions from a bakery. (downloaded from https://www.kaggle.com/xvivancos/transactions-from-a-bakery )
   
    The dataset is in `data/kaggle_data.csv`.  
    In this dataset, the four columns are Date, Time, Transaction, Item.  
    I only use the column of Transaction and Item in my analysis.  
    The items which share the same Transaction are in the same transaction.  
   
    e.g.  
    2016-10-30, 09:58:11, 1, Bread  
    2016-10-30, 10:05:34, 2, Scandinavian  
    2016-10-30, 10:05:34, 2, Scandinavian   
    2016-10-30, 10:07:57, 3, Hot chocolate    
    2016-10-30, 10:07:57, 3, Jam  
    2016-10-30, 10:07:57, 3, Cookies  

    The transactions are: ['Bread']  
			  ['Scandinavian', 'Scandinavian']  
   			  ['Hot Chocolate', 'Jam', 'Cookies']  

  * Use IBM Quest Synthetic Data Generator:  
    The dataset is in `data/ibm_data`.  
    In this dataset, the three columns are CustomID, TransactionID, ItemID  
    I only use the column of TransactionID and ItemID.(Because the CustomID is always equal to TransactionID)  
    The items which share the same TransactionID are in the same transaction.  

    e.g.  
         1          1          6  
         1          1         38  
         1          1         47  
         1          1         49  
         1          1         55  
         1          1         63  
         1          1         67  
         1          1         69  
         1          1         74  
         1          1         78  
         1          1         83  
         2          2          8  
         2          2         34  
         2          2         50  
         2          2         71  
         3          3         36  
         3          3         45  
         3          3         51  
         3          3         52  
         3          3         61  
         3          3         62  
         3          3         63  

      The transactions are: [6, 38, 47, 49, 55, 63, 67, 69, 74, 78, 83]  
			    [8, 34, 50, 71]  
  			    [36, 45, 51, 52, 61, 62, 63]  
   
* data preprocess:  
  * data/kaggle_data.csv:  
      
    ` 
    with open('./data/kaggle_data.csv') as f:  
      data = np.array(list(csv.reader(f, delimiter=','))[1:])[:, 2:]  
    `

    The first row is "Date, Time, Transaction, Item", so I skip it.  
    Besides, I only use the third and the fourth column to analysis.  

  * ibm/data:  
      
      '''
      with open('./data/ibm_data') as f:
        rawdata = f.readlines()
      data = []
      for i in range(len(rawdata)):
        data.append([int(rawdata[i][10:21]), int(rawdata[i][21:])])
      '''

      Each line contains three element, and each of these takes up 10 bytes, for a total of 33 bytes per line.
      And I take the second and the third column to analysis.

*  The method to find the frequent itemsets: Brute force, Apriori, FPgrowth
   1. Apriori, Brute force
      The code is in `./apriori.py`
      
      usage:
      $ python3 apriori.py [dataset] [support] [confidence] > [result_path]

      e.g. $ python3 apriori.py kaggle 0.01 0.01 > result/kaggle_apriori
      The [dataset] can be `kaggle` or `ibm`.
      The [support] and [confidence] value is a `float less than 1`.

      a. First, call the get_transactions() to get all the transactions and the category of items.
      b. Then, call the freq_itemset() to get the frequent itemsets we want.
	 You can choose which method you want to use by changing the parameter `method`.('brute' or 'apriori'(default))
         In this function, the program will scan all the transactions and use get_itemsets() to get the k-frequent itemsets,
  	 and save it to a set.
      c. Then, call gen_rules() to get the association rules.
	 In this function, I want to find the rule: `sample -> target: confidence`.
	 So for each frequent itemsets, each subset of this itemsets is a sample, and the remaining subset is a target.
  	 e.g. frequent itemset: ['Bread', 'Coffee', 'Pastry']
	      sample: ['Bread']
	      target: ['Coffee', 'Pastry']
	      confidence = (frequent itemset support) / (sample support)

   2. FPfrowth
      The code is in `./fpgrowth.py`
      
      usage:
      $ python3 fpgrowth.py [dataset] [support] [confidence] > [result_path]

      e.g. $ python3 fpgrowth.py kaggle 0.01 0.01 > result/kaggle_fpgrowth
      The [dataset] can be `kaggle` or `ibm`.
      The [support] and [confidence] value is a `float less than 1`.

      a. First, we call the get_transactions() to return all the transactions and the category of items.
      b. Then, we call the create_dataset() to return a set, whose key is the kind of the transaction, and the value is how many times this transaction occur in this dataset.
      c. Then, we call the create_tree() to return the fptree and the header table.
      d. Then, we call the fptree() to return the frequent itemsets we want.
      e. Then, call gen_rules() to get the association rules.
	 In this function, I want to find the rule: `sample -> target: confidence`.
	 So for each frequent itemsets, each subset of this itemsets is a sample, and the remaining subset is a target.
  	 e.g. frequent itemset: [38, 63, 69]
	      sample: [38]
	      target: [63, 69]
	      confidence = (frequent itemset support) / (sample support)

*  Result
   The result file will be:
   
   '''
   * Execution time : 
   * Min support:
   * Frequent itemset:
   .
   .
   .
   .
   * Min confidence:
   * Association Rules:
   .
   .
   .
   .
   '''
   
   1. The result of kaggle data is in `result/kaggle_apriori` and `result/kaggle_fpgrowth`
      (with support = 0.01, confidence = 0.01)
   
   2. The result of ibm data is in `result/ibm_apriori` and `result/ibm_fpgrowth`
      (with support = 0.05, confidence = 0.05) 
