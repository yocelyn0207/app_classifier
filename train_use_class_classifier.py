import os
import argparse

from ray.tune import CLIReporter
from ray.tune.schedulers import ASHAScheduler
from ray import tune

from scripts.models.use_class_classifier.training_setup_T5 import training_setup
from scripts.models.utils import Params

# https://docs.ray.io/en/latest/tune/tutorials/tune-pytorch-lightning.html#tune-pytorch-lightning-ref
parser = argparse.ArgumentParser()



parser.add_argument('--config_dir', type=str, default='config/lr_t5')
parser.add_argument('--pretrained_T5_model_name', type=str, default='google/t5-efficient-tiny')
parser.add_argument('--use_classes', type=list, default=['sui generis', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b8',
                                                         'c1', 'c2', 'c3', 'c4', 'd1', 'd2'])
parser.add_argument('--source_max_token_len', type=int, default=256)
parser.add_argument('--num_beams', type=int, default=16)


parser.add_argument('--data_dir', type=str, default='/Users/alicewong/Documents/Programming/application-classifier/datasets/mini')
parser.add_argument('--save_dir', type=str, default='/Users/alicewong/Documents/Programming/application-classifier/predictions')
parser.add_argument('--train_file_name', type=str, default='train.csv')
parser.add_argument('--valid_file_name', type=str, default='valid.csv')
parser.add_argument('--valid_fscore_save_file_name', type=str, default='valid_fscore')
parser.add_argument('--test_file_name', type=str, default='test.csv')
parser.add_argument('--test_fscore_save_file_name', type=str, default='test_fscore')
parser.add_argument('--test_preds_save_file_name', type=str, default='test_preds')
parser.add_argument('--predict_file_name', type=str, default='predict_nolabel.csv')
parser.add_argument('--predict_preds_save_file_name', type=str, default='predict_preds')

parser.add_argument('--local_checkpoint_dir', type=str, default='checkpoint')
parser.add_argument('--upload_dir', type=str, default=None)
parser.add_argument('--checkpoint_resume_dir', type=str, default=None)
parser.add_argument('--best_checkpoint_file_path_for_predict', type=str, default=None)
parser.add_argument('--experiment_name', type=str, default='T5_tiny')


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


    train_fn_with_parameters = tune.with_parameters(training_setup,
                                                    num_epochs = args.num_epochs, gpus_per_trial = args.gpus_per_trial,
                                                    tpu_cores_ID = args.tpu_cores_ID,
                                                    pretrained_T5_model_name = args.pretrained_T5_model_name,
                                                    use_classes = args.use_classes,
                                                    source_max_token_len = args.source_max_token_len,
                                                    num_beams = args.num_beams, num_workers = args.num_workers,
                                                    data_dir = args.data_dir, save_dir = args.save_dir,
                                                    train_file_name = args.train_file_name,
                                                    valid_file_name = args.valid_file_name,
                                                    valid_fscore_save_file_name = args.valid_fscore_save_file_name,
                                                    test_file_name = args.test_file_name,
                                                    test_fscore_save_file_name = args.test_fscore_save_file_name,
                                                    test_preds_save_file_name = args.test_preds_save_file_name,
                                                    predict_file_name = args.predict_file_name,
                                                    predict_preds_save_file_name = args.predict_preds_save_file_name,
                                                    checkpoint_resume_dir = args.checkpoint_resume_dir,
                                                    best_checkpoint_file_path_for_predict = args.best_checkpoint_file_path_for_predict)


    resources_per_trial = {"cpu": 1, "gpu": args.gpus_per_trial}

    # num_samples: Number of times to sample from the hyperparameter space. Defaults to 1. If grid_search is provided
    # as an argument, the grid will be repeated num_samples of times. If this is -1, (virtually) infinite samples are
    # generated until a stopping condition is met.
    analysis = tune.run(train_fn_with_parameters, resources_per_trial=resources_per_trial,
                        metric="f1_avg", mode="max",
                        config=config.dict, num_samples=args.num_samples,
                        scheduler=scheduler, progress_reporter=reporter,
                        name=args.experiment_name,
                        resume="AUTO",
                        local_dir=args.local_checkpoint_dir,
                        checkpoint_score_attr = 'f1_avg',
                        keep_checkpoints_num=1,
                        sync_config=tune.SyncConfig(upload_dir=args.upload_dir)
                        )

    print(f"Best checkpoint found was: {analysis.best_checkpoint} \n"
          f"Best results found were: {analysis.best_result}")




if __name__ == '__main__':
    args = parser.parse_args()
    main(args)


