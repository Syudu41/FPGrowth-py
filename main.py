import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import os
from FPTree.FPT_utils import fpt

'''
Assignment 1: Data Mining (COMP 7118)
Author: Sudarshan Balaji, UofM (U00895733)

Instructions:
- Run this main.py file, change the threshold if necessary (below). 
- Make sure that the format of the files (vocab.txt, topic-x.txt) do not change.
- Make sure to enter the vocab.txt file.
- Ensure that the correct topic-x.txt file is used as the input file.
- Similarly, make sure to change the name of the output file as pattern-x.txt, 
  failing which the outputs would be overwritten on the same file.

References used:
- ChatGPT
- GitHub: (Repo) https://github.com/chonyy/fpgrowth_py
- Medium Articles: https://medium.com/towards-data-science/fp-growth-frequent-pattern-generation-in-data-mining-with-python-implementation-244e561ab1c3

'''

# User can change file names here.
vocab_dir_ = r"Assignment1/vocab.txt" # change vocab file path here
ip_dir_ = r"Assignment1/topic-4.txt" # change input file path here 
op_dir_ = r"Assignment1/Outputs/pattern-4.txt" # change output file path here


index = 0
tid = 1
df = pd.DataFrame()
df['TID'] = '' # Transaction ID (int)
df['Transactions'] = '' # Transactions. Ex: TID: 1 -> Transactions: ['Philosophical', 'learning']


# Input (.txt) file
data_dict = {}

with open(vocab_dir_, 'r') as file: # Vocab file
    lines = file.readlines()

for line in lines:
    number, string = line.strip().split()
    data_dict[int(number)] = string



# Input (.txt) file
with open(ip_dir_, 'r') as file: 
    lines = file.readlines()
for line in lines:
    list_ = []
    for i in line.strip().split():
        list_.append(data_dict[int(i)])
    df.loc[index] = [tid, list_]
    index += 1
    tid += 1


if __name__ == "__main__":

    # driver function
    transactions = list(df['Transactions']) # input -> list of lists
    min_support = 400 # threshold (int),
    frequent_patterns = fpt(transactions, min_support)

    # Output (.txt) file:
    with open(op_dir_,'w') as output_file: 
        for pattern in frequent_patterns:
            new_str = ' '.join(pattern[0])
            output_file.write(f"{pattern[1]} \t {new_str}\n")

        print(f'Output at: {op_dir_}')