'''
    Python module of different functions for working with data.
    These functions are used in the other libraries as utilities.
'''

__author__ = 'hpreston'


def dict_filter(source_dict, filter_list):
    '''
    For a given dictionary, return a new dictionary with only the keys included
    in the filter.  If the filter_list is empty, return entire source_dict
    :param source_dict:  The dictionary to filter key values for.
    :param filter_list:  A list of the key values you wish to maintain.
    :return:
    '''
    if (len(filter_list) == 0): return source_dict
    result = {key: source_dict[key] for key in filter_list}
    # print result
    return result

def list_search(list, result_filter):
    '''
    Filter down a given list of dictionaries for only those elements where there is
    a match for one of the key:value matches in the result_filter dictionary.
    If there are more than one entry in the result_filter, only one must match.
      (searching is an OR construct)
    If the result_filter is empty, return the whole list.
    :param list: The list of dictionaries to search over
    :param result_filter: A dictionary of values to search for
    :return:
    '''
    if (len(result_filter) == 0): return list
    new_list = []
    for l in list:
        for key in result_filter.keys():
            if (l[key] == result_filter[key]):
                new_list.append(l)
                break
    return new_list
