# -*- coding: utf-8 -*-
"""Customer_Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zC68YvusE-43S5ZeK8k9QLyUNPeVEgDe

**Requirements**:

- Columns containing categories with only two factors must be stored as Booleans (bool).

- Columns containing integers only must be stored as 32-bit integers (int32).

- Columns containing floats must be stored as 16-bit floats (float16).

- Columns containing nominal categorical data must be stored as the category data type.

- Columns containing ordinal categorical data must be stored as ordered categories, and not mapped to numerical values, with an order that reflects the natural order of the column.

- The DataFrame should be filtered to only contain students with 10 or more years of experience at companies with at least 1000 employees, as their recruiter base is suited to more experienced professionals at enterprise companies.
"""

import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

# Load the dataset
ds_jobs = pd.read_csv("/content/drive/MyDrive/CustomerAnalysis/customer_train.csv")

# View the dataset
ds_jobs.head()

# Create a copy of ds_jobs for transforming
ds_jobs_transformed = ds_jobs.copy()

# Start coding here. Use as many cells as you like!
ds_jobs.info()

# EDA to help identify ordinal, nominal, and two-factor categories
for col in ds_jobs.select_dtypes("object").columns:
    unique_values = ds_jobs[col].unique()
    value_counts = ds_jobs[col].value_counts()
    print(f"Unique values for {col}: {unique_values}")
    print(f"Value counts for {col}:\n{value_counts}\n")

# Create a dictionary of columns containing ordered categorical data
ordered_cats = {}
ordered_cats['enrolled_university'] = ['no_enrollment', 'Part time course', 'Full time course']
ordered_cats['education_level'] = ['Primary School', 'High School', 'Graduate', 'Masters', 'Phd']
ordered_cats['experience'] = ['<1'] + list(map(str, range(1, 21))) + ['>20']
ordered_cats['company_size'] = ['<10', '10-49', '50-99', '100-499', '500-999', '1000-4999', '5000-9999', '10000+']
ordered_cats['last_new_job'] = ['never', '1', '2', '3', '4', '>4']

for key, value in ordered_cats.items():
    print(f"{key}: {value}")

# Create a mapping dictionary of columns containing two-factor categories to convert to Booleans
columns = ['relevant_experience', 'job_change']
values = [['No relevant experience', 'Has relevant experience'], [0.0, 1.0]]
booleans = [[False, True], [False, True]]

two_factor_cats = {col: {val: bool_val for val, bool_val in zip(values[i], booleans[i])} for i, col in enumerate(columns)}

for key, value in two_factor_cats.items():
    print(key + ":")
    for k, v in value.items():
        print(f"    {k}: {v}")

# Loop through DataFrame columns to efficiently change data types
for col in ds_jobs_transformed:

    # Convert two-factor categories to bool
    if col in ['relevant_experience', 'job_change']:
        ds_jobs_transformed[col] = ds_jobs_transformed[col].map(two_factor_cats[col])

    # Convert integer columns to int32
    elif col in ['student_id', 'training_hours']:
        ds_jobs_transformed[col] = ds_jobs_transformed[col].astype('int32')

    # Convert float columns to float16
    elif col == 'city_development_index':
        ds_jobs_transformed[col] = ds_jobs_transformed[col].astype('float16')

    # Convert columns containing ordered categorical data to ordered categories using dict
    elif col in ordered_cats.keys():
        category = pd.CategoricalDtype(ordered_cats[col], ordered=True)
        ds_jobs_transformed[col] = ds_jobs_transformed[col].astype(category)

    # Convert remaining columns to standard categories
    else:
        ds_jobs_transformed[col] = ds_jobs_transformed[col].astype('category')

# Filter students with 10 or more years experience at companies with at least 1000 employees
ds_jobs_transformed = ds_jobs_transformed[(ds_jobs_transformed['experience'] >= '10') & (ds_jobs_transformed['company_size'] >= '1000-4999')]

ds_jobs_transformed.info()