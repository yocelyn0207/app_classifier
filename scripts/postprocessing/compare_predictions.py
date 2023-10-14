import re
import os
from tqdm import tqdm
import pandas as pd

def comparePredictions(input_old_file_path: str, input_new_file_path: str, output_folder_path: str,
                      output_file_name: str):

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    output_file_path = output_folder_path + f'/{output_file_name}.csv'

    old_data = pd.read_csv(input_old_file_path)
    new_data = pd.read_csv(input_new_file_path)

    use_classes_previous = old_data.pop('predicted_use_classes')
    old_data['use_classes_previous'] = use_classes_previous

    use_classes_updated = new_data['predicted_use_classes']
    old_data['use_classes_updated'] = use_classes_updated

    old_data['use_classes_changed']=''
    old_data['use_classes_incorrect'] = ''
    #old_data['use_classes_changed_a1_or_tpo'] = ''

    for i, row in tqdm(old_data.iterrows(), total=len(old_data)):
        if row['use_classes_previous'] != row['use_classes_updated']:
            old_data.at[i, 'use_classes_changed'] = 'Y'
    #        if re.findall('a1|tpo',row['use_classes_previous']) != re.findall('a1|tpo',row['use_classes_updated']):
    #            old_data.at[i, 'use_classes_changed_a1_or_tpo'] = 'Y'
        if row['use_classes_updated'] != row['ground_truth_use_classes']:
            old_data.at[i, 'use_classes_incorrect'] = 'Y'

    old_data.to_csv(output_file_path, index=False)


comparePredictions(input_old_file_path ='/datasets/landstack_dataset_composite6/evaluation/wiltshireApps_20220322_results_17.csv',
                  input_new_file_path ='/datasets/landstack_dataset_composite6/evaluation/wiltshireApps_20220322_results_18.csv',
                  output_folder_path ='/datasets/landstack_dataset_composite6/evaluation',
                  output_file_name = 'wiltshireApps_20220322_results_comparison_17_vs_18.csv')