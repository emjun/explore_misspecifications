"""
Sample dataset and analysis of Pew Research Center data
"""
import pandas as pd
import os

data_repo_path = "data/"

if __name__ == "__main__": 
    # Load data
    filename = "income_dataset.csv"
    filepath = os.path.join(data_repo_path, filename)    
    df = pd.read_csv(filepath)

    # Wrangle data
    # Age
    # Filter out data where Age == "Don't know/Refused"
    df.sort_values(by=['Age'], inplace=True)
    df = df.query(f"Age != \"Don\'t know/Refused\"")

    # Community
    # 0 = Rural, 1 = Suburban, 2 = Urban
    df.sort_values(by=['Community'], inplace=True)
    df['community_numeric'] = df['Community'].rank(method='dense', na_option='bottom')

    # Highest Edu Completed 
    df.loc[df['Highest Edu Completed'] == "High school graduate (Grade 12 with diploma or GED certificate)", "Highest Edu Completed"] = 0
    df.loc[df['Highest Edu Completed'] == "Some college-no degree (includes some community college)", "Highest Edu Completed"] = 1
    df.loc[df['Highest Edu Completed'] == "Two year associate degree from a college or university", "Highest Edu Completed"] = 2
    df.loc[df['Highest Edu Completed'] == "Four year college or university degree/Bachelor's degree", "Highest Edu Completed"] = 3
    df.loc[df['Highest Edu Completed'] == "Some postgraduate or professional schooling-no postgraduate degree", "Highest Edu Completed"] = 4
    df.loc[df['Highest Edu Completed'] == "Postgraduate or professional degree", "Highest Edu Completed"] = 5
    df['edu_numeric'] = df['Highest Edu Completed'].astype('int')
    
    # Current Student Status
    df = df[df['Current Student Status'].notnull()] # Drop nan
    df = df[df['Current Student Status'] != 'Refused'] # Drop 'Refused'
    # 0 = No, 1 = Yes
    df.sort_values(by=['Current Student Status'], inplace=True)
    df['student_numeric'] = df['Current Student Status'].rank(method='dense', na_option='bottom')

    # Major
    df = df[df['Major'].notnull()] # Drop nan
    df['major_numeric'] = df['Major'].rank(method='dense', na_option='bottom')

    # Employment
    df = df.query(f"Employment != \"Don\'t know/Refused\"")
    # 0 = Not employed, Retired, Disabled; 1 = Part-time; 2 = Full-time
    df.loc[df['Employment'] == "Not employed", "Employment"] = 0
    df.loc[df['Employment'] == "Retired", "Employment"] = 0
    df.loc[df['Employment'] == "Disabled", "Employment"] = 0
    df.loc[df['Employment'] == "Part-time", "Employment"] = 1
    df.loc[df['Employment'] == "Full-time", "Employment"] = 2
    df['employment_numeric'] = df['Employment'].astype('int')

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
    df['income_numeric'] = df['Income'].astype('int')

    # Create and display correlation matrix
    corr_matrix = df.corr()
    print(corr_matrix)

    # Author model 