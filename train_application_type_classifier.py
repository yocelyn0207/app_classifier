import os
import argparse

from ray.tune import CLIReporter
from ray.tune.schedulers import ASHAScheduler
from ray import tune

from scripts.models.application_type_classifier.training_and_predicting_setup import training_and_predicting_setup
from scripts.models.utils import Params

# https://docs.ray.io/en/latest/tune/tutorials/tune-pytorch-lightning.html#tune-pytorch-lightning-ref
parser = argparse.ArgumentParser()



parser.add_argument('--config_dir', type=str, default='config/lr_bert')
parser.add_argument('--pretrained_BERT_model_name', type=str, default='bert-large-uncased')
parser.add_argument('--source_max_token_len', type=int, default=256)

parser.add_argument('--data_dir', type=str, default='/Users/yocelyn/Documents/Programming/application-classifier/datasets/mini')
parser.add_argument('--save_dir', type=str, default='/Users/yocelyn/Documents/Programming/application-classifier/predictions')
parser.add_argument('--type_new_and_indices_mapping_file_name', type=str, default='type_new_and_indices_mapping_dict.json')
parser.add_argument('--train_file_name', type=str, default='train.csv')
parser.add_argument('--valid_file_name', type=str, default='valid.csv')
parser.add_argument('--valid_fscore_save_file_name', type=str, default='valid_fscore')
parser.add_argument('--test_file_name', type=str, default='test.csv')
parser.add_argument('--test_fscore_save_file_name', type=str, default='test_fscore')
parser.add_argument('--test_preds_save_file_name', type=str, default='test_preds')

parser.add_argument('--local_checkpoint_dir', type=str, default='checkpoint')
parser.add_argument('--upload_dir', type=str, default=None)
parser.add_argument('--checkpoint_resume_dir', type=str, default=None)
parser.add_argument('--experiment_name', type=str, default='application_type_classifier_v1.0')

parser.add_argument('--num_epochs', type=int, default=50)
parser.add_argument('--gpus_per_trial', type=float, default=0)
parser.add_argument('--tpu_cores_ID', type=int, default=None)
# parser.add_argument('--num_tpu', type=int, default=0)
parser.add_argument('--num_workers', type=int, default=12)
parser.add_argument('--num_samples', type=int, default=1)




def main(args):
    config = Params(os.path.join(args.config_dir, 'config.json'))



    params_tuned = []
    for k, v in config.dict.items():
        if v['requireTuning'] is False:
            config.dict[k]  = v['defaultValue']
        elif v['requireTuning'] is True and v['tuningValuesType'] == 'Continuous':
            config.dict[k] = tune.loguniform(v['minValue'], v['maxValue'])
            params_tuned.append(k)
        elif v['requireTuning'] is True and v['tuningValuesType'] == 'Discrete':
            config.dict[k] = tune.grid_search(v['candidateValues'])
            params_tuned.append(k)

    # This scheduler decides at each iteration which trials are likely to perform badly, and stops these trials.
    # This way we don’t waste any resources on bad hyperparameter configurations.
    scheduler = ASHAScheduler(max_t=args.num_epochs,  grace_period=1, reduction_factor=2)

    # Instantiate a CLIReporter to specify which metrics we would like to see in our output tables in the command line.
    reporter = CLIReporter(
        parameter_columns=params_tuned,
        metric_columns=['validate_loss_avg', 'precision_avg', 'recall_avg', 'f1_avg', 'training_iteration'])


    train_fn_with_parameters = tune.with_parameters(training_and_predicting_setup,
                                                    mode = 'train',
                                                    num_epochs = args.num_epochs, gpus_per_trial = args.gpus_per_trial,
                                                    tpu_cores_ID = args.tpu_cores_ID,
                                                    pretrained_BERT_model_name = args.pretrained_BERT_model_name,
                                                    source_max_token_len = args.source_max_token_len,
                                                    num_workers = args.num_workers,
                                                    data_dir = args.data_dir, save_dir = args.save_dir,
                                                    type_new_and_indices_mapping_file_name = args.type_new_and_indices_mapping_file_name,
                                                    train_file_name = args.train_file_name,
                                                    valid_file_name = args.valid_file_name,
                                                    valid_fscore_save_file_name = args.valid_fscore_save_file_name,
                                                    test_file_name = args.test_file_name,
                                                    test_fscore_save_file_name = args.test_fscore_save_file_name,
                                                    test_preds_save_file_name = args.test_preds_save_file_name,
                                                    predict_file_name = None,
                                                    predict_inputs_list = None,
                                                    predict_preds_save_file_name = None,
                                                    checkpoint_resume_dir = args.checkpoint_resume_dir,
                                                    best_checkpoint_file_path_for_predict = None)


    resources_per_trial = {"cpu": 1, "gpu": args.gpus_per_trial}

    # num_samples: Number of times to sample from the hyperparameter space. Defaults to 1. If grid_search is provided
    # as an argument, the grid will be repeated num_samples of times. If this is -1, (virtually) infinite samples are
    # generated until a stopping condition is met.
    analysis = tune.run(train_fn_with_parameters, resources_per_trial=resources_per_trial,
                        metric="validate_loss_avg", mode="min",
                        config=config.dict, num_samples=args.num_samples,
                        scheduler=scheduler, progress_reporter=reporter,
                        name=args.experiment_name,
                        resume="AUTO",
                        local_dir=args.local_checkpoint_dir,
                        checkpoint_score_attr = 'validate_loss_avg',
                        keep_checkpoints_num=1,
                        sync_config=tune.SyncConfig(upload_dir=args.upload_dir)
                        )

    print(f"Best checkpoint found was: {analysis.best_checkpoint} \n"
          f"Best results found were: {analysis.best_result}")




if __name__ == '__main__':
    args = parser.parse_args()
    main(args)


