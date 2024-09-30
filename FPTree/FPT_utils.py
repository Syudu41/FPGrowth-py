
class TreeNode:
    def __init__(self, item, freq = 1, parent_node = None): # Default values freq = 1, parent_node = None
        self.item = item # Name of the item
        self.freq = freq # freq. of items
        self.parent_node = parent_node # parent node
        self.child_node = {} # Child node/children/leaf node
        self.next_node = None # pointer to the leaf node. Not used when building the FPtree

    def view_item_details(self):
        print(f'Item: {self.item}')
        print(f'Frequency: {self.freq}')
        if self.parent_node == None or self.parent_node=='Root':
            print('Parent Node: None')
        else:
          print(f'Parent Node: {self.parent_node}')
          # print(f'Parent Node freq: {self.parent_node.freq}') # values cannot be displayed
          print(f'List of Child Node(s): {list(self.child_node.keys())}')
          # print(f'List of Child Node(s) freq.: {list(self.child_node.values())}') # values cannot be displayed

    def update_freq(self, freq): # update the freq. count for the given node.
        self.freq += freq
        # print(f'Update: Freq. of "{self.item}" updated to ->', self.freq)

    def display_simple_tree(self,space = 1, str_ = ''): # without freq.

        print(' '*space,str_+'___'*space,self.item)
        for child in list(self.child_node.values()):
            child.display_simple_tree(space+1, str_ = '|_')

    def display_complete_tree(self,space = 1, str_ = ''): # with freq.

        print(' '*space,str_+'___'*space,self.item,':',self.freq)
        for child in list(self.child_node.values()):
            child.display_complete_tree(space+1, str_ = '|_')



def FPT_insert(transaction, node, index_table):
  if len(transaction) == 0:
    return

  # print('Checking transaction:', transaction)
  first_item = transaction[0]

  # initiallty check for the first item in the transaction
  if first_item in node.child_node:
    node.child_node[first_item].update_freq(1)

  else:
    new_node = TreeNode(first_item, 1, node) # create the new node for the subsequent item
    node.child_node[first_item] = new_node # add the new node as child to the existing node
    # print('Displaying node:', node.view_item_details())


    #index table
    if index_table[first_item][1] == None: # check if the subsequent item within the transaction is None
      index_table[first_item][1] = new_node

    else:
      current_node = index_table[first_item][1]
      while current_node.next_node != None:
        current_node = current_node.next_node
      current_node.next_node = new_node


  FPT_insert(transaction[1:], node.child_node[first_item], index_table) # recursively add transactions


def FPT_index_table(support_dict):
  # index table -> list of (support of items, next node pointer)
  # [freq, None] -> None => index. of the next node
  index_table = {item: [freq, None] for item, freq in support_dict.items()}

  return index_table


def FPT_builder(transaction_list: list, threshold: int):
  support_dt = {}
  for itemlist in transaction_list:
    # print('Checking transaction:', i)
    for item in itemlist:
      if item not in support_dt:
        support_dt[item] = 1
      else:
          support_dt[item] += 1


  # print('Initial items with threshold support:')
  # print(support_dt)

  support_dt_ord = {item:freq for item, freq in support_dt.items() if freq >= threshold}

  # print('Final items with threshold support:')
  # print(support_dt_ord)

  if len(support_dt_ord) == 0: # base case
    return None, None

  # Initialize the index table
  index_table = FPT_index_table(support_dt_ord)
  root_node = TreeNode(None, 1, None)

  ordered_transaction_list = []
  for itemset in transaction_list:
    _list_ = [item for item in itemset if item in support_dt_ord]
    # sorting based on descending order of freq.
    # same freq. will lead to alphabetical sorting.
    _list_.sort(key=lambda item: (-support_dt_ord[item], item))
    ordered_transaction_list.append(_list_)

  for transaction in ordered_transaction_list:
    FPT_insert(transaction, root_node, index_table)

  return root_node, index_table


def FPT_Miner(index_table, min_sup, prefix_path, fp_patrn_list):

  new_index_ = [items for items, _ in sorted(index_table.items(), key=lambda x: x[1][0])]

  for item in new_index_:
    fp_set = prefix_path.copy()
    fp_set.add(item)

    # Add the current frequent set to the list of patterns
    fp_patrn_list.append([fp_set, index_table[item][0]])

    # finding prefix path
    prefix_paths_ = []
    current_node = index_table[item][1]

    while current_node != None:
      prefix_path_ = []
      parent = current_node.parent_node

      while parent != None and parent.item != None:
        prefix_path_.append(parent.item)
        parent = parent.parent_node

      if len(prefix_path_) > 0:
        prefix_paths_.append((prefix_path_, current_node.freq))

      current_node = current_node.next_node

      # Build the conditional FP-tree
      cd_transactions = []
      for path, count in prefix_paths_:
          for _ in range(count):  # Add each path count times
              cd_transactions.append(path)

      cd_Tree, cd_header = FPT_builder(cd_transactions, min_sup)

      # Mine the conditional FP-tree recursively
      if cd_header != None:
          FPT_Miner(cd_header, min_sup, fp_set, fp_patrn_list)

def remove_duplicates(nested_list):
    seen = set()
    result = []

    for sublist in nested_list:
        # Convert set elements in the sublist to sorted tuples for hashing
        converted_sublist = tuple([tuple(sorted(item)) if isinstance(item, set) else item for item in sublist])

        # Add to result if not already seen
        if converted_sublist not in seen:
            seen.add(converted_sublist)
            # Convert tuples back to sets where applicable
            result.append([set(item) if isinstance(item, tuple) else item for item in converted_sublist])

    return result


def fpgrowth(transactions, min_support):
    # Build the initial FP-tree
    root_node, index = FPT_builder(transactions, min_support)

    if index is None:
        return []

    # Mine the FP-tree to extract frequent patterns
    frequent_patterns = []
    FPT_Miner(index, min_support, set(), frequent_patterns)
    freq_patterns = remove_duplicates(frequent_patterns)
    
    return freq_patterns


