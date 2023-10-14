import os
import csv
from tqdm import tqdm

import numpy as np
import pandas as pd

from scripts.preprocessing.unit_num_exraction.augment_data import *
from scripts.preprocessing.change_of_use.split_planning_note_into_demolition_and_erection import split_planning_note_into_demolition_and_erection



def generate_data(input_file_path: str,
                  file_save_path: str,
                  file_save_name: str,
                  max_generated_length_of_single_num_data: int = 50000,
                  max_generated_length_of_demolition_data: int = 10000,
                  max_generated_length_of_erection_data: int = 50000,
                  max_generated_length_of_change_of_use_data: int = 50000,
                  max_generated_length_of_combined_data: int = 50000):

    df = pd.read_csv(input_file_path, dtype= {'notes':str,'units':str})

    if not os.path.exists(file_save_path):
        os.makedirs(file_save_path)

    df['notes'].replace('', np.nan, inplace=True)
    df.dropna(subset=['notes'], inplace=True)
    df.rename(columns={'notes':'planning_note'},inplace=True)


    df['units'].replace('', np.nan, inplace=True)
    df.dropna(subset=['units'], inplace=True)
    df.rename(columns={'units': 'unit_num'}, inplace=True)


    with open(os.path.join(file_save_path, f'{file_save_name}.csv'), mode='a', newline='') as df_new:
        df_new_writer = csv.writer(df_new, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        new_row = ["reference", "planning_note", "unit_num", "unit_num_sequence", "addition_case"]
        df_new_writer.writerow(new_row)


        count_single_num_data = 0
        for _, row in tqdm(df.iterrows(), total=len(df)):
            unit_num_original = int(float(row.unit_num))
            unit_num_word_original = num2words(unit_num_original)
            search_pattern_for_num = search_pattern_of_num(unit_num_original, include_following_no_word=True)
            search_pattern_for_num_and_building = f"({search_pattern_for_num})" + f".*?{c_general_word_search_pattern}"
            _, erection = split_planning_note_into_demolition_and_erection(row.planning_note)

            # Step 1: sanitation check, the planning note must contain units num (int or word, e.g., 'nine')
            if re.search(search_pattern_for_num, erection,flags=re.IGNORECASE) is not None:
                if count_single_num_data < max_generated_length_of_single_num_data:
                    new_row = [row.title, row.planning_note, str(int(float(row.unit_num))), str(int(float(row.unit_num)))]
                    df_new_writer.writerow(new_row)
                    count_single_num_data += 1


                    # Step 2: blocks/buildings of
                    search_pattern_1 = search_pattern_of_num(unit_num_original, include_following_no_word=False)
                    search_pattern_2 = search_pattern_of_num(10, include_following_no_word=False)
                    search_pattern_2 = re.sub('\(10\|10\)', unit_num_word_original, search_pattern_2)
                    search_pattern = f"{search_pattern_1}|{search_pattern_2}"
                    if re.search(search_pattern, row.planning_note, flags=re.IGNORECASE) is not None:
                        planning_note, unit_num = insert_blocks_of(row.planning_note, unit_num_original)
                        new_row = ['', planning_note, str(int(float(row.unit_num))), str(int(float(row.unit_num)))]
                        df_new_writer.writerow(new_row)
                        count_single_num_data += 1


                    # Step 3: pairs of
                    if re.search('pair', row.planning_note, flags=re.IGNORECASE) is None:
                        planning_note, unit_num = substitute_num_with_pair_of_num(row.planning_note, unit_num_original)
                        new_row = ['', planning_note, str(int(float(unit_num))), str(int(float(unit_num)))]
                        df_new_writer.writerow(new_row)
                        count_single_num_data += 1


                    # Step 4: 1
                        if re.search(search_pattern_for_num_and_building, row.planning_note, flags=re.IGNORECASE) is not None:
                            planning_note, unit_num = substitute_num_with_a(row.planning_note, unit_num_original)
                            new_row = ['', planning_note, str(int(float(unit_num))), str(int(float(unit_num)))]
                            df_new_writer.writerow(new_row)
                            count_single_num_data += 1


                    # Step 5: 1+
                        if unit_num_original != 1:
                            planning_note, _ = substitute_num_with_non(row.planning_note, unit_num_original)
                            new_row = ['', planning_note, "indeterminate", "indeterminate"]
                            df_new_writer.writerow(new_row)
                            count_single_num_data += 1


                    if re.search(search_pattern_for_num_and_building, row.planning_note, flags=re.IGNORECASE) is not None:
                    # Step 6: substitute with non c keywords
                        planning_note, unit_num = substitute_with_non_c_keywords(row.planning_note, unit_num_original)
                        new_row = ['', planning_note, str(int(float(unit_num))), str(int(float(unit_num)))]
                        df_new_writer.writerow(new_row)
                        count_single_num_data += 1


                if re.search(search_pattern_for_num_and_building, row.planning_note, flags=re.IGNORECASE) is not None:
                    # Step 7: increase one c3
                    search_result = re.search(search_pattern_for_num_and_building, row.planning_note, flags=re.IGNORECASE).group(0)
                    search_result = re.sub('\)', '\\\)', search_result)
                    search_result = re.sub('\(', '\\\(', search_result)
                    c3_phrase, c3_num = generate_c3_phrase()
                    planning_note = re.sub(search_result,
                                           search_result + random.choice(list(joint_symbols_coordination)) + c3_phrase,
                                           row.planning_note,
                                           count=1, flags=re.IGNORECASE)
                    if c3_num == -1:
                        unit_num = 'indeterminate'
                    else:
                        unit_num = int(float(row.unit_num)) + c3_num
                    num_sequence = join_a_list_of_numbers_with_vertical_bar([int(float(row.unit_num)), c3_num])
                    new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
                    df_new_writer.writerow(new_row)


                    # Step 8: increase one extentions to c3
                    search_result = re.search(search_pattern_for_num_and_building, row.planning_note, flags=re.IGNORECASE).group(0)
                    search_result = re.sub('\)', '\\\)', search_result)
                    search_result = re.sub('\(', '\\\(', search_result)
                    c3_phrase, _ = generate_c3_phrase(allow_adding_blocks_of = False)
                    c3_phrase = generate_extensions_to()+' ' +c3_phrase
                    planning_note = re.sub(search_result,
                                           search_result + random.choice(list(joint_symbols_coordination)) + c3_phrase,
                                           row.planning_note,
                                           count=1, flags=re.IGNORECASE)
                    new_row = ['', planning_note, str(int(float(row.unit_num))), str(int(float(row.unit_num))), 'Y']
                    df_new_writer.writerow(new_row)


                    # Step 9: increase one c1,c2,c4
                    c1_c2_c4_phrase, c1_c2_c4_num = generate_c1_c2_c4_phrase()
                    planning_note = re.sub(search_result,
                                           search_result + random.choice(list(joint_symbols_coordination)) + c1_c2_c4_phrase,
                                           row.planning_note,
                                           count=1, flags=re.IGNORECASE)
                    if c1_c2_c4_num == -1:
                        unit_num = 'indeterminate'
                    else:
                        unit_num = int(float(row.unit_num)) + c1_c2_c4_num
                    num_sequence = join_a_list_of_numbers_with_vertical_bar([int(float(row.unit_num)), c1_c2_c4_num])
                    new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
                    df_new_writer.writerow(new_row)


                    # Step 10: increase one c1,c2,c4 with bed nums
                    c1_c2_c4_phrase_with_bed_num, c1_c2_c4_bed_num = generate_c1_c2_c4_phrase_with_bed_num()
                    planning_note = re.sub(search_result,
                                           search_result + random.choice(list(joint_symbols_coordination)) + c1_c2_c4_phrase_with_bed_num,
                                           row.planning_note,
                                           count=1, flags=re.IGNORECASE)
                    if c1_c2_c4_bed_num == -1:
                        unit_num = 'indeterminate'
                    else:
                        unit_num = int(float(row.unit_num)) + c1_c2_c4_bed_num
                    num_sequence = join_a_list_of_numbers_with_vertical_bar([int(float(row.unit_num)), c1_c2_c4_bed_num])
                    new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
                    df_new_writer.writerow(new_row)


                    # Step 11: increase one non c
                    non_c_phrase, _ = generate_non_c_phrase()
                    planning_note = re.sub(search_result,
                                           search_result + random.choice(list(joint_symbols_coordination)) + non_c_phrase,
                                           row.planning_note,
                                           count=1, flags=re.IGNORECASE)
                    new_row = ['', planning_note, str(int(float(row.unit_num))), str(int(float(row.unit_num)))]
                    df_new_writer.writerow(new_row)
                    count_single_num_data += 1


                    # Step 12: increase 2-4 phrases of random use classes
                    combined_phrases, num_list = generate_combined_phrases()
                    planning_note = re.sub(search_result,
                                           search_result + random.choice(list(joint_symbols_coordination)) + combined_phrases,
                                           row.planning_note,
                                           count=1, flags=re.IGNORECASE)
                    if -1 in set(num_list):
                        unit_num = 'indeterminate'
                    else:
                        unit_num = int(float(row.unit_num)) + sum(num_list)

                    num_sequence = join_a_list_of_numbers_with_vertical_bar([int(float(row.unit_num))]+num_list)
                    new_row = ['', planning_note, str(unit_num),num_sequence, 'Y']
                    df_new_writer.writerow(new_row)


                # Step 13: add a change of use sentence
                planning_note_change_of_use, unit_num_list = generate_change_of_use_data(change_of_use_data_type='change_of_use',
                                                                                         include_patterns_begin_with_non_prompt = False)
                planning_note = combine_planning_notes(row.planning_note,planning_note_change_of_use)
                if -1 in set(unit_num_list):
                    unit_num = 'indeterminate'
                else:
                    unit_num = int(float(row.unit_num)) + sum(unit_num_list)
                num_sequence = join_a_list_of_numbers_with_vertical_bar([int(float(row.unit_num))]+unit_num_list)
                new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
                df_new_writer.writerow(new_row)





            else:
                # Step 14: sanitation check of addition cases, the sum of nums in the planning note must equal to the unit num
                search_pattern_for_list_of_nums = search_pattern_of_num(10, include_following_no_word=False)
                search_pattern_for_list_of_nums = re.sub('10', '\\\d+,?\\\d*', search_pattern_for_list_of_nums)
                num_list_original = [int(re.sub(",","",s)) for s in re.findall(search_pattern_for_list_of_nums, erection, flags=re.IGNORECASE)]
                num_sequence_original = join_a_list_of_numbers_with_vertical_bar(num_list_original)
                if sum(num_list_original) == int(float(row.unit_num)) and sum(num_list_original) !=0:
                    new_row = [row.title, row.planning_note, str(int(float(row.unit_num))), num_sequence_original, 'Y']
                    df_new_writer.writerow(new_row)

                    # Step 15: substitute one of the nums
                    i = random.randint(0, len(num_list_original)-1)
                    search_num = num_list_original[i]
                    search_pattern = f"({search_pattern_of_num(search_num, include_following_no_word=True)})" + f".*?{c_general_word_search_pattern}"
                    if re.search(search_pattern, row.planning_note, flags=re.IGNORECASE) is not None:
                        planning_note,sub_num = substitute_one_of_the_nums_in_an_addition_case(row.planning_note, search_num)
                        num_list = num_list_original.copy()
                        num_list[i] = sub_num
                        if sub_num == -1:
                            unit_num = 'indeterminate'
                        else:
                            unit_num = sum(num_list)
                        num_sequence = join_a_list_of_numbers_with_vertical_bar(num_list)
                        new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
                        df_new_writer.writerow(new_row)


                    # Step 16: increase one c3, only add in the last
                    search_pattern_for_the_last_num_and_building = search_pattern_of_num(num_list_original[-1], include_following_no_word=False) + \
                                                                   f".*?{c_general_word_search_pattern}"

                    if re.search(search_pattern_for_the_last_num_and_building, row.planning_note, flags=re.IGNORECASE) is not None:
                        search_result = re.search(search_pattern_for_the_last_num_and_building, row.planning_note, flags=re.IGNORECASE).group(0)
                        search_result = re.sub('\)', '\\\)', search_result)
                        search_result = re.sub('\(', '\\\(', search_result)
                        c3_phrase, c3_num = generate_c3_phrase()
                        planning_note = re.sub(search_result,
                                               search_result+random.choice(list(joint_symbols_coordination))+c3_phrase,
                                               row.planning_note,
                                               count=1, flags=re.IGNORECASE)
                        if c3_num == -1:
                            unit_num = 'indeterminate'
                        else:
                            unit_num = int(float(row.unit_num)) + c3_num
                        num_sequence = join_a_list_of_numbers_with_vertical_bar(num_list_original+[c3_num])
                        new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
                        df_new_writer.writerow(new_row)


                    # Step 17: increase one c1,c2,c4, only add in the last
                        c1_c2_c4_phrase, c1_c2_c4_num = generate_c1_c2_c4_phrase()
                        planning_note = re.sub(search_result,
                                               search_result + random.choice(list(joint_symbols_coordination)) + c1_c2_c4_phrase,
                                               row.planning_note,
                                               count=1, flags=re.IGNORECASE)
                        if c1_c2_c4_num == -1:
                            unit_num = 'indeterminate'
                        else:
                            unit_num = int(float(row.unit_num)) + c1_c2_c4_num
                        num_sequence = join_a_list_of_numbers_with_vertical_bar(num_list_original + [c1_c2_c4_num])
                        new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
                        df_new_writer.writerow(new_row)


                    # Step 18: increase one extentions to c1,c2,c4, only add in the last
                        c1_c2_c4_phrase, _ = generate_c1_c2_c4_phrase(allow_adding_blocks_of = False)
                        c1_c2_c4_phrase = generate_extensions_to() + ' ' +c1_c2_c4_phrase
                        planning_note = re.sub(search_result,
                                               search_result + random.choice(
                                                   list(joint_symbols_coordination)) + c1_c2_c4_phrase,
                                               row.planning_note,
                                               count=1, flags=re.IGNORECASE)
                        new_row = ['', planning_note, int(float(row.unit_num)), num_sequence_original, 'Y']
                        df_new_writer.writerow(new_row)


                    # Step 19: increase one c1,c2,c4 with bed nums, only add in the last
                        c1_c2_c4_phrase_with_bed_num, c1_c2_c4_bed_num = generate_c1_c2_c4_phrase_with_bed_num()
                        planning_note = re.sub(search_result,
                                               search_result + random.choice(list(joint_symbols_coordination)) + c1_c2_c4_phrase_with_bed_num,
                                               row.planning_note,
                                               count=1, flags=re.IGNORECASE)
                        if c1_c2_c4_bed_num == -1:
                            unit_num = 'indeterminate'
                        else:
                            unit_num = int(float(row.unit_num)) + c1_c2_c4_bed_num
                        num_sequence = join_a_list_of_numbers_with_vertical_bar(num_list_original + [c1_c2_c4_bed_num])
                        new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
                        df_new_writer.writerow(new_row)

                    # Step 20: increase one non c, only add in the last
                        non_c_phrase, _ = generate_non_c_phrase()
                        planning_note = re.sub(search_result,
                                               search_result + random.choice(list(joint_symbols_coordination)) + non_c_phrase,
                                               row.planning_note,
                                               count=1, flags=re.IGNORECASE)
                        new_row = ['', planning_note, str(int(float(row.unit_num))), num_sequence_original, 'Y']
                        df_new_writer.writerow(new_row)


                    # Step 21: + noise num -> word
                    planning_note = row.planning_note
                    for num in num_list_original:
                        word = num2words(num) + ' '
                        planning_note = re.sub(search_pattern_of_num(num, include_following_no_word=False),
                                               word, planning_note, flags=re.IGNORECASE)
                    planning_note = re.sub(' +',' ', planning_note)
                    new_row = ['', planning_note, str(int(float(row.unit_num))), num_sequence_original, 'Y']
                    df_new_writer.writerow(new_row)


                    # Step 22: add a change of use sentence
                    planning_note_change_of_use, unit_num_list = generate_change_of_use_data(
                        change_of_use_data_type='change_of_use',
                        include_patterns_begin_with_non_prompt=False)
                    planning_note = combine_planning_notes(row.planning_note, planning_note_change_of_use)
                    if -1 in set(unit_num_list):
                        unit_num = 'indeterminate'
                    else:
                        unit_num = int(float(row.unit_num)) + sum(unit_num_list)
                    num_sequence = join_a_list_of_numbers_with_vertical_bar(num_list_original + unit_num_list)
                    new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
                    df_new_writer.writerow(new_row)


        # Step 23: generate demolish <FROM> data
        for _ in tqdm(range(max_generated_length_of_demolition_data)):
            planning_note, _ = generate_change_of_use_data(change_of_use_data_type = 'demolition_only')
            new_row = ['', planning_note, str(0), str(0)]
            df_new_writer.writerow(new_row)

        # Step 24: generate erect <TO> data
        for _ in tqdm(range(max_generated_length_of_erection_data)):
            planning_note, unit_num_list = generate_change_of_use_data(change_of_use_data_type = 'erection_only')
            if -1 in set(unit_num_list):
                unit_num = 'indeterminate'
            else:
                unit_num = sum(unit_num_list)
            num_sequence = join_a_list_of_numbers_with_vertical_bar(unit_num_list)
            new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
            df_new_writer.writerow(new_row)

        # Step 25: generate change of use from <FROM> to <to> data
        for _ in tqdm(range(max_generated_length_of_change_of_use_data)):
            planning_note, unit_num_list = generate_change_of_use_data(change_of_use_data_type = 'change_of_use',
                                                                       include_patterns_begin_with_non_prompt=False)
            if -1 in set(unit_num_list):
                unit_num = 'indeterminate'
            else:
                unit_num = sum(unit_num_list)
            num_sequence = join_a_list_of_numbers_with_vertical_bar(unit_num_list)
            new_row = ['', planning_note, str(unit_num), num_sequence, 'Y']
            df_new_writer.writerow(new_row)


    df = pd.read_csv(os.path.join(file_save_path, f'{file_save_name}.csv'))
    print(f"Total data length before combining data: {len(df)}.")
    df = df[df['unit_num'] != '0']
    len_df = len(df)


    # Step 26: combine data and sum unit nums
    with open(os.path.join(file_save_path, f'{file_save_name}.csv'), mode='a', newline='') as df_new:
        df_new_writer = csv.writer(df_new, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        half_max_generated_length_of_combined_data = max_generated_length_of_combined_data//2
        for _ in tqdm(range(half_max_generated_length_of_combined_data)):
            row_1_index = random.choice(range(len_df))
            row_1 = df.iloc[row_1_index]

            row_2_index = random.choice(range(len_df))
            row_2 = df.iloc[row_2_index]

            planning_note = combine_planning_notes(row_1.planning_note, row_2.planning_note)
            if row_1.unit_num == 'indeterminate' or row_2.unit_num == 'indeterminate':
                unit_num = 'indeterminate'
            else:
                unit_num = int(float(row_1.unit_num)) + int(float(row_2.unit_num))

            new_row = ['', planning_note, str(unit_num), f"{str(row_1.unit_num_sequence)}|{str(row_2.unit_num_sequence)}", 'Y']
            df_new_writer.writerow(new_row)


        for _ in tqdm(range(half_max_generated_length_of_combined_data)):
            row_1_index = random.choice(range(len_df))
            row_1 = df.iloc[row_1_index]

            row_2_index = random.choice(range(len_df))
            row_2 = df.iloc[row_2_index]

            row_3_index = random.choice(range(len_df))
            row_3 = df.iloc[row_3_index]

            planning_note = combine_planning_notes(row_1.planning_note, row_2.planning_note, row_3.planning_note)
            if row_1.unit_num == 'indeterminate' or row_2.unit_num == 'indeterminate' or row_3.unit_num == 'indeterminate':
                unit_num = 'indeterminate'
            else:
                unit_num = int(float(row_1.unit_num)) + int(float(row_2.unit_num)) + int(float(row_3.unit_num))

            new_row = ['', planning_note, str(unit_num), f"{str(row_1.unit_num_sequence)}|{str(row_2.unit_num_sequence)}|{str(row_3.unit_num_sequence)}", 'Y']
            df_new_writer.writerow(new_row)

    df = pd.read_csv(os.path.join(file_save_path, f'{file_save_name}.csv'))
    len_df = len(df)
    len_addition_cases = len(df[df['addition_case'] == 'Y'])
    percent = (len_addition_cases / len_df) * 100

    print(f"Total data length: {len_df}.\n"
          f"Additional data length: {len_addition_cases}, percentage: {format(percent, '.2f')}%")





if __name__ == '__main__':
    input_file_path = 'datasets/resi_unit_num/appsWithSizeAndUnits.csv'
    file_save_path = 'datasets/resi_unit_num'
    file_save_name = 'appsWithSizeAndUnits_20230223'
    max_generated_length_of_single_num_data = 30000
    max_generated_length_of_demolition_data = 10000
    max_generated_length_of_erection_data = 50000
    max_generated_length_of_change_of_use_data = 50000
    max_generated_length_of_combined_data = 50000
    generate_data(input_file_path = input_file_path,
                  file_save_path = file_save_path,
                  file_save_name = file_save_name,
                  max_generated_length_of_single_num_data = max_generated_length_of_single_num_data,
                  max_generated_length_of_demolition_data = max_generated_length_of_demolition_data,
                  max_generated_length_of_erection_data = max_generated_length_of_erection_data,
                  max_generated_length_of_change_of_use_data = max_generated_length_of_change_of_use_data,
                  max_generated_length_of_combined_data = max_generated_length_of_combined_data
                  )

