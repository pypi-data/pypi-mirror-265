<h1>About</h1>

**MultiMatch | Multi-Dimensional Match Scores**

How to use this package:

1. Customise the built-in class to generate a matrix of match scores across multiple dimensions.
2. Apply your own rules to the scores in the matrix as per your specific use-case to identify matches.

Key features:

1. Methods to cleanse and standardise company names.
2. A method to dedupe data sets and add new IDs.
3. Functionality to match in subsets to optimise performance.

<h1>Dependencies</h1>

**Required**

| Package	| Version	| License						|
|---------------|---------------|-------------------------------------------------------|
| pandas	| 1.3.5		| BSD License (BSD 3-Clause License			|
| numpy		| 1.20.3	| BSD License						|
| rapidfuzz	| 1.9.1		| MIT License (MIT)					|
| unidecode	| 1.2.0		| GNU General Public License v2 or later (GPLv2+)	|

**Optional**

| Package	| Version	| License						|
|---------------|---------------|-------------------------------------------------------|
| networkx	| TBC		| BSD License						|

<h1>Data Preparation</h1>

Instructions:

1. Create one frame comprising the data to lookup and one frame comprising the data to match it to.
2. Ensure each frame has (1) a key which is (a) a string and (b) the index; and (2) a primary field on which to match.
3. Ideally there should be secondary fields to increase the robustness of the matching.
4. The two data sets should have the exactly same column names.
5. To de-dupe a record set the same frame can be used as both the lookup and match frames.

<h1>Build a Custom Class</h1>

<h2>Initialise the class</h2>

**Positional arguments:**

* lookup_frame
* lookup_key
* lookup_name
* match_frame
* match_key
* match_name
* threshold
            
**Optional arguments:**

1. primary_field_type
    * company_name: this will do company name specific cleansing and STANDARDISE legal text.
    * company_name_stripped: this will do company name specific cleansing and REMOVE legal text.
    * address: can be used to cleanse first line of address and city.
    * domain_stripped: this will remove the suffixes at the end of the domains. 
2. match_function
    * fuzz.ratio: fuzzy matching using Levenstein Distance (the default)
    * fuzz.token_set_ratio: set intersection match score
    * set_intersection_match_score: alternative to the above
3. remove_spaces: True or False (useful for postcodes)
4. log_path: self explanatory

Example code below.

	# import objects
    from matchmatrix import MatchManager

    # optional: create a company suffixes dictionary to integrate with default one
    csd = {'ltd': ['ltd', 'ltd.', 'limited', 'l.i.m.i.t.e.d.', 'limmyted']
          , 'plc': ['plc', 'plc.', 'public limited company', 'pee ell see']
          , 'gmbh': ['gmbh', 'gmbh.']}
    
    # create class
    MyMatch = MatchManager()
    
    # build class
    MyMatch.build_class(
                        # positional arguments
                        lookup_frame, lookup_key, lookup_name
                        , match_frame, match_key, match_name
                        , 70
                        # optional arguments
                        , primary_field_type='company_name'
                        # , match_function = 'fuzz.ratio'
                        # , remove_spaces = False
                        , log_path=log_path
                        )

    # optional: integrate company suffixes dictionary with default one (if defined above)
    # set replace=True to replace the default one completely
    MyMatch.integrate_company_suffixes_dictionary(csd)    
    
    # if necessary re-instate the default dictionary
    # MyMatch.reset_company_dictionary()

<h2>Optional (but recommended): define subsetting fields.</h2>

This will do the matching in subsets e.g. county e.g. Yorkshire to Yorkshire to SIGNIFICANTLY speed up processing time.\

    MyMatch.subset_fields = ('county_name', 'county_name')

<h2>Optional (but recommended): cleanse the primary matching fields</h2>

    MyMatch.cleanse_primary_fields()
    
<h2>Get the primary matches</h2>
    
    MyMatch.get_primary_matches()

<h2>Have a look at the results</h2>
    
    initial_results = MyMatch.initial_results
    
<h2>Optional (but recommended): add secondary matches to the class</h2>
    
**Positional argugments:**

* lookup_name: name of column to match from in lookup frame.
* match_name: name of column to match to in match frame.

**Optional argugments:**

* field_type: same options as primary_field_type above.
* remove_spaces: as defined above.
* match_function: as defined above.
* duplicate_suffix: text to add to a duplicate column e.g. '_stripped'.
* cleanse_data: True or False.
* secondary_match_name: a name to refer to later e.g. if doing additional join matches.

Example code below.
    
    MyMatch.clear_secondary_matches()
    MyMatch.add_secondary_match('address', 'address', field_type='address', cleanse_data=True, secondary_match_name='address')
    MyMatch.add_secondary_match('postcode', 'postcode', field_type='address', remove_spaces=True, cleanse_data=True, secondary_match_name='postcode')
    
<h2>Optional: get additional primary matches by joining a pair of secondary match fields</h2>

**Positional arguments:**

* secondary_match_name: the name defined above
    
**Optional arguments:**

* explode_column: True or False (if a column contains multiple values separated by a comma).

Example code below.
	
	# get additional join matches
    MyMatch.get_additional_join_matches('postcode')

<h2>Optional: create and integrate a separate class e.g. a primary match on address.</h2>

	# to be developed
    
<h2>Optional: Get secondary matches (if defined above)</h2>

    MyMatch.get_secondary_matches()  

<h2>Have a look at the results</h2>
    
    initial_results = MyMatch.initial_results
    
<h2>Identify matches</h2>

Instructions:

1. Apply a series of rules across the different scores in **MyMatch.initial_results** to identify matches.\

2. Create the frame **MyMatch.matched_results** in the class comprising matches ONLY.\

<h2>Dedupe matched results and add match ids</h2>

    # add deduped ids to original keys
    MyMatch.create_deduped_match_ids()

    # get xref frame that maps original keys to deduped ids
    final_key_map = MyMatch.final_key_map
    
    # get dimension table at a deduped id level
    match_ref_data = MyMatch.match_ref_data