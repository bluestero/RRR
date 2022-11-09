#Imports
import pandas as pd
from bisect import bisect_left
# import RRR

#Initializing DataFrames in ascending order (Except for reporters).
#To utilize binary search and reduce time complexity.
df_reporters = pd.read_csv('Test_Reporters.csv')
df_jobs = pd.read_csv('Test_Jobs.csv')
df_remove = pd.read_csv('Test_Remove.csv')

#Adding New Designation column.
df_reporters['new_designation'] = df_reporters['designation']

#Removes the first ', ' because of string concat.
def cleaner(text):
    if(text.startswith(', ')):
        return text.replace(', ','',1)
    else:
        return text

#Binary search function with Time Complexity of O(logn).
def binary_element_search(array, element, dataframe):
   array = sorted(array)
   i = bisect_left(array, element)
   if i != len(array) and array[i].strip().lower() == element.strip().lower():
      return dataframe[dataframe['original'] == element].index
   else:
      return -1

#Iterating the Dataframe to be sorted out.
for first_element in df_reporters['designation']:
   #Initializing Replacement for the final string and Result for any operations done.
   replacement = ''
   result = ''
   
   #Index of Reporters Dataframe to have a DataFrame iterator.
   ind_reporters = df_reporters[df_reporters['designation'] == first_element].index
   #Converting the multiple designation string into a list and assigning it to a vairable for further use.
   split_list = first_element.split(', ')
   #Iterating each element of the list.
   for sub_first_element in split_list:
      #Redundancy check, if receive more than one count, element gets removed.
      while(split_list.count(sub_first_element) > 1):
         print(split_list)
         split_list.remove(sub_first_element)
         #Appending the result as the operation is performed.
         if('redundant' not in result):
            result = result + ', redundant'

      #Checking if any element matches the elements from the Removal DataFrame.
      ind_remove = binary_element_search(df_remove['original'].tolist(), sub_first_element, df_remove)

      #Removing the matching element from the iterating split-list.
      if(ind_remove != -1):
         split_list.remove(sub_first_element)
         #Appending the result.
         if('remove' not in result):
            result = result + ', ' + 'remove'

   #Exiting the loop and performing match and replace in the updated split-list.
   for sub_first_element in split_list:
      #Initializing Jobs DataFrame Iterator and getting the index value if element is a match.
      ind_jobs = binary_element_search(df_jobs['original'].tolist(), sub_first_element, df_jobs)
      #Checking if find any match.
      if(ind_jobs != -1):
         #Concating the replacement value to the final string.
         replacement = replacement + ', ' + df_jobs.at[ind_jobs[0], 'replacement']
         #Checking if replacement operation already performed before.
         if('replace' not in result):
            #Appending the result.
            result = result + ', ' + 'replace'
      elif(ind_jobs == -1):
         #If no match, giving the original element back.
         replacement =  replacement + ', ' + sub_first_element

   #Finally adding the updated values to the DataFrame.
   # print(replacement.replace(', ','',1))
   df_reporters.at[ind_reporters[0], 'new_designation'] = cleaner(replacement)
   df_reporters.at[ind_reporters[0], 'found_in'] = cleaner(result)
            
#Exporting the saved CSV.
df_reporters.to_csv('Reporters_Replaced.csv')
# print(df_reporters['designation'].apply(lambda x: RRR.remove(x)))