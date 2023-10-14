import os
from pathlib import Path
import math

import json
import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger
from ray.tune.integration.pytorch_lightning import TuneReportCheckpointCallback
from ray import tune

from scripts.models.application_type_classifier.model import CustomBERT
from scripts.models.utils import process_preds_and_labels_to_readable_list



def training_and_predicting_setup(config, mode: str, num_epochs: int, gpus_per_trial: float, tpu_cores_ID:int,
                   pretrained_BERT_model_name: str,
                   source_max_token_len:int, num_workers: int,
                   data_dir: Path, save_dir: Path,
                   type_new_and_indices_mapping_file_name: str,
                   train_file_name: str = None, valid_file_name:str = None, valid_fscore_save_file_name: str = 'valid_fscore',
                   test_file_name: str = None, test_fscore_save_file_name: str = 'test_fscore', test_preds_save_file_name: str = 'test_preds',
                   predict_file_name: str = None, predict_inputs_list: list = None, predict_preds_save_file_name: str = 'predict_preds',
                   checkpoint_resume_dir: str = None, best_checkpoint_file_path_for_predict: Path = None):

    #pl.seed_everything(2022)

    if not os.path.exists(save_dir): os.makedirs(save_dir)

    if mode == 'train':
        model = CustomBERT(config = config, pretrained_BERT_model_name = pretrained_BERT_model_name,
                           source_max_token_len = source_max_token_len,
                           num_workers = num_workers,
                           data_dir = data_dir, save_dir = save_dir,
                           type_new_and_indices_mapping_file_name = type_new_and_indices_mapping_file_name,
                           train_file_name = train_file_name,
                           valid_file_name = valid_file_name, valid_fscore_save_file_name = valid_fscore_save_file_name,
                           test_file_name = test_file_name, test_fscore_save_file_name = test_fscore_save_file_name,
                           test_preds_save_file_name = test_preds_save_file_name,
                           predict_file_name = predict_file_name, predict_preds_save_file_name = predict_preds_save_file_name,
                           predict_inputs_list = predict_inputs_list)
    else:
        if predict_inputs_list is not None and predict_file_name is None:
            if type(predict_inputs_list[0]) is dict:
                planning_notes = [dic['Planning Notes'] for dic in predict_inputs_list]
                try:
                    planning_refs = [dic['Planning Reference'] for dic in predict_inputs_list]
                except:
                    try:
                        planning_refs = [dic['reference'] for dic in predict_inputs_list]
                    except:
                        planning_refs = None
            else:
                planning_notes = predict_inputs_list
                planning_refs = None
        elif predict_inputs_list is None and predict_file_name is not None:
            predict_DataFrame = pd.read_csv(os.path.join(data_dir, predict_file_name), dtype={'reference': str, 'Planning Reference': str})
            planning_notes = predict_DataFrame['planning_notes']
            try:
                planning_refs = predict_DataFrame['Planning Reference']
            except:
                try:
                    planning_refs = predict_DataFrame['reference']
                except:
                    planning_refs = None
        elif predict_inputs_list is not None and predict_file_name is not None:
            raise ValueError('Please do NOT pass predict_inputs_list and predict_file_name at the same time.')
        else:
            raise ValueError('Please pass predict_inputs_list OR predict_file_name.')

        model = CustomBERT.load_from_checkpoint(checkpoint_path = best_checkpoint_file_path_for_predict,
                           config = config, pretrained_BERT_model_name = pretrained_BERT_model_name,
                           source_max_token_len = source_max_token_len,
                           num_workers = num_workers,
                           data_dir = data_dir, save_dir = save_dir,
                           type_new_and_indices_mapping_file_name=type_new_and_indices_mapping_file_name,
                           train_file_name = train_file_name,
                           valid_file_name = valid_file_name, valid_fscore_save_file_name = valid_fscore_save_file_name,
                           test_file_name = test_file_name, test_fscore_save_file_name = test_fscore_save_file_name,
                           test_preds_save_file_name = test_preds_save_file_name,
                           predict_file_name = predict_file_name, predict_preds_save_file_name = predict_preds_save_file_name,
                           predict_inputs_list = planning_notes)

    logger = TensorBoardLogger(save_dir=tune.get_trial_dir(), name="", version=".")
    callbalcks = [TuneReportCheckpointCallback(
        metrics={
                "validate_loss_avg": "validate_loss_avg",
                "precision_avg": "precision_avg",
            },
            filename="checkpoint",
            on="validation_end")]

    kwargs = {
        "max_epochs": num_epochs,
        # If fractional GPUs passed in, convert to int.
        "gpus": math.ceil(gpus_per_trial),
        "tpu_cores": tpu_cores_ID,
        "logger": logger,
        "progress_bar_refresh_rate": 1,
        "callbacks": callbalcks
    }

    if checkpoint_resume_dir is not None:
        kwargs["resume_from_checkpoint"] = os.path.join(checkpoint_resume_dir, 'checkpoint')


    trainer = pl.Trainer(**kwargs)

    if mode == 'train':
        trainer.fit(model)
        trainer.test(model)
    else:
        outputs= trainer.predict(model) # list of lists, len == batch_size
        predicted_class_ids = []
        labels = []
        for i in outputs:
            predicted_class_ids += i['predicted_class_ids']
            labels += i['labels']

        if labels == []:
            labels = None

        with open(os.path.join(data_dir, type_new_and_indices_mapping_file_name), 'r') as f:
            indices_to_type_new_dict = json.load(f)['indices_to_type_new_dict']

        _, preds, labels, correctness = process_preds_and_labels_to_readable_list(model_name = 'app_type_classifier',
                                                            preds = predicted_class_ids, labels=labels,
                                                            indices_to_type_new_dict = indices_to_type_new_dict)

        if predict_preds_save_file_name is not None:
            if labels == []:
                data = pd.DataFrame(
                    {'Planning Reference': planning_refs, 'Planning Notes': planning_notes, 'Predictions': preds})
            else:
                data = pd.DataFrame(
                    {'Planning Reference': planning_refs, 'Planning Notes': planning_notes, 'Predictions': preds,
                     'Labels': labels, 'Correctness Check': correctness})

            data.to_csv(os.path.join(save_dir, predict_preds_save_file_name + '.csv'), index=False)

        return preds













