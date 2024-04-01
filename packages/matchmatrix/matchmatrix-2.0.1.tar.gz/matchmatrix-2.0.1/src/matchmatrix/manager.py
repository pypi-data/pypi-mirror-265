# Copyright (C) 2021-2024 Porte Verte

# =================================================================================================================================
# INITIALISATION
# =================================================================================================================================

# import modules
import pandas as pd
import numpy as np

# import objects
from matchmatrix.functions import (
    write_to_log
    , set_intersection_match_score
    , sub_text
    , trunc_reps
    , single_space
    , my_replace
    , current_method_name
    , explode_frame_list_column
    , convert_dict_to_list
    , merge_dictionaries
)
from matchmatrix.constants import COMPANY_SUFFIXES_DICT, DOMAIN_SUFFIXES_LIST
from rapidfuzz import fuzz

# =================================================================================================================================
# =================================================================================================================================
# =================================================================================================================================

# =================================================================================================================================
# MATCH MANAGER CLASS
# =================================================================================================================================

# create the class that manages everything
class MatchManager:

    # =============================================================================================================================
    # CLASS INITIALISATION / BASIC BUILD
    # =============================================================================================================================
    
    # the initialisation has been split into two where the basic build i.e. passing of variables requires a dedicated method
    # this is so the class can be quickly initialised to use the standardise/stip company name functions
    
    # initialise class and build dictionaries and lists
    def __init__(self):

        # dictionaries and lists
        self.company_suffixes_dict = COMPANY_SUFFIXES_DICT
        self.company_suffixes_list = convert_dict_to_list(self.company_suffixes_dict)               
 
        # optional class variables
        self.subset_fields = None
        self.erase_text = None
        self.primary_blank_subs = None
        self.secondary_matches = []
        
        # alternative names for lookup and match keys and columns -- prefixes with lookup and match in the results
        self.temp_lookup_key = None
        self.temp_lookup_column = None
        self.temp_match_key = None
        self.temp_match_column = None
        
        # the results are created as frames in the class for development purposes -- so they can be repeatedly referred to from inside and outside the class
        self.initial_results = None        
        self.matched_results = None
        self.final_key_map = None
        self.connected_components = None
        self.new_lookup_data = None
        self.match_ref_data = None
        self.temp_additional_results = None
    
    # build class and define other parameters to enable primary matching
    def build_class(self
                 , lookup_frame, lookup_key, lookup_column
                 , match_frame, match_key, match_column
                 , score_cutoff
                 , **kwargs):
            
        # check if the lookup and match frames are the same (meaning it is a de-duping process)
        # this means cleansing only needs to be done to one frame -- a big time-saver
        if lookup_frame.values.base is match_frame.values.base:
            self.duplicate_frames = True
        else:
            self.duplicate_frames = False
        
        # make copies of the frames sent so the originals remain unchanged following cleansing
        # potentially work on the originals if memory becomes an issue -- but it is not a problem right now
        if self.duplicate_frames == True:
            self.lookup_frame = lookup_frame.copy()
            self.match_frame = self.lookup_frame         
        else:
            self.lookup_frame = lookup_frame.copy()
            self.match_frame = match_frame.copy()
        
        # set the lookup and match keys and columns
        self.lookup_key = lookup_key
        self.match_key = match_key
        self.lookup_column = lookup_column
        self.match_column = match_column
        
        # ensure the keys are the indexes
        if self.lookup_frame.index.name != self.lookup_key: self.lookup_frame = self.lookup_frame.set_index(lookup_key)
        if self.match_frame.index.name != self.match_key: self.match_frame = self.match_frame.set_index(match_key)
        
        # format the lookup and match frame indexes i.e. keys as strings
        self.lookup_frame.index = self.lookup_frame.index.astype(str)
        self.match_frame.index = self.match_frame.index.astype(str)
        
        # score cutoff
        self.score_cutoff = score_cutoff
        
        # unpack **kwargs
        self.primary_field_type = None
        self.match_function = 'fuzz.ratio' 
        self.remove_spaces = False
        self.log_path = None
        for key, value in kwargs.items():
            if key == 'primary_field_type':
                self.primary_field_type = value
            if key == 'match_function':
                self.match_function = value      
            if key == 'remove_spaces':
                self.remove_spaces = value
            if key == 'log_path':
                self.log_path = value
     
    # =============================================================================================================================
    # =============================================================================================================================
    # =============================================================================================================================
      
    # =============================================================================================================================
    # FUNCTIONS THAT NEED TO BE VECTORISED TO USE ON A FRAME COLUMN AND REFERENCE A LIST AT THE SAME TIME
    # =============================================================================================================================
        
    def standardise_company_name(self, company_name):
    # standardises company name using the company suffixes dictionary
        my_name = company_name
        # my_suffixes = self.company_suffixes_list()    
        # my_suffixes = COMPANY_SUFFIXES_LIST
        my_suffixes = self.company_suffixes_list
        l = len(company_name)
        for ms in my_suffixes:
            m = len(ms[0])
            if my_name[l - m - 1:] == ' ' + ms[0]:            
                my_name = my_name.replace(ms[0], ms[1])
        return my_name

    def strip_company_name(self, company_name):
    # removes company suffixes from the end of company name
        my_name = company_name
        # my_suffixes = self.company_suffixes_list()    
        # my_suffixes = COMPANY_SUFFIXES_LIST
        my_suffixes = self.company_suffixes_list
        l = len(company_name)
        for ms in my_suffixes:
            m = len(ms[0])
            if my_name[l - m - 1:] == ' ' + ms[0]:            
                my_name = my_name.replace(' ' + ms[0], '')
        return my_name    

    def strip_domain_suffix(self, domain_name):
    # keeps stripping suffixes from the domain until there are none left -- mydomain.com.fr would have .fr removed and then .com removed leaving just mydomain
    
        my_domain = domain_name
        my_suffixes = DOMAIN_SUFFIXES_LIST
        
        l = len(my_domain)
    
        bol_stop = False      
        i = 0
        
        # iterate through the suffixes list adding 1 to the counter each time a replacement has been made
        # if no replacements are made during an iteration the code will exit the loop (because the counter will remain unchanged)
        while bol_stop == False:
            j = i
            for ms in my_suffixes:
                m = len(ms)
                if my_domain[l - m:] == ms:            
                    # my_domain = my_domain.replace(ms, '')
                    my_domain = my_domain[:l - m]
                    l = len(my_domain)
                    i = i + 1
            if i == j:
                bol_stop = True
                   
        return my_domain
    
    def remove_from_start_b(self, my_string):
        bol_stop = False
        while bol_stop == False:
            # check the length inside the while loop in case it is zero after the characters have been removed
            if len(my_string) == 0:
                break
            my_char = my_string[0]
            if my_char in self.temp_char_list:
                my_string = my_string.lstrip(my_char)
            else:
                bol_stop = True
        return my_string
    
    def remove_from_end_b(self, my_string):
        bol_stop = False
        while bol_stop == False:
            # check the length inside the while loop in case it is zero after the characters have been removed
            if len(my_string) == 0:
                break
            my_char = my_string[-1]
            if my_char in self.temp_char_list:
                my_string = my_string.rstrip(my_char)
            else:
                bol_stop = True
        return my_string

    # =============================================================================================================================
    # =============================================================================================================================
    # =============================================================================================================================

    # =============================================================================================================================
    # CLASS METHODS
    # =============================================================================================================================

    def add_secondary_match(self, lookup_column, match_column, **kwargs):
    # optionally adds additional fields for secondary matches to the class after the initial class was created
        
        # set defaults
        field_type = None
        duplicate_suffix = ''
        match_function = 'fuzz.ratio'
        remove_spaces = False
        cleanse_data = False
        secondary_match_name = ''
        
        # unpack kwargs and overwrite defaults if applicable
        for key, value in kwargs.items():
            if key == 'field_type':
                field_type = value
            if key == 'duplicate_suffix':
                duplicate_suffix = value 
            if key == 'match_function':
                match_function = value
            if key == 'remove_spaces':
                remove_spaces = value
            if key == 'cleanse_data':
                cleanse_data = value
            if key == 'secondary_match_name':
                secondary_match_name = value
                
        # add secondary match to master list with all options explicitly defined
        self.secondary_matches.append((lookup_column, match_column, field_type, duplicate_suffix, match_function, remove_spaces, secondary_match_name))
        
        # create duplicate columns if applicable -- a duplicate suffix has been defined AND a field type has (so cleansing needs to be done)
        # a duplicate suffix alone does not require duplicate colunms because it will only yield an additional score for existing columns
        # if duplicate_suffix != None:
        if len(duplicate_suffix) > 0 and field_type != None:
            self.lookup_frame[lookup_column + duplicate_suffix] = self.lookup_frame[lookup_column]
            self.match_frame[match_column + duplicate_suffix] = self.match_frame[match_column]

        if cleanse_data == True:
            # cleanse the column in the lookup frame
            self.cleanse_engine(self.lookup_frame, lookup_column + duplicate_suffix, field_type, remove_spaces, 'secondary', 'lookup')
            if self.duplicate_frames == False:
                # cleanse the data in the match frame (but only if the match frame is different from the lookup frame)
                self.cleanse_engine(self.match_frame, match_column + duplicate_suffix, field_type, remove_spaces, 'secondary', 'match')
            else:
                # otherwise just make the match frame the same as the lookup frame (to ensure they stay the same)
                self.match_frame = self.lookup_frame
        
    def clear_secondary_matches(self):
    # clears out the list of secondary matches -- consider adding code to remove the columns too if secondary matching have already been performed
        
        self.secondary_matches = []
    
    def cleanse_data(self, cleanse_type):
    # wrapper to call the main cleansing engine
    
        # cleanse primary lookup and match fields defined when the class was created
        if cleanse_type == 'primary':
            self.cleanse_engine(self.lookup_frame, self.lookup_column, self.primary_field_type, self.remove_spaces, cleanse_type, 'lookup')
            if self.duplicate_frames == False:
                self.cleanse_engine(self.match_frame, self.match_column, self.primary_field_type, self.remove_spaces, cleanse_type, 'match')
            else:
                self.match_frame = self.lookup_frame
            
            if self.subset_fields != None:
                self.cleanse_engine(self.lookup_frame, self.subset_fields[0], None, self.remove_spaces, cleanse_type, 'lookup')
                if self.duplicate_frames == False:
                    self.cleanse_engine(self.match_frame, self.subset_fields[1], None, self.remove_spaces, cleanse_type, 'match')
                else:
                    self.match_frame = self.lookup_frame
                
        # cleanse secondary match fields added after the class was created
        if cleanse_type == 'secondary':
            for sm in self.secondary_matches:
                self.cleanse_engine(self.lookup_frame, sm[0] + sm[3], sm[2], sm[5], cleanse_type, 'lookup')
                if self.duplicate_frames == False:
                    self.cleanse_engine(self.match_frame, sm[1] + sm[3], sm[2], sm[5], cleanse_type, 'match')
                else:
                    self.match_frame = self.lookup_frame       
    
    def cleanse_engine(self, frame_name, column_name, field_type, remove_spaces, cleanse_type, frame_type):            
    # mutiple types of cleansing performed here as defined when the class was created and any secondary matches added
    
        # *** THIS WAS WRITTEN IN A RUSH AND NEEDS TO BE BROKEN INTO DIFFERENT FUCTIONS AND GENERALLY OPTIMISED ***
        
        # import modules
        import re
        
        # import objects
        from unidecode import unidecode
        
        # update log file
        write_to_log(self.log_path,'cleanse data process started: ' + column_name)
        
        # *** GENERIC CLEANSING FOR ALL STRINGS ***        

        # replace nas with empty string
        frame_name[column_name] = frame_name[column_name].fillna('')
        
        # make strings lowercase and remove leading and trailing white space
        frame_name[column_name] = frame_name[column_name].str.lower().str.strip()
        
        # replace multiple spaces with one space
        # to do this use the split function which uses space as a delimiter and treats multiple spaces as one
        # then use the join function to put the strings back together with a space as the separator
        vec_fun = np.vectorize(single_space)
        frame_name[column_name] = vec_fun(frame_name[column_name])

        # remove duplicate punctuation -- but leave one behind -- so "hello!!! world??" would become "hello! world?"
        vec_fun = np.vectorize(re.sub)
        frame_name[column_name] = vec_fun("([.,_&@#!?:'\-])\\1+", "\\1", frame_name[column_name])
        
        # get rid of accents -- there are a few methods -- but this uses the unidecode module which is pretty neat
        vec_fun = np.vectorize(unidecode)
        frame_name[column_name] = vec_fun(frame_name[column_name])
             
        # *** OPTIONAL -- REMOVE ALL SPACES -- USEFUL FOR POST CODES ***
        if remove_spaces == True:
            vec_fun = np.vectorize(my_replace)
            frame_name[column_name] = vec_fun(frame_name[column_name], ' ', '')
        
        # *** OPTIONAL -- COMPANY NAME SPECIFIC CLEANSING ***

        if field_type != None and field_type[:12] == 'company_name':
        
            # replace comma and underscore with space (sometimes used instead of a space to separate words)
            vec_fun = np.vectorize(my_replace)
            frame_name[column_name] = vec_fun(frame_name[column_name], ',', ' ')
            vec_fun = np.vectorize(my_replace)
            frame_name[column_name] = vec_fun(frame_name[column_name], '_', ' ')                        
            # frame_name[column_name] = frame_name.apply(lambda x: re.sub('[_,]', ' ', x[column_name]), axis=1)
            # ^^^ need to test doing this with one line of code as per the above at some point -- BUT A VECTORISED VERSION

            # remove punctuation unwanted anywhere in the string (comma and underscore left in in case the above changes)
            vec_fun = np.vectorize(re.sub)
            frame_name[column_name] = vec_fun('["`*£$%^()_,;:<>~{}=«»\'|\[\]]', '', frame_name[column_name])
            
            # replace multiple spaces with one space again (if there are now double spaces following the above)   
            vec_fun = np.vectorize(single_space)
            frame_name[column_name] = vec_fun(frame_name[column_name])
        
            # remove leading and trailing white space again (if there is now a space at the start or end following the above)
            frame_name[column_name] = frame_name[column_name].str.strip()
        
            # remove punctuation unwanted at the start of the string (send the function a list)
            # include space at the end of the list in case the string starts with a space once the other characters have been removed
            vec_fun = np.vectorize(self.remove_from_start_b)
            self.temp_char_list = ['+','/', '&', '!', '?', '.', '-', ' ']
            frame_name[column_name] = vec_fun(frame_name[column_name])            
            
            # remove punctuation unwanted at the end of the string (send the function a list)
            # include space at the end the list in case the string ends with a space once the other characters have been removed
            vec_fun = np.vectorize(self.remove_from_end_b)
            self.temp_char_list = ['/', '&', '#', '@', '-', ' ']
            frame_name[column_name] = vec_fun(frame_name[column_name])

            # erase strings that are just one repeated character as defined e.g. "0000" would be replaced by ""
            # some have already been covered by the start removal function but have been left in here in case that changes
            vec_fun = np.vectorize(trunc_reps)
            frame_name[column_name] = vec_fun(frame_name[column_name], '?!0-.')

            # standardise company name using suffixes dictionary e.g. change limited, ltd. and l.t.d. to ltd
            vec_fun = np.vectorize(self.standardise_company_name)
            frame_name[column_name] = vec_fun(frame_name[column_name])
            
            # *** OPTIONAL -- STRIP LEGAL TERMS FROM END OF COMPANY NAME  -- USEFUL FOR SECONDARY MATCHING ***
            if field_type[len(field_type) - 8:] == 'stripped':
                vec_fun = np.vectorize(self.strip_company_name)
                frame_name[column_name] = vec_fun(frame_name[column_name])
            
        # *** OPTIONAL ADDRESS SPECIFIC CLEANSING ***

        # this can be applied to any address field e.g. first line, city etc.
        if field_type == 'address':
            
            # remove punctuation unwanted anywhere in the string
            vec_fun = np.vectorize(re.sub)
            frame_name[column_name] = vec_fun('["+£$%^()_,;:<>~{}=!?*#@&«»|\[\]]', '', frame_name[column_name])

            # replace multiple spaces with one space again (if there are now double spaces following the above)
            vec_fun = np.vectorize(single_space)
            frame_name[column_name] = vec_fun(frame_name[column_name])
            
            # strip it again in case the are any spaces at the start or end after the other characters have been removed
            frame_name[column_name] = frame_name[column_name].str.lower().str.strip()
        
        # *** OPTIONAL DOMAIN SPECIFIC CLEANSING ***
        
        # remove domain suffixes e.g. to make mydomain.com and mydomain.net a match -- only recommended for seconday matching i.e. to validate a potential match
        if field_type == 'domain_stripped':
            vec_fun = np.vectorize(self.strip_domain_suffix)
            frame_name[column_name] = vec_fun(frame_name[column_name])
        
        # *** ADDITIONAL PRIMARY CLEANSING ***
        
        # if any primary match fields are blank following cleansing then replace them as appropriate
        if cleanse_type == 'primary':
            
            # first erase any text if required
            if self.erase_text != None:
                for et in self.erase_text:
                    vec_fun = np.vectorize(my_replace)
                    frame_name[column_name] = vec_fun(frame_name[column_name], et, '')
            
            # if replacement fields have been defined
            if self.primary_blank_subs != None:
                if frame_type == 'lookup':
                    my_col = self.primary_blank_subs[0]
                if frame_type == 'match':
                    my_col = self.primary_blank_subs[1]  
                vec_fun = np.vectorize(sub_text)
                frame_name[column_name] = vec_fun(frame_name[my_col], frame_name[column_name])

            # now replace any remaining blanks with the key (so blank strings aren't matched)
            # can't refer to the index column in the function for some reason so copy it to a regular column
            # need to revisit this in the future when there's more time but for now this works
            frame_name['temp_key'] = frame_name.index
            vec_fun = np.vectorize(sub_text)
            frame_name[column_name] = vec_fun('temp-' + frame_name['temp_key'], frame_name[column_name])            
            frame_name = frame_name.drop(['temp_key'], axis=1, inplace=True)
        
        write_to_log(self.log_path,'cleanse data process finished: ' + column_name)
    
    def cleanse_primary_fields(self):
        self.cleanse_data('primary')
    
    def get_primary_matches(self):
    # wrapper for primary matches that optinally calls the main matching function in subsets (if defined)
        
        # reset indexes to facilitate column renaming and dictionary conversion
        self.lookup_frame = self.lookup_frame.reset_index()
        self.match_frame = self.match_frame.reset_index()
        
        # use subset fields to restrict the iteration to subsets of data where fields are assumed to be 100% correct
        # typically country code for customer data -- this will make the matching process SIGNIFICANTLY faster
        
        # if subset fields have been defined:
        if self.subset_fields != None:
            
            # create an empty dictionary to put the results in
            results_dict = {}
            
            # put the subset values in a list using the lookup frame | filter out NoneTypes | sort the list
            subset_list = (self.lookup_frame[self.subset_fields[0]].unique()).tolist()
            subset_list = list(filter(lambda x: x != None, subset_list))
            subset_list.sort()
            
            # iterate through the subset list
            for ss in subset_list:
                # create frames limited to subset field
                lookup_temp = self.lookup_frame[self.lookup_frame[self.subset_fields[0]] == ss]
                match_temp = self.match_frame[self.match_frame[self.subset_fields[1]] == ss]
                # do the matching and put the results in the dictionary
                temp_dict = self.generate_matches(lookup_temp, match_temp, ss)
                results_dict.update(temp_dict)
        
            # now delete temporary objects to save memory
            del lookup_temp
            del match_temp
            del temp_dict
        
        # if subset fields have not been defined:
        else:
            results_dict = self.generate_matches(self.lookup_frame, self.match_frame, None)
        
        # call the function that converts the results dictionary into a frame
        self.build_primary_results(results_dict)
        
        # now delete the results dictionary to save memory
        del results_dict
        
        # put the original indexes back in place
        self.lookup_frame = self.lookup_frame.set_index(self.lookup_key)
        self.match_frame = self.match_frame.set_index(self.match_key)

    def generate_matches(self, lookup_temp, match_temp, subset_name):
    # iterates through a lookup dictionary and compares each string to a match dictionary
        
        # import objects
        from rapidfuzz import process, fuzz
        
        # tell the log file which subset is being matched if applicable
        if self.subset_fields == None:
            write_to_log(self.log_path,'match process started')
        else:
            write_to_log(self.log_path, 'subset match process started: ' + subset_name)
        
        # convert the frames to dictionaries so the keys can be used in the iteration     
        lookup_dict = lookup_temp.set_index(self.lookup_key).to_dict()[self.lookup_column]
        match_dict = match_temp.set_index(self.match_key).to_dict()[self.match_column]
        
        # set the return limit to the length of the match dictionary
        my_limit = len(match_dict)
        
        # create a blank dictionary to populate with the match results
        # *** a dictionary is being used because it can handle the keys in the match process in the iteration ***
        temp_dict = {}

        # define match function (as per class initialisation)                        
        match_types = {
                        'fuzz.ratio': fuzz.ratio
                        , 'fuzz.token_set_ratio': fuzz.token_set_ratio
                        }
        my_match_function = match_types[self.match_function]
        
        # iterate through the lookup dictionary and match each record against the match dictionary
        for (my_key, my_text) in lookup_dict.items():
            my_match = process.extract(my_text, match_dict, processor=None, score_cutoff=self.score_cutoff, scorer=my_match_function, limit = my_limit)
            if my_match:
                temp_dict[my_key] = my_match
        
        # now delete the dictionaries to save memory
        del lookup_dict
        del match_dict
        
        # update log file
        if self.subset_fields == None:
            write_to_log(self.log_path, 'match process finished')
        else:
            write_to_log(self.log_path, 'subset match process finsihed: ' + subset_name)
        
        return temp_dict
        
    def build_primary_results(self, results_dict):        
    # ues the results dicitonary to put the initial results of primary matches into a frame
            
        # update log file    
        write_to_log(self.log_path, 'build output process started')
        
        # create an empty list to populate
        temp_list = []
        # iterate through the dictioary items
        for a, b in results_dict.items():
            # then iterate through each dictionary item (in this case tuple)
            for c in b:
                # append the tuple items into the list with the key cascaded across them
                temp_list.append((a, c[2], c[1]))
        # put the list into a frame
        results_frame = pd.DataFrame(temp_list, columns=['results_lookup_key', 'results_match_key', 'results_match_score'])

        # now delete the temporary list to save memory
        del temp_list

        # define new names to differentiate between lookup and match columns
        self.temp_lookup_key = 'lookup_' + self.lookup_key
        self.temp_lookup_column = 'lookup_' + self.lookup_column
        self.temp_match_key = 'match_' + self.match_key
        self.temp_match_column = 'match_' + self.match_column 
     
        # merge the lookup frame with the results frame | removed unwanted columns | rename columns
        self.initial_results = pd.merge(self.lookup_frame, results_frame, left_on=self.lookup_key, right_on='results_lookup_key', how='left')      
        self.initial_results = self.initial_results[[self.lookup_key, self.lookup_column,'results_match_key','results_match_score']]
        self.initial_results = self.initial_results.rename(columns = {self.lookup_key: self.temp_lookup_key, self.lookup_column: self.temp_lookup_column})
        
        # merge the new frame with the match frame | removed unwanted columns | rename columns
        self.initial_results = pd.merge(self.initial_results, self.match_frame, left_on='results_match_key', right_on=self.match_key, how='left')
        self.initial_results = self.initial_results[[self.temp_lookup_key, 'results_match_key', self.temp_lookup_column, self.match_column,'results_match_score']]        
        self.initial_results = self.initial_results.rename(columns = {self.temp_lookup_key: 'lookup_key', 'results_match_key': 'match_key', self.match_column: self.temp_match_column, 'results_match_score': self.lookup_column + '_match_score'})

        # print(datetime.datetime.now().strftime("%H:%M:%S"), 'build output process finished')
        write_to_log(self.log_path, 'build output process finished')

    def integrate_additional_primary_matches(self, additional_primary_results):
        
        # import numpy as np
        
        # update log file
        write_to_log(self.log_path,'started integrating additional primary matches')

        # work out which records are not already in the initial matches -- this method is much simpler than messing with the indexes on the results frame
        mask = (additional_primary_results['lookup_key'] + '_' + additional_primary_results['match_key']).isin(self.initial_results['lookup_key'] + '_' + self.initial_results['match_key'])
        append_records = additional_primary_results[~mask]
        append_records = append_records.reset_index(drop=True)
        write_to_log(self.log_path, str(len(append_records)) + ' additional primary match records identified')
        
        # integrate additional results if there were any
        if len(append_records) > 0:
            
            # append the new records to the initial results
            self.initial_results = self.initial_results.append(append_records).reset_index(drop=True)
            
            # *** REALY important -- sort the frame by lookup key, with the record where the key matches to itself first, then the rest by descending match score ***
            # this is the same sort order as the initial results after the primary match iteration -- and is CRITICAL to creating the final key map and indirect linking
            self.initial_results['temp_sort'] = np.where(self.initial_results['lookup_key'] == self.initial_results['match_key'], 1, 2)
            # self.initial_results.sort_values(['lookup_key', 'temp_sort', 'customer_name_match_score'], ascending=[True, True, False], inplace=True)
            self.initial_results.sort_values(['lookup_key', 'temp_sort', self.lookup_column + '_match_score'], ascending=[True, True, False], inplace=True)
            self.initial_results = self.initial_results.drop(['temp_sort'], axis=1)
            self.initial_results = self.initial_results.reset_index(drop=True)
        
        # *** potential enhancement ***
        # could use a sorted tuple comprising the lookup and match keys for the deduping -- with a further deduping stage after the indirect linking
        # then there would be no dependency on sort order -- but this is appears to be working following rigourous testing -- so no panic
        # this news just in: replace this stage with graph theory that identifies connected subgraphs in an undirected graph as an enhancment at some point
        
        # update log file
        write_to_log(self.log_path,'finshed integrating additional primary matches')

    def temp_match(self, match_function, my_string_one, my_string_two):
        
        # from rapidfuzz import fuzz
        
        # either: set the result as none if one or both of the strings in empty
        if len(str(my_string_one)) == 0 or len(str(my_string_two)) == 0:
            my_result = None
        # or: get a match score for the two strings
        else:
            # my_result = match_function(my_string_one, my_string_two)
            my_result = match_function(str(my_string_one), str(my_string_two))
            
        return my_result
                
    def get_secondary_matches(self):
    # adds secondary match fields to the initial results frame and matches them
        
        # import numpy as np
    
        # import objects
        from rapidfuzz import fuzz

        # create a match function and vectorise it -- faster than applying a labmda function to a frame
        vec_fun = np.vectorize(self.temp_match)
        
        # iterate through the list of seondary matches
        for sm in self.secondary_matches:
            
            # print(datetime.datetime.now().strftime("%H:%M:%S"), 'secondary match process started: ' + sm[0] + sm[3] + ' to ' + sm[1] + sm[3])
            write_to_log(self.log_path, 'secondary match process started: ' + sm[0] + sm[3] + ' to ' + sm[1] + sm[3])

            # define match function (as per secondary matches list)                        
            match_types = {
                            'fuzz.ratio': fuzz.ratio
                            , 'fuzz.token_set_ratio': fuzz.token_set_ratio
                            , 'set_intersection_match_score': set_intersection_match_score
                            }
            match_function = match_types[sm[4]]
            
            # if a duplicate suffix has been defined but no field type has (so no cleansing has been done) then the matching can be done on the columns already added
            if len(sm[3]) > 0 and sm[2] == None:
                
                 # do the matching using the function defined above
                self.initial_results[sm[0] + sm[3] + '_match_score'] = vec_fun(match_function, self.initial_results['lookup_' + sm[0]], self.initial_results['match_' + sm[1]])               

            else:            

                # convert the lookup and match frames into dictionaries for fast mapping to frame
                lookup_dict = self.lookup_frame[[sm[0] + sm[3]]].to_dict()
                match_dict = self.match_frame[[sm[1] + sm[3]]].to_dict()
                # ^^^ field defined as list even though there is only one because the code below is desinged to use a dictionary with multiple fields
                # this is from when the entre frame was converted to a dictionary as opposed to only the column needed
    
                # add the secondary match columns by getting the values from the dicitonary above
                self.initial_results['lookup_' + sm[0] + sm[3]] = self.initial_results['lookup_key'].map(lookup_dict[sm[0] + sm[3]])
                self.initial_results['match_' + sm[1] + sm[3]] = self.initial_results['match_key'].map(match_dict[sm[1] + sm[3]])
                
                # now delete the dictionaries to save memory
                del lookup_dict
                del match_dict
                            
                # do the matching using the function defined above
                self.initial_results[sm[0] + sm[3] + '_match_score'] = vec_fun(match_function, self.initial_results['lookup_' + sm[0] + sm[3]], self.initial_results['match_' + sm[1] + sm[3]])
                        
            # print(datetime.datetime.now().strftime("%H:%M:%S"), 'secondary match process finished: ' + sm[0] + sm[3] + ' to ' + sm[1] + sm[3])
            write_to_log(self.log_path, 'secondary match process finished: ' + sm[0] + sm[3] + ' to ' + sm[1] + sm[3])

    def create_key_map(self):
    # creates a single deduped frame of matched results to get from the lookup key to a new match id
        
        # update log file
        write_to_log(self.log_path,'create key map process started')
        
        # remove duplicte match keys (keep the first ones and drop all subsequent ones)
        # this will make the first lookup key the master that all the others get mapped to
        # so the dropped records will be those already matched to the master matching to themselves elsewhere
        # matches to matches of matches will be grouped together later in this function        
        no_dups = self.matched_results.drop_duplicates('match_key', keep='first')
        no_dups = no_dups[['match_key', 'lookup_key']]
        no_dups.columns = ['old_key','new_key']         

# =============================================================================
#         # *** sandbox -- leave commented out ***
#         # the droppping of duplicates is dependent upon sort order -- grouped by key, with the key matching to itself first, then the rest by descending match score
#         # so adding external additional primary records to the initial results frame means it has to be sorted again (which is currently being done)
#         # it is worth investigating dropping duplicates based on a sorted tuple of the lookup and match keys to avoid a dependency on sort order
#         # but the indirect linking would then take longer and another de-duping stage would be required -- so since it works OK now maybe it's best left as it is
#         no_dups = self.matched_results
#         no_dups['key_tuple'] = list(zip(no_dups['lookup_key'], no_dups['match_key']))
#         no_dups['sorted_tuple'] = [tuple(sorted(x)) for x in no_dups['key_tuple']]
#         no_dups = no_dups.drop_duplicates('sorted_tuple', keep='first')
#         # *** another de-duping stage would be required after the indirect linking ***
# =============================================================================
               
        # join the match output to the original reference data
        map_key_temp = pd.merge(self.lookup_frame, no_dups, left_on=self.lookup_key, right_on='old_key', how='inner')
        # map_key_temp = pd.merge(self.match_frame, no_dups, left_on=self.match_key, right_on='old_key', how='inner')
        
        # choose columns and set names up for iteration
        map_key_temp = map_key_temp[['old_key', 'new_key']]
        map_key_temp.columns = ['old_key','new_key_0']
        
        # *** scenario ***
        # customer A matches customer B *AND* customer B matches customer C *BUT* customer A does NOT match customer C
        # e.g. "my company inc" matches to "my company" which matches to "my company sys" which does *not* match to "my company inc"
        # and we want all three of them to be flagged as the same company
        
        # *** solution ***
        # select A as the master and map B to it | look up C and map it to B | lookup B and map it to A
        # keep looking up the new key in the dictionary and adding the result as a new column
        # then when the last 2 columns are the same it means there is no more remapping to be done
        
        # *** method ***
        # look the new key up in the dictionary and see if the result is itself
        # if it is that means the master key has been found
        # if it is not that means the key can be mapped to another key
        # keep doing this until the master key has been found for all records
        
        # create a dictionary to map the old keys to the new keys
        map_key_dict = map_key_temp.set_index('old_key').to_dict()['new_key_0']
        
        # set variable to stop when mapping has finished to false and counter to 1
        bol_stop = False
        i = 1
        
        # do a loop to add columns to the frame
        while bol_stop == False:
            
            # create dynamic headers based on i
            new_hdr = 'new_key' + '_' + str(i)
            old_hdr = 'new_key' + '_' + str(i - 1)
            
            # look the latest key up in the dictionary to remap it
            map_key_temp[new_hdr] = map_key_temp[old_hdr].map(map_key_dict)
            
            # check how many records there are where the lastest key does not equal the previous key
            # if the result is greater than zero then carry on remapping otherwise stop
            if len(map_key_temp[map_key_temp[old_hdr] != map_key_temp[new_hdr]]) == 0:
                bol_stop = True
            
            # add one to the counter
            i = i + 1
        
        # create the final frame and remove the suffix from the final key column
        self.final_key_map = map_key_temp[['old_key', new_hdr]]
        self.final_key_map.columns = ['lookup_key', 'match_key']
        
        # sort the frame by new key to group all the duplicates together
        self.final_key_map = self.final_key_map.sort_values(by = ['match_key','lookup_key'], ascending = [True, True], na_position = 'last').reset_index(drop=True)
        
        # add a brand new key based on the match key
        # self.final_key_map['match_id'] = self.final_key_map['match_key'].ne(self.final_key_map['match_key'].shift()).cumsum()
        self.final_key_map['match_id'] = self.final_key_map['match_key'].astype('category').cat.codes.add(1)
        # change the id to int32 if it isn't already
        self.final_key_map = self.final_key_map.astype({'match_id': np.int32})
        
        # make lookup key the index
        self.final_key_map = self.final_key_map.set_index(['lookup_key'])
        
        # update log file
        write_to_log(self.log_path,'create key map process finished')

    def connect_components(self, **kwargs):
    
        import networkx as nx
        
        write_to_log(self.log_path, 'started connecting components')
        
        self.dedupe_data = False
        for key, value in kwargs.items():
            if key == 'dedupe_data':
                self.dedupe_data = value
        
        data_frame = self.matched_results.copy()
        
        if self.dedupe_data == True:
            
            mask = data_frame['lookup_key'] == data_frame['match_key']
            data_frame = data_frame[~mask]
            
            data_frame['key_tuple'] = list(zip(data_frame['lookup_key'], data_frame['match_key']))
            data_frame['sorted_tuple'] = [tuple(sorted(x)) for x in data_frame['key_tuple']]
            data_frame = data_frame.drop_duplicates('sorted_tuple', keep='first')
        
        link_list = list(zip(data_frame['lookup_key'], data_frame['match_key']))
        
        G = nx.Graph()
        
        for ll in link_list:
            G.add_edge(ll[0], ll[1])
        
        # connected_components = []    
        # for cc in nx.connected_components(G):
        #     connected_components.append(cc)
        
        # key_group_list = []
        # for cc in connected_components:
        #     my_index = connected_components.index(cc)
        #     for c in connected_components[my_index]:
        #         key_group_list.append((c, my_index))
        
        # populate the key group list during the connected component iteration -- a separate iteration afterwards would take a LONG time
        key_group_list = []
        i = 1 
        for cc in nx.connected_components(G):
            for c in cc:   
                key_group_list.append((c, i))
            i = i + 1
                
        self.connected_components = pd.DataFrame(data=key_group_list, columns=['lookup_key', 'match_id'])
        self.connected_components = self.connected_components.set_index(['lookup_key'])
        
        write_to_log(self.log_path, 'finished connecting components')
        
    def get_new_lookup_data(self, lookup_source):
    # takes the original lookup frame and adds the match id as a new column
    
        # update log file
        write_to_log(self.log_path,'get new lookup data process started')
        
        # determine if final key map or connected componets should be used
        if lookup_source == 'final_key_map':
            my_frame = self.final_key_map
            my_cols = ['match_id', 'match_key']
        elif lookup_source == 'connected_components':
            my_frame = self.connected_components
            my_cols = ['match_id']
        
        # merge the lookup frame with the source frame defined above
        self.new_lookup_data = self.lookup_frame.reset_index().merge(my_frame.reset_index(), left_on=self.lookup_key, right_on='lookup_key', how='left')
        # self.new_lookup_data = self.match_frame.reset_index().merge(my_frame.reset_index(), left_on=self.match_key, right_on='lookup_key', how='left')
        
        # move the new columns to after the first column -- put them in reverse order because the next one will get inserted in front of the previous one
        for mc in my_cols:
            my_col = self.new_lookup_data.pop(mc)
            self.new_lookup_data.insert(1, mc, my_col)
        
        # drop unwanted columns | reinstate original column names | reinstate original index
        self.new_lookup_data = self.new_lookup_data.drop('lookup_key', axis=1)
        self.new_lookup_data = self.new_lookup_data.rename(columns={self.temp_lookup_key: self.lookup_key, self.temp_lookup_column: self.lookup_column})
        self.new_lookup_data = self.new_lookup_data.set_index(self.lookup_key)

        # delete duplicate columns if applicable (that were added to the class after it was created)       
        for sm in self.secondary_matches:
            if len(sm[3]) > 0 and sm[2] != None:
                self.new_lookup_data = self.new_lookup_data.drop(sm[0] + sm[3], axis=1)
        
        # update log file
        write_to_log(self.log_path,'get new lookup data process finished')

    def aggregate_match_data(self):
    # creates reference data for the match ids in final key map
    
        # update log file
        write_to_log(self.log_path,'aggregate match data process started')
    
        # *** TEMPORARY CODE FOR NOW JUST TO PICK THE FIRST ONE IN THE LIST ***
        
        def cust_agg(x):
            # y = x.tolist()
            y = list(dict.fromkeys(x.tolist()))
            y = list(i for i in y if i)
            if len(y) == 0:
                z = ''
            else:
                z = y[0]
            return z
    
        # drop match key and move match id to the front (it will form the basis of the group by)
        my_frame = self.new_lookup_data.copy().reset_index()
        if 'match_key' in my_frame.columns:
            my_frame = my_frame.drop('match_key', axis=1)
        # my_frame = my_frame.drop(['match_key', self.lookup_key], axis=1)
        my_pop = my_frame.pop('match_id')
        my_frame.insert(0, 'match_id', my_pop)
        
        # group by match id and aggreate all other columns to lists
        # self.match_ref_data = my_frame.groupby('match_id').agg(lambda x: x.tolist())
        self.match_ref_data = my_frame.groupby('match_id').agg(lambda x: cust_agg(x))
        
        # # add a primary match field using the first value in each list in the lookup column
        # self.match_ref_data = self.match_ref_data.copy()
        # self.match_ref_data['primary_' + self.lookup_column] = self.match_ref_data.apply(lambda x: x[self.lookup_column][0], axis=1)
        
        # # and finally move the new primary column to the front
        # my_pop = self.match_ref_data.pop('primary_' + self.lookup_column)
        # self.match_ref_data.insert(0, 'primary_' + self.lookup_column, my_pop)
        
        # update log file
        write_to_log(self.log_path,'aggregate match data process finished')
        
    def get_additional_join_matches(self, secondary_match_name, **kwargs):
    # get matches by joining a pair of secondary match fields to supplement the initial primary matches
    # they can then be integrated into the primary matches using the class function integrate_additional_primary_matches
    
        # leave commented out (testing only)
        # secondary_match_name = 'domain_stripped'
            
        # define variables
        log_path = self.log_path
        initial_results = self.initial_results
        subset_fields = self.subset_fields    
        # lookup_key = self.lookup_key
        lookup_name = self.lookup_column
        lookup_subset = self.subset_fields[0]    
        # match_key = self.match_key
        match_name = self.match_column
        match_subset = self.subset_fields[1]
    
        # tell the log file what's happening
        write_to_log(log_path, 'function ' + current_method_name() + ' started')
    
        # set defaults
        explode_column = False
        match_threshold = 0
    
        # unpack kwargs and overwrite defaults if applicable
        for key, value in kwargs.items():
            if key == 'explode_column':
                explode_column = value
            if key == 'match_threshold':
                match_threshold = value
    
        # get the names of the respective join fields as defined in the class's secondary matches (the list of tuples)
        for i, sm in enumerate(self.secondary_matches):
            if sm[6] == secondary_match_name:
                lookup_join = sm[0] + sm[3]
                match_join = sm[1] + sm[3] 
        
        # set frames to merge -- filter for only necessary columns -- means column name changes won't affect originals
        left_frame = self.lookup_frame.copy()[[lookup_name, lookup_join, lookup_subset]]
        right_frame = self.match_frame.copy()[[match_name, match_join, match_subset]]
        
        # explode the join field if applicable
        if explode_column == True: 
            left_frame = explode_frame_list_column(left_frame, lookup_join)
            right_frame = explode_frame_list_column(right_frame, match_join)
                    
        # define unwanted values
        unwanted_values = ['unwanteddomain.com']
        
        # give name variables appropriate prefixes so they are the same after the merge
        temp_lookup_name = 'lookup_' + lookup_name 
        temp_match_name = 'match_' + match_name    
        
        # give indexes appropriate names so they are the same after the merge
        left_frame.index.names = ['lookup_key']
        right_frame.index.names = ['match_key']
        
        # rename columns as defined above
        left_frame = left_frame.rename(columns={lookup_name: temp_lookup_name})
        right_frame = right_frame.rename(columns={match_name: temp_match_name})
        
        # either do the merge on the join field and the subset field (if subset fields were defined)
        if subset_fields != None:
        
            # remove unwanted columns from the frames -- and blank and unwanted values from the join field -- and reset the index
            temp_data = left_frame[[temp_lookup_name, lookup_join, lookup_subset]][(left_frame[lookup_join].str.len() > 0) & (~left_frame[lookup_join].isin(unwanted_values))].reset_index()
            temp_data_2 = right_frame[[temp_match_name, match_join, match_subset]][(right_frame[match_join].str.len() > 0) & (~right_frame[match_join].isin(unwanted_values))].reset_index()
            
            # get matches by joining the match frame to the lookup frame on the join field and the subset field
            join_matches = pd.merge(temp_data, temp_data_2, how='inner', left_on=[lookup_join, lookup_subset], right_on=[match_join, match_subset])
        
        # or just do the merge on the join field
        else:
    
            # remove unwanted columns from the frames -- and blank and unwanted values from the join field -- and reset the index
            temp_data = left_frame[[temp_lookup_name, lookup_join]][(left_frame[lookup_join].str.len() > 0) & (~left_frame[lookup_join].isin(unwanted_values))].reset_index()
            temp_data_2 = right_frame[[temp_match_name, match_join]][(right_frame[match_join].str.len() > 0) & (~right_frame[match_join].isin(unwanted_values))].reset_index()
    
            
            # get matches by joining the match frame to the lookup frame on the join field
            join_matches = pd.merge(temp_data, temp_data_2, how='inner', left_on=[lookup_join], right_on=[match_join])        
    
        # if there are no results then get out since the subsequent code will fail
        if join_matches.shape[0] == 0:
            write_to_log(log_path, 'no additional primary match records identified')
            return pd.DataFrame()
    
        # remove unwanted columns
        # join_matches = join_matches[['lookup_key', 'match_key', temp_lookup_name, temp_match_name, temp_lookup_name + '_stripped', temp_match_name + '_stripped']]
        join_matches = join_matches[['lookup_key', 'match_key', temp_lookup_name, temp_match_name]]
    
        # remove duplicates
        join_matches = join_matches.drop_duplicates(keep='first')
    
        # add fuzz ratio match score
        vec_fun = np.vectorize(fuzz.ratio)
        join_matches[lookup_name + '_match_score'] = vec_fun(join_matches[temp_lookup_name], join_matches[temp_match_name])
    
        # add token set match score
        vec_fun = np.vectorize(fuzz.token_set_ratio)
        
        # filter for potential matches
        join_matches = join_matches[(join_matches[lookup_name + '_match_score'] >= match_threshold)]
    
        # remove unwanted columns
        join_matches = join_matches[[
            'lookup_key'
            , 'match_key'
            , temp_lookup_name
            , temp_match_name
            , lookup_name + '_match_score'
        ]]
        
        # work out which records are not already in the initial matches -- this method is much simpler than messing with the indexes on the results frame from the class
        mask = (join_matches['lookup_key'] + '_' + join_matches['match_key']).isin(initial_results['lookup_key'] + '_' + initial_results['match_key'])
        additional_results = join_matches[~mask]
        additional_results = additional_results.reset_index(drop=True)
        
        # create a class frame so the results can be manually inspected from outside the class
        self.temp_additional_results = additional_results
        
        # integrate the additional results if there are any
        if not additional_results.shape[0] == 0:
            self.integrate_additional_primary_matches(additional_results)
        else:
            write_to_log(log_path, 'no additional primary match records identified')
        
        # now tell the log file it's all over
        write_to_log(log_path, 'function ' + current_method_name() + ' finished')

    def create_deduped_match_ids(self):
        
        # EITHER: create key map -- some indirect matches may be missed -- but none will be wrong
        self.create_key_map()
        
        # OR: generate connected components -- no indirect matches will be missed -- but some may be wrong
        # self.connect_components()
        
        # EITHER: use final_key_map (determined above) to create new lookup data
        self.get_new_lookup_data('final_key_map')
        
        # OR: use connected_components (determined above) to create new lookup data
        # self.get_new_lookup_data('connected_components')
        
        # create aggregated match ref data
        self.aggregate_match_data()
        
    def integrate_company_suffixes_dictionary(self, d, *, replace=False):
        
        if replace == True:
            self.company_suffixes_dict = d            
        else:
            self.company_suffixes_dict = merge_dictionaries(self.company_suffixes_dict, d)
    
    def reset_company_suffixes_dictionary(self):
        
        self.company_suffixes_dict = COMPANY_SUFFIXES_DICT
        self.company_suffixes_list = convert_dict_to_list(self.company_suffixes_dict)             
    
    # =============================================================================================================================
    # =============================================================================================================================
    # =============================================================================================================================    
    
# =================================================================================================================================
# =================================================================================================================================
# =================================================================================================================================