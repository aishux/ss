import pandas as pd

# Assuming you have your DataFrame already loaded, replace the data below with your actual DataFrame
data = {
    'KPI_ID': ['CA10461', 'CA10461', 'CA50205', 'CA50205', 'CA1','CA1'],
    'KPI_NAME': ['Return on Assets', 'Return on Assets', 'Return on Business Volume', 'Return on Business Volume', 'A&L','B&L'],
    'PARENT_CODE': [1, 'ALK10', 2, 'ALK12','ALK10','ALK100'],
    'PARENT_LEVEL': [2, 3, 2, 3, 3, 4],
    'PARENT_DESC': ['Assets & Liabilities', 'Cumulative Volumes', 'Assets & Liabilities', 'Cumulative Volumes', 'AAL', 'BVL']
}

df = pd.DataFrame(data)

# Custom function to concatenate parent codes based on minimum and maximum parent levels
def concatenate_parent_codes(group):
    min_parent_code = group.loc[group['PARENT_LEVEL'] == group['PARENT_LEVEL'].min(), 'PARENT_CODE']
    max_parent_code = group.loc[group['PARENT_LEVEL'] == group['PARENT_LEVEL'].max(), 'PARENT_CODE']
    parent_member_output = f"[{min_parent_code.iloc[0]}]&[{max_parent_code.iloc[0]}]"
    group["PARENT_MEMBER"] = parent_member_output
    return group

# Group by 'KPI_ID' and apply the custom function to create the 'PARENT_MEMBER' column
grouped = df.groupby('KPI_ID').apply(concatenate_parent_codes).reset_index(drop=True)
grouped = grouped.drop_duplicates(subset=['KPI_ID'], keep='last').reset_index(drop=True)

print(grouped.to_string())
