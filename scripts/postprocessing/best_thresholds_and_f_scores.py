import pandas as pd
import torch
import numpy as np
from numpy import argmax
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import precision_recall_fscore_support


def find_best_thresholds(input_dict_of_tensors: dict = None,
                         use_classes: list = ['sui generis', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b8', 'c1',
                                              'c2', 'c3', 'c4', 'd1', 'd2', 'householder', 'tpo', 'other']):

    golden_labels = input_dict_of_tensors['golden_labels']
    logits = input_dict_of_tensors['logits']

    best_threholds = []
    for n, _ in enumerate(use_classes):
        precision, recall, thresholds = precision_recall_curve(golden_labels[:, n:n+1], logits[:, n:n+1])
        fscore = (2 * precision * recall) / (precision + recall)
        ix = argmax(fscore)
        best_threholds.append(thresholds[ix])

    return best_threholds


def f_scores(input_dict_of_tensors: dict = None,
                                      use_classes: list = ['sui generis', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2',
                                                           'b8', 'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'householder',
                                                           'tpo', 'other'],
                                      thresholds: list = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                                          0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                output_save_folder_path: str = 'datasets/landstack_dataset_composite6/evaluation',
                                output_save_file_name: str = 'best_threholds_and_f_scores'):


    golden_labels = input_dict_of_tensors['golden_labels']
    logits = input_dict_of_tensors['logits']
    thresholds = torch.tensor(thresholds)

    scores = precision_recall_fscore_support(golden_labels, logits > thresholds, average=None)
    df = pd.DataFrame(np.around(np.concatenate([thresholds.view(1,-1), scores[:3]]), decimals=3), index=['best_threholds','precision', 'recall', 'f1'], columns=use_classes)

    output_save_file_path = output_save_folder_path + f'/{output_save_file_name}.csv'
    df.to_csv(output_save_file_path)








