import pandas as pd
import torch
from torch.utils.data import Dataset
import torch.nn.functional as F
from transformers import BertTokenizer




class LandstackDataset(Dataset):
    def __init__(self, data: pd.DataFrame, tokenizer: BertTokenizer,
                 source_max_token_len: int, num_labels: int):

        self.tokenizer = tokenizer
        self.source_max_token_len = source_max_token_len
        self.num_labels = num_labels
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



        if 'type_new' in self.data.columns:
            labels = data_row['type_new']
            labels_ids = torch.tensor([int(data_row['type_new_indices'])])
            labels_onehot = F.one_hot(labels_ids, num_classes=self.num_labels)
        else: # for inference time
            labels = None
            labels_ids = None
            labels_onehot = None


        return dict(
            input_ids = sources_encoding['input_ids'],
            attention_mask=sources_encoding["attention_mask"],
            labels = labels,
            labels_ids = labels_ids,
            labels_onehot = labels_onehot
        )




