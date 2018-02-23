import csv

class Transaction:
    def __init__(self, items):
        self.items = set(items)


class Apriori:
    def __init__(self, list_transactions):
        self.transactions = list_transactions
        self.all_items = set() #set is not allowed duplicated date, the big reason of using set Data Structure.
        for trn in self.transactions:
            self.all_items |= trn.items
        pass

    def get_support(self, set_items):
        # !!! Write code to return support of set_items
        count = 0
        for transaction in self.transactions:
            if set_items <= transaction.items:
                count += 1
        return count*1.0/len(transactions)

    # Perfectly using recursion!!!!!!!
    def get_combinations(self, items, num):
        # return "num" number of combinations of items
        if num>len(items) or num == 0:
            return [set()]
        if num == len(items):
            return [set(items)]

        items = list(items)
        total_comb = []
        for index,item in enumerate(items):
            other_items = items[index+1:]
            if len(other_items) < num - 1:
                continue
            comb_using_other_items = self.get_combinations(other_items,num-1)
            total_comb.extend([{item}|other for other in comb_using_other_items]) #be carefully! difference between extend and append.
        return total_comb

    #return type should be a set {item,item,item,...}
    def get_all_items(self, itemsets):
        # !!! Write code to merge all the itemsets and return the current items
        items = set()
        for itemset in itemsets:
            items |= itemset
        return items
    pass

    def get_subsets(self, items):
        # return all subsets of "items"
        subsets = []
        for item in items:
            for i in range(0, len(subsets)):
                subsets.append(subsets[i].union([item]))
            subsets.append(set([item]))

        return subsets

    def get_rules(self, min_sup, min_con):
        #var_a --> candidates_items   [{},{},{}...]
        #va_b --> candidates_supports
        # frequent_itemsets
        var_a = self.get_combinations(self.all_items, 1)
        num = 2
        freq_items = []
        supports = []
        while True:
            var_b = map(lambda x: self.get_support(x), var_a)
            # chosen_itemset [{},{},{}..], reason of using extend: freq_items data structure remains [{},{},{},{}..]
            chosen_itemset = []
            chosen_supports = []
            # freq_items [{},{},{},{}..]
            # supports[0.1, 0.2 , etc]
            # if use append, data structure change to [ [{},{},{}], [{},{},{}], [ ] ]
            for index, items in enumerate(var_a):
                if var_b[index] >= min_sup:
                    chosen_itemset.append(items)
                    chosen_supports.append(var_b[index])

            freq_items.extend(chosen_itemset)
            supports.extend(chosen_supports)
            #var_c --> items,gotten from last-level frequent item set, used to get next level combination.
            var_c = self.get_all_items(chosen_itemset)
            if num > len(var_c):
                break
            var_a = self.get_combinations(var_c, num)
            num += 1
        print "Frequent Itemsets"
        for item, support in sorted(zip(freq_items, supports), key=lambda x: x[1]):
            print ",".join(item), support

        #data structure of rules is [({},{}) , ({},{}) ,(),    ]
        rules = []
        confidences = []
        print "Rules"
        for items in freq_items:
            subsets = self.get_subsets(items)
            support = self.get_support(items)
            for var_d in subsets:
                if len(items - var_d) == 0:
                    continue
                support_A = self.get_support(var_d)
                if support / support_A > min_con:
                    rules.append((var_d, items - var_d))
                    confidences.append(support / support_A)

        for rule, confidence in sorted(zip(rules, confidences), key=lambda x: x[1]):
            print ",".join(rule[0]), "=>", ",".join(rule[1]), confidence

if __name__ == "__main__":
    test_data = [
        ['bread', 'milk'],
        ['bread', 'diaper', 'beer', 'egg'],
        ['milk', 'diaper', 'beer', 'cola'],
        ['bread', 'milk', 'diaper', 'beer'],
        ['bread', 'milk', 'diaper', 'cola'],
    ]

    transactions = []
    test = False

    if test:
        for row in test_data:
            transactions.append(Transaction(set(row)))
    else:
        with open("apriori_data.csv", "r") as f:
            for row in csv.reader(f):
                transactions.append(Transaction(set(row)))

    a = Apriori(transactions)
    a.get_rules(min_sup=0.15, min_con= 0.6)