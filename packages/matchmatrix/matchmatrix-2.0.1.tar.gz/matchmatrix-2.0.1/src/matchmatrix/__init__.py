# Copyright (C) 2021-2024 Porte Verte

from matchmatrix.functions import (
    write_to_log
    , current_method_name
    , number_of_words_in_string
    , get_initials
    , explode_frame_list_column
)

from matchmatrix.manager import MatchManager

from matchmatrix.constants import COMPANY_SUFFIXES_DICT, DOMAIN_SUFFIXES_LIST

def standardise_company_name(my_string):

    return MatchManager().standardise_company_name(my_string)

def strip_company_name(my_string):

    return MatchManager().standardise_company_name(my_string)

def strip_domain_suffix(my_string):
    
    return MatchManager().strip_domain_suffix(my_string)