import re
import os
from tqdm import tqdm
import pandas as pd
import torch



def process_prediction(input_file_path: str, output_folder_path: str = None):
    '''
    The input file is the output prediction from BERT_Finetune_Multiclass.ipynb, which contains three columns: the
    planning note, the ground truth use class, and the logits. This function generates two tensors, the ground truth
    use_class tensor and the logits tensor, both of which have size (data_length, num of use classes).
    :param input_file_path: path of input file
    :param output_folder_path: path of output folder
    :return: a dictionary of two items, the ground truth use_class tensor and the logits tensor. We can choose the save
            the dictionary into a .pt file.
    '''
    data = pd.read_csv(input_file_path)
    logits_stack = torch.tensor([])
    golden_labels_stack = torch.tensor([])

    logits_not_equal_18 = 0

    #df = pd.DataFrame(columns=['text', 'sui generis', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2',
    #                           'b8', 'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'householder', 'tpo', 'other'])


    for _, row in tqdm(data.iterrows(), total=len(data)):
        text = row['text']
        golden_labels = row['ground_truth_use_classes'] # type(golden_labels) == string, e.g., tensor([0, 1, 1])
        logits = row['predicted_use_classes'] # type(logits) == string

        golden_labels = re.search('\[.+\]', golden_labels)
        golden_labels = golden_labels.group(0)[2:-2]
        golden_labels = golden_labels.split(',')
        golden_labels = [float(i) for i in golden_labels]
        golden_labels = torch.tensor(golden_labels)

        logits = logits[9:-3]
        logits = re.sub(' +', '', logits)
        logits = logits.split(',')
        logits = [float(i) for i in logits]
        logits = torch.tensor(logits)


        golden_labels_stack = torch.cat([golden_labels_stack, golden_labels.view(1,-1)])
        logits_stack = torch.cat([logits_stack, logits.view(1,-1)])



        '''df = df.append({
            "text": text,
            'sui generis': golden_labels[0].item(),
            'sui generis_p':logits[0].item(),
            'a1': golden_labels[1].item(),
            'a1_p':logits[1].item(),
            'a2': golden_labels[2].item(),
            'a2_p':logits[2].item(),
            'a3': golden_labels[3].item(),
            'a3_p':logits[3].item(),
            'a4': golden_labels[4].item(),
            'a4_p':logits[4].item(),
            'a5': golden_labels[5].item(),
            'a5_p':logits[5].item(),
            'b1': golden_labels[6].item(),
            'b1_p':logits[6].item(),
            'b2': golden_labels[7].item(),
            'b2_p':logits[7].item(),
            'b8': golden_labels[8].item(),
            'b8_p':logits[8].item(),
            'c1': golden_labels[9].item(),
            'c1_p':logits[9].item(),
            'c2': golden_labels[10].item(),
            'c2_p':logits[10].item(),
            'c3': golden_labels[11].item(),
            'c3_p':logits[11].item(),
            'c4': golden_labels[12].item(),
            'c4_p':logits[12].item(),
            'd1': golden_labels[13].item(),
            'd1_p':logits[13].item(),
            'd2': golden_labels[14].item(),
            'd2_p':logits[14].item(),
            'householder': golden_labels[15].item(),
            'householder_p':logits[15].item(),
            'tpo': golden_labels[16].item(),
            'tpo_p':logits[16].item(),
            'other': golden_labels[17].item(),
            'other_p':logits[17].item()
        }, ignore_index=True)



    df.to_csv('eva_result.csv')'''



    m = {'golden_labels': golden_labels_stack, 'logits': logits_stack}

    if output_folder_path is not None:
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        output_file_path = output_folder_path+'/ground_truth_and_logits_tensors.pt'
        torch.save(m, output_file_path)
        print('The ground truth use_class tensor and the logits tensor are save in {}'.format(output_file_path))



    return m












