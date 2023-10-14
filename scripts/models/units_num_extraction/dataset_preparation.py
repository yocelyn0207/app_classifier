import pandas as pd
import torch
from torch.utils.data import Dataset
from transformers import T5Tokenizer




class LandstackDataset(Dataset):
    def __init__(self, data: pd.DataFrame, tokenizer: T5Tokenizer,
                 source_max_token_len: int, target_max_token_len: int):

        self.tokenizer = tokenizer
        self.source_max_token_len = source_max_token_len
        self.target_max_token_len = target_max_token_len
        self.data = data


    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int):
        data_row = self.data.iloc[index]


        sources_encoding = self.tokenizer(
          str(data_row["planning_notes"]).lower(),
          max_length=self.source_max_token_len,
          padding="max_length",
          truncation=True,
          return_attention_mask=True,
          add_special_tokens=True,
          return_tensors="pt"
          )




        # Just check one label column.
        if 'units' in self.data.columns:
            labels = str(data_row['units'])

            targets_encoding = self.tokenizer(
                labels,
                max_length=self.target_max_token_len,
                padding="max_length",
                truncation=True,
                return_attention_mask=True,
                add_special_tokens=False,
                return_tensors="pt"
            )


            output_ids = targets_encoding['input_ids']
            output_ids[output_ids == 0] = -100 # cannot be used in T5Model, only T5ForConditionalGeneration

        else:
            labels = []
            output_ids = torch.tensor([]) # for inference time



        return dict(
            input_ids = sources_encoding['input_ids'],
            attention_mask=sources_encoding["attention_mask"],
            output_ids = output_ids,
            labels = labels
        )




