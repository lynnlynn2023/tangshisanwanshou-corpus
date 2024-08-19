import pandas as pd

# Load the two CSV files
zhongxiao_df = pd.read_csv('zhongxiao_with_popularity.csv')
songci_df = pd.read_csv('songci_with_popularity.csv')
tangshi_df = pd.read_csv('唐诗鉴赏辞典_with_popularity.csv')

# Extract the first 11 characters of the "Poem" column for both DataFrames
zhongxiao_df['Poem_prefix'] = zhongxiao_df['Poem'].str[:11]
songci_df['Poem_prefix'] = songci_df['Poem'].str[:11]
tangshi_df['Poem_prefix'] = tangshi_df['Poem'].str[:11]

# Find the rows in zhongxiao_df that have a matching "Poem_prefix" in songci_df
duplicates = zhongxiao_df[zhongxiao_df['Poem_prefix'].isin(
    songci_df['Poem_prefix'].tolist() + tangshi_df['Poem_prefix'].tolist())]

# Remove duplicates from zhongxiao_df
zhongxiao_final_df = zhongxiao_df[~zhongxiao_df['Poem_prefix'].isin(duplicates['Poem_prefix'])]

# Drop the temporary "Poem_prefix" column
zhongxiao_final_df = zhongxiao_final_df.drop(columns=['Poem_prefix'])

# Save the final DataFrame to a new CSV file
output_path = 'zhongxiao_final.csv'
zhongxiao_final_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"Duplicates removed and final data saved to {output_path}")
