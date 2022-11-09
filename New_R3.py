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
        
        
def REPLACE(main_array: list[DataFrame], string: str, redundancy:  bool = False, remove: bool = False, keep_empty: bool = False) -> str:
    final_string  = []
    match redundancy:
        case False:
            match keep_empty:
                case False:
                    for text in string.split(','):
                        if(text.strip() != ''):
                            search_result = binary_element_search(main_array[0].tolist(), text)
                            if(search_result):
                                element_replacement =  main_array[1][main_array[0].tolist().index(search_result.strip())]
                                final_string.append(element_replacement)
                            else:
                                final_string.append(text.strip())
                        
                case True:
                    for text in string.split(','):
                        search_result = binary_element_search(main_array[0].tolist(), text)
                        if(search_result):
                            element_replacement =  main_array[1][main_array[0].tolist().index(search_result.strip())]
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
                                element_replacement =  main_array[1][main_array[0].tolist().index(search_result.strip())]
                                if(element_replacement not in final_string):
                                    final_string.append(element_replacement)
                            elif(search_result ==  None and text.strip() not in final_string):
                                final_string.append(text.strip())
                
                case True:
                    for text in string.split(','):
                        search_result = binary_element_search(main_array[0].tolist(), text)
                        if(search_result):
                            element_replacement =  main_array[1][main_array[0].tolist().index(search_result.strip())]
                            if(element_replacement not in final_string):
                                final_string.append(element_replacement)
                        elif(search_result ==  None and text.strip() not in final_string):
                            final_string.append(text.strip())
    
    match remove:
        case True:
            if len(main_array) > 2:
                return remove(main_array[2].tolist(), ', '.join(final_string))
            else:
                return ', '.join(final_string)
        case False:
            return ', '.join(final_string)