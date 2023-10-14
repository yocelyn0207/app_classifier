import os
import math

import pandas as pd
import pytorch_lightning as pl
from ray import tune

from scripts.models.use_class_classifier.model_T5 import CustomT5
from scripts.models.utils import Params, process_preds_and_labels_to_readable_list
from scripts.preprocessing.change_of_use.split_planning_note_into_demolition_and_erection import split_planning_note_into_demolition_and_erection

# Try to handle OSError: [Errno 24] Too many open files.
import torch.multiprocessing
torch.multiprocessing.set_sharing_strategy('file_system')




def inference_setup(model_name: str = 'change_of_use',
                    predict_file_path: str = None,
                    predict_planning_notes: list = None,
                    save_dir: str = None,
                    predictions_save_file_name: str = None,
                    num_workers: int = 2,
                    gpus_per_trial: float = 0,
                    tpu_cores_ID: int = None,
                    best_checkpoint_file_path: str = 'checkpoints/version=1.31-epoch=97-step=1838680.ckpt',
                    config_dir: str = 'config/lr_t5'):

    '''
    This function takes EITHER a .csv file which contains 'planning_notes' column OR a list of planning notes (format is
    stated as below).

    :param model_name: should be one of {'use_class_classifier', 'units_num_extraction'}
    :param predict_file_path: the path to the input file. It ONLY accepts .csv file with a 'planning_notes' column.
    :param predict_planning_notes: if inputs are not complied in a file, you can choose to pass a list of planning notes.
            Can be a list of strings, e.g.,
            ['Erection of 3no. dwellings and associated works and the demolition of existing extension.',
            'Change of use from use class B2 (General Industrial) and ancillary offices to flexible use class E(g)(iii) (Industrial Processes)',
            'Change of use from offices (class E (g)) to 12no. studio apartments (class C3)']
            or a list of dictionaries which contain "Planning Reference" and "Planning Notes" as keys, e.g.,
            [{"Planning Reference": "S/21/1399",
            "Planning Notes": "Erection of 3no. dwellings and associated works and the demolition of existing extension."},
            {"Planning Reference": "S/21/1961",
            "Planning Notes": "Change of use from use class B2 (General Industrial) and ancillary offices to flexible use class E(g)(iii) (Industrial Processes), B2 (General Industrial) and/or B8 (Storage or Distribution) and ancillary offices."},
            {"Planning Reference": "S/22/0244",
            "Planning Notes": "Change of use from offices (class E (g)) to 12no. studio apartments (class C3) and associated works."}]
    :param save_dir: if you want to save the results into a file, please specify save_dir and predictions_save_file_name.
                     It will be saved into a .csv file including the planning refs, planning notes, predictions
                     (demolitions and erections for change_of_use model), labels (if applicable),
                     correctness check (if applicable).
    :param predictions_save_file_name: will be saved into a .csv file. Please do NOT include the filename extension.
    :param num_workers: number of workers.
    :param gpus_per_trial: number of GPUs.
    :param tpu_cores_ID: TPU cores ID.
    :param best_checkpoint_file_path: the path to the best checkpoint file.
    :param config_dir: the directory to the config.json file.
    :return results: return a dictionary with planning reference as keys and predictions as values, e.g.,
            if model_name == 'use_class_classifier',  {'S/34/5634': ['c3'], 'S/44/5574': ['b1','c3'], 'S/21/5634': []};
            if model_name == 'change_of_use', {'S/34/5634': ([], ['c3']), 'S/44/5574': (['b1'], []), 'S/21/5634': (['c1'], ['a3'])},
            the first element within each tuple is demolitions, the second one is erections.
    '''

    config = Params(os.path.join(config_dir, 'config.json'))

    params_tuned = []
    for k, v in config.dict.items():
        if v['requireTuning'] is False:
            config.dict[k] = v['defaultValue']
        elif v['requireTuning'] is True and v['tuningValuesType'] == 'Continuous':
            config.dict[k] = tune.loguniform(v['minValue'], v['maxValue'])
            params_tuned.append(k)
        elif v['requireTuning'] is True and v['tuningValuesType'] == 'Discrete':
            config.dict[k] = tune.grid_search(v['candidateValues'])
            params_tuned.append(k)




    if predict_planning_notes is not None and predict_file_path is None:
        if type(predict_planning_notes[0]) is dict:
            demolitions = []
            erections = planning_notes = [dic['Planning Notes'] for dic in predict_planning_notes]
            planning_refs = [dic['Planning Reference'] for dic in predict_planning_notes]
        else:
            demolitions = []
            erections = planning_notes = predict_planning_notes
            planning_refs = None
    elif predict_planning_notes is None and predict_file_path is not None:
        predict_DataFrame = pd.read_csv(predict_file_path, dtype={'reference': str, 'Planning Reference': str}, lineterminator='\n')
        demolitions = []
        erections = planning_notes = predict_DataFrame['planning_notes']

        try:
            planning_refs = predict_DataFrame['Planning Reference']
        except:
            try:
                planning_refs = predict_DataFrame['reference']
            except:
                planning_refs = None
    elif predict_planning_notes is not None and predict_file_path is not None:
        raise ValueError('Please do NOT pass predict_planning_notes and predict_file_path at the same time.')
    else:
        raise ValueError('Please pass predict_planning_notes OR predict_file_path.')



    if model_name == 'change_of_use':
        demolitions = []
        erections = []
        for planning_note in planning_notes:
            try:
                splitted_planning_note = split_planning_note_into_demolition_and_erection(planning_note)
                demolitions.append(splitted_planning_note[0])
                erections.append(splitted_planning_note[1])
            except:
                demolitions.append('')
                erections.append('')


    model = CustomT5.load_from_checkpoint(checkpoint_path=best_checkpoint_file_path,
                                          config=config.dict, pretrained_T5_model_name='google/t5-efficient-tiny',
                                          use_classes=['sui generis', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b8', 'c1', 'c2', 'c3', 'c4', 'd1','d2'],
                                          source_max_token_len=512,
                                          num_beams=16, num_workers=num_workers,
                                          data_dir=None, save_dir=save_dir,
                                          train_file_name=None,
                                          valid_file_name=None, valid_fscore_save_file_name=None,
                                          test_file_name=None, test_fscore_save_file_name=None, test_preds_save_file_name=None,
                                          predict_file_name=None,
                                          predict_inputs=demolitions+erections,
                                          predict_preds_save_file_name=predictions_save_file_name)


    kwargs = {
        # If fractional GPUs passed in, convert to int.
        "gpus": math.ceil(gpus_per_trial),
        "tpu_cores": tpu_cores_ID,
    }

    trainer = pl.Trainer(**kwargs)
    outputs = trainer.predict(model)  # list of lists, len == batch_size

    preds = []
    labels = []
    for i in outputs:
        preds += i['preds']
        labels += i['labels']

    if labels == []:
        labels = None




    demolitions, erections, labels, correctness = process_preds_and_labels_to_readable_list(model_name=model_name, preds=preds, labels=labels)

    if model_name == 'use_class_classifier':
        preds = erections
    elif model_name == 'change_of_use':
        # convert to a list tuples, the first element within each tuple is demolitions, the second one is erections, e.g.,
        # [([], ['c3']), (['b1'], []), (['c1'], ['a3'])]
        preds = list(zip(demolitions, erections))



    if planning_refs is not None:
        # convert to the final dictionary, e.g., {'S/34/5634': ([], ['c3']), 'S/44/5574': (['b1'], []), 'S/21/5634': (['c1'], ['a3'])}
        results = pd.DataFrame({'Planning Reference': planning_refs, 'Predictions':preds})
        results.set_index('Planning Reference', inplace=True)
        results = results.to_dict()['Predictions']
    else:
        results = preds


    if save_dir is not None and os.path.exists(save_dir) is False:
        os.makedirs(save_dir)

    if predictions_save_file_name is not None:
        if model_name == 'use_class_classifier':
            if labels == []:
                data = pd.DataFrame({'Planning Reference': planning_refs, 'Planning Notes': planning_notes, 'Predictions':preds})
            else:
                data = pd.DataFrame({'Planning Reference': planning_refs, 'Planning Notes': planning_notes, 'Predictions':preds,
                                     'Labels':labels, 'Correctness Check':correctness})
        elif model_name == 'change_of_use':
            data = pd.DataFrame({'Planning Reference': planning_refs, 'Planning Notes': planning_notes,
                                 'Demolitions': demolitions, 'Erections': erections})

        data.to_csv(os.path.join(save_dir, predictions_save_file_name+'.csv'), index=False)

    return results


