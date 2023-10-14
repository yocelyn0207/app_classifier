import os
from tqdm import tqdm
import csv

from dotenv import load_dotenv
import pandas as pd
import openai






def inference_setup(env_path: str,
                    GPT_finetuned_model_name: str = 'ada:ft-thovex-ltd:unit-num-extraction-2023-02-24-01-22-14',
                    max_tokens: int = 15,
                    vote_from_num_of_predictions: int = 3,
                    input_planning_note_list: list = None,
                    input_planning_note_file: str = None,
                    save_dir: str = None,
                    save_file_name: str = None):
    '''
    This function takes EITHER a .csv file OR a list (of dictionaries) (format stated as below) as input, and extracts
    the number of residential units to be built (the output type is string rather than int). The output will be
    'indeterminate' when unit num is not specified in the planning note.

    NOT ALL APPLICATIONS NEED TO BE FED INTO THIS MODEl. ONLY when its type is in below set AND its erection use classes
    contain c1, c2, c3 and/or c4.
    {Section 73, Section 106, Prior Notification, Permitted Development, Reserved Matters,
    Certificate of Lawfulness for Proposed or Existing Use, Permission in Principle, Technical Details Consent,
    County Matters Application, Councils Own Application (Reg3/Reg4), Neighbouring Authority Application,
    Hybrid Application, Outline Application, Full Application, Listed Building Application, Conservation Area}

    :param env_path: file path to .env openAI password
    :param GPT_finetuned_model_name: the name of finetuned GPT model.
    :param max_tokens: the max num of tokens to be generated. Please set it big enough. On one hand, we've set the
                       stop token ' END', from where the model will stop generating further tokens. Therefore, a big
                       num will not waste budget. On the other hand, if the num is too small, the model is not able to
                       generate
    :param vote_from_num_of_predictions: the number of times the model will run for one application. Must be a
                                         number >= 1. If > 1, it will then use the most common prediction as final
                                         result to against unstable outputs.
    :param input_planning_note_list: a list of input contents to be processed.
            It can be a list of planning note strings, e.g.,
            ['Erection of 3no. dwellings and associated works and the demolition of existing extension.',
            'Change of use from use class B2 (General Industrial) and ancillary offices to flexible use class E(g)(iii) (Industrial Processes)',
            'Change of use from offices (class E (g)) to 12no. studio apartments (class C3)'],
            or a list of dictionaries which contain below keys -
              "Planning Reference",
              "Planning Note" or "planning_notes" or "planning_note",
              "Unit Num"(optional, manually labeled, works as ground truth labels),
          e.g.,
            [{"Planning Reference": "S/21/1399",
            "Planning Note": "Erection of 3no. dwellings and associated works and the demolition of existing extension.",
            "Unit Num": "3"},
            {"Planning Reference": "S/21/1961",
            "Planning Note": "Change of use from use class B2 (General Industrial) and ancillary offices to flexible use class E(g)(iii) (Industrial Processes), B2 (General Industrial) and/or B8 (Storage or Distribution) and ancillary offices.",
            "Unit Num": "0"}
            {"Planning Reference": "S/22/0244",
            "Planning Note": "Change of use from offices (class E (g)) to 12no. studio apartments (class C3) and associated works.",
            "Unit Num": "12"}].
    :param input_planning_note_file: the path to the input .csv file to be processed. The file should contain below
            columns -
              "Planning Reference",
              "Planning Note" or "planning_notes" or "planning_note",
              "Unit Num"(optional, manually labeled, works as ground truth labels),
    :param save_dir: the directory of the results to be saved.
    :param save_file_name: the file name of the results to be saved. Please do NOT include the filename extension.
                           The results will be saved into a .csv file automatically, which includes below columns -
                           "Planning Reference", "Planning Note", "Unit Num",'Unit Num Sequence',
                           "Label of Unit Num"(if applicable), "Correctness Check" (if applicable).
    :return result: return a dictionary with planning references as keys and predictions as values, e.g.,
                    {'S/34/5634': '8', 'S/44/5574': 'indeterminate', 'S/21/5634': '0'}.
    '''

    load_dotenv(dotenv_path=env_path)
    openai.api_key = os.getenv('PASSWORD')

    if save_dir is not None and save_file_name is not None:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    elif save_dir is None and save_file_name is None:
        result = {}
    else:
        raise ValueError('Please pass BOTH save_dir and save_file_name or NEITHER of them.')


    # Step 1: read input data.
    if input_planning_note_list is not None and input_planning_note_file is None:
        if type(input_planning_note_list[0]) is dict:
            try:
                planning_notes = [dic['Planning Note'] for dic in input_planning_note_list]
            except:
                try:
                    planning_notes = [dic['planning_notes'] for dic in input_planning_note_list]
                except:
                    try:
                        planning_notes = [dic['planning_note'] for dic in input_planning_note_list]
                    except:
                        raise ValueError("The input dict must contain a key called 'Planning Note'.")

            try:
                planning_refs = [dic['Planning Reference'] for dic in input_planning_note_list]
            except:
                try:
                    planning_refs = [dic['reference'] for dic in input_planning_note_list]
                except:
                    planning_refs = None

            try:
                unit_num = [dic['Unit Num'] for dic in input_planning_note_list]
            except:
                try:
                    unit_num = [dic['unit num'] for dic in input_planning_note_list]
                except:
                    try:
                        unit_num = [dic['unit'] for dic in input_planning_note_list]
                    except:
                        try:
                            unit_num = [dic['units'] for dic in input_planning_note_list]
                        except:
                            try:
                                unit_num = [dic['unit_num'] for dic in input_planning_note_list]
                            except:
                                unit_num = None
        else:
            planning_notes = input_planning_note_list
            planning_refs = None
            unit_num = None
    elif input_planning_note_list is None and input_planning_note_file is not None:
        predict_DataFrame = pd.read_csv(input_planning_note_file,
                                        dtype={'reference': str, 'Planning Reference': str,
                                               'planning_note': str, 'Planning Note':str,
                                               'planning_notes': str,'Unit Num':str,
                                               'unit num': str, 'unit':str,'units':str,
                                               'unit_num':str}, lineterminator='\n')

        try:
            planning_refs = predict_DataFrame['Planning Reference']
        except:
            try:
                planning_refs = predict_DataFrame['reference']
            except:
                planning_refs = None



        try:
            planning_notes = predict_DataFrame['Planning Note']
        except:
            try:
                planning_notes = predict_DataFrame['planning_notes']
            except:
                try:
                    planning_notes = predict_DataFrame['planning_note']
                except:
                    raise ValueError("The input file must contain a column called 'Planning Note'.")

        try:
            unit_num = predict_DataFrame['Unit Num']
        except:
            try:
                unit_num = predict_DataFrame['unit num']
            except:
                try:
                    unit_num = predict_DataFrame['unit']
                except:
                    try:
                        unit_num = predict_DataFrame['units']
                    except:
                        try:
                            unit_num = predict_DataFrame['unit_num']
                        except:
                            unit_num = None



    elif input_planning_note_list is not None and input_planning_note_file is not None:
        raise ValueError('Please do NOT pass input_planning_note_list and input_planning_note_file at the same time.')
    else:
        raise ValueError('Please pass input_planning_note_list OR input_planning_note_file.')




    # Step 2: write output data.

    if save_dir is not None and save_file_name is not None:
        with open(os.path.join(save_dir, f'{save_file_name}.csv'), mode='a', newline='') as df:
            df_writer = csv.writer(df, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if unit_num is not None:
                row = ["Planning Reference", "Planning Note", "Label of Unit Num", 'Unit Num','Unit Num Sequence', 'Correctness Check']
            else:
                row = ["Planning Reference", "Planning Note", 'Unit Num', 'Unit Num Sequence']
            df_writer.writerow(row)


            for i,planning_note in enumerate(tqdm(planning_notes)):
                # For some planning note that have a type name in the database, they need to follow our hard coded mapping rules,
                # rather than inferencing its type by the planning note text.
                if len(str(planning_note)) > 2000:
                    planning_note = str(planning_note)[:2000]
                else:
                    planning_note = str(planning_note)

                predictions = []
                for _ in range(vote_from_num_of_predictions):
                    prediction_of_unit_num, prediction_of_unit_num_sequence = _GPT_prediction_from_planning_note(
                            planning_note=planning_note,
                            GPT_finetuned_model_name=GPT_finetuned_model_name,
                            max_tokens=max_tokens)
                    predictions.append((prediction_of_unit_num, prediction_of_unit_num_sequence))
                most_common_prediction = _Most_Common(predictions)
                prediction_of_unit_num,prediction_of_unit_num_sequence = most_common_prediction[0],most_common_prediction[1]



                # Correctness Check
                if unit_num is not None:
                    if unit_num[i] == 'indeterminate':
                        correctness = 'Y' if prediction_of_unit_num == unit_num[i] else 'N'
                    else:
                        try:
                            prediction_of_unit_num = int(float(prediction_of_unit_num))
                            correctness = 'Y' if prediction_of_unit_num == int(float(unit_num[i])) else 'N'
                        except:
                            correctness = 'N'
                    row_new = [planning_refs[i], planning_notes[i], str(unit_num[i]), prediction_of_unit_num, prediction_of_unit_num_sequence, correctness]
                else:
                    row_new = [planning_refs[i], planning_notes[i], prediction_of_unit_num, prediction_of_unit_num_sequence]

                df_writer.writerow(row_new)

    elif save_dir is None and save_file_name is None:
        for i, planning_note in enumerate(tqdm(planning_notes)):
            # For some planning note that have a type name in the database, they need to follow our hard coded mapping rules,
            # rather than inferencing its type by the planning note text.
            if len(str(planning_note)) > 2000:
                planning_note = str(planning_note)[:2000]
            else:
                planning_note = str(planning_note)

            predictions = []
            for _ in range(vote_from_num_of_predictions):
                prediction_of_unit_num, prediction_of_unit_num_sequence = _GPT_prediction_from_planning_note(
                    planning_note=planning_note,
                    GPT_finetuned_model_name=GPT_finetuned_model_name,
                    max_tokens=max_tokens)
                predictions.append((prediction_of_unit_num, prediction_of_unit_num_sequence))
            most_common_prediction = _Most_Common(predictions)
            prediction_of_unit_num, _ = most_common_prediction[0], most_common_prediction[1]
            result[str(planning_refs[i])] = prediction_of_unit_num

        return result


def _GPT_prediction_from_planning_note(planning_note: str,
                                       GPT_finetuned_model_name: str = 'ada:ft-thovex-ltd-2023-01-22-03-06-38',
                                       max_tokens: int = 10):
    '''
    1. Given a planning note extract a sequence of numbers, e.g., '14|63|88'
    2. Split the str into separate numbers and sum them up,
    :param planning_note: a str of planning note.
    :param GPT_finetuned_model_name: the name of finetuned GPT model.
    :param max_tokens: the max num of tokens to be generated.
    :return unit_num: the total sum up number
    :return unit_num_sequence: the original number sequence
    '''

    unit_num_sequence = openai.Completion.create(
        model=GPT_finetuned_model_name,
        prompt=planning_note + '\n\n###\n\n',
        stop=' END',
        max_tokens=max_tokens)['choices'][0]["text"]

    if '|' in unit_num_sequence:
        unit_num = unit_num_sequence.split('|')
        try:
            unit_num = [int(float(x)) for x in unit_num]
            unit_num = str(sum(unit_num))
        except:
            unit_num = 'indeterminate'
    else:
        try:
            unit_num = str(int(float(unit_num_sequence)))
        except:
            unit_num = 'indeterminate'

    return unit_num, unit_num_sequence





from collections import Counter

def _Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]
