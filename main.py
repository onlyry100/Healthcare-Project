from sqlalchemy import  create_engine

import pandas as pd

df = pd.read_csv("healthcare_dataset.csv")

# print(df.shape)        # kitne rows, columns
# print(df.dtypes)       # data types
# print(df.head())         # pehli 10 rows dekho
# print(df.isnull().sum()) # missing values check

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")      #
print(df.columns)                                                          #
                                                                           #
df["name"] = df["name"].str.lower()                                        #
df["doctor"] = df["doctor"].str.lower()                                    #  ---- FIRST WE DO COULMNS IN CORRECT MANNER ----
df["hospital"] = df["hospital"].str.lower()                                # 
df["insurance_provider"] = df["insurance_provider"].str.lower()            #
df["medication"] = df["medication"].str.lower()                            #
df["medical_condition"] = df["medical_condition"].str.lower()              #
# print(df.head)

# Checking Duplicate Data in Dataset ------------

dulpicate = df.duplicated().sum()                                          # ---- FOUND 536 Duplicate rows in raw dataset -----
# print(dulpicate)

# Droping the Duplicate data in the Dataset ------

df = df.drop_duplicates()                                                  # ---- DROP 536 Duplicate rows in this dataset
# print(df.shape)                                                          # ---- FINAL CLEANED DATASET : 54860


# Date Conversion in Python --------

df["date_of_admission"] = pd.to_datetime(df["date_of_admission"])          # ---- 
df["discharge_date"] = pd.to_datetime(df["discharge_date"])
# print(df.dtypes)

# Cleaing Age and Billing Deatils --------

# print(df["age"].describe())
# print(df["billing_amount"].describe())

# Negative Values in Billing Amount ------

# print((df["billing_amount"] < 0).sum())   # Found 106 Negative Billing Amount Values in the Dataset

df = df[df["billing_amount"] >= 0]
# print(df.shape)


# MySQL Connection -----------
from urllib.parse import quote_plus   # urllib.parse.quote_plus is used to encode special characters in the password for the connection string

username = "root"
password = quote_plus("Papa@2003")   # quote_plus is used to encode special characters in the password for the connection string
host = "127.0.0.1"
database = "healthcare_project"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")
# print(engine.connect())


# making Patient Table in MySQL Database -----------

patients = df[['name', 'age', 'gender', 'blood_type']].drop_duplicates().reset_index(drop=True)
patients['patient_id'] = patients.index + 1
# print(patients.shape)
# print(patients.head())

# Making Admission Table ---------------

df_merge = df.merge(patients, on=["name", "age", "gender", "blood_type"], how="left")
admission = df_merge[[ 'patient_id', 'doctor', 'hospital', 'medical_condition',
    'date_of_admission', 'discharge_date', 'admission_type',
    'insurance_provider', 'billing_amount', 'room_number',
    'medication', 'test_results']].reset_index(drop=True)

admission["admission_id"] = admission.index + 1
# print(admission.shape)
# print(admission.head())

## Saving the DataFrames to MySQL Database -----------

# patients.to_sql("patients", con=engine, if_exists="replace", index=False)      #to_sql() method is used to save the DataFrame to a SQL database. The parameters are as follows:
# admission.to_sql("admission", con=engine, if_exists="replace", index=False)    # if_exists="replace" means that if the table already exists, it will be replaced with the new data. index=False means that the index of the DataFrame will not be saved to the database.
# print("DataFrames saved to MySQL database successfully!")

query = """
SELECT p.name, p.age, p.gender, a.medical_condition, a.doctor, a.hospital, a.billing_amount
FROM patients p
JOIN admission a ON p.patient_id = a.patient_id
"""

analysis_df = pd.read_sql(query, con=engine)
print(analysis_df.shape)
print(analysis_df.head())

# Analysis of the DataFrame -----------

# Most Common Medical Condition -----------   ("ARTHRITIS") but all 6 Conditions are very close in count (~9000 - 9200) ----------

max_disease = analysis_df['medical_condition'].value_counts().idxmax()
print(f"The most common medical condition is: {max_disease}")

# Highest Revenue Doctor -----------   (by SUM()) = "MICHAEL SMITH" ----

high_rev_doc = analysis_df.groupby("doctor")["billing_amount"].sum().round(2).idxmax()
print(f"Highest Revenue Doctor is: {high_rev_doc}")

# Most Expensive Dcotor -------        (by MEAN()) = "KATHLEEN GRIFFIN" ----

most_exp_doc = analysis_df.groupby("doctor")["billing_amount"].mean().sort_values(ascending=False).round(2)
print(most_exp_doc.head())

# Most Expensive Hospital ------   = ("HERNANDEZ MORTON") -- by AVG Per Person ----

most_exp_hos = analysis_df.groupby("hospital")["billing_amount"].mean().sort_values(ascending=False).round(2)
print(most_exp_hos.head())

# Highesh Revenue of Hospital -----  = ("JOHNSON PLC") -- BY total Billing ---

high_rev_hos = analysis_df.groupby("hospital")["billing_amount"].sum().round(2).idxmax()
print(f"Highest Revenue Hospital is: {high_rev_hos}")


# Length of Stay Calculation -----------

query2 = """
SELECT p.patient_id, a.date_of_admission, a.discharge_date
FROM patients p
JOIN admission a ON p.patient_id = a.patient_id
"""
los_df = pd.read_sql(query2, con=engine)
los_df['length_of_stay'] = (los_df['discharge_date'] - los_df['date_of_admission']).dt.days  # .dt.days is used to extract the number of days from the timedelta object returned by the subtraction of two datetime objects.

import numpy as np
print("Average stay (days):", np.mean(los_df['length_of_stay']).round(1))
print("Median stay (days):", np.median(los_df['length_of_stay']))
print("Std deviation:", np.round(np.std(los_df['length_of_stay']), 2))

# Importing MATPLOTLIB and SEABORN for Charts ------

import matplotlib.pyplot as plt
import seaborn as sns

# Top 10 Medical Conditions (BAR Chart) --------

plt.style.use("seaborn-v0_8-whitegrid")

top_conditions = analysis_df["medical_condition"].value_counts().head(10)     # All medical conditions have nearly equal patient counts -- visually confirms the dataset
                                                                              # is synthetically balanced rather than modeling real-world disease frequency
plt.figure(figsize=(10,6))
ax = sns.barplot(x=top_conditions.values, y=top_conditions.index, hue=top_conditions.index, palette="crest", legend=False)

# Showing Values under the Bar ----
for i, v in enumerate(top_conditions.values):
    ax.text(v + 50, i, str(v), va ="center", fontsize = 10)


plt.title("Top 10 Medical Condition by Patient Count",  fontsize =14, fontweight = "bold")
plt.xlabel("Number of Patients", fontsize =12)
plt.ylabel("Medical Conditions", fontsize =12)
sns.despine()
plt.tight_layout()
plt.show()


# Top 10 Doctors by Average Billing ------

top_doctors = analysis_df.groupby('doctor')['billing_amount'].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=top_doctors.values, y=top_doctors.index, hue=top_doctors.index, palette='flare', legend=False)

for i, v in enumerate(top_doctors.values):
    ax.text(v - (v * 0.05), i, f"{v:.0f}", va='center', ha='right', fontsize=10, color='black', fontweight='bold')

plt.title('Top 10 Doctors by Average Billing Amount', fontsize=14, fontweight='bold')
plt.xlabel('Average Billing Amount', fontsize=12)
plt.ylabel('Doctor', fontsize=12)
sns.despine()
plt.tight_layout()
plt.show()

# Hospital =-wise Total Revenue --------

hos_rev = analysis_df.groupby("hospital")["billing_amount"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))                                                                                                
ax = sns.barplot(x=hos_rev.values, y=hos_rev.index, hue=hos_rev.index, palette='magma', legend=False)              

for i, v in enumerate(hos_rev.values):
    ax.text(v - (v * 0.05), i, f"{v:,.0f}", va='center', ha='right', fontsize=10, color='white', fontweight='bold')

plt.title('Top 10 Hospitals by Total Revenue', fontsize=14, fontweight='bold')
plt.xlabel('Total Billing Amount (Revenue)', fontsize=12)
plt.ylabel('Hospital', fontsize=12)
sns.despine()
plt.tight_layout()
plt.show()

# Billiong Amount Distribution (Histogram) --------

plt.figure(figsize=(10, 6))
sns.histplot(analysis_df['billing_amount'], bins=30, color='teal', kde=True)                               # Billing amount is uniformly distributed across the full range (0-50,000), not right-skewed
                                                                                                           # like real-world healthcare billing typically is -- strong evidence this is synthetic data
plt.title('Distribution of Billing Amount', fontsize=14, fontweight='bold')                  
plt.xlabel('Billing Amount', fontsize=12)
plt.ylabel('Number of Patients', fontsize=12)
sns.despine()
plt.tight_layout()
plt.show()


# Length of Stay Distribution (Histogram) --------

plt.figure(figsize=(10, 6))
sns.histplot(los_df['length_of_stay'], bins=30, color='orange', kde=True)                                  # Length of stay is also uniformly distributed (0-30 days) -- consistent with the billing
                                                                                                           # distribution finding, further confirming synthetic data generation
plt.title('Distribution of Length of Stay', fontsize=14, fontweight='bold')
plt.xlabel('Length of Stay (days)', fontsize=12)
plt.ylabel('Number of Patients', fontsize=12)
sns.despine()
plt.tight_layout()
plt.show()


# Age vs Billing Amount (Scatter Plot)  ---------

plt.figure(figsize=(10, 6))
sns.scatterplot(x=analysis_df['age'], y=analysis_df['billing_amount'], alpha=0.3, color='steelblue')        # No visible correlation between age and billing_amount -- points are scattered randomly
                                                                                                            # across all ages, confirming billing was generated independent of patient demographics
plt.title('Age vs Billing Amount', fontsize=14, fontweight='bold')
plt.xlabel('Age', fontsize=12)
plt.ylabel('Billing Amount', fontsize=12)
sns.despine()
plt.tight_layout()
plt.show()


# Excel Export of Healthcare Analysis DataFrames -----------

with pd.ExcelWriter('healthcare_analysis_summary.xlsx', engine='openpyxl') as writer:                    # ExcelWriter is used to write multiple DataFrames to different sheets in a single Excel file. The engine 'openpyxl' is specified for writing .xlsx files.
    
    top_conditions.to_frame(name='patient_count').to_excel(writer, sheet_name='Top Medical Conditions')  # to_frame() is used to convert the Series to a DataFrame, and name parameter is used to specify the column name in the resulting DataFrame.
    
    most_exp_doc.to_frame(name='avg_billing').to_excel(writer, sheet_name='Top Doctors')                 # to_excel() is used to write the DataFrame to an Excel file, and sheet_name parameter is used to specify the name of the sheet in the Excel file.pip
    
    most_exp_hos.to_frame(name='avg_billing').to_excel(writer, sheet_name='Top Hospitals')
    
    summary_stats = pd.DataFrame({
        'Metric': ['Average Length of Stay', 'Median Length of Stay', 'Std Dev (Length of Stay)'],
        'Value': [np.mean(los_df['length_of_stay']).round(1), np.median(los_df['length_of_stay']), np.round(np.std(los_df['length_of_stay']), 2)]
    })
    summary_stats.to_excel(writer, sheet_name='Summary Stats', index=False)

print("Excel file created successfully!")