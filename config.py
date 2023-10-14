import argparse
from dotenv import load_dotenv


args_parser = argparse.ArgumentParser(description='Run App Classifier')
args_parser.add_argument('-env', '--env', type=str, help='Runs for a passed Environment', default='dev',
                         choices=['live', 'staging', 'dev', 'local'])
args = args_parser.parse_args()
load_dotenv(f'./environment_files/{args.env}.env')
