# This script uses the pandas python library
import pandas as pd

# Read in the classifications and reconciled CSV. Change these file names
class_df = pd.read_csv("star-notes-classifications.csv")
reconcile_df = pd.read_csv("fleming_1st_month_reconciled_5.28.csv")

# subset the data based on workflow. Change this to agree with the reconciled file above
clean_df = class_df.loc[(class_df.workflow_id == 12765) & (class_df.workflow_version == 5.28)].copy()

# Don't change anything below this line

# drop duplicate column from reconciled csv
reconcile_df = reconcile_df.drop(reconcile_df.columns[1], axis=1)

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
df_url = clean_df.subject_data.str.split(",").str[-4]
df_img_id = clean_df.subject_data.str.split(",").str[-3]
df_item_id = clean_df.subject_data.str.split(",").str[-2]
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

# delete subject_id and subject_data columns
df_merge_col.drop(['subject_id','subject_ids','subject_data'], inplace = True, axis = 1)

# write new csv
df_merge_col.to_csv('new.csv', index=False)
