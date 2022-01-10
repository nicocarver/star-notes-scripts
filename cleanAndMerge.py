# This script uses the pandas library extensively. I'm using the common shorthand 'pd'
import pandas as pd

# Read in the classifications and reconciled CSV. Change these file names
class_df = pd.read_csv("star-notes-classifications.csv")
reconcile_df = pd.read_csv("reconciled.csv")

# subset the data based on workflow. Change this to agree with the reconciled file above
clean_df = class_df.loc[(class_df.workflow_version == 6.29)].copy()

# Don't change anything below this line

# drop duplicate column from reconciled csv
reconcile_df = reconcile_df.drop(reconcile_df.columns[1], axis=1)

# everything lowercase
reconcile_df['annotations'] = reconcile_df.annotations.str.lower()

# remove formatting
reconcile_df['annotations'] = reconcile_df.annotations.str.replace('\'','')
reconcile_df['annotations'] = reconcile_df.annotations.str.replace('\[','')
reconcile_df['annotations'] = reconcile_df.annotations.str.replace('\]','')
reconcile_df['annotations'] = reconcile_df.annotations.str.replace('\{','')
reconcile_df['annotations'] = reconcile_df.annotations.str.replace('\}','')
reconcile_df['annotations'] = reconcile_df.annotations.str.replace('text:','')
clean_df['subject_data'] = clean_df.subject_data.str.replace('"' , '')
clean_df['subject_data'] = clean_df.subject_data.str.replace('!' , '')
clean_df['subject_data'] = clean_df.subject_data.str.replace('}' , '')

# Delete unnecessary columns
clean_df.drop(class_df.iloc[:, 0:12], inplace = True, axis = 1)

# pull out Phaedra info into seperate data frames
df_url = clean_df.subject_data.str.split(",").str[-6]
df_img_id = clean_df.subject_data.str.split(",").str[-5]
df_item_id = clean_df.subject_data.str.split(",").str[-4]
df_page_sequence = clean_df.subject_data.str.split(",").str[-1]

# remove unnecessary values
df_url = df_url.str.replace('url:','')
df_img_id = df_img_id.str.replace('img_id:','')
df_item_id = df_item_id.str.replace('item_id:','')
df_page_sequence = df_page_sequence.str.replace('page_sequence:','')

# add the Phaedra info back in as seperate columns
clean_df['url'] = df_url
clean_df['img_id'] = df_img_id
clean_df['item_id'] = df_item_id
clean_df['page_sequence'] = df_page_sequence

# Merge the cleaned up classification file with the reconciled data
df_merge_col = pd.merge(clean_df, reconcile_df, left_on='subject_ids', right_on='subject_id')
df_merge_col = df_merge_col.drop_duplicates()

# delete subject_data column
df_merge_col.drop(['subject_data'], inplace = True, axis = 1)

# remove blank rows
df_merge_col.dropna(axis = 0, how = 'any', inplace = True)

# extract numerics in to new dataframe
df_messy_premerge1 = df_merge_col[~df_merge_col['annotations'].str.contains('[A-Za-z]')]
df_merge_col = df_merge_col[~df_merge_col.apply(tuple,1).isin(df_messy_premerge1.apply(tuple,1))]

# seperate other messy rows in to new dataframe
df_merge_clean = df_messy_premerge1[~df_merge_col.annotations.str.contains("\*|\d*\/|kg|jd|ngc|\#|\(|\)|\.|\=|\?", na=False)].copy()
df_messy_premerge2 = df_merge_col[~df_merge_col.apply(tuple,1).isin(df_merge_clean.apply(tuple,1))]

# concatenate two messy dataframes
df_messy = pd.concat([df_messy_premerge1, df_messy_premerge2], ignore_index=True)

# cosmetic changes
df_merge_clean['annotations'] = df_merge_clean['annotations'].apply(lambda s: ', '.join(set(s.split(', '))))
df_merge_clean['annotations'] = df_merge_clean['annotations'].str.replace(' ', '')
df_merge_clean['annotations'] = df_merge_clean['annotations'].str.replace('plate', '')
df_merge_clean['annotations'] = df_merge_clean['annotations'].str.replace(r'\\n','', regex=True)
df_merge_clean['annotations'] = df_merge_clean['annotations'].str.replace('^\,','', regex=True)
df_merge_clean.rename(columns={'annotations':'plate_numbers'}, inplace=True)

# delete subject_ids column
df_merge_clean.drop(['subject_ids'], inplace = True, axis = 1)

# write two csvs
df_messy.to_csv('messy.csv', index=False)
df_merge_clean.to_csv('clean.csv', index=False)
