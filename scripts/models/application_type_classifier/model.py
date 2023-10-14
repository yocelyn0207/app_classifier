import re
import os.path
from pathlib import Path

import pandas as pd
import json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics import classification_report

from scripts.models.application_type_classifier.dataset_preparation import LandstackDataset
from scripts.models.utils import process_preds_and_labels_to_readable_list





class CustomBERT(pl.LightningModule):
    def __init__(self, config, pretrained_BERT_model_name: str,
                 source_max_token_len: int,
                 num_workers: int,
                 data_dir: Path, save_dir: Path,
                 type_new_and_indices_mapping_file_name: str,
                 train_file_name: str,
                 valid_file_name: str, valid_fscore_save_file_name: str,
                 test_file_name: str, test_fscore_save_file_name: str, test_preds_save_file_name: str,
                 predict_file_name: str, predict_preds_save_file_name: str,
                 predict_inputs_list: list):
        super().__init__()

        self.lr = config['learning_rate']
        self.batch_size = config['batch_size']

        self.source_max_token_len = source_max_token_len
        self.num_workers = num_workers

        self.data_dir = data_dir
        self.save_dir = save_dir
        self.type_new_and_indices_mapping_file_name = type_new_and_indices_mapping_file_name
        self.train_file_name = train_file_name
        self.valid_file_name = valid_file_name
        self.valid_fscore_save_file_name = valid_fscore_save_file_name
        self.test_file_name = test_file_name
        self.test_fscore_save_file_name = test_fscore_save_file_name
        self.test_preds_save_file_name = test_preds_save_file_name
        self.predict_file_name = predict_file_name
        self.predict_preds_save_file_name = predict_preds_save_file_name
        self.predict_inputs_list = predict_inputs_list

        with open(os.path.join(self.data_dir, self.type_new_and_indices_mapping_file_name), 'r') as f:
            data = json.load(f)
        self.type_new_to_indices_dict = data['type_new_to_indices_dict']
        self.indices_to_type_new_dict = data['indices_to_type_new_dict']
        self.num_labels = len(self.indices_to_type_new_dict)

        self.tokenizer = BertTokenizer.from_pretrained(pretrained_BERT_model_name)
        self.model = BertForSequenceClassification.from_pretrained(pretrained_BERT_model_name, num_labels=self.num_labels,
                                                                   problem_type="multi_label_classification")
        for name, param in self.model.named_parameters():
            # if re.search('bert.embeddings|bert.encoder.layer', name) is not None:
            #     param.requires_grad = False
            if re.search('layer23|bert.pooler|classifier', name) is None:
                param.requires_grad = False


    def forward(self, input_ids, attention_mask, labels_onehot = None):
        # input_ids, attention_mask (batch_size, source_max_token_len)
        # labels_onehot (batch_size, num_labels) float tensor
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, labels = labels_onehot)
        return outputs

    def _calculate_weighted_loss(self, logits, labels_onehot):
        # logits,labels_onehot (batch_size * num_labels)
        loss_fn = nn.CrossEntropyLoss(weight=self.weights)
        logits = logits.cpu()
        labels_onehot = labels_onehot.cpu()
        loss = loss_fn(logits, labels_onehot)
        return loss

    def _decode_preds_from_logits(self, logits):
        # logits (batch_size * num_labels)
        predicted_class_ids = torch.argmax(logits, dim=1)
        return predicted_class_ids  # (batch_size)

    def _precision_recall_fscore(self, predicted_class_ids, labels_ids):
        # predicted_class_ids, labels: indices of classes, e.g., tensor([24, 0, 10, 18, 3]). (batch_size)
        preds_tensors = predicted_class_ids.cpu()
        preds_tensors = preds_tensors.long()
        labels_tensors = labels_ids.cpu()
        labels_tensors = labels_tensors.long()

        # A dict of use classes with precision, recall, and f1-score, e.g.,
        # {'Full Application': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 1},
        # 'Other': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 2},
        # 'micro avg': {'precision': 1.0, 'recall': 0.83, 'f1-score': 0.90, 'support': 6},
        # 'macro avg': {'precision': 1.0, 'recall': 0.87, 'f1-score': 0.91, 'support': 6},
        # 'weighted avg': {'precision': 1.0, 'recall': 0.83, 'f1-score': 0.88, 'support': 6},
        # 'samples avg': {'precision': 1.0, 'recall': 0.88, 'f1-score': 0.93, 'support': 6}

        # target_names=self.application_types can not pass Sanity Checking DataLoader process which only uses 2 batches
        involved_ids = torch.unique(torch.concat([predicted_class_ids, labels_ids]), sorted=True).tolist()
        involved_application_types = [self.indices_to_type_new_dict[str(i)] for i in involved_ids]
        scores = classification_report(y_pred=preds_tensors, y_true=labels_tensors,
                                       target_names=involved_application_types, output_dict=True, zero_division=1)
        return scores

    def training_step(self, batch, batch_idx):
        # input_ids, attention_mask (batch_size, 1, source_max_token_len) -> (batch_size, source_max_token_len)
        # labels_onehot (batch_size, 1, num_labels) -> (batch_size, num_labels)
        input_ids, attention_mask, labels_onehot = batch['input_ids'].view(-1, self.source_max_token_len), \
                                                batch['attention_mask'].view(-1, self.source_max_token_len), \
                                                batch['labels_onehot'].view(-1, self.num_labels).float()
        outputs = self(input_ids, attention_mask, labels_onehot)
        loss = self._calculate_weighted_loss(outputs.logits, labels_onehot)
        self.log('train_loss', loss, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        # input_ids, attention_mask (batch_size, 1, source_max_token_len) -> (batch_size, source_max_token_len)
        # labels_onehot (batch_size, 1, num_labels) -> (batch_size, num_labels)
        input_ids, attention_mask, labels_onehot,labels_ids = batch['input_ids'].view(-1, self.source_max_token_len), \
                                                       batch['attention_mask'].view(-1, self.source_max_token_len), \
                                                       batch['labels_onehot'].view(-1, self.num_labels).float(), \
                                                       torch.squeeze(batch['labels_ids'])
        outputs = self(input_ids, attention_mask, labels_onehot)
        # loss = outputs.loss
        loss = self._calculate_weighted_loss(outputs.logits, labels_onehot)

        predicted_class_ids = self._decode_preds_from_logits(outputs.logits)
        self.log('validate_loss', loss, prog_bar=True, logger=True)
        return {'validate_loss': loss, 'predicted_class_ids': predicted_class_ids, 'labels_ids': labels_ids}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x["validate_loss"] for x in outputs]).mean()
        predicted_class_ids = torch.concat([x["predicted_class_ids"] for x in outputs])
        labels_ids = torch.concat([x["labels_ids"] for x in outputs])

        scores = self._precision_recall_fscore(predicted_class_ids, labels_ids)
        file_name = f'{self.valid_fscore_save_file_name}_epoch={self.current_epoch}.pt'
        torch.save(scores, os.path.join(self.save_dir, file_name))
        self.log_dict({'validate_loss_avg': avg_loss,
                       'precision_avg': torch.tensor(scores['weighted avg']["precision"]),
                       'recall_avg': torch.tensor(scores['weighted avg']["recall"]),
                       'f1_avg': torch.tensor(scores['weighted avg']["f1-score"])})

    def test_step(self, batch, batch_idx):
        # input_ids, attention_mask (batch_size, 1, source_max_token_len) -> (batch_size, source_max_token_len)
        # labels_onehot (batch_size, 1, num_labels) -> (batch_size, num_labels)
        input_ids, attention_mask, labels, labels_onehot,labels_ids = \
            batch['input_ids'].view(-1, self.source_max_token_len), \
            batch['attention_mask'].view(-1, self.source_max_token_len), \
            batch['labels'],\
            batch['labels_onehot'].view(-1, self.num_labels).float(), \
            torch.squeeze(batch['labels_ids'])

        outputs = self(input_ids, attention_mask, labels_onehot)
        # loss = outputs.loss
        loss = self._calculate_weighted_loss(outputs.logits, labels_onehot)
        predicted_class_ids = self._decode_preds_from_logits(outputs.logits)
        self.log('test_loss', loss, prog_bar=True, logger=True)
        return {'test_loss': loss, 'predicted_class_ids': predicted_class_ids,'labels':labels, 'labels_ids': labels_ids}

    def test_epoch_end(self, outputs):
        avg_loss = torch.stack([x["test_loss"] for x in outputs]).mean()
        predicted_class_ids = torch.concat([x["predicted_class_ids"] for x in outputs])
        labels = []
        for x in outputs:
            labels += x["labels"]
        labels_ids = torch.concat([x["labels_ids"] for x in outputs])

        scores = self._precision_recall_fscore(predicted_class_ids, labels_ids)
        file_name = f'{self.test_fscore_save_file_name}_epoch={self.current_epoch}.pt'
        torch.save(scores, os.path.join(self.save_dir, file_name))

        _, preds, labels, correctness = process_preds_and_labels_to_readable_list(model_name = 'app_type_classifier',
                                                            preds = predicted_class_ids.tolist(), labels=labels,
                                                            indices_to_type_new_dict = self.indices_to_type_new_dict)
        results = pd.DataFrame({'Planning Notes': self.test_DataFrame['planning_notes'], 'Predictions': preds.tolist(),
             'Labels': labels, 'Correctness Check': correctness})
        file_name = f'{self.test_preds_save_file_name}_epoch={self.current_epoch}.csv'
        results.to_csv(os.path.join(self.save_dir, file_name))

        self.log_dict({'test_loss_avg': avg_loss,
                       'precision_avg': torch.tensor(scores['weighted avg']["precision"]),
                       'recall_avg': torch.tensor(scores['weighted avg']["recall"]),
                       'f1_avg': torch.tensor(scores['weighted avg']["f1-score"])})

    def predict_step(self, batch, batch_idx):
        # input_ids, attention_mask (batch_size, 1, source_max_token_len) -> (batch_size, source_max_token_len)
        # labels_onehot (batch_size, 1, num_labels) -> (batch_size, num_labels)
        input_ids, attention_mask, labels, labels_onehot, labels_ids = \
            batch['input_ids'].view(-1, self.source_max_token_len), \
            batch['attention_mask'].view(-1, self.source_max_token_len), \
            batch['labels'], \
            batch['labels_onehot'], \
            batch['labels_ids']
        if labels_onehot is not None:
            labels_onehot = labels_onehot.view(-1, self.num_labels).float()
            labels_ids = torch.squeeze(labels_ids)

        outputs = self(input_ids, attention_mask, labels_onehot)
        predicted_class_ids = self._decode_preds_from_logits(outputs.logits)

        precision = None
        if labels_ids is not None:
            precision = self._precision_recall_fscore(predicted_class_ids, labels_ids)

        return {'predicted_class_ids': predicted_class_ids.tolist(), 'labels': labels, 'precision': precision}

    def prepare_data(self):
        if self.train_file_name is not None:
            train_DataFrame = pd.read_csv(os.path.join(self.data_dir, self.train_file_name), encoding='utf_8',lineterminator='\n')
            self.train_dataset = LandstackDataset(train_DataFrame, self.tokenizer, self.source_max_token_len, self.num_labels)
            new_types_frequency = train_DataFrame.type_new.value_counts(normalize=True) * 100
            weights = new_types_frequency.rdiv(other=new_types_frequency.iloc[0])
            weights = pd.DataFrame(weights).reset_index()
            weights.columns = ["type_new", "weight"]
            type_new_indices = weights['type_new'].map(self.type_new_to_indices_dict)
            weights['type_new_indices'] = type_new_indices
            weights.sort_values(by='type_new_indices', inplace=True)
            self.weights = torch.tensor(weights['weight'])

        if self.valid_file_name is not None:
            valid_DataFrame = pd.read_csv(os.path.join(self.data_dir, self.valid_file_name), encoding='utf_8',lineterminator='\n')
            self.valid_dataset = LandstackDataset(valid_DataFrame, self.tokenizer, self.source_max_token_len, self.num_labels)

        if self.test_file_name is not None:
            self.test_DataFrame = pd.read_csv(os.path.join(self.data_dir, self.test_file_name), encoding='utf_8',lineterminator='\n')
            self.test_dataset = LandstackDataset(self.test_DataFrame, self.tokenizer, self.source_max_token_len, self.num_labels)

        if self.predict_file_name is not None:
            self.predict_DataFrame = pd.read_csv(os.path.join(self.data_dir, self.predict_file_name), encoding='utf_8',lineterminator='\n')
            self.predict_dataset = LandstackDataset(self.predict_DataFrame, self.tokenizer, self.source_max_token_len, self.num_labels)

        if self.predict_inputs_list is not None:
            self.predict_DataFrame = pd.DataFrame(self.predict_inputs, columns=['planning_notes'])
            self.predict_dataset = LandstackDataset(self.predict_DataFrame, self.tokenizer, self.source_max_token_len, self.num_labels)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.valid_dataset, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=False)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=False)

    def predict_dataloader(self):
        return DataLoader(self.predict_dataset, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=False)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)