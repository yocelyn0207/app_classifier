import os
import csv
import random
import re

from tqdm import tqdm
import pandas as pd
import numpy as np



from scripts.preprocessing.use_class_classifier.utils import incontinuous_descriptions_with_or_without_tags, \
    tags_only_expressions, generate_non_sense_data, generate_general_description_with_specific_tags, \
    continuous_descriptions_with_continuous_tags, generate_fake_data



class augment_data:
    def __init__(self,output_folder_path:str, output_file_name:str):

        # self.data = pd.read_csv(input_file_path, encoding='latin_1')
        # columns = ['planning_notes'] + use_classes
        # self.data = self.data[columns]
        # self.original_data_length = len(self.data)
        self.use_classes = ['sui generis', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2','b8', 'c1', 'c2', 'c3',
                            'c4', 'd1', 'd2']

        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        self.output_file_path = output_folder_path + f'/{output_file_name}.csv'

    def register_keywords(self, **kwargs):
        self.headword_synonyms_list_sui_generis = kwargs['headword_synonyms_list_sui_generis']
        self.headword_synonyms_list_a1 = kwargs['headword_synonyms_list_a1']
        self.headword_synonyms_list_a2 = kwargs['headword_synonyms_list_a2']
        self.headword_synonyms_list_a3 = kwargs['headword_synonyms_list_a3']
        self.headword_synonyms_list_a4 = kwargs['headword_synonyms_list_a4']
        self.modifier_synonyms_list_a5 = kwargs['modifier_synonyms_list_a5']
        self.headword_synonyms_list_a5 = kwargs['headword_synonyms_list_a5']
        self.headword_synonyms_list_b1 = kwargs['headword_synonyms_list_b1']
        self.headword_synonyms_list_b2 = kwargs['headword_synonyms_list_b2']
        self.headword_synonyms_list_b8 = kwargs['headword_synonyms_list_b8']
        self.headword_synonyms_list_c1 = kwargs['headword_synonyms_list_c1']
        self.headword_synonyms_list_c2 = kwargs['headword_synonyms_list_c2']
        self.headword_synonyms_list_c3 = kwargs['headword_synonyms_list_c3']
        self.headword_synonyms_list_c4 = kwargs['headword_synonyms_list_c4']
        self.headword_synonyms_list_d1 = kwargs['headword_synonyms_list_d1']
        self.headword_synonyms_list_d2 = kwargs['headword_synonyms_list_d2']
        self.headword_synonyms_list_a = kwargs['headword_synonyms_list_a']
        self.headword_synonyms_list_b = kwargs['headword_synonyms_list_b']
        self.headword_synonyms_list_c = kwargs['headword_synonyms_list_c']
        self.headword_synonyms_list_d = kwargs['headword_synonyms_list_d']
        self.headword_synonyms_list_all = kwargs['headword_synonyms_list_all']

    def other_information(self,**kwargs):
        self.keywords_list_irrelative_words=kwargs['keywords_list_irrelative_words']
        self.general_words=kwargs['general_words']
        self.joint_symbol_list = kwargs['joint_symbol_list']
        self.change_of_use_patterns_dict = {'one_span':[],'two_spans':[]}
        for pattern in kwargs['change_of_use_patterns']:
            if re.search('<FROM>',pattern) is None or re.search('<TO>',pattern) is None:
                self.change_of_use_patterns_dict['one_span'].append(pattern)
            else:
                self.change_of_use_patterns_dict['two_spans'].append(pattern)


    def add_fake_data(self, target_use_class, num_generate_length_per_keyword:int = 2000):

        row_use_class = [0.0] * len(self.use_classes)
        index_target_use_class_c3 = self.use_classes.index('c3')

        if target_use_class == 'a':
            index_target_use_class = self.use_classes.index('a1')
            row_use_class[index_target_use_class] = 1.0
            randomly_adding_tags = False
        elif target_use_class == 'b':
            index_target_use_class = self.use_classes.index('b1')
            row_use_class[index_target_use_class] = 1.0
            randomly_adding_tags = False
        elif target_use_class == 'c':
            index_target_use_class = index_target_use_class_c3
            row_use_class[index_target_use_class] = 1.0
            randomly_adding_tags = False
        elif target_use_class == 'd':
            index_target_use_class = self.use_classes.index('d1')
            row_use_class[index_target_use_class] = 1.0
            randomly_adding_tags = False
        else:
            index_target_use_class = self.use_classes.index(target_use_class)
            row_use_class[index_target_use_class] = 1.0
            randomly_adding_tags = True


        if target_use_class == 'sui generis':
            target_use_class_for_getting_keywords_list = 'sui_generis'
        else:
            target_use_class_for_getting_keywords_list = target_use_class

        headwords = set(getattr(self, f'headword_synonyms_list_{target_use_class_for_getting_keywords_list}'))

        with open(self.output_file_path, mode='a') as new_data:
            new_data_writer = csv.writer(new_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row = ['planning_notes']+self.use_classes+['data_with_tags','modified_non_sense_data']
            new_data_writer.writerow(row)
            for headword in tqdm(headwords):
                for _ in range(num_generate_length_per_keyword):
                    text, _, has_tag, has_live_work_units = generate_fake_data(self_of_class=self, target_use_class=target_use_class,
                                              general_words=self.general_words,
                                              keywords_list_irrelative_words=self.keywords_list_irrelative_words,
                                              joint_symbol_list=self.joint_symbol_list,
                                              headwords=[headword],
                                              randomly_adding_tags=randomly_adding_tags)

                    if random.choice(['use_pattern', 'no']) == 'use_pattern':
                        pattern = random.choice(self.change_of_use_patterns_dict['one_span'])
                        text = re.sub('<FROM>|<TO>', text, pattern)

                    if has_live_work_units is True:
                        row_use_class[index_target_use_class_c3] = 1.0

                    row = [text]
                    row += row_use_class
                    row += [has_tag]
                    new_data_writer.writerow(row)



            # if hmo/house in multiple occupation doesn't specify no. of dwellers, but specify tag of sui generis,
            # should be sui generis.
            if target_use_class == 'sui generis':
                headwords = ['hmo', 'house in multiple occupation']
                for headword in tqdm(headwords):
                    for _ in range(num_generate_length_per_keyword):
                        text, _, has_tag,_ = generate_fake_data(self_of_class=self, target_use_class=target_use_class,
                                                  keywords_list_irrelative_words=self.keywords_list_irrelative_words,
                                                  joint_symbol_list=self.joint_symbol_list,
                                                  general_words=self.general_words,
                                                  headwords=[headword],
                                                  randomly_adding_tags=False,
                                                  must_add_tags=True,
                                                  diversify_tags=False,
                                                  allow_add_dweller_num=False)
                        if random.choice(['use_pattern','no']) == 'use_pattern':
                            pattern = random.choice(self.change_of_use_patterns_dict['one_span'])
                            text = re.sub('<FROM>|<TO>', text, pattern)
                        row = [text]
                        row += row_use_class
                        row += [has_tag]
                        new_data_writer.writerow(row)


            # if hmo/house in multiple occupation doesn't specify no. of dwellers or tags, default to be c4.
            if target_use_class == 'c4':
                headwords = ['hmo', 'house in multiple occupation']
                for headword in tqdm(headwords):
                    for _ in range(num_generate_length_per_keyword):
                        text, _, has_tag,_ = generate_fake_data(self_of_class=self, target_use_class=target_use_class,
                                                  keywords_list_irrelative_words=self.keywords_list_irrelative_words,
                                                  joint_symbol_list=self.joint_symbol_list,
                                                  general_words=self.general_words,
                                                  headwords=[headword],
                                                  randomly_adding_tags=True,must_add_tags=False,allow_add_dweller_num=False)

                        if random.choice(['use_pattern','no']) == 'use_pattern':
                            pattern = random.choice(self.change_of_use_patterns_dict['one_span'])
                            text = re.sub('<FROM>|<TO>', text, pattern)
                        row = [text]
                        row += row_use_class
                        row += [has_tag]
                        new_data_writer.writerow(row)




    def add_general_expressions_with_specific_tags(self, target_use_class:str,
                                                   num_generate_length_per_keyword:int = 2000,
                                                   allow_gibberish:bool = True):
        headwords = getattr(self, f'headword_synonyms_list_{target_use_class}')
        with open(self.output_file_path, mode='a') as new_data:
            new_data_writer = csv.writer(new_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row = ['planning_notes']+self.use_classes+['data_with_tags','modified_non_sense_data']
            new_data_writer.writerow(row)
            for headword in tqdm(headwords):
                for _ in range(num_generate_length_per_keyword):
                    text, all_chosen_use_classes = \
                        generate_general_description_with_specific_tags(self_of_class=self,
                                                                        target_use_class = target_use_class,
                                                                        keywords_list_irrelative_words=self.keywords_list_irrelative_words,
                                                                        joint_symbol_list=self.joint_symbol_list,
                                                                        general_words=self.general_words,
                                                                        headwords=[headword],
                                                                        allow_gibberish=allow_gibberish)

                    if random.choice(['use_pattern', 'no']) == 'use_pattern':
                        pattern = random.choice(self.change_of_use_patterns_dict['one_span'])
                        text = re.sub('<FROM>|<TO>', text, pattern)

                    row = [text]
                    row += [1.0 if use_class in all_chosen_use_classes else 0.0 for use_class in self.use_classes]
                    row += ['Y']
                    new_data_writer.writerow(row)



    def add_tags_only_data(self, max_generate_length:int=500000, allow_gibberish:bool = True):
        with open(self.output_file_path, mode='a') as new_data:
            new_data_writer = csv.writer(new_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row = ['planning_notes']+self.use_classes+['data_with_tags','modified_non_sense_data']
            new_data_writer.writerow(row)
            for _ in tqdm(range(max_generate_length)):
                text, all_chosen_use_classes = \
                    tags_only_expressions(self_of_class=self,
                                          keywords_list_irrelative_words = self.keywords_list_irrelative_words,
                                          joint_symbol_list=self.joint_symbol_list,
                                          allow_gibberish = allow_gibberish)

                if random.choice(['use_pattern', 'no']) == 'use_pattern':
                    pattern = random.choice(self.change_of_use_patterns_dict['one_span'])
                    text = re.sub('<FROM>|<TO>', text, pattern)

                row = [text]
                row += [1.0 if use_class in all_chosen_use_classes else 0.0 for use_class in self.use_classes]
                row += ['Y','Y']
                new_data_writer.writerow(row)


    def add_non_sense_data(self,max_generate_length:int=50000):
        row_use_classes = [0.0] * len(self.use_classes)
        with open(self.output_file_path, mode='a') as new_data:
            new_data_writer = csv.writer(new_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row = ['planning_notes']+self.use_classes+['data_with_tags','modified_non_sense_data']
            new_data_writer.writerow(row)
            for _ in tqdm(range(max_generate_length)):
                text = generate_non_sense_data(self_of_class=self,
                                               keywords_list_irrelative_words=self.keywords_list_irrelative_words,
                                               joint_symbol_list=self.joint_symbol_list)
                if random.choice(['use_pattern', 'no']) == 'use_pattern':
                    pattern = random.choice(self.change_of_use_patterns_dict['one_span'])
                    text = re.sub('<FROM>|<TO>', text, pattern)

                row = [text]
                row += row_use_classes
                row += ['', 'Y']
                new_data_writer.writerow(row)





    def add_incontinuous_descriptions(self, max_generate_length:int = 500000, allow_gibberish: bool = True):
        with open(self.output_file_path, mode='a') as new_data:
            new_data_writer = csv.writer(new_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row = ['planning_notes']+self.use_classes+['data_with_tags','modified_non_sense_data']
            new_data_writer.writerow(row)
            for _ in tqdm(range(max_generate_length)):
                text, all_chosen_use_classes, has_tags = \
                    incontinuous_descriptions_with_or_without_tags(self_of_class = self,
                                                                   joint_symbol_list = self.joint_symbol_list,
                                                                   keywords_list_irrelative_words=self.keywords_list_irrelative_words,
                                                                   general_words=self.general_words,
                                                                   allow_gibberish = allow_gibberish)

                if random.choice(['use_pattern', 'no']) == 'use_pattern':
                    pattern = random.choice(self.change_of_use_patterns_dict['one_span'])
                    text = re.sub('<FROM>|<TO>', text, pattern)

                row = [text]
                row += [1.0 if use_class in all_chosen_use_classes else 0.0 for use_class in self.use_classes]
                row += [has_tags]
                new_data_writer.writerow(row)



    def add_continuous_descripstions_with_continuous_tags(self, max_generate_length=500000, allow_gibberish: bool = True):
        with open(self.output_file_path, mode='a') as new_data:
            new_data_writer = csv.writer(new_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row = ['planning_notes']+self.use_classes+['data_with_tags','modified_non_sense_data']
            new_data_writer.writerow(row)
            for _ in tqdm(range(max_generate_length)):
                text, all_chosen_use_classes = \
                    continuous_descriptions_with_continuous_tags(self_of_class=self, joint_symbol_list=self.joint_symbol_list,
                                                                 keywords_list_irrelative_words = self.keywords_list_irrelative_words,
                                                                 general_words=self.general_words,
                                                                 allow_gibberish=allow_gibberish)
                if random.choice(['use_pattern', 'no']) == 'use_pattern':
                    pattern = random.choice(self.change_of_use_patterns_dict['one_span'])
                    text = re.sub('<FROM>|<TO>', text, pattern)

                row = [text]
                row += [1.0 if use_class in all_chosen_use_classes else 0.0 for use_class in self.use_classes]
                row += ['Y']
                new_data_writer.writerow(row)







    def add_combined_data_with_and_without_tags(self,
                                                max_generated_length_for_data_with_tags: int = 300000,
                                                max_generated_length_for_data_without_tags: int = 1000000,
                                                max_generated_length_for_data_with_and_without_tags: int = 500000):
        data = pd.read_csv(self.output_file_path, encoding='utf_8')

        data_with_tags = data[data.data_with_tags == 'Y']
        data_without_tags = data[data.data_with_tags != 'Y']
        current_data_length_with_tags = len(data_with_tags)
        current_data_length_without_tags = len(data_without_tags)


        with open(self.output_file_path, mode='a') as new_data:
            new_data_writer = csv.writer(new_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # 1. Gnerate combined data with tags.
            for _ in tqdm(range(max_generated_length_for_data_with_tags)):
                chosen_num_of_rows_with_tags = random.randint(2, 3)
                rows_indices_with_tags = random.sample(range(current_data_length_with_tags), chosen_num_of_rows_with_tags)
                rows_with_tags = data_with_tags.iloc[rows_indices_with_tags]
                use_classes_of_rows_with_tags = set(use_class for use_class in self.use_classes if sum(rows_with_tags.loc[:, use_class]>=1))
                planning_notes_of_rows_with_tags = rows_with_tags['planning_notes'].values
                random.shuffle(planning_notes_of_rows_with_tags)

                # Generate combined data.
                joint_symbol = random.choice(self.joint_symbol_list)
                new_row = [joint_symbol.join(planning_notes_of_rows_with_tags)]
                new_row += [1.0 if use_class in use_classes_of_rows_with_tags else 0.0 for use_class in self.use_classes]
                new_row += ['Y'] # 'data_with_tags'
                new_data_writer.writerow(new_row)

                # new_row = {use_class: 1.0 if use_class in use_classes_of_rows_with_tags else 0.0 for use_class in self.use_classes}
                # new_row.update({'planning_notes': joint_symbol.join(planning_notes_of_rows_with_tags), 'data_with_tags': 'Y'})
                # new_row = pd.DataFrame([new_row])
                # self.data = pd.concat([self.data, new_row])


            # 2. Gnerate combined data without tags.
            for _ in tqdm(range(max_generated_length_for_data_without_tags)):
                chosen_num_of_rows_without_tags = random.randint(2, 3)
                rows_indices_without_tags = random.sample(range(current_data_length_without_tags), chosen_num_of_rows_without_tags)
                rows_without_tags = data_without_tags.iloc[rows_indices_without_tags]
                use_classes_of_rows_without_tags = set(use_class for use_class in self.use_classes if sum(rows_without_tags.loc[:, use_class] >= 1))
                planning_notes_of_rows_without_tags = rows_without_tags['planning_notes'].values
                random.shuffle(planning_notes_of_rows_without_tags)

                # Generate combined data.
                joint_symbol = random.choice(self.joint_symbol_list)
                new_row = [joint_symbol.join(planning_notes_of_rows_without_tags)]
                new_row += [1.0 if use_class in use_classes_of_rows_without_tags else 0.0 for use_class in self.use_classes]
                new_data_writer.writerow(new_row)

                # new_row = {use_class: 1.0 if use_class in use_classes_of_rows_without_tags else 0.0 for use_class in self.use_classes}
                # joint_symbol = random.choice(joint_symbol_list)
                # new_row.update({'planning_notes': joint_symbol.join(planning_notes_of_rows_without_tags)})
                # new_row = pd.DataFrame([new_row])
                # self.data = pd.concat([self.data, new_row])


            # 3. Generate combined data with and without tags.
            for _ in tqdm(range(max_generated_length_for_data_with_and_without_tags)):
                chosen_num_of_rows_with_tags = random.randint(1, 2)
                rows_indices_with_tags = random.sample(range(current_data_length_with_tags), chosen_num_of_rows_with_tags)
                rows_with_tags = data_with_tags.iloc[rows_indices_with_tags]
                use_classes_of_rows_with_tags = set(use_class for use_class in self.use_classes if sum(rows_with_tags.loc[:, use_class]>=1))
                planning_notes_of_rows_with_tags = rows_with_tags['planning_notes'].values

                chosen_num_of_rows_without_tags = random.randint(1, 2)
                rows_indices_without_tags = random.sample(range(current_data_length_without_tags), chosen_num_of_rows_without_tags)
                rows_without_tags = data_without_tags.iloc[rows_indices_without_tags]
                use_classes_of_rows_without_tags = set(use_class for use_class in self.use_classes if sum(rows_without_tags.loc[:, use_class] >= 1))
                planning_notes_of_rows_without_tags = rows_without_tags['planning_notes'].values

                # Generate combined data.
                combination_of_use_classes = use_classes_of_rows_with_tags.union(use_classes_of_rows_without_tags)
                planning_notes_combined = np.concatenate((planning_notes_of_rows_with_tags, planning_notes_of_rows_without_tags))
                random.shuffle(planning_notes_combined)
                joint_symbol = random.choice(self.joint_symbol_list)
                new_row = [joint_symbol.join(planning_note for planning_note in planning_notes_combined)]
                new_row += [1.0 if use_class in combination_of_use_classes else 0.0 for use_class in self.use_classes]
                new_row += ['Y']  # 'data_with_tags'
                new_data_writer.writerow(new_row)











