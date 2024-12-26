import pandas as pd
import os

# get the directory of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
# input file path
file_path = os.path.join(dir_path, 'input', 'Customer_Call_List.xlsx')

df = pd.read_excel(file_path)
print("original data\n", df)

# remove duplicates
df = df.drop_duplicates()

# remove cloumns I don't need
df = df.drop(columns="Not_Useful_Column")

# standardize Last_Name column
## using left & right strip

# df["Last_Name"] = df["Last_Name"].str.lstrip("...")
# df["Last_Name"] = df["Last_Name"].str.lstrip("/")
# df["Last_Name"] = df["Last_Name"].str.rstrip("_")

## using strip all characters together: numbers, ., /, _, etc
df["Last_Name"] = df["Last_Name"].str.strip("123./_")

# standardize Phone_Number column: 123-345-7890
## step 1: repalce all non-alphanumeric values with nothing
df["Phone_Number"] = df["Phone_Number"].str.replace('[^a-zA-Z0-9]', "", regex=True)

## step 2: note the non string values like NaN,... so that's why they should be all string  
df["Phone_Number"] = df["Phone_Number"].apply(lambda x: str(x))
## step 3: apply lambda func (it can be also done using a for loop)
df["Phone_Number"] = df["Phone_Number"].apply(lambda x: x[0:3] + "-" + x[3:6] + "-" + x[6:10])
## step 4: remvoe nan-- values
df["Phone_Number"] = df["Phone_Number"].str.replace("nan--", "")
df["Phone_Number"] = df["Phone_Number"].str.replace("Na--", "")

# standardize Address column
df[["Street Address", "State", "Zip"]]= df["Address"].str.split(',', n=2, expand=True)

# standardize Paying Customer Do_Not_Contact 
df["Paying Customer"] = df["Paying Customer"].str.replace("Yes", "Y")
df["Paying Customer"] = df["Paying Customer"].str.replace("No", "N")
df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace("Yes", "Y")
df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace("No", "N")

# remove N/a
df = df.replace("N/a", "")

# remove NaN
df = df.fillna("")

# remove rows that either have no number or they're no contact
for x in df.index:
    if df.loc[x, "Do_Not_Contact"] == "Y":
        df.drop(x, inplace=True)

for x in df.index:
    if df.loc[x, "Phone_Number"] == "":
        df.drop(x, inplace=True)

# drop the Address column
df = df.drop(columns=["Address"])

# rest the indexes
df = df.reset_index(drop=True)


print("cleaned data\n", df)
