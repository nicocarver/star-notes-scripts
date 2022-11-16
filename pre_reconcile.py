import pandas as pd
panoptes = pd.read_csv("shape_extractor_rectangle_extractions.csv")
panoptes.drop(panoptes.iloc[:, 7:13], inplace = True, axis = 1)
panoptes.rename(columns={'data.frame0.T1_tool0_details':'annotations'}, inplace=True)
panoptes['annotations'] = panoptes.annotations.str.replace('gold_standard','')
panoptes['annotations'] = panoptes.annotations.str.replace('\, \'\'\:','')
panoptes['annotations'] = panoptes.annotations.str.replace(' False','')
panoptes.to_csv('pre_reconciled.csv', index=False)
