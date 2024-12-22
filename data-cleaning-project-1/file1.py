#this project is to clean up messy sales data and explains each step used

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








