import pandas as pd

# Read in the classifications and reconciled CSV
class_df = pd.read_csv("f.csv")
reconcile_df = pd.read_csv("g.csv")

# subset the data based on workflow
clean_df = class_df.loc[(class_df.workflow_id == 12765) & (class_df.workflow_version == 5.28)].copy()

# Delete unnecessary columns
clean_df.drop(class_df.iloc[:, 0:12], inplace = True, axis = 1)

# Merge the cleaned up classification file with the reconciled data
df_merge_col = pd.merge(clean_df, reconcile_df, left_on='subject_ids', right_on='subject_id')

# write new csv
df_merge_col.to_csv('new.csv', index=False)
