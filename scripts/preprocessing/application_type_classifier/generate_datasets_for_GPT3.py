import os
import pandas as pd
import numpy as np

from scripts.preprocessing.application_type_classifier.type_set import *



def convert_trainset_for_GPT3(input_file_path:str,file_save_path:str, file_save_name:str,
                              train_set_percentage:float = 0.7):

    df = pd.read_csv(input_file_path)


    df.rename(columns={"planning_notes": "prompt"},inplace=True)

    df['demolitions_new'] = df['demolitions'].str.strip('[]')
    df['erections_new'] = df['erections'].str.strip('[]')


    df['demolitions_new'] = df['demolitions_new'].str.replace("'", '')
    df['erections_new'] = df['erections_new'].str.replace("'", '')

    for type in types_without_use_classes:
        df.loc[df["type_new"] == type, "demolitions_new"] = ''
        df.loc[df["type_new"] == type, "erections_new"] = ''

    df.change_of_use = df.change_of_use.fillna('')

    df['completion'] = "Demolitions: " + df['demolitions_new'] + ", Erections: " + df['erections_new'] + \
                       ", Type: " + df['type_new'] + ', Change of Use: ' + df['change_of_use']


    if os.path.exists(file_save_path) is None:
        os.makedirs(file_save_path)

    df.to_csv(os.path.join(file_save_path,f'{file_save_name}.csv'), index=False)

    train, valid = np.split(df.sample(frac=1),[int(train_set_percentage * len(df))])
    train.to_csv(os.path.join(file_save_path, f'{file_save_name}_train.csv'), index=False)
    valid.to_csv(os.path.join(file_save_path, f'{file_save_name}_valid.csv'), index=False)


    train_new = pd.DataFrame()
    train_new['prompt'] = train['prompt'] + "\n\n###\n\n"
    train_new['completion'] = train['completion'] + " END"
    train_new.to_json(os.path.join(file_save_path, f'{file_save_name}_train.jsonl'),orient='records', lines=True)

    valid_new = pd.DataFrame()
    valid_new['prompt'] = valid['prompt'] + "\n\n###\n\n"
    valid_new['completion'] = valid['completion'] + " END"
    valid_new.to_json(os.path.join(file_save_path, f'{file_save_name}_valid.jsonl'),orient='records', lines=True)

if __name__ == '__main__':
    input_file_path = 'datasets/application_type_classifier/historic_data_20230119_with_use_classes_from_v1.31_epoch97_type_new_20230423.csv'
    file_save_path = 'datasets/application_type_classifier'
    file_save_name = 'historic_data_20230119_with_use_classes_from_v1.31_epoch97_type_new_20230423_GPT3'
    train_set_percentage = 0.35
    convert_trainset_for_GPT3(input_file_path, file_save_path, file_save_name, train_set_percentage)
