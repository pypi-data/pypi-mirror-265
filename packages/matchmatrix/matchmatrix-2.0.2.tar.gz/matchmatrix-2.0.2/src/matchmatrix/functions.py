# Copyright (C) 2021-2024 Porte Verte

# =================================================================================================================================
# STRING FUNCTIONS
# =================================================================================================================================

def get_initials(s):
    # try:
    return ''.join([x[0] for x in str(s).split()])
    # except AttributeError:
    #     return s

def all_same_character(s, **kwargs):
    
    for k, v in kwargs.items():
        if k == 'c':
            c = v
    
    n = len(s)
    for i in range(1, n):
        if s[i] != c:
            return False
        if s[i] != s[0]:
            return False
 
    return True

def number_of_words_in_string(my_string):
    
    # make sure we are dealing with a string (in case a float is passed)
    my_string = str(my_string)
    
    # determine the number of words in the string by splitting it into into a list and getting its length    
    return len(my_string.strip().split())

def remove_from_start(my_string, my_char_list):
    bol_stop = False
    while bol_stop == False:
        # check the length inside the while loop in case it is zero after the characters have been removed
        if len(my_string) == 0:
            break
        my_char = my_string[0]
        if my_char in my_char_list:
            my_string = my_string.lstrip(my_char)
        else:
            bol_stop = True
    return my_string

def remove_from_end(my_string, my_char_list):
    bol_stop = False
    while bol_stop == False:
        # check the length inside the while loop in case it is zero after the characters have been removed
        if len(my_string) == 0:
            break
        my_char = my_string[-1]
        if my_char in my_char_list:
            my_string = my_string.rstrip(my_char)
        else:
            bol_stop = True
    return my_string

def sub_text(my_sub, my_text):
    my_output = my_text
    if len(my_text) == 0:
        if len(my_sub) > 0:
            my_output = my_sub
    return my_output

def trunc_reps(my_string, my_chars):
# if my_string comprises only one character in my_chars (on its own or repeated) then it will be replaced by a blank string e.g. "?????" becomes ""
    
    l = len(my_string)
    my_output = my_string
    
    # iterate through my_chars
    for mc in my_chars:                  
                
        # iterate through the characters in the string and bump the counter up by 1 if it's in my_chars
        k = 0
        for j in my_string:
            if j == mc:
                k = k + 1
    
        if k > 0:
            # if every character is the same and one of the ones in my_chars then make it blank
            # to do this divide the length by the counter and if the result is 1 then it's true
            if l/k == 1:
                my_output = ''
                break
            
    return my_output

def single_space(my_string):
            
    return ' '.join(my_string.split())

def my_replace(my_string, remove_string, replace_string):
    
    return my_string.replace(remove_string, replace_string)

# =================================================================================================================================
# =================================================================================================================================
# =================================================================================================================================

# =================================================================================================================================
# MISCELLANEOUS FUNCTIONS
# =================================================================================================================================

def current_method_name():
    
    import inspect
    
    # [0] is this method's frame and [1] is its parent's
    return inspect.stack()[1].function

def literal_return(val):
    
    from ast import literal_eval
    
    try:
        return literal_eval(val)
    except (ValueError, SyntaxError) as e:
        return val
    
def convert_to_set(my_object):   
    
    if type(my_object) == str:    
        try:        
            my_set = set(eval(my_object))            
        except Exception as e:
            my_set = set()
    else:
        if my_object == None:
            my_set = set()
        else:
            my_set = set(my_object)
            
    return my_set

def set_intersection_match_score(s1, s2):
    
    s1, s2 = convert_to_set(s1), convert_to_set(s2)
    
    # l = [s1, s2]
    # if None in l: return 0            
    # s1, s2 = set(s1), set(s2)  
    
    l1, l2 = len(s1), len(s2)    
    i = len(s1.intersection(s2))
    d = min(l1, l2)
    
    if d == 0: m = 0
    else: m = (i/d) * 100
    
    return m

def explode_frame_list_column(my_frame, my_column):
        
    # remove blank values -- and make a copy to keep the original frame in tact
    my_frame = my_frame[my_frame[my_column].str.len() > 0].copy()
    
    # evaluate the column -- because the lists are stored as text
    my_frame[my_column] = my_frame[my_column].apply(lambda x: literal_return(str(x)))
    
    # now do the actual explosion
    my_frame = my_frame.explode(my_column)
    
    return my_frame

def convert_dict_to_list(my_dict):
# turns the company suffixes dicitonary into a list to be used in company standardisation    
    my_list = []
    for md in my_dict:
        for my_item in my_dict[md]:
            my_list.append((my_item, md))
    # sort the list by the descending length of the first tuple value
    # this is so that replacments are made to the longest strings first in case one shorter term is inside another longer one 
    # e.g. kg is also at the end of gmbh & co kg so if it found a variant of kg first it would not replace all of the term
    my_list.sort(key=lambda x: len(x[0]), reverse=True)
    return my_list

def merge_dictionaries(d1, d2):
    
    # make copies of dictionaries to avoid messing them up
    d1_copy = d1.copy()
    d2_copy = d2.copy()
    
    # create a list comprising all keys from both dictionaries (convert list to set then back to list to dedupe it)
    my_keys = list(set([*d1_copy] + [*d2_copy]))
    
    # if a key is missing from one of the dictionaries then add it (then both will have exactly the same keys)
    for m in my_keys:
        if not m in d1_copy:
            d1_copy.update({m: None})
        if not m in d2_copy:
            d2_copy.update({m: None})
    
    # create blank dictionary
    d = {}
    
    # add each item in the keys list to the dictionary as a key with None as the value 
    for i in my_keys:
        d[i] = None
    
    # merge the values for the keys in each dictionary and add them to the new one
    for k in d.keys():
        # merge the lists of values (will produce a list of lists)
        merged_lists = [d1_copy[k],d2_copy[k]]
        # remove NoneType from lists
        clean_list = [x for x in merged_lists if x is not None]
        # flatten the list of lists into one plain list
        flat_list = [x for xs in clean_list for x in xs]
        # dedupe the list
        deduped_list = list(set(flat_list))
        # add the list to the dictionary
        d[k] = deduped_list
    
    return d

def write_to_log(log_path, my_text, **kwargs):
    
    import datetime
            
    # create output text
    output_text = datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + my_text
    
    # print to screen
    print(output_text)
    
    # write to log
    if log_path != None:
        log_file = open(log_path, 'a')
        log_file.write(output_text + '\n')
        log_file.close()
    
# =================================================================================================================================
# =================================================================================================================================
# =================================================================================================================================