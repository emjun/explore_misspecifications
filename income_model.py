"""
Analyze Income dataset from Pew Research Center data
Preprocess script: income_preprocess.py
"""
import pandas as pd
import os
import statsmodels.api as sm
import statsmodels.formula.api as smf

# --- (BOBA_CONFIG)
{
  "graph": [
    "INTERACTION->FIXED->MODEL"
  ],
  "decisions": [{"var": "fixed", "options": [[], ["community_numeric"], ["edu_numeric"], ["student_numeric"], ["major_numeric"], ["employment_numeric"], ["income_numeric"], ["community_numeric", "edu_numeric"], ["community_numeric", "student_numeric"], ["community_numeric", "major_numeric"], ["community_numeric", "employment_numeric"], ["community_numeric", "income_numeric"], ["edu_numeric", "student_numeric"], ["edu_numeric", "major_numeric"], ["edu_numeric", "employment_numeric"], ["edu_numeric", "income_numeric"], ["student_numeric", "major_numeric"], ["student_numeric", "employment_numeric"], ["student_numeric", "income_numeric"], ["major_numeric", "employment_numeric"], ["major_numeric", "income_numeric"], ["employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric"], ["community_numeric", "edu_numeric", "major_numeric"], ["community_numeric", "edu_numeric", "employment_numeric"], ["community_numeric", "edu_numeric", "income_numeric"], ["community_numeric", "student_numeric", "major_numeric"], ["community_numeric", "student_numeric", "employment_numeric"], ["community_numeric", "student_numeric", "income_numeric"], ["community_numeric", "major_numeric", "employment_numeric"], ["community_numeric", "major_numeric", "income_numeric"], ["community_numeric", "employment_numeric", "income_numeric"], ["edu_numeric", "student_numeric", "major_numeric"], ["edu_numeric", "student_numeric", "employment_numeric"], ["edu_numeric", "student_numeric", "income_numeric"], ["edu_numeric", "major_numeric", "employment_numeric"], ["edu_numeric", "major_numeric", "income_numeric"], ["edu_numeric", "employment_numeric", "income_numeric"], ["student_numeric", "major_numeric", "employment_numeric"], ["student_numeric", "major_numeric", "income_numeric"], ["student_numeric", "employment_numeric", "income_numeric"], ["major_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "major_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "employment_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "major_numeric", "employment_numeric"], ["community_numeric", "edu_numeric", "major_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "student_numeric", "major_numeric", "employment_numeric"], ["community_numeric", "student_numeric", "major_numeric", "income_numeric"], ["community_numeric", "student_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["edu_numeric", "student_numeric", "major_numeric", "employment_numeric"], ["edu_numeric", "student_numeric", "major_numeric", "income_numeric"], ["edu_numeric", "student_numeric", "employment_numeric", "income_numeric"], ["edu_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["student_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "major_numeric", "employment_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "major_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "student_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["edu_numeric", "student_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "major_numeric", "employment_numeric", "income_numeric"]]}, {"var": "interaction", "options": [["community_numeric", "edu_numeric"], ["community_numeric", "student_numeric"], ["community_numeric", "major_numeric"], ["community_numeric", "employment_numeric"], ["community_numeric", "income_numeric"], ["edu_numeric", "student_numeric"], ["edu_numeric", "major_numeric"], ["edu_numeric", "employment_numeric"], ["edu_numeric", "income_numeric"], ["student_numeric", "major_numeric"], ["student_numeric", "employment_numeric"], ["student_numeric", "income_numeric"], ["major_numeric", "employment_numeric"], ["major_numeric", "income_numeric"], ["employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric"], ["community_numeric", "edu_numeric", "major_numeric"], ["community_numeric", "edu_numeric", "employment_numeric"], ["community_numeric", "edu_numeric", "income_numeric"], ["community_numeric", "student_numeric", "major_numeric"], ["community_numeric", "student_numeric", "employment_numeric"], ["community_numeric", "student_numeric", "income_numeric"], ["community_numeric", "major_numeric", "employment_numeric"], ["community_numeric", "major_numeric", "income_numeric"], ["community_numeric", "employment_numeric", "income_numeric"], ["edu_numeric", "student_numeric", "major_numeric"], ["edu_numeric", "student_numeric", "employment_numeric"], ["edu_numeric", "student_numeric", "income_numeric"], ["edu_numeric", "major_numeric", "employment_numeric"], ["edu_numeric", "major_numeric", "income_numeric"], ["edu_numeric", "employment_numeric", "income_numeric"], ["student_numeric", "major_numeric", "employment_numeric"], ["student_numeric", "major_numeric", "income_numeric"], ["student_numeric", "employment_numeric", "income_numeric"], ["major_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "major_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "employment_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "major_numeric", "employment_numeric"], ["community_numeric", "edu_numeric", "major_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "student_numeric", "major_numeric", "employment_numeric"], ["community_numeric", "student_numeric", "major_numeric", "income_numeric"], ["community_numeric", "student_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["edu_numeric", "student_numeric", "major_numeric", "employment_numeric"], ["edu_numeric", "student_numeric", "major_numeric", "income_numeric"], ["edu_numeric", "student_numeric", "employment_numeric", "income_numeric"], ["edu_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["student_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "major_numeric", "employment_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "major_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "student_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["edu_numeric", "student_numeric", "major_numeric", "employment_numeric", "income_numeric"], ["community_numeric", "edu_numeric", "student_numeric", "major_numeric", "employment_numeric", "income_numeric"], []]}]
}
# --- (END)

if __name__ == '__main__':
  # Read data
  # data_repo_path = "data/"
  # os.chdir(os.path.dirname(__file__))
  # dir = os.getcwd()
  dir_path = "/Users/emjun/Git/explore_misspecifications/data"
  filename = "income_dataset_clean.csv"
  filepath = os.path.join(dir_path, filename)    
  df = pd.read_csv(filepath)

  # Author model 
  # Key variables of interest: IV - Education, DV - Income

  # --- (INTERACTION)
  # Try all combinations of interaction effects
  # Generate superset of interaction terms
  ixn_terms = {{interaction}}

  ixn_terms_list = list()
  # TODO: Can generate multiple interactions
  # for term in ixn_terms: 
  #   ixn = '*'.join(term)
  #   ixn_terms_list.append(ixn)

  # ixn_terms_formula = '+'.join(ixn_terms_list)

  # TIMEBEING: 
  ixn_terms_formula = '*'.join(ixn_terms)

  # --- (FIXED)
  # Try all combinations of fixed effects
  # Generate superset of variables --> These are considered the options
  fixed_terms = {{fixed}}
  
  fixed_terms_formula = '+'.join(fixed_terms)

  # --- (MODEL)
  formula = 'income_numeric ~ ' + fixed_terms_formula + " + " + ixn_terms_formula
  # TODO: Start with just linear regression 
  lm = smf.ols(formula, data=df)
  # table = sm.stats.anova_lm(lm, typ=2)
  # print(table)
  results = lm.fit()
  print(results)
  

  ## Modeling script
  # Read in clean data
  # Decision points
  # Execute model and print table of results  
  # Q: How to call different modeling lines of code depending on family/link functions?