import pandas as pd

# The file path of the raw CMS data
file_path = 'data/raw/Medicare_IP_Hospitals_by_Provider_and_Service_2023.csv'

# Naming the csv file, df, for dataframe.
df = pd.read_csv(file_path, encoding='latin-1')

## Data cleanup ##
''' Cleanup Steps:
Change the column names
Investigate the null and unknown rows
Handle the null and unknown rows 
Change the data types of necessary fields: zip, fips, provider ccn, ruca, and drg
Create flags to verify data: is zip len = 5, is drg code len = 3, and fips len = 2; 1. 
Create flags to verify data: tot discharges >0, submitted charge > tot charge, and tot charge > medicare charge. 2. 
Evaluate the flags to determine if there are rows to drop
'''

# Renaming multiple columns for easier reading. I removed the Rndrng because all columns are referencing the rendering physician.
df = df.rename(columns={"Rndrng_Prvdr_CCN":"prvdr_ccn", "Rndrng_Prvdr_Org_Name": "org_name", "Rndrng_Prvdr_City": "city",
                   "Rndrng_Prvdr_St": "street_address", "Rndrng_Prvdr_State_FIPS": "state_fips", "Rndrng_Prvdr_Zip5": "zip5",
                   "Rndrng_Prvdr_State_Abrvtn": "state_abrvtn", "Rndrng_Prvdr_RUCA": "ruca", "Rndrng_Prvdr_RUCA_Desc": "ruca_desc",
                   "DRG_Cd": "drg_cd", "DRG_Desc": "drg_desc", "Tot_Dschrgs": "tot_dschrgs", "Avg_Submtd_Cvrd_Chrg": "avg_submtd_chrg", 
                   "Avg_Tot_Pymt_Amt": "avg_tot_pymnt", "Avg_Mdcr_Pymt_Amt": "avg_mdcr_pymt"})

print(df.columns)
# print(df.head(10))


# Handling null and unknown rows
df = df.dropna(subset=['ruca', 'ruca_desc'])
df = df[df['ruca_desc'] != 'Unknown']
# print(df.shape)

# Changing data types of fips, zip5, provider ccn, and drg codes. These are dimensions, not measures.
df['state_fips'] = df['state_fips'].astype(str)
df['zip5'] = df['zip5'].astype(str)
df['drg_cd'] = df['drg_cd'].astype(str)
df['prvdr_ccn'] = df['prvdr_ccn'].astype(str)
df['ruca'] = df['ruca'].astype(str)
# print(df.dtypes)

# Adding leading 0's back to zip, fips, ccn, and drgs
df['state_fips'] = df['state_fips'].str.zfill(2)
df['zip5'] = df['zip5'].str.zfill(5)
df['drg_cd'] = df['drg_cd'].str.zfill(3)
df['prvdr_ccn'] = df['prvdr_ccn'].str.zfill(6)

# Creating validation flags for 
df['flag_zip_len'] = df['zip5'].str.len() == 5
df['flag_drg_cd'] = df['drg_cd'].str.len() == 3
df['flag_state_fips'] = df['state_fips'].str.len() == 2
df['flag_tot_dschrgs'] = df['tot_dschrgs'] > 0 # no negative values
df['flag_avg_submtd_chrg_gt_tot_pymnt'] = df['avg_submtd_chrg'] > df['avg_tot_pymnt'] # where gt is greater than
df['flag_tot_pymnt_gt_mdcr_pymnt'] = df['avg_tot_pymnt'] > df['avg_mdcr_pymt']

# print(df.head(5))

# Evaluating flag columns for any irregularities
flag_cols = ['flag_zip_len', 'flag_drg_cd', 'flag_state_fips', 
             'flag_tot_dschrgs', 'flag_avg_submtd_chrg_gt_tot_pymnt', 
             'flag_tot_pymnt_gt_mdcr_pymnt']

print(df[flag_cols].value_counts())

# Investigating rows where the submitted charges are less than the total payments. Interesting, most hospitals are federally funded or county funded. Lower ses community served potentially.
# print(df[df['flag_avg_submtd_chrg_gt_tot_pymnt'] == False][['org_name']])

# Investigating rows where the total payment charges are less than the medicare payments. These lines are okay, medicare paid total bill
# print(df[df['flag_tot_pymnt_gt_mdcr_pymnt'] == False][['org_name', 'drg_desc', 'tot_dschrgs', 'avg_submtd_chrg', 'avg_tot_pymnt', 'avg_mdcr_pymt']])

print("Final cleaned shape:", df.shape)