import os
import pandas as pd
import numpy as np



def convert_trainset_for_GPT3(input_file_path:str,file_save_path:str, file_save_name:str,
                              train_set_percetage:float = 0.7):

    df = pd.read_csv(input_file_path,dtype= {"unit_num":"str"})

    df.rename(columns={"planning_note": "prompt", "unit_num_sequence":"completion"},inplace=True)
    df['prompt'].replace('', np.nan, inplace=True)
    df['completion'].replace('', '0', inplace=True)
    df = df.dropna(subset=['prompt'])


    if os.path.exists(file_save_path) is None:
        os.makedirs(file_save_path)

    df.to_csv(os.path.join(file_save_path,f'{file_save_name}.csv'), index=False)

    train, valid = np.split(df.sample(frac=1),[int(train_set_percetage * len(df))])
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
    input_file_path = 'datasets/resi_unit_num/appsWithSizeAndUnits_20230223.csv'
    file_save_path = 'datasets/resi_unit_num'
    file_save_name = 'appsWithSizeAndUnits_20230223_GPT3'
    train_set_percetage = 0.7
    convert_trainset_for_GPT3(input_file_path, file_save_path, file_save_name, train_set_percetage)
