import os

import numpy as np
from tqdm import tqdm
import json
import math

from dotenv import load_dotenv
import pandas as pd
import openai

from scripts.preprocessing.application_type_classifier.type_set import *
from scripts.inferencing.application_type_classifier.process_input import process_input
from scripts.inferencing.application_type_classifier.inference_a_batch_of_data import inference_a_batch_of_planning_notes_by_GPT






def inference_setup(env_path: str,
                    input_planning_note_list: list = None,
                    input_planning_note_file: str = None,
                    lineterminator_of_input_file: str = '\n',
                    truncate_input_planning_note_into_length: int = 1000,
                    type_mapping_file: str = None,
                    use_hard_coded_type: bool = True,
                    GPT_finetuned_model_name: str = 'ada:ft-thovex-ltd:app-type-and-use-class-classifier-2023-04-24-01-13-26',
                    max_output_tokens: int = 1000,
                    batch_size: int = 20,
                    save_dir: str = None,
                    save_file_name: str = None):
    '''
    This function takes EITHER a .csv file OR a list (of dictionaries) (format stated as below) as input, and predicts
    4 things at the same time: 1) demolition of use classes, 2) erection of use classes, 3) application type and
    4) change of use tag ('Y' or '').

    :param env_path: file path to .env openAI password
    :param input_planning_note_list: a list of input contents to be processed.
            It can be a list of planning note strings, e.g.,
            ['Erection of 3no. dwellings and associated works and the demolition of existing extension.',
            'Change of use from use class B2 (General Industrial) and ancillary offices to flexible use class E(g)(iii) (Industrial Processes)',
            'Change of use from offices (class E (g)) to 12no. studio apartments (class C3)'],
            or a list of dictionaries which contain below keys -
              "Planning Reference",
              "Planning Note" or "planning_notes" or "planning_note",
              "Type"(optional, record from councils in our date base),
              "Demolition"(optional, prediction from previous T5 model, works as ground truth labels),
              "Erection"(optional, prediction from previous T5 model, works as ground truth labels),
              "Type_new"(optional, type name inferenced by keywords in the planning note, should be one of the merged 33 types, works as ground truth labels),
            e.g.,
            [{"Planning Reference": "S/21/1399",
            "Planning Note": "Erection of 3no. dwellings and associated works and the demolition of existing extension.",
            "Type": "Full Application: Change of Use",
            "Demolition": "[]",
            "Erection": "['c3']",
            "Type_new": "Full Application"},
            {"Planning Reference": "S/21/1961",
            "Planning Note": "Change of use from use class B2 (General Industrial) and ancillary offices to flexible use class E(g)(iii) (Industrial Processes), B2 (General Industrial) and/or B8 (Storage or Distribution) and ancillary offices.",
            "Type": "Largescale Major full"},
            "Demolition": "['b1', 'b2']",
            "Erection": "['b1', 'b2', 'b8']",
            "Type_new": "Full Application"},
            {"Planning Reference": "S/22/0244",
            "Planning Note": "Change of use from offices (class E (g)) to 12no. studio apartments (class C3) and associated works.",
            "Type": "Full Application Major",
            "Demolition": "['b1']",
            "Erection": "['c3']",
            "Type_new": "Full Application"}].
    :param input_planning_note_file: path to an input .csv file to be processed. The file should contain below
            columns -
              "Planning Reference",
              "Planning Note" or "planning_notes" or "planning_note",
              "Type"(optional, record from councils in our date base),
              "Demolition"(optional, prediction from previous T5 model, works as labels),
              "Erection"(optional, prediction from previous T5 model, works as labels),
              "Type_new"(optional, type name inferenced by keywords in the planning note, should be one of the merged 33 types, works as labels)
    :param lineterminator_of_input_file: the lineterminator of input_planning_note_file.
    :param truncate_input_planning_note_into_length: truncate each planning note string into a certain length incase
                                                     exceeding GPT input limitation. Please note this variable truncates
                                                     string length rather than token no.
    :param type_mapping_file: a json file for hard coding.
    :param use_hard_coded_type: if True and when the application has an old type name from the council, the model will
                                 search its new type name from the type_mapping_file first, in which case the new type
                                 name is inferenced from its old type name by searching a predefined dictionary.
                                 When its new type name cannot be found, the application will then be fed into GPT3, in
                                 which case the new type name is inferenced from the application text.
                                 If False the application will be fed into GPT3 directly.
                                 When one application in our input has an old type name, please set it as True to ensure
                                 the accuracy of predictions. Otherwise, please set it as False to save some searching time.
    :param GPT_finetuned_model_name: the name of finetuned GPT model.
    :param max_output_tokens: the max num of tokens to be generated. Please set it big enough. On one hand, we've set the
                       stop token ' END', from where the model will stop generating further tokens. Therefore, a big
                       num will not waste budget. On the other hand, if the num is too small, the model is not able to
                       generate enough tokens.
    :param batch_size: the number of planning notes processed at one time. Must be an integer no greater than 20.
    :param save_dir: the directory of the results to be saved.
    :param save_file_name: the file name of the results to be saved. Please do NOT include the filename extension.
                           The results will be saved into a .csv file automatically, which includes below columns -
                           "reference", "planning_note", "type_from_councils",
                           "label_of_demolition", "label_of_erection",
                           "label_of_type_from_text", "label_of_change_of_use,
                           "planning_note_for_GPT", "type_hard_coded", "type", "demolition","erection","change_of_use",
                           "correctness_check_of_type","correctness_check_of_demolition","correctness_check_of_erection",
                           "correctness_check_of_change_of_use".
    :return: if both save_dir and save_file_name is None, return a dictionary with planning references as keys
            and predictions as values, e.g.,
            {
             'S/16/0095': {'demolition': ['c3'], 'erection': [], 'application_type': 'Other', 'change_of use': ''},
             'S/16/0096': {'demolition': [], 'erection': ['sui generis'], 'application_type': 'Full Application', 'change_of use': ''},
             'S/17/0205': {'demolition': ['c1'], 'erection': ['a1','b8'], 'application_type': 'Outline Application', 'change_of use': 'Y'}
            }.

    '''

    load_dotenv(dotenv_path=env_path)
    openai.api_key = os.getenv('PASSWORD')

    if batch_size > 20:
        raise ValueError('Batch_size must be no greater than 20.')


    if save_dir is not None and save_file_name is not None:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    elif save_dir is None and save_file_name is None:
        pass
    else:
        raise ValueError('Please pass BOTH save_dir and save_file_name or NEITHER of them.')

    ###################################################################################################################
    # Read input data.
    ###################################################################################################################
    input_df = process_input(input_planning_note_list = input_planning_note_list,
                             input_planning_note_file = input_planning_note_file,
                             lineterminator_of_input_file = lineterminator_of_input_file)
    input_df['planning_note_for_GPT'] = input_df['planning_note'].str.slice(0, truncate_input_planning_note_into_length) + '\n\n###\n\n'
    input_df['type_hard_coded'] = np.nan
    input_df['type'] = np.nan
    input_df['demolition'] = np.nan
    input_df['erection'] = np.nan
    input_df['change_of_use'] =''

    input_df['correctness_check_of_type'] = np.nan
    input_df['correctness_check_of_demolition'] = np.nan
    input_df['correctness_check_of_erection'] = np.nan
    input_df['correctness_check_of_change_of_use'] = np.nan


    ###################################################################################################################
    # Filter out planning notes that need to be sent to GPT.
    # For some planning notes that have type names from councils, they need to follow our hard coded mapping rules first.
    # If cannot be mapped, then send them to GPT and inference their types by the planning note text.
    ###################################################################################################################
    if use_hard_coded_type is True:
        try:
            with open(type_mapping_file) as f:
                type_mapping_dict = json.load(f)
        except:
            raise ValueError('Please pass type_mapping_file.')

        input_df['type'] = input_df['type_hard_coded'] = input_df['type_from_councils'].map(type_mapping_dict)
        types_without_use_classes_mapping_dict = {x:[] for x in types_without_use_classes}
        input_df['demolition'] = input_df['erection'] = input_df['type_hard_coded'].map(types_without_use_classes_mapping_dict)
        no_demolition_row_indices = list(input_df[input_df['demolition'].notnull()].index)
        planning_notes_for_GPT = input_df[input_df['demolition'].isna()]['planning_note'] # exclude type_without_use_classes
    else:
        no_demolition_row_indices = []
        planning_notes_for_GPT = input_df['planning_note']


    ###################################################################################################################
    # Get inferences from GPT.
    ###################################################################################################################
    batch_num = int(math.ceil(len(planning_notes_for_GPT) / batch_size))

    for i in tqdm(range(batch_num)):

        start_index = i * batch_size
        if batch_num == 1:
            end_index = -1
        else:
            end_index = (i+1)*batch_size

        if i == batch_num-1:
            a_batch_of_planning_notes = planning_notes_for_GPT[start_index:]
        else:
            a_batch_of_planning_notes =  planning_notes_for_GPT[start_index:end_index]

        row_indices = list(a_batch_of_planning_notes.index)

        demolitions, erections, app_types, changes_of_use = \
            inference_a_batch_of_planning_notes_by_GPT(planning_notes = list(a_batch_of_planning_notes),
                                                       GPT_finetuned_model_name = GPT_finetuned_model_name,
                                                       max_tokens = max_output_tokens)

        new_column_of_type = pd.Series(app_types, name='type', index=row_indices)
        input_df.update(new_column_of_type, overwrite=False) # if already exists value by hard coding, don't update
        input_df.loc[row_indices, 'demolition'] = demolitions
        input_df.loc[row_indices, 'erection'] = erections
        input_df.loc[row_indices, 'change_of_use'] = changes_of_use


    ###################################################################################################################
    # Convert demolition, erection string into list.
    ###################################################################################################################
    input_df['label_of_demolition'] = input_df['label_of_demolition'].map(lambda x: pd.eval(x, engine='python'))
    input_df['label_of_erection'] = input_df['label_of_erection'].map(lambda x: pd.eval(x, engine='python'))
    input_df['demolition'] = input_df['demolition'].map(lambda x: pd.eval(x, engine='python'))
    input_df['erection'] = input_df['erection'].map(lambda x: pd.eval(x, engine='python'))


    ###################################################################################################################
    # Correctness check.
    ###################################################################################################################
    if len(input_df['label_of_type_from_text'].value_counts()) != 0:
        non_null_type_hard_coded_row_indices = list(input_df[input_df['type_hard_coded'].notnull()].index)
        input_df.loc[non_null_type_hard_coded_row_indices, 'correctness_check_of_type'] = 'Ignore'

        comparison_column = np.where(input_df["label_of_type_from_text"] == input_df["type"], True, False)
        comparison_column = pd.Series(comparison_column, name='correctness_check_of_type')
        input_df.update(comparison_column, overwrite=False)

    if len(input_df['label_of_demolition'].value_counts()) != 0:
        input_df.loc[no_demolition_row_indices, 'correctness_check_of_demolition'] = 'Ignore'

        comparison_column = np.where(input_df["label_of_demolition"] == input_df["demolition"], True, False)
        comparison_column = pd.Series(comparison_column, name='correctness_check_of_demolition')
        input_df.update(comparison_column, overwrite=False)

    if len(input_df['label_of_erection'].value_counts()) != 0:
        input_df.loc[no_demolition_row_indices, 'correctness_check_of_erection'] = 'Ignore'

        comparison_column = np.where(input_df["label_of_erection"] == input_df["erection"], True, False)
        comparison_column = pd.Series(comparison_column, name='correctness_check_of_erection')
        input_df.update(comparison_column, overwrite=False)

    if len(input_df['label_of_change_of_use'].value_counts()) != 0:
        input_df.loc[no_demolition_row_indices, 'correctness_check_of_change_of_use'] = 'Ignore'

        comparison_column = np.where(input_df["label_of_change_of_use"] == input_df["change_of_use"], True, False)
        comparison_column = pd.Series(comparison_column, name='correctness_check_of_change_of_use')
        input_df.update(comparison_column, overwrite=False)


    ###################################################################################################################
    # Output file.
    ###################################################################################################################
    if save_dir is not None and save_file_name is not None:
        input_df.to_csv(os.path.join(save_dir,save_file_name+'.csv'),index=False)
    elif save_dir is None and save_file_name is None:
        input_df = input_df[["reference", "demolition","erection","type","change_of_use"]]
        input_df = input_df.rename(columns={"type": "application_type"})
        input_df.fillna('', inplace=True)

        if len(input_df['reference'].value_counts()) == 0: # if reference is empty, use index as keys
            input_df_keys = input_df.index
        else:
            input_df_keys = input_df['reference']

        input_df.set_index('reference', inplace=True)
        input_df_values = input_df.to_dict(orient='records')
        input_df = dict(zip(input_df_keys, input_df_values))

        return input_df



