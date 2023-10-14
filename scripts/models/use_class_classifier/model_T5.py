import os.path
from pathlib import Path

import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.metrics import classification_report

from scripts.models.use_class_classifier.dataset_preparation_T5 import LandstackDataset
from scripts.models.utils import generate_bad_words_ids




class CustomT5(pl.LightningModule):
    def __init__(self, config, pretrained_T5_model_name: str, use_classes: list,
                 source_max_token_len: int,
                 num_beams: int, num_workers: int,
                 data_dir: Path, save_dir: Path,
                 train_file_name: str,
                 valid_file_name: str, valid_fscore_save_file_name: str,
                 test_file_name: str, test_fscore_save_file_name: str, test_preds_save_file_name: str,
                 predict_file_name: str, predict_preds_save_file_name: str,
                 predict_inputs: list):
        super().__init__()

        self.lr = config['learning_rate']
        self.batch_size = config['batch_size']

        self.pretrained_T5_model_name = pretrained_T5_model_name
        self.use_classes = use_classes
        self.source_max_token_len = source_max_token_len
        self.target_max_token_len = len(use_classes)
        self.num_beams = num_beams
        self.num_workers = num_workers

        self.data_dir = data_dir
        self.save_dir = save_dir
        self.train_file_name = train_file_name
        self.valid_file_name = valid_file_name
        self.valid_fscore_save_file_name = valid_fscore_save_file_name
        self.test_file_name = test_file_name
        self.test_fscore_save_file_name = test_fscore_save_file_name
        self.test_preds_save_file_name = test_preds_save_file_name
        self.predict_file_name = predict_file_name
        self.predict_preds_save_file_name = predict_preds_save_file_name
        self.predict_inputs = predict_inputs

        self.tokenizer = T5Tokenizer.from_pretrained(pretrained_T5_model_name)
        self.tokenizer.add_tokens([use_class for use_class in use_classes])  # add each use class as special tokens

        self.model = T5ForConditionalGeneration.from_pretrained(pretrained_T5_model_name)
        self.model.resize_token_embeddings(len(self.tokenizer))

        use_classes_encoding = self.tokenizer(
            ' '.join([cl for cl in self.use_classes]),
            max_length=self.target_max_token_len,
            padding="max_length",
            truncation=True,
            return_attention_mask=True,
            add_special_tokens=False,
            return_tensors="pt"
        )
        self.use_classes_indices = use_classes_encoding.input_ids.view(-1)  # (num_use_classes)

    def forward(self, input_ids, attention_mask, output_ids=None):

        if output_ids is not None:
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, labels=output_ids)
        else:
            bad_words_ids = generate_bad_words_ids(self.tokenizer, self.use_classes)
            outputs = self.model.generate(input_ids=input_ids, attention_mask=attention_mask,
                                          num_beams=self.num_beams, max_length=self.target_max_token_len + 1,
                                          # there's a <PAD> at beginning
                                          min_length=self.target_max_token_len + 1,
                                          bad_words_ids=bad_words_ids)

        return outputs

    def _decode_preds_from_logits(self, logits):
        # logits: (batch_size, out_sequence_len, vocab_size)
        # indices of tokens, e.g., tensor([[    1, 32098,     2,    46, 32098]]). (batch_size, target_max_token_len)
        preds_ids = torch.max(logits, dim=2).indices  # (batch_size, out_sequence_len)
        # a list of strings, e.g., ['None a1 a2 b8...', 'sui generis None None...']. len(preds) = batch_size
        preds = self.tokenizer.batch_decode(preds_ids, skip_special_tokens=True)
        return preds, preds_ids

    def _precision_recall_fscore(self, preds_ids, labels_ids):
        # preds_ids, labels_ids: indices of tokens, e.g., tensor([[    1, 32098,     2,    46, 32098]]). (batch_size, target_max_token_len)

        preds_tensors = preds_ids.cpu() == self.use_classes_indices.cpu()  # (batch_size, target_max_token_len) with true or false
        preds_tensors = preds_tensors.long()  # (batch_size, target_max_token_len) with 0 or 1
        labels_tensors = labels_ids.cpu() == self.use_classes_indices.cpu()
        labels_tensors = labels_tensors.long()

        # A dict of use classes with precision, recall, and f1-score, e.g.,
        # {'c1': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 1},
        # 'c2': {'precision': 1.0, 'recall': 1.0, 'f1-score': 1.0, 'support': 2},
        # 'micro avg': {'precision': 1.0, 'recall': 0.83, 'f1-score': 0.90, 'support': 6},
        # 'macro avg': {'precision': 1.0, 'recall': 0.87, 'f1-score': 0.91, 'support': 6},
        # 'weighted avg': {'precision': 1.0, 'recall': 0.83, 'f1-score': 0.88, 'support': 6},
        # 'samples avg': {'precision': 1.0, 'recall': 0.88, 'f1-score': 0.93, 'support': 6}
        scores = classification_report(y_pred=preds_tensors, y_true=labels_tensors,
                                       target_names=self.use_classes, output_dict=True, zero_division=1)
        return scores

    def training_step(self, batch, batch_idx):
        # input_ids, attention_mask (batch_size, 1, source_max_token_len) -> (batch_size, source_max_token_len)
        # output_ids (batch_size, 1, target_max_token_len) -> (batch_size, target_max_token_len)
        input_ids, attention_mask, output_ids = batch['input_ids'].view(-1, self.source_max_token_len), \
                                                batch['attention_mask'].view(-1, self.source_max_token_len), \
                                                batch['output_ids'].view(-1, self.target_max_token_len)
        loss = self(input_ids, attention_mask, output_ids).loss
        self.log('train_loss', loss, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        # input_ids, attention_mask (batch_size, 1, source_max_token_len) -> (batch_size, source_max_token_len)
        # output_ids (batch_size, 1, target_max_token_len) -> (batch_size, target_max_token_len)
        input_ids, attention_mask, output_ids = batch['input_ids'].view(-1, self.source_max_token_len), \
                                                batch['attention_mask'].view(-1, self.source_max_token_len), \
                                                batch['output_ids'].view(-1, self.target_max_token_len)
        outputs = self(input_ids, attention_mask, output_ids)
        loss = outputs.loss
        preds, preds_ids = self._decode_preds_from_logits(outputs.logits)
        self.log('validate_loss', loss, prog_bar=True, logger=True)
        return {'validate_loss': loss, 'preds': preds, 'preds_ids': preds_ids, 'labels_ids': output_ids}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x["validate_loss"] for x in outputs]).mean()
        preds_ids = torch.concat([x["preds_ids"] for x in outputs])
        labels_ids = torch.concat([x["labels_ids"] for x in outputs])

        scores = self._precision_recall_fscore(preds_ids, labels_ids)
        file_name = f'{self.valid_fscore_save_file_name}_epoch={self.current_epoch}.pt'
        torch.save(scores, os.path.join(self.save_dir, file_name))
        self.log_dict({'validate_loss_avg': avg_loss,
                       'precision_avg': torch.tensor(scores['weighted avg']["precision"]),
                       'recall_avg': torch.tensor(scores['weighted avg']["recall"]),
                       'f1_avg': torch.tensor(scores['weighted avg']["f1-score"])})

    def test_step(self, batch, batch_idx):
        # input_ids, attention_mask (batch_size, 1, source_max_token_len) -> (batch_size, source_max_token_len)
        # output_ids (batch_size, 1, target_max_token_len) -> (batch_size, target_max_token_len)
        input_ids, attention_mask, output_ids, labels = batch['input_ids'].view(-1, self.source_max_token_len), \
                                                        batch['attention_mask'].view(-1, self.source_max_token_len), \
                                                        batch['output_ids'].view(-1, self.target_max_token_len), \
                                                        batch['labels']
        outputs = self(input_ids, attention_mask, output_ids=None)
        loss = outputs.loss
        preds, preds_ids = self._decode_preds_from_logits(outputs.logits)
        self.log('test_loss', loss, prog_bar=True, logger=True)
        return {'test_loss': loss, 'preds': preds, 'preds_ids': preds_ids, 'labels': labels, 'labels_ids': output_ids}

    def test_epoch_end(self, outputs):
        avg_loss = torch.stack([x["test_loss"] for x in outputs]).mean()
        preds = np.hstack((x["preds"] for x in outputs))
        preds_ids = torch.concat([x["preds_ids"] for x in outputs])
        labels = np.hstack((x["labels"] for x in outputs))
        labels_ids = torch.concat([x["labels_ids"] for x in outputs])

        scores = self._precision_recall_fscore(preds_ids, labels_ids)
        file_name = f'{self.test_fscore_save_file_name}_epoch={self.current_epoch}.pt'
        torch.save(scores, os.path.join(self.save_dir, file_name))

        # results = process_preds_to_readable_file(model = 'use_class_classifier', preds = preds,
        #                                          planning_notes = self.test_DataFrame['planning_notes'], labels=labels)
        # file_name = f'{self.test_preds_save_file_name}_epoch={self.current_epoch}.csv'
        # results.to_csv(os.path.join(self.save_dir, file_name))

        self.log_dict({'test_loss_avg': avg_loss,
                       'precision_avg': torch.tensor(scores['weighted avg']["precision"]),
                       'recall_avg': torch.tensor(scores['weighted avg']["recall"]),
                       'f1_avg': torch.tensor(scores['weighted avg']["f1-score"])})

    def predict_step(self, batch, batch_idx):
        # input_ids, attention_mask (batch_size, 1, source_max_token_len) -> (batch_size, source_max_token_len)
        input_ids, attention_mask, output_ids, labels = batch['input_ids'].view(-1, self.source_max_token_len), \
                                                        batch['attention_mask'].view(-1, self.source_max_token_len), \
                                                        batch['output_ids'].view(-1, self.target_max_token_len), \
                                                        batch['labels']

        # outputs = self(input_ids, attention_mask, output_ids) # token indices, (batch_size, target_max_token_len)
        # preds, preds_ids = self._decode_preds_from_logits(outputs.logits)
        preds_ids = self(input_ids, attention_mask)  # token indices, (batch_size, target_max_token_len)
        preds = self.tokenizer.batch_decode(preds_ids, skip_special_tokens=True,
                                            clean_up_tokenization_spaces=True)  # list of string,  (batch_size)
        return {'preds': preds, 'labels': labels}

    def prepare_data(self):
        if self.train_file_name is not None:
            train_DataFrame = pd.read_csv(os.path.join(self.data_dir, self.train_file_name), encoding='utf_8')
            self.train_dataset = LandstackDataset(train_DataFrame, self.tokenizer, self.use_classes,
                                                  self.source_max_token_len)

        if self.valid_file_name is not None:
            valid_DataFrame = pd.read_csv(os.path.join(self.data_dir, self.valid_file_name), encoding='utf_8')
            self.valid_dataset = LandstackDataset(valid_DataFrame, self.tokenizer, self.use_classes,
                                                  self.source_max_token_len)

        if self.test_file_name is not None:
            self.test_DataFrame = pd.read_csv(os.path.join(self.data_dir, self.test_file_name), encoding='utf_8')
            self.test_dataset = LandstackDataset(self.test_DataFrame, self.tokenizer, self.use_classes,
                                                 self.source_max_token_len)

        if self.predict_file_name is not None:
            self.predict_DataFrame = pd.read_csv(os.path.join(self.data_dir, self.predict_file_name), encoding='utf_8')
            self.predict_dataset = LandstackDataset(self.predict_DataFrame, self.tokenizer, self.use_classes,
                                                    self.source_max_token_len)

        if self.predict_inputs is not None:
            self.predict_DataFrame = pd.DataFrame(self.predict_inputs, columns=['planning_notes'])
            self.predict_dataset = LandstackDataset(self.predict_DataFrame, self.tokenizer, self.use_classes,
                                                    self.source_max_token_len)



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