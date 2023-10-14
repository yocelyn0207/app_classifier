from typing import Literal

from scripts.preprocessing.unit_num_exraction.utils import *
from scripts.preprocessing.use_class_classifier.keywords import *



c_general_word_search_pattern = '(?<!\w)(dwellings|dwellinghouses|dwellinghouse|dwelling houses|dwelling house|' \
                                'dwelling|apartments|apartment|accommodations|accommodation|flats|flat|houses|house|' \
                                'bungalows|bungalow|cottages|cottage|homes|home|units|unit|' \
                                'residents|resident|persons|person|adults|adult|children|people)(?!\w)'


def convert_to_numbers(planning_note:str):
    words_to_numbers = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'ten': '10',
        'eleven': '11',
        'twelve': '12',
        'twenty':'20'
    }

    # pattern = re.compile(r'\b(' + '|'.join(words_to_numbers.keys()) + r')\b')
    pattern = '\b(' + '|'.join(words_to_numbers.keys()) + r')\b'
    return re.sub(pattern, lambda x: words_to_numbers[x.group()], planning_note, flags=re.IGNORECASE)



# blocks/buildings of
def insert_blocks_of(planning_note: str, num: int):
    word = num2words(num)
    num_with_thousand_separators = f'{num:,}'

    search_pattern_1 = search_pattern_of_num(num,include_following_no_word=False)
    search_pattern_2 = search_pattern_of_num(10,include_following_no_word=False)
    search_pattern_2 = re.sub('\(10\|10\)', word, search_pattern_2)
    search_pattern = f"{search_pattern_1}|{search_pattern_2}"

    block_phrase = generate_blocks_of()
    sub_pattern = f"{block_phrase} " \
                  f"{random.choice([str(num), num_with_thousand_separators, word+' '])}"

    planning_note = re.sub(search_pattern, sub_pattern, planning_note,  flags=re.IGNORECASE)

    planning_note = re.sub(' +', ' ', planning_note)

    return planning_note, int(num)




# pairs of
def substitute_num_with_pair_of_num(planning_note: str, num: int):
    search_pattern = search_pattern_of_num(num, include_following_no_word=True)
    if num == 1:
        pair_pattern = 'pair'
        num_word = random.choice([num2words(num),'a'])
        num_with_thousand_separators = f'{num:,}'
    else:
        pair_pattern = 'pairs'
        num_word = num2words(num)
        num_with_thousand_separators = f'{num:,}'

    sub_pattern = f"{random.choice([str(num), num_with_thousand_separators, num_word])} {pair_pattern} of "

    planning_note = re.sub(search_pattern, sub_pattern, planning_note, flags=re.IGNORECASE)
    num = 2*num

    planning_note = re.sub(' +',' ',planning_note)

    return planning_note, int(num)



# 1
def substitute_num_with_a(planning_note: str, num: int):
    search_pattern_for_building = f"({search_pattern_of_num(num, include_following_no_word=True)})"+f".*?{c_general_word_search_pattern}"
    search_pattern_for_num = search_pattern_of_num(num, include_following_no_word=True)


    search_result = re.search(search_pattern_for_building, planning_note, flags=re.IGNORECASE).group(0)
    if search_result[-1] == 's':
        planning_note = re.sub(search_pattern_for_building, search_result[:-1],planning_note, flags=re.IGNORECASE)
    planning_note = re.sub(search_pattern_for_num,
                           random.choice([' a ',' a single ',' one ', ' an ',
                                          f" 1{random.choice(['',' '])}{random.choice(['no. ','no ','num. ','num ','X ','x ',''])}",
                                          ' ']),
                           planning_note, flags=re.IGNORECASE)
    num = 1

    planning_note = re.sub(' +',' ',planning_note)
    return planning_note, int(num)


# 1+
def substitute_num_with_non(planning_note: str, num: int):
    search_pattern = search_pattern_of_num(num, include_following_no_word=True)
    planning_note = re.sub(search_pattern, " ", planning_note, flags=re.IGNORECASE)
    planning_note = re.sub(' +',' ',planning_note)
    return planning_note, int(num)


# substitute with non c keywords
def substitute_with_non_c_keywords(planning_note: str, num:int):
    if num == 1:
        word = generate_non_c_keyword(mode='single')
    else:
        word = generate_non_c_keyword(mode='plural')

    search_pattern_for_building = f"({search_pattern_of_num(num, include_following_no_word=True)})" + f".*?{c_general_word_search_pattern}"
    search_result = re.search(search_pattern_for_building, planning_note, flags=re.IGNORECASE).group(0)
    sub_pattern = re.sub(c_general_word_search_pattern, word, search_result, flags=re.IGNORECASE)
    search_result = re.sub('\)', '\\\)', search_result)
    search_result = re.sub('\(', '\\\(', search_result)
    planning_note = re.sub(search_result, sub_pattern, planning_note, flags=re.IGNORECASE)
    num = 0

    return planning_note, num






# substitute one of the nums in an addition case
def substitute_one_of_the_nums_in_an_addition_case(planning_note: str, num:int):
    unit_num_str, unit_num = generate_random_int(mode='mixed_either')

    even_num_converted_to_pairs_of = False
    if unit_num % 2 == 0 and choice(['convert_to_pairs_of','no'],p=[0.2,0.8]):
        unit_num_str = convert_an_even_num_to_pairs_of(unit_num)
        even_num_converted_to_pairs_of = True

    search_pattern_for_building = f"({search_pattern_of_num(num, include_following_no_word=True)})" + f".*?{c_general_word_search_pattern}"
    search_result = re.search(search_pattern_for_building, planning_note, flags=re.IGNORECASE).group(0)
    search_result = re.sub('\)', '\\\)', search_result)
    search_result = re.sub('\(', '\\\(', search_result)
    try:
        int(unit_num_str)
    except:
        unit_num_str = unit_num_str + ' '

    if unit_num == -1:
        sub_pattern = re.sub(search_pattern_of_num(num, include_following_no_word = True), ' ', search_result, flags=re.IGNORECASE)
        if sub_pattern[-1] != 's':
            sub_pattern = sub_pattern + 's'
    elif unit_num == 1:
        if unit_num_str != '1' and unit_num_str != 'one ':
            search_pattern_include_following_no_word = True
        else:
            search_pattern_include_following_no_word = False
        sub_pattern = re.sub(search_pattern_of_num(num, include_following_no_word=search_pattern_include_following_no_word),
                             unit_num_str, search_result,flags=re.IGNORECASE)
        if sub_pattern[-1] == 's':
            sub_pattern = sub_pattern[:-1]
    else:
        if even_num_converted_to_pairs_of is True:
            search_pattern_include_following_no_word = True
        else:
            search_pattern_include_following_no_word = False
        sub_pattern = re.sub(search_pattern_of_num(num, include_following_no_word=search_pattern_include_following_no_word),
                             unit_num_str, search_result,flags=re.IGNORECASE)
        if sub_pattern[-1] != 's':
            sub_pattern = sub_pattern + 's'

    planning_note = re.sub(search_result, sub_pattern, planning_note, flags=re.IGNORECASE)
    planning_note = re.sub(' +',' ',planning_note)

    return planning_note, unit_num




#
# # substitute with other c3 keywords
# def substitute_dwelling_with_other_c3_keywords(planning_note: str, num:int):
#     word = generate_c3_keyword()
#     planning_note = re.sub(c_general_word_search_pattern,word, planning_note, flags=re.IGNORECASE)
#     return planning_note, int(num)
#
#
# # substitute dwelling with c1, c2, c4 keywords
# def substitute_dwelling_with_c_keywords_other_than_c3(planning_note: str, num: int):
#     word = generate_c1_c2_c4_keyword()
#     planning_note = re.sub(c_general_word_search_pattern, word, planning_note, flags=re.IGNORECASE)
#     return planning_note, int(num)
#
#
#
#
# # substitute dwelling with c1, c2, c4 keywords + bed num
# '''
# care home (Class C2) for up to four residents
# '''
# def substitute_dwelling_with_c_keywords_other_than_c3_with_beds_num(planning_note: str, num: int):
#     word, num = generate_c1_c2_c4_phrase_with_bed_num()
#     word = re.sub(' +',' ',word)
#     planning_note = re.sub(c_general_word_search_pattern, word, planning_note, flags=re.IGNORECASE)
#     return planning_note, int(num)










_MODES = Literal["c3", "c1_c2_c4", "c1_c2_c4_with_beds_num", 'non_c', 'random']
def generate_combined_phrases(mode:_MODES='random',min_phrase_num:int = 2, max_phrase_num:int = 4,
                              allow_to_accommodate:bool = True):
    num_of_phrases = random.randint(min_phrase_num, max_phrase_num)
    # irrelative_words = random.choices(list(keywords_list_irrelative_words), k=random.randint(1, 4))
    phrases = []
    nums = []
    if mode == 'c3':
        for _ in range(num_of_phrases):
            phrase, num = generate_c3_phrase(allow_to_accommodate=allow_to_accommodate)
            phrases.append(phrase)
            nums.append(num)
    elif mode == 'c1_c2_c4':
        for _ in range(num_of_phrases):
            phrase, num = generate_c1_c2_c4_phrase(allow_to_accommodate=allow_to_accommodate)
            phrases.append(phrase)
            nums.append(num)
    elif mode == 'c1_c2_c4_with_beds_num':
        for _ in range(num_of_phrases):
            phrase, num = generate_c1_c2_c4_phrase_with_bed_num(allow_to_accommodate=allow_to_accommodate)
            phrases.append(phrase)
            nums.append(num)
    elif mode == 'non_c':
        for _ in range(num_of_phrases):
            phrase, num = generate_non_c_phrase(allow_to_accommodate=allow_to_accommodate)
            phrases.append(phrase)
            nums.append(num)
    else:
        for _ in range(num_of_phrases):
            target = random.choice(['c3','c1_c2_c4','c1_c2_c4_with_bed_num','non_c'])
            if target == 'c3':
                phrase, num = generate_c3_phrase(allow_to_accommodate=allow_to_accommodate)
                phrases.append(phrase)
                nums.append(num)
            elif target == 'c1_c2_c4':
                phrase, num = generate_c1_c2_c4_phrase(allow_to_accommodate=allow_to_accommodate)
                phrases.append(phrase)
                nums.append(num)
            elif target == 'c1_c2_c4_with_bed_num':
                phrase, num = generate_c1_c2_c4_phrase_with_bed_num(allow_to_accommodate=allow_to_accommodate)
                phrases.append(phrase)
                nums.append(num)
            else:
                phrase, _ = generate_non_c_phrase(allow_to_accommodate=allow_to_accommodate)
                phrases.append(phrase)
                nums.append(0)

    combined_phrases = combine_a_list_of_keywords(phrases)
    return combined_phrases, nums






# change of use
_Change_of_Use_Data_Type = Literal["demolition_only", "erection_only", "change_of_use"]
def generate_change_of_use_data(change_of_use_data_type:_Change_of_Use_Data_Type = 'change_of_use',
                                include_patterns_begin_with_non_prompt: bool = True):

    if include_patterns_begin_with_non_prompt is True:
        pattern_from = random.choice(change_of_use_patterns['from']['begin_with_prompt']+
                                     change_of_use_patterns['from']['begin_with_non_prompt'])
        pattern_to = random.choice(change_of_use_patterns['to']['begin_with_prompt']+
                                   change_of_use_patterns['to']['begin_with_non_prompt'])
        pattern_from_to = random.choice(change_of_use_patterns['from_to']['begin_with_prompt']+
                                        change_of_use_patterns['from_to']['begin_with_non_prompt'])
    else:
        pattern_from = random.choice(change_of_use_patterns['from']['begin_with_prompt'])
        pattern_to = random.choice(change_of_use_patterns['to']['begin_with_prompt'])
        pattern_from_to = random.choice(change_of_use_patterns['from_to']['begin_with_prompt'])

    if change_of_use_data_type == 'demolition_only':
        combined_phrases,_ = generate_combined_phrases(allow_to_accommodate=False)
        planning_note = re.sub('<FROM>', combined_phrases, pattern_from)
        nums_list = [0]
    elif change_of_use_data_type == 'erection_only':
        combined_phrases, nums_list = generate_combined_phrases()
        planning_note = re.sub('<TO>',combined_phrases,pattern_to)
    else:
        planning_note = random.choice([combine_two_change_of_use_patterns(pattern_from, pattern_to),
                                       combine_two_change_of_use_patterns(pattern_to, pattern_from),
                                       pattern_from_to])
        combined_phrases_from, _ = generate_combined_phrases(min_phrase_num = 1, max_phrase_num = 1, allow_to_accommodate=False)
        combined_phrases_to, nums_list = generate_combined_phrases()
        planning_note = re.sub('<FROM>', combined_phrases_from, planning_note)
        planning_note = re.sub('<TO>', combined_phrases_to, planning_note)

    planning_note = re.sub(' +',' ',planning_note)

    return planning_note, nums_list





