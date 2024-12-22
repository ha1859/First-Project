
# Hi, I'm Hussan! 👋

I'm aspiring to become a data scientist or a data engineer one day (doing projects in both fields!).

I've built a number of different projects like this one to showcase my skillset.

# Project 1 - Using Python to clean a dataset

This was my very first project where I used python to clean a dataset. 

    Steps: 
    1. Obtained messay sales dataset from chatGPT 
    2. Uploaded dataset to VS code 
    3. Wrote python script to clean the data 
        - Imported and used Pandas library to create dataframe
        - Removed columns that are irrelevant
        - Filled missing data
        - Removed any duplicates
        - Standardized all columns by capitalization and title case
        - Used IQR method to identify outliers and removed them
        - Saved to a new CSV file


## Access the Dataset

You can view the dataset directly in the Google Sheet using the link below:

[Click here to view the dataset](https://docs.google.com/spreadsheets/d/1Zce-BjZRPm6IfTQ-n7rp6V6sn7uEhsVYNvr4bXTxUM0/edit?usp=sharing)

This sheet includes both the messy and cleaned versions of the dataset for reference.

## Dataset Before


Below is the original messy dataset:

| Order ID | Date        | Customer Name | State       | Sales | Profit | Category         | Discount |
|----------|-------------|---------------|-------------|-------|--------|------------------|----------|
| ORD032   | 01-02-2024  | John Doe      | Ca          | 100   | 1000   | office supplies  |          |
| ORD013   | 01-02-2024  | John Doe      | California  | 200   | 1000   | technology       |          |
| ORD005   | 01-02-2024  | John Doe      |             | 450   | 50     | office supplies  | 0.3      |
| ORD046   | Invalid     |               | California  | 100   | 20     | technology       | 0.3      |
| ORD026   | Invalid     | John Doe      |             | -10   |        | furniture        | 0.1      |
| ORD040   | 2024/01/01  |               | Ca          | 450   | 20     | office supplies  | 0.3      |
| ORD011   | 01-02-2024  | jane SMITH    | Ca          | 100   | 50     | unknown          | 0.1      |
|          |             |               |             |       |        |                  |          |


## Dataset After

Below is the cleaned dataset:

| Order ID | Date        | Customer Name | State       | Sales | Profit | Category         | Discount |
|----------|-------------|---------------|-------------|-------|--------|------------------|----------|
| ORD032   | 2024-01-02  | John Doe      | CA          | 100   | 1000   | Office Supplies  |          |
| ORD013   | 2024-01-02  | John Doe      | CA          | 200   | 1000   | Technology       |          |
| ORD005   | 2024-01-02  | John Doe      |             | 450   | 50     | Office Supplies  | 0.3      |
| ORD046   | 2024-01-02  |               | CA          | 100   | 20     | Technology       | 0.3      |
| ORD026   | 2024-01-02  | John Doe      |             | 0     |        | Furniture        | 0.1      |
| ORD040   | 2024-01-02  |               | CA          | 450   | 20     | Office Supplies  | 0.3      |
| ORD011   | 2024-01-02  | Jane Smith    | CA          | 100   | 50     | Unknown          | 0.1      |
|          |             |               |             |       |        |                  |          |


## My Python Script Below:

```python

import pandas as pd

# this is where we load our data set. We're not using an API call, the data is on our local server

file_path = "messy_sales_data.csv"
df = pd.read_csv(file_path)

#check first 5 rows
print(df.head())

# check basic info
print(df.info())



# ------- this is where we find missing values ---------- # 

print("Missing Values Per Column:")
print(df.isnull().sum()) # the .isnull() function checks to see which columns are missing 


# ------- this is where we drop and fill columns that have errors ---------- # 

# Drop rows where 'Order ID' is missing (essential column)  
df = df.dropna(subset=["Order ID"])

# Fill missing 'Sales' values with the column mean
df['Sales'] = df['Sales'].fillna(df['Sales'].mean())

# Fill missing 'Category' with 'Unknown'
df['Category'] = df['Category'].fillna("Unknown")

# we use print() statements to check if our missing values have been handled. 
print("Missing Values After Cleaning:") 
print(df.isnull().sum())


# ------- this is where we standardize text columns (we format the data) ---------- # 

# Standardize 'State' column to title case
df['State'] = df['State'].str.strip().str.title()

# Standardize 'Category' column to lower case
df['Category'] = df['Category'].str.strip().str.lower()

# Standardize 'Customer Name' to title case
df['Customer Name'] = df['Customer Name'].str.strip().str.title()

# print statements to check on values 
print("Unique States:")
print(df['State'].unique())

print("Unique Categories:")
print(df['Category'].unique())



# ------- this is where we remove any duplicates ---------- # 

# we print out a statement and use methods to get the total sum of duplicated values
print("Number of Duplicates:", df.duplicated().sum())

# we use the drop_duplicates() method to drop any dupes
df = df.drop_duplicates()

# we confirm by printing a statement
print("Duplicates After Removal:", df.duplicated().sum())




# ------- this is where we correct any data types format ---------- # 

# Convert 'Date' column to datetime format and turns non-date entries in this column into NaT
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Check data types
print(df.info()) 

# Drop rows with non-date entries that have turned into NaT 
df = df.dropna(subset=['Date'])


# ------- this is where we handle any outliers ---------- # 

# Numerical columns like Sales and Profit may have invalid or extreme values.

# Find rows with negative 'Sales' values (check for negative values)
print("Negative Sales Values:")
print(df[df['Sales'] < 0])

# Replace negative 'Sales' with 0
df['Sales'] = df['Sales'].apply(lambda x: x if x > 0 else 0)

            # ----- below we use the Interquartile Range (IQR) method to identify and remove extreme outliers.

# Calculate IQR for 'Sales'
Q1 = df['Sales'].quantile(0.25)
Q3 = df['Sales'].quantile(0.75)
IQR = Q3 - Q1

# Define outlier bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers
df = df[(df['Sales'] >= lower_bound) & (df['Sales'] <= upper_bound)]


# check the cleaned datasheet
print("Cleaned Dataset:")
print(df.head())

print("Dataset Information:")
print(df.info())

# Save to a new CSV file
df.to_csv("cleaned_sales_data.csv", index=False)
print("Cleaned data saved to 'cleaned_sales_data.csv'")




