#Imports
import pandas as pd
import r3_space
import sys

#Initializing DataFrames in ascending order (Except for reporters).
#To utilize binary search and reduce time complexity.
df_reporters = pd.read_csv('Test_Reporters.csv')
df_jobs = pd.read_csv('Test_Jobs.csv').sort_values('original')
df_remove = pd.read_csv('Test_Remove.csv').sort_values('original')

# df_reporters['new_designation'] = df_reporters['new_designation'].apply(lambda x: r3_space.remove(df_remove['original'].tolist(), x))
df_reporters['new_designation'] =  df_reporters['designation'].apply(lambda x:r3_space.redundant(x, keep_empty=True))
# df_reporters['new_designation'] = df_reporters['designation'].apply(lambda x: r3_space.REPLACE([df_jobs['original'], df_jobs['replacement'], df_remove['original']], x, redundancy=True, keep_empty=True, removal=True))
df_reporters.to_csv('TestNew.csv', index = False)

list1 = df_reporters['designation']
list2 = df_reporters['designation']
list3 = [list1, list2]
dict1 = dict(zip(list1, list2))
print(sys.getsizeof(list1))
print(sys.getsizeof(list2))
print(sys.getsizeof(list3))