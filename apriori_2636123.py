import argparse
import itertools


def load_transactions(filename):
    transactions = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if line == "":
                continue

            parts = line.split(",")
            transaction = set()

            for item in parts:
                item = item.strip()
                if item != "":
                    transaction.add(int(item))

            transactions.append(transaction)

    return transactions


def find_frequent_1_itemsets(transactions, min_support):
    counts = {}

    for transaction in transactions:
        for item in transaction:
            one_itemset = frozenset([item])

            if one_itemset in counts:
                counts[one_itemset] += 1
            else:
                counts[one_itemset] = 1

    frequent = {}

    for itemset in counts:
        if counts[itemset] >= min_support:
            frequent[itemset] = counts[itemset]

    return frequent


def has_infrequent_subset(candidate, prev_frequent):
    subsets = itertools.combinations(candidate, len(candidate) - 1)

    for subset in subsets:
        if frozenset(subset) not in prev_frequent:
            return True

    return False


def apriori_gen(prev_frequent, k):
    candidates = set()
    prev_list = list(prev_frequent)

    for i in range(len(prev_list)):
        for j in range(i + 1, len(prev_list)):
            l1 = sorted(list(prev_list[i]))
            l2 = sorted(list(prev_list[j]))

            if l1[:k - 2] == l2[:k - 2]:
                candidate = frozenset(prev_list[i] | prev_list[j])

                if len(candidate) == k:
                    if not has_infrequent_subset(candidate, prev_frequent):
                        candidates.add(candidate)

    return candidates


def count_support(transactions, candidates):
    counts = {}

    for candidate in candidates:
        counts[candidate] = 0

    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                counts[candidate] += 1

    return counts


def apriori(transactions, min_support):
    all_frequent = []

    L1 = find_frequent_1_itemsets(transactions, min_support)
    current_frequent = L1
    k = 2

    while len(current_frequent) > 0:
        current_list = list(current_frequent.keys())
        current_list.sort(key=lambda x: sorted(list(x)))

        for itemset in current_list:
            all_frequent.append(itemset)

        prev_frequent = set(current_frequent.keys())
        candidates = apriori_gen(prev_frequent, k)

        if len(candidates) == 0:
            break

        candidate_counts = count_support(transactions, candidates)

        next_frequent = {}

        for itemset in candidate_counts:
            if candidate_counts[itemset] >= min_support:
                next_frequent[itemset] = candidate_counts[itemset]

        current_frequent = next_frequent
        k += 1

    return all_frequent


def format_itemset(itemset):
    items = sorted(list(itemset))
    return "{ " + ", ".join(str(x) for x in items) + " }"

def run_apriori_from_text(text, min_support):
    transactions = []

    for line in text.splitlines():
        line = line.strip()

        if line == "":
            continue

        parts = line.split(",")
        transaction = set()

        for item in parts:
            item = item.strip()
            if item != "":
                transaction.add(int(item))

        transactions.append(transaction)

    frequent_itemsets = apriori(transactions, min_support)

    output = []
    output.append("min_sup " + str(min_support))

    for itemset in frequent_itemsets:
        output.append(format_itemset(itemset))

    output.append("End - total items: " + str(len(frequent_itemsets)))

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, dest="input_file")
    parser.add_argument("-m", required=True, type=int, dest="min_support")
    args = parser.parse_args()

    transactions = load_transactions(args.input_file)
    frequent_itemsets = apriori(transactions, args.min_support)

    print("inputfile", args.input_file)
    print("min_sup", args.min_support)

    for itemset in frequent_itemsets:
        print(format_itemset(itemset), end=" ")
    print()

    print("End - total items:", len(frequent_itemsets))


if __name__ == "__main__":
    main()