"""
- Functions to handle REMOVE, REPLACE and REDUNDANT while trying to balance having:
- More efficiency by reducing time and space complexity.
- Precision by making sure the functionality remains intact for more generalized dataframe columns.
- As this version makes use of Nested Lists and focuses more on reducing Space Complexity,
  The Average Time Complexity is O(nlogn) for Replace, Remove and O(n) for Redundant.
"""
import pandas as pd
from bisect import bisect_left
from pandas import DataFrame

def binary_element_search(array:list, element: str) -> str:
    """
    - Using binary search algorithm (by implementing python in-built bisect_left function)
    to reduce the search (For remove and replace) to O(logn) instead of O(n).

    - It takes 2 arguments:
      the string element that is to be searched for in the list array.

    - If element is found in the given array, it RETURNS the ELEMENT else
    it RETURNS None.
    """


    #ADD ANOTHER DATAFRAME COLUMN. IF PROVIDED WILL SHOW THE OPERATION DONE IN THERE.
    array = sorted(array)
    i = bisect_left(array, element.strip())
    if i != len(array) and array[i].strip().lower() == element.strip().lower():
        return array[i].strip()


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


def redundant(string: str, keep_empty: bool = False) -> str:
    """
    PARAMETERS:
    - string: str.
        - The str which will be split using comma as the separator and worked on to find redundancies.
            Ex: 'Apple, Monkey, Gorilla, Doraemon'.

    - keep_empty: bool. False by default.
        - If set to True, would remove all empty elements.
            Ex: 'Apple, Doraemon, , Neko' would return 'Apple, Doraemon, Neko'.
    
    WORKING:
    - It takes STRING as the argument. Initializes a FINAL_STRING which elements will
        be appended to after they go through the filtering process.

    - The filter process first checks if the element is present in the FINAL_STRING, if not then will append
        the elements to FINAL_STRING.
    
    - If KEEP_EMPTY is set to True, it will retain one empty element.
    """
    final_string = []
    match keep_empty:
        case False:
            for text in string.split(','):
                if(text.strip() != ''):
                    if(text.strip() not in final_string):
                        final_string.append(text.strip())
        case True:
            for text in string.split(','):
                if(text.strip() != ''):
                    if(text.strip() not in final_string):
                        final_string.append(text.strip())
                else:
                    final_string.append(text)

    return ', '.join(final_string)
    
# def replace(main_array: list[DataFrame], string: str, redundancy = False) -> str:
    # final_string = []
    # for text in string.split(','):
    #     if(text.strip() != ''):
    #         search_result = binary_element_search(main_array[0].tolist(), text)
    #         if(redundancy == False):
    #             if(search_result):
    #                 final_string.append(main_array[1][main_array[0].tolist().index(search_result.strip())])
    #             else:
    #                 final_string.append(text.strip())

    #         elif(redundancy == True):                
    #             if(search_result and main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())] not in final_string):
    #                 final_string.append(main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())])

    #             elif(search_result == None and text.strip() not in final_string):
    #                 final_string.append(text.strip())
    # return ', '.join(final_string)


def remove(search_array: list, string: str, keep_empty: bool = False) -> str:
    final_string = []
    match keep_empty:
        case False:
            for text in string.split(','):
                if(text.strip() != ''):
                    search_result = binary_element_search(search_array, text)
                    if(search_result == None):
                        final_string.append(text.strip())
        case True:
            for text in string.split(','):
                search_result = binary_element_search(search_array, text)
                if(search_result == None):
                    final_string.append(text.strip())
    return ', '.join(final_string)


def replace(main_array: list[DataFrame], string: str, redundancy:  bool = False, keep_empty: bool = False, removal: bool = False) -> str:
    """
    PARAMETERS:
    -  main_array: [DataFrame['search_column'], DataFrame['replace_column']].
       - The DF['search_column'] is the DF Column where your Main Column (.apply() one) will search for elements.
       - If a match is made, it will then replace that element with the same index element from DF['replace_column'].
       - Ex: [df['original'], df['replacement']].
    - string: str.
       - The string the function would fetch from each row and work on.
       - Ex: A DataFrame cell containing multiple elements separated by a comma: 'Elephant, Monkey, Ant'.
    - redundancy: bool. False by default.
       - If set to True, would remove all redundant elements from the given string.
       - Ex: 'Monkey, Ant, Dog, Ant' would return 'Monkey, Ant, Dog'.
    
    WORKING:
    - Takes 
    
    - It takes String as the argument. Initializes a Final_String which elements will
    be appended to after it goes through the filtering process.

    - The filterin process first checks for empty strings, then checks if the element is found in the
      first list (Original) and if match is found, then takes the index and appends the ELEMENT from the
      second list (Replacement) else appends the original element.

    - After all the filtering is done, the FINAL_STRING is then returned.
    """
    final_string  = []
    match redundancy:
        case False:
            match keep_empty:
                case False:
                    for text in string.split(','):
                        if(text.strip() != ''):
                            search_result = binary_element_search(main_array[0].tolist(), text)
                            if(search_result):
                                element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                final_string.append(element_replacement)
                            else:
                                final_string.append(text.strip())
                        
                case True:
                    for text in string.split(','):
                        search_result = binary_element_search(main_array[0].tolist(), text)
                        if(search_result):
                            element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                            final_string.append(element_replacement)
                        else:
                            final_string.append(text.strip())
        
        case True:
            match keep_empty:
                case False:
                    for text in  string.split(','):
                        if(text.strip() != ''):
                            search_result = binary_element_search(main_array[0].tolist(), text)
                            if(search_result):
                                element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                if(element_replacement not in final_string):
                                    final_string.append(element_replacement)
                            elif(search_result ==  None and text.strip() not in final_string):
                                final_string.append(text.strip())
                
                case True:
                    for text in string.split(','):
                        search_result = binary_element_search(main_array[0].tolist(), text)
                        if(search_result):
                            element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                            if(element_replacement not in final_string):
                                final_string.append(element_replacement)
                        elif(search_result ==  None and text.strip() not in final_string):
                            final_string.append(text.strip())
    
    match removal:
        case True:
            if len(main_array) > 2:
                return remove(main_array[2].tolist(), ', '.join(final_string),keep_empty = True)
            else:
                return ', '.join(final_string)
        case False:
            return ', '.join(final_string)


def REPLACE(main_array: list[DataFrame], string: str, redundancy:  bool = False, keep_empty: bool = False, removal: bool = False) -> str:

    final_string  = []
    match redundancy:
        case False:
            match keep_empty:
                case False:
                    match removal:
                        case False:
                            for text in string.split(','):
                                if(text.strip() != ''):
                                    search_result = binary_element_search(main_array[0].tolist(), text)
                                    if(search_result):
                                        element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                        final_string.append(element_replacement)
                                    else:
                                        final_string.append(text.strip())

                        case True:
                            for text in string.split(','):
                                if(text.strip() != ''):
                                    search_result = binary_element_search(main_array[0].tolist(), text)
                                    if len(main_array) > 2:
                                        removal_result = binary_element_search(main_array[2].tolist(), text)
                                        if(search_result and removal_result == None):
                                            element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                            final_string.append(element_replacement)
                                        elif(search_result == None and removal_result == None):
                                            final_string.append(text.strip())
                                    else:
                                        if(search_result):
                                            element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                            final_string.append(element_replacement)
                                        else:
                                            final_string.append(text.strip())
                        
                case True:
                    match removal:
                        case False:
                            for text in string.split(','):
                                search_result = binary_element_search(main_array[0].tolist(), text)
                                if(search_result):
                                    element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                    final_string.append(element_replacement)
                                else:
                                    final_string.append(text.strip())

                        case True:
                            for text in string.split(','):
                                search_result = binary_element_search(main_array[0].tolist(), text)
                                if len(main_array) > 2:
                                    removal_result = binary_element_search(main_array[2].tolist(), text)
                                    if(search_result and removal_result == None):
                                        element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                        final_string.append(element_replacement)
                                    elif(search_result == None and removal_result == None):
                                        final_string.append(text.strip())
                                else:
                                    if(search_result):
                                        element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                        final_string.append(element_replacement)
                                    else:
                                        final_string.append(text.strip())

        case True:
            match keep_empty:
                case False:
                    match removal:
                        case False:
                            for text in  string.split(','):
                                if(text.strip() != ''):
                                    search_result = binary_element_search(main_array[0].tolist(), text)
                                    if(search_result):
                                        element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                        if(element_replacement not in final_string):
                                            final_string.append(element_replacement)
                                    elif(search_result ==  None and text.strip() not in final_string):
                                        final_string.append(text.strip())

                        case True:
                            for text in  string.split(','):
                                if(text.strip() != ''):
                                    search_result = binary_element_search(main_array[0].tolist(), text)
                                    if len(main_array) > 2:
                                        removal_result = binary_element_search(main_array[2].tolist(), text)
                                        if(search_result and removal_result == None):
                                            element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                            if(element_replacement not in final_string):
                                                final_string.append(element_replacement)
                                        elif(search_result == None and removal_result == None):
                                            final_string.append(text.strip())
                                    else:
                                        if(search_result):
                                            element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                            if(element_replacement not in final_string):
                                                final_string.append(element_replacement)
                                        elif(search_result ==  None and text.strip() not in final_string):
                                            final_string.append(text.strip())
                                        
                
                case True:
                    match removal:
                        case False:                            
                            for text in string.split(','):
                                search_result = binary_element_search(main_array[0].tolist(), text)
                                if(search_result):
                                    element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                    if(element_replacement not in final_string):
                                        final_string.append(element_replacement)
                                elif(search_result ==  None and text.strip() not in final_string):
                                    final_string.append(text.strip())

                        case True:                            
                            for text in string.split(','):
                                search_result = binary_element_search(main_array[0].tolist(), text)
                                if len(main_array) > 2:
                                    removal_result  = binary_element_search(main_array[2].tolist(), text)
                                    if(search_result and removal_result == None):
                                        element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                        if(element_replacement not in final_string):
                                            final_string.append(element_replacement)
                                    elif(search_result == None and text.strip() not in final_string and removal_result == None):
                                        final_string.append(text.strip())
                                else:
                                    if(search_result):
                                        element_replacement =  main_array[1].tolist()[main_array[0].tolist().index(search_result.strip())]
                                        if(element_replacement not in final_string):
                                            final_string.append(element_replacement)
                                    elif(search_result ==  None and text.strip() not in final_string):
                                        final_string.append(text.strip())

    return ', '.join(final_string)