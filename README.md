# ss

import pandas as pd

# create the initial dataframe
df = pd.DataFrame({'ID': [1, 2, 3], 'CODE': ['ABC', 'XYZ', 'LMN.'], 'CODE_DESC': ['A FOR APPLE', 'Z FOR ZEBRA', 'L FOR LOTUS']})

# create a list to hold the modified rows
new_rows = []

# iterate over the rows of the dataframe
for i, row in df.iterrows():
    # add the original row
    new_rows.append(row)

    # create a new row with modified values
    new_row = {'ID': row['ID'], 'CODE': 'CA-' + row['CODE'], 'CODE_DESC': 'CA-' + row['CODE_DESC']}
    # add the modified row
    new_rows.append(new_row)

# create a new dataframe with the modified rows
new_df = pd.DataFrame(new_rows)

# set the index to the ID column
new_df.set_index('ID', inplace=True)

# display the resulting dataframe
print(new_df)
