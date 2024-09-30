import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import os
from FPTree.FPT_utils import fpgrowth

# User can change file names here.
ip_dir_ = r"Assignment1/topic-4.txt" # change input file path here 
op_dir_ = r"Assignment1/pattern-4.txt" # change output file path here
vocab_dir_ = r"Assignment1/vocab.txt" # change vocab file path here

index = 0
ID = 1
df = pd.DataFrame()
df['TID'] = '' # Transaction ID (int)
df['Transactions'] = '' # Transactions. Ex: TID 1 -> (['Philosophical', 'learning'])  


# Input (.txt) file
data_dict = {}

with open(vocab_dir_, 'r') as file: # Vocab file
    lines = file.readlines()

for line in lines:
    number, string = line.strip().split()
    data_dict[int(number)] = string



# Input (.txt) file
with open(ip_dir_, 'r') as file: # input topic file goes here
    lines = file.readlines()
for line in lines:
    list_ = []
    for i in line.strip().split():
        list_.append(data_dict[int(i)])
    df.loc[index] = [ID, list_]
    index += 1
    ID += 1


if __name__ == "__main__":

    # driver function
    transactions = list(df['Transactions']) # input -> list of lists
    min_support = 400 # threshold (int),
    frequent_patterns = fpgrowth(transactions, min_support)


    # Output (.txt) file:
    with open(op_dir_,'w') as output_file: # change file name here (for output)
        for pattern in frequent_patterns:
            new_str = ' '.join(pattern[0])
            output_file.write(f"{pattern[1]} \t {new_str} \n")