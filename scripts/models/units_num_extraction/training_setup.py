import os
from pathlib import Path
import math

import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger
from ray.tune.integration.pytorch_lightning import TuneReportCheckpointCallback
from ray import tune

from scripts.models.units_num_extraction.model import CustomT5
from scripts.models.utils import process_preds_to_readable_file



def training_setup(config, num_epochs: int, gpus_per_trial: float, tpu_cores_ID:int,
                   pretrained_T5_model_name: str,
                   source_max_token_len:int, num_beams: int, num_workers: int,
                   data_dir: Path, save_dir: Path,
                   train_file_name: str = None, valid_file_name:str = None, valid_fscore_save_file_name: str = 'valid_fscore',
                   test_file_name: str = None, test_fscore_save_file_name: str = 'test_fscore', test_preds_save_file_name: str = 'test_preds',
                   predict_file_name: str = None, predict_preds_save_file_name: str = 'predict_preds', predict_inputs_list: list = None,
                   checkpoint_resume_dir: str = None, best_checkpoint_file_path_for_predict: Path = None):

    #pl.seed_everything(2022)

    if not os.path.exists(save_dir): os.makedirs(save_dir)

    if best_checkpoint_file_path_for_predict is None:
        model = CustomT5(config = config, pretrained_T5_model_name = pretrained_T5_model_name,
                         source_max_token_len = source_max_token_len,
                         num_beams = num_beams, num_workers = num_workers,
                         data_dir = data_dir, save_dir = save_dir,
                         train_file_name = train_file_name,
                         valid_file_name = valid_file_name, valid_fscore_save_file_name = valid_fscore_save_file_name,
                         test_file_name = test_file_name, test_fscore_save_file_name = test_fscore_save_file_name,
                         test_preds_save_file_name = test_preds_save_file_name,
                         predict_file_name = predict_file_name, predict_preds_save_file_name = predict_preds_save_file_name,
                         predict_inputs_list = predict_inputs_list)
    else:
        model = CustomT5.load_from_checkpoint(checkpoint_path = best_checkpoint_file_path_for_predict,
                         config = config, pretrained_T5_model_name = pretrained_T5_model_name,
                         source_max_token_len = source_max_token_len,
                         num_beams = num_beams, num_workers = num_workers,
                         data_dir = data_dir, save_dir = save_dir,
                         train_file_name = train_file_name,
                         valid_file_name = valid_file_name, valid_fscore_save_file_name = valid_fscore_save_file_name,
                         test_file_name = test_file_name, test_fscore_save_file_name = test_fscore_save_file_name,
                         test_preds_save_file_name = test_preds_save_file_name,
                         predict_file_name = predict_file_name, predict_preds_save_file_name = predict_preds_save_file_name,
                         predict_inputs_list = predict_inputs_list)

    logger = TensorBoardLogger(save_dir=tune.get_trial_dir(), name="", version=".")
    callbalcks = [TuneReportCheckpointCallback(
        metrics={
                "validate_loss_avg": "validate_loss_avg",
                "precision": "precision"
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

    trainer.fit(model)
    trainer.test(model)
    outputs= trainer.predict(model) # list of lists, len == batch_size
    preds = []
    labels = []
    for i in outputs:
        preds += i['preds']
        labels += i['labels']
    if labels == []: labels = None


    predict_DataFrame = pd.read_csv(os.path.join(data_dir, predict_file_name))
    results = process_preds_to_readable_file(predict_DataFrame, preds, labels)
    file_name = f'{predict_preds_save_file_name}.csv'
    results.to_csv(os.path.join(save_dir, file_name))

    # if train_file_name is not None:
    #     trainer.fit(model)
    #
    # if test_file_name is not None:
    #     trainer.test(model)
    #
    # if predict_file_name is not None:
    #     trainer.predict(model)












