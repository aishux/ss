# Prefix each full rule block with "### Rule"
df['rephrased_rules'] = df['rephrased_rules'].apply(lambda rules: [f"### Rule\n{rule}" for rule in rules])

# Explode the rules into separate rows
df_exploded = df.explode('rephrased_rules').reset_index(drop=True)

# Optional: To view the full content in console
pd.set_option('display.max_colwidth', None)
print(df_exploded[['split_rules', 'rephrased_rules']])
