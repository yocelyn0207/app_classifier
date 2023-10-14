import os
import re
import random

import pandas as pd
import numpy as np
import json
import csv
from tqdm import tqdm

from scripts.preprocessing.application_type_classifier.utils import generate_research_regex_pattern_from_keyword_list
from scripts.preprocessing.application_type_classifier.keywords_of_types import *
from scripts.preprocessing.application_type_classifier.clean_types_by_keywords import clean_data_by_keywords
from scripts.preprocessing.application_type_classifier.augment_data import combine_two_applications, outline_to_full, outline_plus_all_matters_reserved, change_of_use_fake_data, non_advertisement_consent_fake_data
from scripts.preprocessing.change_of_use.split_planning_note_into_demolition_and_erection import split_planning_note_into_demolition_and_erection







def preprocess_data(mapping_list_file_path: str, sheet_name: str,
                    historic_data_file_path: str,
                    file_save_path: str,
                    type_old_and_hard_coding_mapping_save_file_name: str,
                    full_data_save_file_name: str,
                    max_generated_length_of_housholder_and_change_of_use: int = 300000,
                    max_generated_length_of_housholder_and_dwelling: int = 500000,
                    max_generated_length_of_mineral: int = 100000,
                    max_generated_length_of_waste: int = 100000,
                    max_generated_length_of_hazardous: int = 100000,
                    max_generated_length_of_agricultural: int = 100000,
                    max_generated_length_of_per_non_advertisement_keywords: int = 10000,
                    max_generated_length_of_per_non_advertisement_keywords_with_ad: int = 10000,
                    max_generated_length_of_non_advertisement_preps: int = 50000,
                    max_generated_length_of_advertisement_and_full: int = 50000):
    '''
    :param mapping_list_file_path: should be an excel file which includes 'type' and 'type_new' columns.
    :param sheet_name: the sheet name in the mapping list file.
    :param historic_data_file_path: should be a .csv file which includes 'planning_notes' and 'type' columns.
    :param file_save_path: the dir to save the new files.
    :param full_data_save_file_name: the name to save the full data to a new file. Please do not include the extension file name.
                                     Will be saved into a .csv file.s
    :return the new full data file which at least includes below columns:
             'reference',
             'planning_notes'
             'type': type of planning_note in our database from councils
             'type_list_mapping': new type by mapping rules from type
             'type_new': new type by keywords screening from type_list_mapping
             'demolitions',
             'erections',
             'change_of_use'
    :return statistics of new data vs old data
    '''

    # Step 1: Define keywords patterns
    pattern_non = generate_research_regex_pattern_from_keyword_list(non_keywords)
    pattern_consultation = generate_research_regex_pattern_from_keyword_list(Consultation_keywords)
    pattern_73 = generate_research_regex_pattern_from_keyword_list(Section_73_keywords)
    pattern_106 = generate_research_regex_pattern_from_keyword_list(Section_106_keywords)
    pattern_extension = generate_research_regex_pattern_from_keyword_list(Extension_of_Time_Application_keywords)
    pattern_discharge = generate_research_regex_pattern_from_keyword_list(Discharge_Of_Conditions_keywords)
    pattern_discharge_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Discharge_Of_Conditions_for_the_other_types_keywords)
    pattern_variation = generate_research_regex_pattern_from_keyword_list(Variation_or_Removal_of_Conditions_keywords)
    pattern_variation_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Variation_or_Removal_of_Conditions_for_the_other_types_keywords)
    pattern_details = generate_research_regex_pattern_from_keyword_list(Approval_of_Details_Pursuant_to_Conditions_keywords)
    pattern_details_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Approval_of_Details_Pursuant_to_Conditions_for_the_other_types_keywords)
    pattern_non_material = generate_research_regex_pattern_from_keyword_list(Non_Material_Amendments_keywords)
    pattern_minor_amendments = generate_research_regex_pattern_from_keyword_list(Minor_Amendments_keywords)
    pattern_prior_notification = generate_research_regex_pattern_from_keyword_list(Prior_Notification_keywords)
    pattern_permitted = generate_research_regex_pattern_from_keyword_list(Permitted_Development_keywords)
    pattern_reserved = generate_research_regex_pattern_from_keyword_list(Reserved_Matters_keywords)
    pattern_lawfulness = generate_research_regex_pattern_from_keyword_list(Certificate_of_Lawfulness_for_Proposed_or_Existing_Use_keywords)
    pattern_screening = generate_research_regex_pattern_from_keyword_list(Screening_Scoping_EIA_keywords)
    pattern_principle = generate_research_regex_pattern_from_keyword_list(Permission_in_Principle_keywords)
    pattern_technical_details = generate_research_regex_pattern_from_keyword_list(Technical_Details_Consent_keywords)
    pattern_county = generate_research_regex_pattern_from_keyword_list(County_Matters_Application_keywords)
    pattern_council = generate_research_regex_pattern_from_keyword_list(Councils_Own_Application_keywords)
    pattern_neighbouring = generate_research_regex_pattern_from_keyword_list(Neighbouring_Authority_Application_keywords)
    pattern_hybrid = generate_research_regex_pattern_from_keyword_list(Hybrid_Application_keywords)
    pattern_outline = generate_research_regex_pattern_from_keyword_list(Outline_Application_keywords)
    pattern_full = generate_research_regex_pattern_from_keyword_list(Full_Application_keywords)
    pattern_hedgerow = generate_research_regex_pattern_from_keyword_list(Hedgerow_Removal_keywords)
    pattern_telecom = generate_research_regex_pattern_from_keyword_list(Telecommunications_and_Overhead_Electricity_Lines_keywords)
    pattern_telecom_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Telecommunications_and_Overhead_Electricity_Lines_for_the_other_types_keywords)
    pattern_mineral = generate_research_regex_pattern_from_keyword_list(Minerals_Application_keywords)
    pattern_mineral_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Minerals_Application_keywords_for_the_other_types_keywords)
    pattern_waste = generate_research_regex_pattern_from_keyword_list(Waste_Management_Application_keywords)
    pattern_waste_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Waste_Management_Application_for_the_other_types_keywords)
    pattern_hazardous = generate_research_regex_pattern_from_keyword_list(Hazardous_Substances_Consent_Application_keywords)
    pattern_hazardous_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Hazardous_Substances_Consent_Application_for_the_other_types_keywords)
    pattern_agricultural = generate_research_regex_pattern_from_keyword_list(Agricultural_Development_keywords)
    pattern_agricultural_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Agricultural_Development_for_the_other_types_keywords)
    pattern_listed = generate_research_regex_pattern_from_keyword_list(Listed_Building_Application_keywords)
    pattern_listed_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Listed_Building_Application_for_the_other_types_keywords)
    pattern_conservation = generate_research_regex_pattern_from_keyword_list(Conservation_Area_keywords)
    pattern_conservation_for_the_other_types = generate_research_regex_pattern_from_keyword_list(Conservation_Area_for_the_other_types_keywords)
    pattern_other = generate_research_regex_pattern_from_keyword_list(Other_keywords)
    pattern_change_of_use = generate_research_regex_pattern_from_keyword_list(Change_of_Use_keywords)

    # Step 2: Process mapping list and create mapping dictionaries: type -> type_new,
    # type -> change_of_use
    mapping_df = pd.read_excel(mapping_list_file_path, sheet_name=sheet_name)

    type_old_to_type_new_dict = dict(zip(mapping_df.type, mapping_df.type_new))
    type_old_to_change_of_use_dict = dict(zip(mapping_df.type, mapping_df.change_of_use))

    mapping_df_copy = mapping_df.copy()
    mapping_df_copy['type_hard_coding'].replace('', np.nan, inplace=True)
    mapping_df_copy.dropna(subset=['type_hard_coding'], inplace=True)
    types_old_to_hard_coding_dict = dict(zip(mapping_df_copy.type, mapping_df_copy.type_hard_coding))

    if os.path.exists(file_save_path) is None:
        os.makedirs(file_save_path)

    with open(os.path.join(file_save_path, f'{type_old_and_hard_coding_mapping_save_file_name}.json'), 'w') as f:
        json.dump(types_old_to_hard_coding_dict, f)


    # Step 3: Map historic data using above mapping dictionaries
    # Drop rows where planning_notes is nan
    df = pd.read_csv(historic_data_file_path,lineterminator='\n', dtype = str)
    df['planning_notes'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['planning_notes'])
    original_data_len = len(df)
    original_types_num = len(df.type.dropna().unique())

    # Map type_new -> change_of_use
    change_of_use_column = df['type'].map(type_old_to_change_of_use_dict)
    df['change_of_use'] = change_of_use_column

    # Map type -> type_list_mapping
    type_list_mapping = df['type'].map(type_old_to_type_new_dict)
    # type_new = df['type'].map(types_mapping).fillna(df['type'])
    df['type_list_mapping'] = type_list_mapping

    # Map type_list_mapping -> type_new by keywords
    with open(os.path.join(file_save_path, f'{full_data_save_file_name}.csv'), mode='a', newline='') as df_new:
        df_new_writer = csv.writer(df_new, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        row = ["reference", "planning_notes", "type", "type_list_mapping", "type_new",
               "demolitions", "erections", "change_of_use"]
        df_new_writer.writerow(row)

        for _, row in tqdm(df.iterrows(), total=len(df)):
            type_new, change_of_use = clean_data_by_keywords(row,
                                   non = pattern_non,
                                   pattern_consultation = pattern_consultation,
                                   pattern_73 = pattern_73,
                                   pattern_106 = pattern_106,
                                   pattern_extension = pattern_extension,
                                   pattern_discharge = pattern_discharge,
                                   pattern_discharge_for_the_other_types= pattern_discharge_for_the_other_types,
                                   pattern_variation = pattern_variation,
                                   pattern_variation_for_the_other_types = pattern_variation_for_the_other_types,
                                   pattern_details = pattern_details,
                                   pattern_details_for_the_other_types = pattern_details_for_the_other_types,
                                   pattern_non_material = pattern_non_material,
                                   pattern_minor_amendments = pattern_minor_amendments,
                                   pattern_prior_notification = pattern_prior_notification,
                                   pattern_permitted = pattern_permitted,
                                   pattern_reserved = pattern_reserved,
                                   pattern_lawfulness = pattern_lawfulness,
                                   pattern_screening = pattern_screening,
                                   pattern_principle = pattern_principle,
                                   pattern_technical_details = pattern_technical_details,
                                   pattern_county = pattern_county,
                                   pattern_council = pattern_council,
                                   pattern_neighbouring = pattern_neighbouring,
                                   pattern_hybrid = pattern_hybrid,
                                   pattern_outline = pattern_outline,
                                   pattern_full = pattern_full,
                                   pattern_hedgerow = pattern_hedgerow,
                                   pattern_telecom = pattern_telecom,
                                   pattern_telecom_for_the_other_types = pattern_telecom_for_the_other_types,
                                   pattern_mineral = pattern_mineral,
                                   pattern_mineral_for_the_other_types = pattern_mineral_for_the_other_types,
                                   pattern_waste = pattern_waste,
                                   pattern_waste_for_the_other_types = pattern_waste_for_the_other_types,
                                   pattern_hazardous = pattern_hazardous,
                                   pattern_hazardous_for_the_other_types = pattern_hazardous_for_the_other_types,
                                   pattern_agricultural = pattern_agricultural,
                                   pattern_agricultural_for_the_other_types = pattern_agricultural_for_the_other_types,
                                   pattern_listed = pattern_listed,
                                   pattern_listed_for_the_other_types = pattern_listed_for_the_other_types,
                                   pattern_conservation = pattern_conservation,
                                   pattern_conservation_for_the_other_types = pattern_conservation_for_the_other_types,
                                   pattern_other = pattern_other,
                                   pattern_change_of_use = pattern_change_of_use)
            if type_new != '':
                row_new = [row.reference,row.planning_notes, row.type, row.type_list_mapping, type_new,
                           row.demolitions, row.erections, change_of_use]
                df_new_writer.writerow(row_new)



            if type_new == 'Outline Application':
                # data augmentation: outline -> full
                full_app = outline_to_full(str(row.planning_notes))
                if full_app != '':
                    demolition, erection = split_planning_note_into_demolition_and_erection(full_app)
                    if re.search(pattern_telecom_for_the_other_types, erection, flags=re.IGNORECASE) is None and \
                            re.search(pattern_mineral_for_the_other_types, erection, flags=re.IGNORECASE) is None and \
                            re.search(pattern_waste_for_the_other_types, erection, flags=re.IGNORECASE) is None and \
                            re.search(pattern_hazardous_for_the_other_types, erection, flags=re.IGNORECASE) is None and \
                            re.search(pattern_agricultural_for_the_other_types, erection, flags=re.IGNORECASE) is None:

                        row_new = ['fake data',full_app, '', '', 'Full Application',
                                   row.demolitions, row.erections, change_of_use]
                        df_new_writer.writerow(row_new)


                # data augmentation: outline + all matters reserved
                if re.search('matters? reserve', str(row.planning_notes)) is None:
                    outline_new = outline_plus_all_matters_reserved(str(row.planning_notes))
                    row_new = ['fake data', outline_new, '', '', 'Outline Application',
                               row.demolitions, row.erections, change_of_use]
                    df_new_writer.writerow(row_new)



            # data augmentation: Ad ATM - Ad keywords -> full
            if type_new == 'Advertisement Consent' and re.search('(^|\W)ATMs?($|\W)',row.planning_notes,re.IGNORECASE) is not None:
                full_app = re.sub(Advertisement_Consent_keywords[0], ' ',row.planning_notes, flags=re.IGNORECASE)
                full_app= re.sub('(^|\W)to ((the )|(new ))?ATMs?($|\W)', 'ATM', full_app, flags=re.IGNORECASE)
                full_app = full_app.lstrip().strip()
                full_app = re.sub(' +', ' ', full_app)
                if full_app[:3] == 'of ' or full_app[:3] == 'OF ':
                    full_app = random.choice([full_app[3:], random.choice(['installation ', 'retention ']) + full_app])
                elif full_app[:4] == 'for ' or full_app[:4] == 'FOR ':
                    full_app = 'application ' + full_app
                if re.search('sui generis',row.erections) is None:
                    erections = "['sui generis', " + row.erections[1:]
                else:
                    erections = row.erections
                row_new = ['fake data', full_app, '', '', 'Full Application', row.demolitions, erections, change_of_use]
                df_new_writer.writerow(row_new)


            # data augmentation: Ad shopfront - Ad keywords -> full
            if type_new == 'Advertisement Consent' and re.search('(^|\W)shop\s?fronts?($|\W)',row.planning_notes,re.IGNORECASE) is not None:
                full_app = re.sub(Advertisement_Consent_keywords[0], ' ',row.planning_notes, flags=re.IGNORECASE)
                full_app= re.sub('(^|\W)((to)|(on)|(behind)|(inside)) ((the )|(new ))?shop\s?fronts??($|\W)', 'shopfront', full_app, flags=re.IGNORECASE)
                full_app = full_app.lstrip().strip()
                full_app = re.sub(' +', ' ', full_app)
                if full_app[:3] == 'of ' or full_app[:3] == 'OF ':
                    full_app = random.choice([full_app[3:], random.choice(['installation ', 'retention ']) + full_app])
                elif full_app[:4] == 'for ' or full_app[:4] == 'FOR ':
                    full_app = 'application ' + full_app
                if re.search('a1',row.erections) is None:
                    if re.search('sui generis',row.erections) is None:
                        erections = "['a1', " + row.erections[1:]
                    else:
                        erections = "['sui generis', 'a1', " + row.erections[16:]
                else:
                    erections = row.erections
                row_new = ['fake data', full_app, '', '', 'Full Application', row.demolitions, erections, change_of_use]
                df_new_writer.writerow(row_new)


            # data augmentation: Ad marketing suite - Ad keywords -> full
            if type_new == 'Advertisement Consent' and re.search('(^|\W)marketing suites?($|\W)',row.planning_notes,re.IGNORECASE) is not None:
                full_app = re.sub(Advertisement_Consent_keywords[0], ' ',row.planning_notes, flags=re.IGNORECASE)
                full_app= re.sub('(^|\W)((to)|(on)|(behind)|(inside)) ((the )|(new ))?marketing suites?($|\W)', 'marketing suite', full_app, flags=re.IGNORECASE)
                full_app = full_app.lstrip().strip()
                full_app = re.sub(' +', ' ', full_app)
                if full_app[:3] == 'of ' or full_app[:3] == 'OF ':
                    full_app = random.choice([full_app[3:], random.choice(['installation ', 'retention ']) + full_app])
                elif full_app[:4] == 'for ' or full_app[:4] == 'FOR ':
                    full_app = 'application ' + full_app
                if re.search('a1',row.erections) is None:
                    if re.search('sui generis',row.erections) is None:
                        erections = "['a1', " + row.erections[1:]
                    else:
                        erections = "['sui generis', 'a1', " + row.erections[16:]
                else:
                    erections = row.erections
                row_new = ['fake data', full_app, '', '', 'Full Application', row.demolitions, erections, change_of_use]
                df_new_writer.writerow(row_new)





    df_new = pd.read_csv(os.path.join(file_save_path, f'{full_data_save_file_name}.csv'))


    householder = df_new[df_new["type_new"] == "Householder Application"]
    full_and_change_of_use = df_new[(df_new.change_of_use == 'Y') & (df_new.type_new == 'Full Application')]
    full_and_c3 = df_new[((df_new.demolitions == "['c3']") | (df_new.erections == "['c3']")) & (df_new.type_new == 'Full Application')]
    advertisement = df_new[df_new["type_new"] == "Advertisement Consent"]
    full = df_new[df_new["type_new"] == "Full Application"]
    len_householder = len(householder)
    len_full_and_change_of_use = len(full_and_change_of_use)
    len_full_and_c3 = len(full_and_c3)
    len_advertisement = len(advertisement)
    len_full = len(full)
    with open(os.path.join(file_save_path, f'{full_data_save_file_name}.csv'), mode='a') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # data augmentation: householder + change of use
        for _ in tqdm(range(max_generated_length_of_housholder_and_change_of_use)):
            householder_row_index = random.choice(range(len_householder))
            householder_row = householder.iloc[householder_row_index]

            full_and_change_of_use_row_index = random.choice(range(len_full_and_change_of_use))
            full_and_change_of_use_row = full_and_change_of_use.iloc[full_and_change_of_use_row_index]

            new_app = random.choice([combine_two_applications(householder_row['planning_notes'],
                                                              full_and_change_of_use_row['planning_notes']),
                                     combine_two_applications(full_and_change_of_use_row['planning_notes'],
                                                              householder_row['planning_notes'])])

            new_row = ['fake data', new_app, '', '', 'Full Application',
                       full_and_change_of_use_row.demolitions, full_and_change_of_use_row.erections,
                       full_and_change_of_use_row.change_of_use]
            writer.writerow(new_row)

        # data augmentation: householder + c3
        for _ in tqdm(range(max_generated_length_of_housholder_and_dwelling)):
            householder_row_index = random.choice(range(len_householder))
            householder_row = householder.iloc[householder_row_index]

            full_and_c3_row_index = random.choice(range(len_full_and_c3))
            full_and_c3_row_row = full_and_c3.iloc[full_and_c3_row_index]

            new_app = random.choice([combine_two_applications(householder_row['planning_notes'],
                                                              full_and_c3_row_row['planning_notes']),
                                     combine_two_applications(full_and_c3_row_row['planning_notes'],
                                                              householder_row['planning_notes'])])
            new_row = ['fake data', new_app, '', '', 'Full Application',
                       full_and_c3_row_row.demolitions, full_and_c3_row_row.erections,
                       full_and_c3_row_row.change_of_use]
            writer.writerow(new_row)

        # data augmentation: advertisement + full
        for _ in tqdm(range(max_generated_length_of_advertisement_and_full)):
            advertisement_row_index = random.choice(range(len_advertisement))
            advertisement_row = advertisement.iloc[advertisement_row_index]

            full_row_index = random.choice(range(len_full))
            full_row = full.iloc[full_row_index]

            new_app = random.choice([combine_two_applications(advertisement_row['planning_notes'],
                                                              full_row['planning_notes']),
                                     combine_two_applications(full_row['planning_notes'],
                                                              advertisement_row['planning_notes'])])
            new_row = ['fake data', new_app, '', '', 'Full Application',
                       full_row.demolitions, full_row.erections, full_row.change_of_use]
            writer.writerow(new_row)


        # data augmentation: mineral
        for _ in tqdm(range(max_generated_length_of_mineral)):
            app, type, demolition, erection = change_of_use_fake_data('Minerals Application')
            new_row = ['fake data', app, '', '', type, demolition, erection, 'Y']
            writer.writerow(new_row)

        # data augmentation: waste
        for _ in tqdm(range(max_generated_length_of_waste)):
            app, type, demolition, erection = change_of_use_fake_data('Waste Management Application')
            new_row = ['fake data', app, '', '', type, demolition, erection, 'Y']
            writer.writerow(new_row)

        # data augmentation: hazardous
        for _ in tqdm(range(max_generated_length_of_hazardous)):
            app, type, demolition, erection = change_of_use_fake_data('Hazardous Substances Consent Application')
            new_row = ['fake data', app, '', '', type, demolition, erection, 'Y']
            writer.writerow(new_row)

        # data augmentation: agricultural
        for _ in tqdm(range(max_generated_length_of_agricultural)):
            app, type, demolition, erection = change_of_use_fake_data('Agricultural Development')
            new_row = ['fake data', app, '', '', type, demolition, erection, 'Y']
            writer.writerow(new_row)


        # data augmentation: advertisement
        for keyword in Non_Advertisement_Consent_keywords:
            if re.search('(atm)|(food)|(vinyl)|(marketing)|(shop)',keyword) is not None:
                generated_length = max_generated_length_of_per_non_advertisement_keywords * 2
            else:
                generated_length = max_generated_length_of_per_non_advertisement_keywords
            for _ in tqdm(range(generated_length)):
                app, type, demolition, erection, change_of_use = non_advertisement_consent_fake_data('non_advertisement_consent_keywords',keyword)
                new_row = ['fake data', app, '', '', type, demolition, erection, change_of_use]
                writer.writerow(new_row)
            for _ in tqdm(range(max_generated_length_of_per_non_advertisement_keywords_with_ad)):
                app, type, demolition, erection, change_of_use = non_advertisement_consent_fake_data('non_advertisement_consent_keywords',keyword)
                advertisement_row_index = random.choice(range(len_advertisement))
                advertisement_row = advertisement.iloc[advertisement_row_index]
                new_app = random.choice([combine_two_applications(advertisement_row['planning_notes'], app),
                                         combine_two_applications(app, advertisement_row['planning_notes'])])
                new_row = ['fake data', new_app, '', '', type, demolition, erection, change_of_use]
                writer.writerow(new_row)

        for _ in tqdm(range(max_generated_length_of_non_advertisement_preps)):
            app, type, demolition, erection, change_of_use = non_advertisement_consent_fake_data('all_use_classes_with_advertisement_preps')
            new_row = ['fake data', app, '', '', type, demolition, erection, change_of_use]
            writer.writerow(new_row)





    df_new = pd.read_csv(os.path.join(file_save_path, f'{full_data_save_file_name}.csv'))
    new_data_len = len(df_new)
    new_types_num = len(df_new.type_new.unique())
    new_types_frequency = df_new.type_new.value_counts(normalize=True) * 100



    print(f'{new_data_len/original_data_len*100}% ({new_data_len}/{original_data_len}) data are left.'
          f'{original_types_num} types are merged to {new_types_num} new types.\n\n'
          f'New types frequency (%): \n{new_types_frequency}')









if __name__ == "__main__":
    mapping_list_file_path = 'datasets/application_type_classifier/application_types_mapping_list.xlsx'
    sheet_name = 'Sheet1'
    historic_data_file_path = 'datasets/application_type_classifier/historic_data_20230119_with_use_classes_from_v1.31_epoch97.csv'
    file_save_path = 'datasets/application_type_classifier'
    type_old_and_hard_coding_mapping_save_file_name = 'type_old_to_type_new_hard_coding_mapping_dict'
    full_data_save_file_name = 'historic_data_20230119_with_use_classes_from_v1.31_epoch97_type_new_20230423'
    preprocess_data(mapping_list_file_path, sheet_name,
                                       historic_data_file_path,
                                       file_save_path,
                                       type_old_and_hard_coding_mapping_save_file_name,
                                       full_data_save_file_name)


