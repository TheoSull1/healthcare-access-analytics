import pandas as pd

# The file path of the raw CMS data
file_path = 'data/raw/Medicare_IP_Hospitals_by_Provider_and_Service_2023.csv'

# Naming the csv file, df, for dataframe.
df = pd.read_csv(file_path, encoding='latin-1')

'''
Data Exploration
Analyzing the data to understand the volume, data entry errors, and structure of the data.
Investigating any null values or unexpected data entries
'''

# pd.set_option('display.max_columns',None)  # displays all columns using pandas
print("Shape: ",df.shape)
print("Columns: ",df.columns)
print("Data Types: ",df.dtypes)
print("Null Values: ",df.isnull().sum())
print("First 3 Rows: ",df.head(3))

# Checking for irregular data entries
print(df['DRG_Desc'].value_counts())
print(df['DRG_Cd'].value_counts())
print(df['Rndrng_Prvdr_Zip5'].value_counts())
print(df['Rndrng_Prvdr_State_FIPS'].value_counts())
print(df['Rndrng_Prvdr_CCN'].value_counts())


# Investigating the rows with Null for RUCA 
print(df['Rndrng_Prvdr_RUCA_Desc'].value_counts()) # there are also 'unknown' values in RUCA
null_rows = df[df.isnull().any(axis=1)]
print(null_rows)



