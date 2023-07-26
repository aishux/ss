
# Custom function to concatenate parent codes based on minimum and maximum parent levels
def concatenate_parent_codes(group):
    min_parent_code = group.loc[group['PARENT_LEVEL'].idxmin(), 'PARENT_CODE']
    max_parent_code = group.loc[group['PARENT_LEVEL'].idxmax(), 'PARENT_CODE']
    return f"[{min_parent_code}]&[{max_parent_code}]"

# Group by 'KPI_ID' and apply the custom function to create the 'PARENT_MEMBER' column
df['PARENT_MEMBER'] = df.groupby('KPI_ID').apply(concatenate_parent_codes).reset_index(drop=True)

print(df)
