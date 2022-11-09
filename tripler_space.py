"""
- Functions to handle REMOVE, REPLACE and REDUNDANT while trying to balance having:
- More efficiency by reducing time and space complexity.
- Precision by making sure the functionality remains intact for more generalized dataframe columns.
- As this version makes use of Nested Lists and focuses more on reducing Space Complexity,
  The Average Time Complexity is O(nlogn) for Replace, Remove and O(n) for Redundant.
"""
import pandas as pd
from bisect import bisect_left

def binary_element_search(array:list, element: str) -> str:
    """
    - Using binary search algorithm (by implementing python in-built bisect_left function)
    to reduce the search (For remove and replace) to O(logn) instead of O(n).

    - It takes 2 arguments:
      the string element that is to be searched for in the list array.

    - If element is found in the given array, it RETURNS the ELEMENT else
    it RETURNS None.
    """
    array = sorted(array)
    i = bisect_left(array, element.strip())
    if i != len(array) and array[i].strip().lower() == element.strip().lower():
        return array[i]


"""
- These redundant functions were scratched because 2 FOR loops were done
for creating a new list without empty strings and another to iterate and apply
the redundancy removal by just skipping the element if it already exists.
"""
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


def redundant(string: str) -> str:
    """
    - It takes String as the argument. Initializes a FINAL_STRING which elements will
    be appended to after they goes through the filtering process.

    - The filtering process first checks for empty strings, then proceeds to append elements to
    the FINAL_STRING
    
    - After all the filtering is done, the FINAL_STRING is then returned as a STRING.
    """
    final_string = []
    for text in string.split(','):
        if(text.strip() != ''):
            if(text.strip() not in final_string):
                final_string.append(text.strip())
    return ', '.join(final_string)
    
def replace(main_array, string) -> str:
    """
    - It takes String as the argument. Initializes a Final_String which elements will
    be appended to after it goes through the filtering process.

    - The filterin process first checks for empty strings, then checks if the element is found in the
      first list (Original) and if match is found, then takes the index and appends the ELEMENT from the
      second list (Replacement) else appends the original element.

    - After all the filtering is done, the FINAL_STRING is then returned.
    """
    final_string = []
    for text in string.split(','):
        if(text.strip() != ''):
            search_result = binary_element_search(main_array[0], text)
            if(search_result):
                final_string.append(main_array[1][main_array[0].index(search_result.strip())])
            else:
                final_string.append(text.strip())
    return ', '.join(final_string)

def replace_redundant(main_array, string) -> str:
    """
    - It takes String as the argument. Initializes a Final_String which elements will
    be appended to after it goes through the filtering process.

    - It is the combination of Redundant and Replacement functions to perform them in one loop to further
      reduce the time and space complexity.

    - The filterin process first checks for empty strings, then checks if the element is found in the
      first list (Original) and if match is found, then takes the index and appends the ELEMENT from the
      second list (Replacement) else appends the original element to the FINAL_LIST only when the
      element is not already present in the final_string.
      
    - After all the filtering is done, the FINAL_STRING is then returned.
    """
    final_string = []
    for text in string.split(','):
        if(text.strip() != ''):
            search_result = binary_element_search(main_array[0], text)
            if(search_result and text.strip() not in final_string):
                final_string.append(main_array[1][main_array[0].index(search_result.strip())])
            else:
                final_string.append(text.strip())
    return ', '.join(final_string)

def remove(search_array, string) -> str:
    final_string = []
    for text in string.split(','):
        if(text.strip() != ''):
            search_result = binary_element_search(search_array, text)
            if(search_result == None):
                final_string.append(text.strip())
    return ', '.join(final_string)