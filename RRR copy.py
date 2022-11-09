import pandas as pd
from bisect import bisect_left

df_reporters = pd.read_csv('Test_Reporters.csv')
df_jobs = pd.read_csv('Test_Jobs.csv')
df_remove = pd.read_csv('Test_Remove.csv')

def binary_element_search(array, element):
   array = sorted(array)
   i = bisect_left(array, element.strip())
   if i != len(array) and array[i].strip().lower() == element.strip().lower():
      return array[i]
   else:
      return -1

# def redundant(string):
#     split_string = sorted(set([text.strip() for text in string.split(',') if text.strip() !='']))
#     return ', '.join(split_string)

# def redundant(string):
#     split_string = [text.strip() for text in string.split(',') if text.strip() !='']
#     final_string = []
#     for text in split_string:
#         if(text not in final_string):
#             final_string.append(text)
#     return ', '.join(final_string)

def redundant(string):
    final_string = []
    for text in string.split(','):
        if(text.strip() != ''):
            if(text.strip() not in final_string):
                final_string.append(text.strip())
    return ', '.join(final_string)
    
def replace(search_array, replace_array, string):
    final_string = []
    for text in string.split(','):
        if(text.strip() != ''):
            search_result = binary_element_search(search_array, text)
            if(search_result != -1):
                final_string.append(replace_array[search_array.index(search_result.strip())])
            else:
                final_string.append(text.strip())
    return ', '.join(final_string)

def replace_redundant(search_array, replace_array, string):
    final_string = []
    for text in string.split(','):
        if(text.strip() != ''):
            search_result = binary_element_search(search_array, text)
            if(search_result != -1 and text.strip() not in final_string):
                final_string.append(replace_array[search_array.index(search_result.strip())])
            else:
                final_string.append(text.strip())
    return ', '.join(final_string)

def remove(search_array, string):
    final_string = []
    for text in string.split(','):
        if(text.strip() != ''):
            search_result = binary_element_search(search_array, text)
            if(search_result == -1):
                final_string.append(text.strip())
    return ', '.join(final_string)