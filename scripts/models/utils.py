import re
import json
import numpy as np



class Params():
    """Class that loads hyperparameters from a json file.
    Example:
    ```
    params = Params(json_path)
    print(params.learning_rate)
    params.learning_rate = 0.5  # change the value of learning_rate in params
    ```
    """

    def __init__(self, json_path):
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    def save(self, json_path):
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)

    def update(self, json_path):
        """Loads parameters from json file"""
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    @property
    def dict(self):
        """Gives dict-like access to Params instance by `params.dict['learning_rate']"""
        return self.__dict__



def generate_bad_words_ids(tokenizer, use_classes: list):
    '''
    :param tokenizer: T5Tokenizer
    :param use_classes: a list of use classes
    :return: a list of bad words ids, e.g., [0, 1, 2, 4,...]. It should only exclude use classes ids and <EOS>.
    '''
    use_classes.append('None')
    good_words_ids = set(tokenizer(' '.join(use_classes), add_special_tokens=False).input_ids)
    return [[i] for i in range(len(tokenizer)) if i not in good_words_ids]





def process_preds_and_labels_to_readable_list(model_name:str, preds: np.array, labels: np.array = None,
                                              **kwargs):
    '''
    :param model_name: should be one of {'use_class_classifier', 'change_of_use', 'app_type_classifier'}
    :param preds:
                'use_class_classifier', 'change_of_use': a list of predicted use classes, e.g.,
                ['sui generis None a2 None a3 None None b1 b2 b8 c1 None c3 None d1 None']
                'app_type_classifier': a list of predicted label ids, e.g., [0,1,38,5,10]
    :param labels:
                 'use_class_classifier', 'change_of_use': a list of ground truth use classes, e.g.,
                 ['sui generis None a2 None a3 None None b1 b2 b8 c1 None c3 None d1 None']
                 'app_type_classifier': a list of labels, e.g.,
                 ['Full Application', 'Outline application','Conservation Area','Full Application']
    :return demolitions_sequences:
                                'use_class_classifier', 'change_of_use': a list of lists, e.g.,
                                [['sui generis','c3'], ['a1'], []]
                                'app_type_classifier': None
    :return erections_sequences:
                                'use_class_classifier', 'change_of_use': a list of lists, e.g.,
                                [['sui generis','c3'], ['a1'], []]
                                'app_type_classifier': a list of labels, e.g.,
                                ['Full Application', 'Outline application','Conservation Area','Full Application']
    :return labels_sequences:
                                'use_class_classifier', 'change_of_use':  a list of lists, e.g.,
                                [['sui generis','c3'], ['a1'], []]
                                'app_type_classifier': a list of labels, e.g.,
                                ['Full Application', 'Outline application','Conservation Area','Full Application']
    :return correctnessCheck: a list of strings, e.g., ['Y', 'N', 'N', 'Y']. 'Y' is correct, 'N' is incorrect.
    '''

    def _process_string_to_list_items(text: str):
        text_clean_None = re.sub('None', '', text)
        text_clean_None = re.sub(' +', ' ', text_clean_None)


        if text_clean_None == ' ':
            text_sequence_list = []
        else:
            if text_clean_None[0] == ' ':
                text_clean_None = text_clean_None[1:]
            if text_clean_None[-1] == ' ':
                text_clean_None = text_clean_None[:-1]
            if 'sui' in text_clean_None:
                if text_clean_None == 'sui generis':
                    text_sequence_list = ['sui generis']
                else:
                    text_sequence_list = ['sui generis'] + re.split(' ', text_clean_None[12:])
            else:
                text_sequence_list = re.split(' ', text_clean_None)
        return text_sequence_list



    if model_name == 'use_class_classifier':
        demolitions_sequences = []
        erections_sequences = []
        correctnessCheck = []
        labels_sequences = []

        for pred in preds:
            erections_sequences.append(_process_string_to_list_items(pred))

        if labels is not None:
            for i in range(len(preds)):
                correctnessCheck.append('Y') if preds[i] == labels[i] else correctnessCheck.append('N')

            for label in labels:
                labels_sequence = _process_string_to_list_items(label)
                labels_sequences.append(labels_sequence)



    elif model_name == 'change_of_use':
        middle = int(len(preds) / 2)
        demolitions = preds[:middle]
        erections = preds[middle:]


        demolitions_sequences = []
        for demolition in demolitions:
            demolitions_sequences.append(_process_string_to_list_items(demolition))


        erections_sequences = []
        for erection in erections:
            erections_sequences.append(_process_string_to_list_items(erection))

        labels_sequences = []
        correctnessCheck = []



    elif model_name == 'app_type_classifier':
        demolitions_sequences = []
        erections_sequences = []
        correctnessCheck = []
        labels_sequences = labels

        for pred in preds:
            erections_sequences.append(kwargs['indices_to_type_new_dict'][str(pred)])

        if labels is not None:
            for i in range(len(preds)):
                correctnessCheck.append('Y') if preds[i] == labels[i] else correctnessCheck.append('N')

    return demolitions_sequences, erections_sequences, labels_sequences, correctnessCheck




