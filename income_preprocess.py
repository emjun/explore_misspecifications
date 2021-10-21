"""
Clean dataset and generate Boba JSON for Income dataset from Pew Research Center
Analysis script: income_model.py
"""

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import os
from itertools import chain, combinations
import json

def powerset(iterable, min_length=0):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(min_length, len(s)+1))


data_repo_path = "data/"
_decisions_ = dict()

def setup_decisions(): 
    global _decisions_

    _decisions_["decisions"] = list()

def clean_dataset():
    # Load data
    filename = "income_dataset.csv"
    filepath = os.path.join(data_repo_path, filename)    
    df = pd.read_csv(filepath)
    clean_dict = dict()

    # Wrangle data
    # Age
    # Filter out data where Age == "Don't know/Refused"
    df.sort_values(by=['Age'], inplace=True)
    df = df.query(f"Age != \"Don\'t know/Refused\"")

    # Community
    # 0 = Rural, 1 = Suburban, 2 = Urban
    df.sort_values(by=['Community'], inplace=True)
    clean_dict['community_numeric'] = df['Community'].rank(method='dense', na_option='bottom')
    

    # Highest Edu Completed 
    df.loc[df['Highest Edu Completed'] == "High school graduate (Grade 12 with diploma or GED certificate)", "Highest Edu Completed"] = 0
    df.loc[df['Highest Edu Completed'] == "Some college-no degree (includes some community college)", "Highest Edu Completed"] = 1
    df.loc[df['Highest Edu Completed'] == "Two year associate degree from a college or university", "Highest Edu Completed"] = 2
    df.loc[df['Highest Edu Completed'] == "Four year college or university degree/Bachelor's degree", "Highest Edu Completed"] = 3
    df.loc[df['Highest Edu Completed'] == "Some postgraduate or professional schooling-no postgraduate degree", "Highest Edu Completed"] = 4
    df.loc[df['Highest Edu Completed'] == "Postgraduate or professional degree", "Highest Edu Completed"] = 5
    clean_dict['edu_numeric'] = df['Highest Edu Completed'].astype('int')
    
    # Current Student Status
    df = df[df['Current Student Status'].notnull()] # Drop nan
    df = df[df['Current Student Status'] != 'Refused'] # Drop 'Refused'
    # 0 = No, 1 = Yes
    df.sort_values(by=['Current Student Status'], inplace=True)
    clean_dict['student_numeric'] = df['Current Student Status'].rank(method='dense', na_option='bottom')

    # Major
    df = df[df['Major'].notnull()] # Drop nan
    clean_dict['major_numeric'] = df['Major'].rank(method='dense', na_option='bottom')

    # Employment
    df = df.query(f"Employment != \"Don\'t know/Refused\"")
    # 0 = Not employed, Retired, Disabled; 1 = Part-time; 2 = Full-time
    df.loc[df['Employment'] == "Not employed", "Employment"] = 0
    df.loc[df['Employment'] == "Retired", "Employment"] = 0
    df.loc[df['Employment'] == "Disabled", "Employment"] = 0
    df.loc[df['Employment'] == "Part-time", "Employment"] = 1
    df.loc[df['Employment'] == "Full-time", "Employment"] = 2
    clean_dict['employment_numeric'] = df['Employment'].astype('int')

    # SKIP Marital Status

    # SKIP Housing

    # Income
    df = df.query(f"Income != \"Don\'t know/Refused\"")
    df['Income'].rank(method='dense', na_option='bottom')

    df.loc[df['Income'] == "Less than $10K", "Income"] = 0
    df.loc[df['Income'] == "$10K to under $20K", "Income"] = 1
    df.loc[df['Income'] == "$20K to under $30K", "Income"] = 2
    df.loc[df['Income'] == "$30K to under $40K", "Income"] = 3
    df.loc[df['Income'] == "$40K to under $50K", "Income"] = 4
    df.loc[df['Income'] == "$50K to under $75K", "Income"] = 5
    df.loc[df['Income'] == "$75K to under $100K", "Income"] = 6
    df.loc[df['Income'] == "$100K to under $150", "Income"] = 7
    df.loc[df['Income'] == "$150K or more", "Income"] = 8
    clean_dict['income_numeric'] = df['Income'].astype('int')

    # Output clean dataset
    variables = ['community_numeric', 'edu_numeric', 'student_numeric', 'major_numeric', 'employment_numeric', 'income_numeric']
    clean_filename = "income_dataset_clean.csv"
    clean_filepath = os.path.join(data_repo_path, clean_filename)    
    clean_df = pd.DataFrame.from_dict(clean_dict)
    clean_df.to_csv(clean_filepath)

    # Return clean dataframe
    return clean_df

def generate_multiverse_json(variables): 
    global _decisions_
    
    # Generate all combinations of fixed effects
    fixed_pset = list(powerset(variables))
    assert(isinstance(fixed_pset, list))
    
    # Add fixed effects into decisions
    fixed_dec = dict()
    fixed_dec["var"] = "fixed"
    fixed_dec["options"] = fixed_pset

    _decisions_["decisions"].append(fixed_dec)
    
    # Generate all possible interaction effects
    ixn_eff_pset = list(powerset(variables, min_length=2))
    # empty_tup = ()
    # ixn_eff_pset.append(empty_tup)
    # import pdb; pdb.set_trace()
    
    # Generate all possible *combinations* of interaction effects
    ixn_pset = list(powerset(ixn_eff_pset))
    assert(isinstance(ixn_pset, list))

    # Add interaction effects into decisions
    ixn_dec = dict()
    ixn_dec["var"] = "interaction"
    ixn_dec["options"] = ixn_pset

    _decisions_["decisions"].append(ixn_dec)

    # Output the JSON with options
    _decisions_

    with open('decisions.json', 'w') as f:
        json.dump(_decisions_, f)

def output_data_diagnostics(df: pd.DataFrame):
    # Show data diagnostics
    # Create and display correlation matrix
    corr_matrix = df.corr()
    print(corr_matrix)

if __name__ == "__main__": 

    clean_df = clean_dataset()

    variables = list(clean_df.columns.values)
    setup_decisions()
    generate_multiverse_json(variables)

    output_data_diagnostics(clean_df)



    
    

    