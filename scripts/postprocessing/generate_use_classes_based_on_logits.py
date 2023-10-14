import os
import re
from tqdm import tqdm
import csv
import pandas as pd

import torch

def generate_use_classes_based_on_logits(input_file_path: str, best_threholds:list = [0.5]*18,
                                         use_classes:list = ['sui generis', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b8',
                                                        'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'householder', 'tpo', 'other'],
                                         output_folder_path:str = 'datasets/landstack_dataset_composite6/evaluation',
                                         output_file_name:str = 'test_reults'):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    output_file_path = output_folder_path + f'/{output_file_name}.csv'

    best_threholds = torch.tensor(best_threholds)

    data = pd.read_csv(input_file_path)

    with open(output_file_path, 'w') as f:
        wr = csv.writer(f)
        wr.writerow(['text', 'ground_truth_use_classes', 'predicted_use_classes', 'incorrect_predictions'])

        for i, row in tqdm(data.iterrows(),total=len(data)):
            text = row['text']

            ground_truth_use_classes = row['ground_truth_use_classes']
            ground_truth_use_classes = re.search('\[.+\]', ground_truth_use_classes)
            ground_truth_use_classes = ground_truth_use_classes.group(0)[2:-2]
            ground_truth_use_classes = ground_truth_use_classes.split(',')
            ground_truth_use_classes = [float(i) for i in ground_truth_use_classes]
            ground_truth_use_classes = torch.tensor(ground_truth_use_classes)
            ground_truth_use_classes_indices = (ground_truth_use_classes == 1).nonzero(as_tuple=True)[0]
            ground_truth_use_classes_tags = [use_classes[i.item()] for i in ground_truth_use_classes_indices]

            predicted_use_classes_logits = row['predicted_use_classes']
            predicted_use_classes_logits = predicted_use_classes_logits[9:-3]
            predicted_use_classes_logits = re.sub(' +', '', predicted_use_classes_logits)
            predicted_use_classes_logits = predicted_use_classes_logits.split(',')
            predicted_use_classes_logits = [float(i) for i in predicted_use_classes_logits]
            predicted_use_classes_logits = torch.tensor(predicted_use_classes_logits)
            predicted_use_classes_one_hot = torch.where(predicted_use_classes_logits >= best_threholds,1,0)
            predicted_use_classes_indices = (predicted_use_classes_one_hot == 1).nonzero(as_tuple=True)[0]
            predicted_use_classes_tags = [use_classes[i.item()] for i in predicted_use_classes_indices]

            if ground_truth_use_classes_tags!=predicted_use_classes_tags:
                incorrect_predictions = 'Y'
            else:
                incorrect_predictions = None
            wr.writerow([text, ground_truth_use_classes_tags, predicted_use_classes_tags,incorrect_predictions])



