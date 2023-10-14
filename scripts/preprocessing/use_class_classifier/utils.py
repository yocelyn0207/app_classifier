import re
import random
from collections import defaultdict
from numpy.random import choice
# import nltk
# from nltk.corpus import words
# nltk.download('words')

use_classes = ['sui generis', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b8','c1', 'c2', 'c3', 'c4', 'd1', 'd2']

# tag_patterns = ['<TAG>', 'use class <TAG>', 'use class: <TAG>',' <TAG> use class',
#                 'use classes <TAG>', 'use classes: <TAG>',  '<TAG> use classes',
#                 '<TAG> use', 'use <TAG>', 'use: <TAG>',
#                 '<TAG> uses', 'uses <TAG>', 'uses: <TAG>',
#                 'class <TAG>', 'class: <TAG>', '<TAG> class',
#                 'classes <TAG>', 'classes: <TAG>', '<TAG> classes']


diversified_b1 =  ['b1a','b1b','b1c','b1 a','b1 b','b1 c','b1(a)','b1(b)','b1(c)','b1 (a)','b1 (b)','b1 (c)']




def _add_plural(keyword:str):
    if keyword in {'child','people','children','hmo'}:
        if keyword == 'child':
            keyword = 'children'
        elif keyword == 'hmo':
            keyword = 'hmos'
    else:
        if keyword[-1] == 'y' and keyword[-2] != 'a' and keyword[-2] != 'e' and keyword[-2] != 'i' and keyword[-2] != 'o' and keyword[-2] != 'u':
            keyword = keyword[:-1] + 'ies'
        elif keyword[-2:] == 'es': # ignore 'pitches'
            pass
        elif keyword[-2:] == 'ch' or keyword[-2:] == 'sh' or keyword[-2:] == 'ss' or \
                keyword[-1] == 's' or keyword[-1] == 'x' or keyword[-1] == 'z' or keyword[-1] == 'o':
            keyword = keyword + 'es'
        else:
            keyword = keyword+'s'

    return keyword





def _random_chose_a_tag_pattern():
    extra_modifier = random.choice(['use','class','use class', None])
    if extra_modifier is None:
        chosen_tag_pattern = '<TAG>'
    else:
        if random.choice(['add_plural','no_add']) == 'add_plural':
            extra_modifier = _add_plural(extra_modifier)
        chosen_tag_pattern = random.choice([f'{extra_modifier} <TAG>',
                                            f'<TAG> {extra_modifier}',
                                            f'{extra_modifier}: <TAG>'
                                            ])
    return chosen_tag_pattern


def _force_random_chose_use_classes_with_spans():
    part1_1 = ['a1','a2','a3']
    part1_2 = ['sui generis', 'a4', 'a5', 'b1', 'b2', 'b8','c1', 'c2', 'c3', 'c4', 'd1', 'd2']

    part2_1 = ['a1','a2','a3','a4']
    part2_2 = ['sui generis', 'a5', 'b1', 'b2', 'b8','c1', 'c2', 'c3', 'c4', 'd1', 'd2']

    part3_1 = ['a1','a2','a3','a4','a5']
    part3_2 = ['sui generis', 'b1', 'b2', 'b8','c1', 'c2', 'c3', 'c4', 'd1', 'd2']

    part3_1 = ['c1','c2','c3']
    part3_2 = ['sui generis', 'a1','a2','a3','a4','a5', 'b1', 'b2', 'b8', 'c4', 'd1', 'd2']

    part4_1 = ['c1','c2','c3','c4']
    part4_2 = ['sui generis', 'a1','a2','a3','a4','a5', 'b1', 'b2', 'b8', 'd1', 'd2']

    index = random.randint(1, 4)

    chosen_use_classes = locals()[f'part{index}_1'] + random.sample(locals()[f'part{index}_2'], k= random.randint(1, len(locals()[f'part{index}_2'])))

    return chosen_use_classes



def _get_continuous_spans_in_chosen_use_classes(chosen_use_classes:set) -> list:
    '''
    :param chosen_use_classes: a set of random chosen use classes.
    :return: a list of lists which are the tags within continuous spans in chosen_use_classes, e.g.,
            [['a1', 'a2', 'a3'], ['c1', 'c2', 'c3', 'c4']]
    '''
    split_general_use_class_with_num = defaultdict(list)

    for i in chosen_use_classes:
        if re.match('(\w)(\d)$', i) is not None:
            split_general_use_class_with_num[i[0]].append(int(i[1]))

    continuous_spans = []
    for k, v in split_general_use_class_with_num.items():

        if len(v) <= 2:
            pass
        else:
            v.sort()
            start, end = v[0], v[0]
            for n in range(len(v) - 1):
                if v[n + 1] - v[n] == 1:
                    end = v[n + 1]
                else:
                    if start != end:
                        continuous_spans.append([k + str(i) for i in range(start, end+1)])
                    start, end = v[n + 1], v[n + 1]
            if start != end:
                continuous_spans.append([k + str(i) for i in range(start, end+1)])
    return continuous_spans



def _generate_noise_tag(use_classes: list = use_classes):
    '''
    Generate following types of noise tags:
    1) general use class with random nums, e.g., 'a156',
    2) 'phase' + use class, e.g., 'phase a1',
    3) use class e or f, e.g., 'classes e'.
    :param use_classes: a list of all use classes to add into the planning notes. Default list excludes the application
                        classes, 'householder', 'tpo', 'other'.
    :return noise_tag: a string of noise tag, e.g., 'a156'.
    '''
    # only keep use_classes end up with numbers, i.e., exclude sui generis
    use_classes_with_nums = []
    for use_class in use_classes:
        if re.match(r"([a-z]+)([0-9]+)", use_class) is not None:
            use_classes_with_nums.append(use_class)

    use_class = random.choice(use_classes_with_nums)
    noise = random.choice(['noise_tag_with_random_num', 'noise_tag_with_phase', 'e_f_tag'])
    if noise == 'noise_tag_with_random_num':
        random_num = random.randint(1,99)
        noise_tag = use_class + str(random_num)
    elif noise == 'noise_tag_with_phase':
        noise_tag = f'phase {use_class}'
    else:
        noise_tag = re.sub('<TAG>', random.choice(['e','f']), _random_chose_a_tag_pattern())

    return noise_tag





def _join_use_classes_tags(chosen_use_classes: set, joint_characters: list = [', ', '/'],
                           last_joint_characters: list =[' and ', ' & '],
                           to_characters: list = ['-',' to ']) -> str:
    '''
    Given a list of chosen use classes, join them together into a string, e.g., 'a1-a5, b1 & c1'. If there is a
    continuous span in chosen use classes, it must be abbreviated, e.g., 'a1-a5' or 'a1 to a5'.
    :param chosen_use_classes: a set of chosen use classes to be joint together, e.g., ['a1','a2','a3','a4','a5','b1','c1'].
    :param joint_characters: a list of joint characters, e.g.,[',', '/'].
    :param last_joint_characters: a list of joint characters that may be replaced by at the last joint position, e.g.,
                                 [' and ', ' & '].
    :param to_characters: a list of characters that used to join a successive of use classes, e.g., ['-',' to '].
    :return tags: a string of use classes joint with joint characters, e.g., 'a1-a5, b1 & c1'.
    '''
    joint_character = random.choice(joint_characters)
    last_joint_characters = random.choice(last_joint_characters)
    continuous_spans = _get_continuous_spans_in_chosen_use_classes(chosen_use_classes)
    continuous_spans_flatten = [i for span in continuous_spans for i in span]
    temp = []

    for i in chosen_use_classes:
        try:
            continuous_spans_flatten.index(i)  # if tag in continuous_spans_flatten, pass
        except:
            temp.append(i) # if tag not in continuous_spans_flatten, append
    for span in continuous_spans:
        temp.append(span[0] + random.choice(to_characters)+ span[-1]) # append span as 'c1-c4', or 'c1 to c4'


    random.shuffle(temp)
    tags = joint_character.join([use_class for use_class in temp])

    if random.choice([True, False]) is True: # Randomly replace the last ',' or '/' with 'and'.
        tags = re.sub(', |/', last_joint_characters[::-1],tags[::-1], count=1)[::-1]

    return tags



def _change_into_an_incorrect_use_class(use_class:str, use_classes: list = use_classes + ['e','f']):
    index_use_class = use_classes.index(use_class)
    candidate_incorrect_use_classes = use_classes[:index_use_class] + use_classes[index_use_class+1:]
    incorrect_use_class = random.choice(candidate_incorrect_use_classes)
    return incorrect_use_class





def _add_dweller_num_to_description(description: str, chosen_use_class: str):
    '''
     (for) between 3 to 6 residents
    hmo (5 person) hmo
    for/comprising up to 4 occupants
    occupied by 6 individuals
    with a maximum occupancy of 6 persons
    (for) 3-6 persons
    for a maximum of six residents
    for maximum 9 persons
    with a maximum occupancy of 6 persons
    for up to max 5 no of people
    (unrelated) people
    upto

    3 children and young people

    ['persons', 'dwellers', 'people', 'occupants', 'residents','individuals','children']
    '''

    def _generate_dweller_num_pattern(unrelated_people: bool = True):
        preps = ['for', 'with', 'comprising', 'by', 'occupied by', '']
        weights_preps = [0.5 / (len(preps) - 1)] * (len(preps) - 1) + [0.5]
        prep = choice(preps, p=weights_preps)

        post_preps = ['between', 'up to', 'a maximum of', 'maximum', 'a maximum occupancy of', 'up to max', '']
        weights_post_preps = [0.5 / (len(post_preps) - 1)] * (len(post_preps) - 1) + [0.5]
        post_prep = choice(post_preps, p=weights_post_preps)

        noun = random.choice(['person', 'dweller', 'people', 'occupant', 'resident', 'individual',
                              'bed','bedroom','bedsit','letting room','room'])
        if noun!='people' and random.choice(['add_plural','no']) == 'add_plural':
            noun = _add_plural(noun)
        if unrelated_people is True and re.search('bed',noun) is None and \
                random.choice(['add_unrelated', 'no']) == 'add_unrelated':
            noun = f'unrelated {noun}'

        noun_phrases = [f'no of {noun}',  f'no. of {noun}', f'no {noun}',f'no. {noun}',
                        f'num of {noun}', f'number of {noun}',f'num {noun}', f'number {noun}',
                        noun]
        weights_noun_phrases = [0.3 / (len(noun_phrases) - 1)] * (len(noun_phrases) - 1) + [0.7]
        noun_phrase = choice(noun_phrases, p=weights_noun_phrases)



        if post_prep == 'between':
            dweller_num_pattern = random.choice([f'{prep} {post_prep} <NUM> to <NUM> {noun_phrase}',
                                                 f'{prep} {post_prep} <NUM>-<NUM> {noun_phrase}'])
        else:
            dweller_num_pattern = choice([f'{prep} {post_prep} <NUM> to <NUM> {noun_phrase}',
                                          f'{prep} {post_prep} <NUM>-<NUM> {noun_phrase}',
                                          f'{prep} {post_prep} <NUM> {noun_phrase}',
                                          f'{prep} {post_prep} <NUM>-{noun_phrase}'],
                                         p=[0.15, 0.15, 0.5, 0.2])

        dweller_num_description = re.sub(' +', ' ', dweller_num_pattern)

        return dweller_num_description



    def _replace_NUM(dweller_num_description: str, start_num: int, end_num: int):
        ten_dict = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
                    10: 'ten'}
        num_of_NUM = len(re.findall('<NUM>', dweller_num_description))
        chosen_nums = set()

        for i in range(num_of_NUM):
            if i == 0:
                start_num = random.randint(start_num, end_num)
            else:
                if start_num != end_num:
                    start_num = random.randint(start_num + 1, end_num)
                else:
                    start_num = end_num
            chosen_nums.update({start_num})
            dweller_num_description = re.sub('<NUM>', str(start_num), dweller_num_description, count=1)

        for chosen_num in chosen_nums:
            if chosen_num <= 10 and random.choice(
                    ['replace_num_with_string', 'no_replace']) == 'replace_num_with_string':
                dweller_num_description = re.sub(str(chosen_num), ten_dict[chosen_num], dweller_num_description)

        return dweller_num_description




    if chosen_use_class == 'c4':
        # if re.search('hmo|house in multiple occupation',description) is not None:
        if random.choice(['add_residents_num', 'no_add']) == 'add_residents_num':
            dweller_num_description = _generate_dweller_num_pattern(unrelated_people=True)
            dweller_num_description = _replace_NUM(dweller_num_description, 3, 6)
            description = random.choice([f'{dweller_num_description} {description}',
                                         f'{description} {dweller_num_description}'])


    if (chosen_use_class == 'c1' or chosen_use_class == 'c2') and \
            random.choice(['add_residents_num', 'no_add']) == 'add_residents_num':
        dweller_num_description = _generate_dweller_num_pattern(unrelated_people=True)
        dweller_num_description = random.choice([_replace_NUM(dweller_num_description, 3, 6),
                                                 _replace_NUM(dweller_num_description, 7, 999)])
        description = random.choice([f'{dweller_num_description} {description}',
                                     f'{description} {dweller_num_description}'])


    if (chosen_use_class == 'c3' or chosen_use_class == 'c') and random.choice(['add_residents_num', 'no_add']) == 'add_residents_num':
        dweller_num_description = _generate_dweller_num_pattern(unrelated_people=False)
        dweller_num_description = random.choice([_replace_NUM(dweller_num_description, 3, 6),
                                                 _replace_NUM(dweller_num_description, 7, 999)])
        description = random.choice([f'{dweller_num_description} {description}',
                                     f'{description} {dweller_num_description}'])

    if chosen_use_class == 'sui generis' and re.search('hmo|house in multiple occupation',description) is not None:
        dweller_num_description = _generate_dweller_num_pattern(unrelated_people=True)
        dweller_num_description = _replace_NUM(dweller_num_description, 7, 999)
        description = random.choice([f'{dweller_num_description} {description}',
                                     f'{description} {dweller_num_description}',
                                     f'large {description}'])

    return description



def _generate_description(self_of_class, chosen_use_class:str, headwords:set=None):
    '''
    Generate a description of a use class from its keywords list, e.g., clinic
    :param self_of_class: the self of a class which contains attributes of self.headword_synonyms_list and/or
                          self.keywords_list, self.modifier_synonyms_list.
    :param chosen_use_class: a use class, e.g., 'd1'.
    :param headwords: a set of headwords, if not given, randomly choose a keyword from the use class's keywords list.
    :return description: a string of description without tags without diversification, e.g., 'social home'.
    '''
    if headwords is None:
        if chosen_use_class == 'sui generis':
            chosen_use_class_to_get_headwords = 'sui_generis'
        else:
            chosen_use_class_to_get_headwords = chosen_use_class
        headwords = set(getattr(self_of_class, f'headword_synonyms_list_{chosen_use_class_to_get_headwords}'))

    description = random.sample(headwords, 1)[0]

    if chosen_use_class == 'sui generis':
        # if description == 'solar':
            # modifier = random.choice(['ground based','ground-based','ground mounted','ground-mounted','on the ground'])
            # description += ' '+random.choice(['photovoltatic','pv','array','panel','electric','module','tracker','energy',''])
            # if modifier =='on the ground':
            #     description =  description+ ' ' + modifier
            # else:
            #     description = modifier + ' ' + description
        if description == 'agriculture':
            description = random.choice(['agriculture', 'agricultural'])
        if description == 'camp':
            description = random.choice(['camp', 'camping'])
        if description == 'boarding':
            description = random.choice(['dog boarding', 'cat boarding',
                                         'boarding for dog','boarding for cat'])

    if chosen_use_class == 'a5':
        modifier = random.choice(getattr(self_of_class, f'modifier_synonyms_list_a5'))
        description = random.choice([f'{modifier} {description}', f'{description} {modifier}'])

    if chosen_use_class == 'b1' or chosen_use_class == 'b':
        if description == 'industrial':
            description = random.choice(['industrial', 'industry'])

    # must add a c general word
    if (chosen_use_class == 'c1' and description == 'guest') or \
            (chosen_use_class == 'c2' and description in {'nursing','offender','care','caretaker','boarding','authority','retirement','assisted'}):
        description = choice([f"{description} {random.choice(getattr(self_of_class, 'headword_synonyms_list_c'))}",
                               f"{random.choice(getattr(self_of_class, 'headword_synonyms_list_c'))} for {choice(['the',''])} {description}"])

    if chosen_use_class == 'c2' and description == 'older':
        description = random.choice(['older people','older person'])
        description = random.choice([f"{random.choice(getattr(self_of_class, 'headword_synonyms_list_c'))} for {choice(['the',''])} {description}",
                                     f"{description} {random.choice(getattr(self_of_class, 'headword_synonyms_list_c'))}"])

    if chosen_use_class == 'c2' and description == 'elderly':
        description = random.choice(['elderly','elderly people', 'elderly person'])
        description = random.choice([f"{random.choice(getattr(self_of_class, 'headword_synonyms_list_c'))} for {random.choice(['the',''])} {description}",
                                     f"{description} {random.choice(getattr(self_of_class, 'headword_synonyms_list_c'))}"])

    if chosen_use_class == 'c3' and re.search('social|affordable|market', description) is not None:
        description += ' ' + random.choice(getattr(self_of_class, 'headword_synonyms_list_c'))

    if chosen_use_class == 'd2' and description == 'swim':
        description = random.choice(['swim', 'swimming'])


    return description





def _diversify_description(description: str, chosen_use_class:str,
                           general_words: list, allow_add_general_word:bool=True,
                           allow_add_dweller_num:bool = True):
    '''
    Given a description, diversify it using following types:
    1) randomly replace 'centre' with 'center',
    2) randomly replace 'theatre' with 'theater',
    3) randomly replace 'cafe' with 'café',
    4) randomly replace 'and' with '&',
    5) randomly add plural,
    6) randomly add building num from 1 to 999, randomly change 1-10 numbers into words,
    7) randomly add 'no./no. of/no/no of/num/num of/number/number of' after building num.
       This is to noise the change_of_use model.
    8) randomly add a general word, e.g., land, unit
    9) must call _add_dweller_num_to_description function,
    10) randomly add sqm.
    :param description: a string of description, e.g., 'theatre'.
    :param chosen_use_class: a string of chosen use class, e.g., 'c1'.
    :param general_words: a list of general descriptions, e.g., ['unit', 'use', 'space'].
    :param allow_add_general_word: True if allow, else False.
    :return description: a string of diversified description, e.g., '34 theaters units 453 sqm'
    '''
    ten_dict = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
                10: 'ten'}

    if re.search('centre', description) is not None and random.choice(['change_centre', 'no_change']) == 'change_centre':
        description = re.sub('centre', 'center', description)

    if re.search('theatre', description) is not None and random.choice(['change_theatre', 'no_change']) == 'change_theatre':
        description = re.sub('theatre', 'theater', description)

    if re.search('cafe', description) is not None and random.choice(['change_cafe', 'no_change']) == 'change_cafe':
        description = re.sub('cafe', 'café', description)

    if re.search('and', description) is not None and random.choice(['change_and', 'no_change']) == 'change_and':
        description = re.sub('and', '&', description)

    if random.choice(['add_plural', 'no_add']) == 'add_plural':
        description = _add_plural(description)

    if random.choice(['add_random_numbers','no_add']) == 'add_random_numbers':
        if chosen_use_class == 'c3' or \
                chosen_use_class == 'c' or \
                (chosen_use_class=='sui generis' and re.search('hmo|house in multiple occupation',description) is not None):
            num = choice([random.randint(3, 6), random.randint(7, 999)],p=[0.8, 0.2])
            if 1<=num<=10 and random.choice(['change_to_word','no'])=='change_to_word':
                num = ten_dict[num]
        else:
            num = random.randint(1, 999)

        if random.choice(['add_num_word','no']) == 'add_num_word':
            num_word = choice(['no.','no. of', 'no','no of','num','num of','number','number of'])
        else:
            num_word = ''

        description = str(num) + f' {num_word} ' + description

    if allow_add_general_word is True:
        if random.choice(['add_general_word', 'no_add']) == 'add_general_word':
            if chosen_use_class == 'd1' or chosen_use_class == 'd2':
                general_words += ['centre', 'center']
            general_word = random.choice(general_words)
            if random.choice(['add_plural', 'no_add']) == 'add_plural':
                general_word = _add_plural(general_word)
            if random.choice(['add_random_sqm', 'no_add']) == 'add_random_sqm':
                if chosen_use_class == 'c3' or \
                        chosen_use_class == 'c' or \
                        (chosen_use_class=='sui generis' and re.search('hmo|house in multiple occupation',description) is not None):
                    sqm_num = choice([random.randint(3, 6),random.randint(7, 2000)],p=[0.8, 0.2])
                    if 1 <= sqm_num <= 10 and random.choice(['change_to_word', 'no']) == 'change_to_word':
                        sqm_num = ten_dict[sqm_num]
                    random_sqm = f'{sqm_num} sqm'
                else:
                    random_sqm = f'{random.randint(1, 2000)} sqm'

                if random.choice(['add_up_to', 'no']) == 'add_up_to':
                    random_sqm = f'up to {random_sqm}'
            else:
                random_sqm = ''

            # 'of/for' is to noise the change-of-use model
            description = random.choice([random_sqm + random.choice([' of ',' for ', ' ']) + description + ' ' + general_word,
                                         description + random.choice([' of ',' for ',' ']) + random_sqm + ' ' + general_word,
                                         description + ' ' + general_word + random.choice([' of ',' for ',' ']) + random_sqm,
                                         random_sqm + random.choice([' of ',' for ',' ']) + general_word + random.choice([' of ',' for ',' ']) + description,
                                         general_word + random.choice([' of ',' for ',' ']) + random_sqm + random.choice([' of ',' for ',' ']) + description,
                                         general_word + random.choice([' of ',' for ',' ']) + description + random.choice([' of ',' for ',' ']) + random_sqm])
        else:
            if random.choice(['add_random_sqm', 'no_add']) == 'add_random_sqm':
                if chosen_use_class == 'c3' or \
                        chosen_use_class == 'c' or \
                        (chosen_use_class=='sui generis' and re.search('hmo|house in multiple occupation',description) is not None):
                    sqm = choice([random.randint(3, 6),random.randint(7, 2000)],p=[0.8, 0.2])
                    if 1 <= sqm <= 10 and random.choice(['change_to_word', 'no']) == 'change_to_word':
                        sqm = ten_dict[sqm]
                else:
                    sqm = random.randint(1, 2000)

                if random.choice(['add_up_to', 'no']) == 'add_up_to':
                    sqm = f'up to {sqm}'

                description = random.choice([f'{sqm} sqm {description}',
                                                f'{description} {sqm} sqm'])
    else:
        if random.choice(['add_random_sqm', 'no_add']) == 'add_random_sqm':
            if chosen_use_class == 'c3' or \
                    chosen_use_class == 'c' or \
                        (chosen_use_class=='sui generis' and re.search('hmo|house in multiple occupation',description) is not None):
                sqm = choice([random.randint(3, 6), random.randint(7, 2000)], p=[0.8, 0.2])
            else:
                sqm = random.randint(1, 2000)

            if random.choice(['add_up_to', 'no']) == 'add_up_to':
                sqm = f'up to {sqm}'

            description = random.choice([f'{sqm} sqm {description}',
                                         f'{description} {sqm} sqm'])


    if allow_add_dweller_num is True and chosen_use_class in {'c1', 'c2', 'c3', 'c4', 'sui generis','c'}:
        description = _add_dweller_num_to_description(description=description,
                                                      chosen_use_class=chosen_use_class)

    description = re.sub(' +', ' ', description)

    return description



def _add_noise_to_description(self_of_class, descriptions:list,
                              joint_symbol_list:list,
                              keywords_list_irrelative_words: list = None,
                              allow_gibberish:bool=False,
                              max_num_irrelative_words:int = 3,
                              max_num_gibberish_words:int = 5,
                              use_classes:list = use_classes):
    '''
    Given a list descriptions, add gibberish and join them together. Types of gibberish are as following:
    1) randomly add '** style' to a description, e.g., 'chaplet style dwelling'.
    2) collected irrelative words, e.g., ['landscaping', 'ancillary facilities', 'car parking'].
    3) randomly add 'access to/into/for **' to a chosen irrelative word, e.g., 'access to car parking'.
    4) gibberish words from NLTK vocabulary.
    5) randomly add an address with a keyword in, e.g, 'retail street'.
    6) randomly add 'adjacent to **', e.g., 'adjacent to dwelling'.
    :param self_of_class: the self of a class which contains attributes of self.headword_synonyms_list and/or
                          self.keywords_list, self.modifier_synonyms_list.
    :param descriptions: a list of descriptions, e.g., ['34 theaters units 453 sqm','retails']
    :param allow_gibberish: True if allow gibberish else False.
    :param keywords_list_irrelative_words: a list of irrelative words,  e.g., ['landscaping', 'ancillary facilities',
                                          'car parking']. Will randomly chose some irrelative words if this list is
                                          given, else won't.
    :param joint_symbol_list: a list of joint symbols. Will chose white space more often.
    :param use_classes: a list of all use classes to add into the planning notes. Default list excludes the application
                        classes, 'householder', 'tpo', 'other'.
    :return text: a string
    '''

    if descriptions!=[] and choice(['add_style','no']) == 'add_style':
        chosen_use_class = random.choice(use_classes)
        chosen_keyword = _generate_description(self_of_class, chosen_use_class)
        modifier = f'{chosen_keyword} style'
        if choice(['add_before_description','random_add_anywhere']) == 'add_before_description':
            chosen_description_index = random.randint(0,len(descriptions)-1)
            descriptions[chosen_description_index] = f'{modifier} {descriptions[chosen_description_index]}'
        else:
            descriptions += [modifier]


    if keywords_list_irrelative_words is not None:
        num_irrelative_words = random.randint(1, max_num_irrelative_words)
        chosen_irrelative_words = random.sample(keywords_list_irrelative_words, k=num_irrelative_words)

        # if 'solar' in irrelative_string:
        #     if random.choice(['add_modifier','no_add'])=='add_modifier':
        #         irrelative_string.remove('solar')
        #         new_solar = 'solar'+' '+random.choice(['photovoltatic','pv','array','panel','electric','module','tracker','energy'])
        #         irrelative_string.update({new_solar})
        #     if random.choice(['add_roof','no_add']) == 'add_roof':
        #         descriptions += ['roof']

        descriptions += chosen_irrelative_words

    if allow_gibberish is True:
        num_random_words = random.randint(1, max_num_gibberish_words)
        random_words = random.sample(words.words(), num_random_words)
        descriptions += random_words

    if choice(['add_access_to','no']) == 'add_access_to':
        chosen_use_class = random.choice(use_classes)
        chosen_keyword = _generate_description(self_of_class, chosen_use_class)
        prep = random.choice(['into','to','for','in to','onto','on to'])
        descriptions += [f'access {prep} {chosen_keyword}']

    if choice(['add_address', 'no_add']) == 'add_address':
        chosen_use_class = random.choice(use_classes)
        chosen_keyword = _generate_description(self_of_class, chosen_use_class)
        address_word = random.choice(['street', 'road', 'st','st.','s.t.','lane'])
        descriptions += [chosen_keyword+' ' +address_word]

    if choice(['add_adjacent','no']) == 'add_adjacent':
        chosen_use_class = random.choice(use_classes)
        chosen_keyword = _generate_description(self_of_class, chosen_use_class)
        descriptions += ['adjacent to '+ chosen_keyword]


    random.shuffle(descriptions)
    text = ''
    joint_symbol_list_with_space = joint_symbol_list + [' ']
    weights_of_joint_symbols = [0.5 / (len(joint_symbol_list_with_space) - 1)] * (len(joint_symbol_list_with_space) - 1) + [0.5]

    for i, dsc in enumerate(descriptions):
        if i == 0:
            text += dsc
        else:
            joint_symbol = choice(joint_symbol_list_with_space, p=weights_of_joint_symbols)
            text += f'{joint_symbol}{dsc}'

    text = re.sub(' +', ' ', text)

    return text





def _combine_description_and_tags(description, tags):
    tag_pattern = _random_chose_a_tag_pattern()
    tags = re.sub('<TAG>', tags, tag_pattern)

    combined_description_and_tags_string = random.choice([f'{description} {tags}',
                                                          f'{tags} {description}',
                                                          f'({description}) {tags}',
                                                          f'{tags} ({description})',
                                                          f'{description} ({tags})',
                                                          f'({tags}) {description}'
                                                          ])
    return combined_description_and_tags_string




def _diversify_chosen_use_classes(chosen_use_classes):
    chosen_use_classes_diversified = chosen_use_classes.copy()
    if 'b1' in chosen_use_classes_diversified and random.choice(['diversify_b1', 'no_diversify']) == 'diversify_b1':
        chosen_use_classes_diversified.remove('b1')
        chosen_use_classes_diversified.add(random.choice(diversified_b1))

    if random.choice(['add_random_noise_of_tags', 'no_add']) == 'add_random_noise_of_tags':
        chosen_use_classes_diversified.add(_generate_noise_tag())
    return chosen_use_classes_diversified


# def substitute_keywords(self_of_class, text:str, replaced_use_class:str, target_use_class:str,
#                         replaced_keywords_list:list=None):
#
#     '''
#     Substitute keywords in a text with synonyms.
#     :param text: a string of planning notes.
#     :param keywords_list: a list of keywords being replaced, e.g., ['hotel']
#     :param headword_synonyms_list: a list of headword synonyms to replace keywords, e.g., ['hostel']
#     :param modifier_synonyms_list: a list of modifiers synonyms to replace keywords, e.g., ['care']. Modifiers randomly
#                                     combine with headwords as a whole and replace keywords.
#     :return: a string of text after substitution
#     '''
#     # Turn a list words into a string joined with |, e.g., ['hotel', 'boarding house'] -> 'hotel|boarding house'
#     if replaced_keywords_list is None:
#         replaced_keywords_list = getattr(self_of_class, f'keywords_list_{replaced_use_class}')
#     pattern = '|'.join(replaced_keywords_list)
#     description = _generate_description(self_of_class = self_of_class, chosen_use_class= target_use_class)
#     description = _diversify_description(description, target_use_class)
#
#     has_tag = ''
#     if random.choice(['add_tag','no_add']) == 'add_tag':
#         if target_use_class == 'b1' and random.choice(['diversify_b1', 'no_diversify']) == 'diversify_b1':
#             target_use_class = random.choice(diversified_b1)
#         if random.choice(['add_random_noise_of_tags', 'no_add']) == 'add_random_noise_of_tags':
#             target_use_class = _generate_noise_tag()
#         description = _combine_description_and_tags(description, target_use_class)
#         has_tag = 'Y'
#
#     new_text = re.sub(pattern, description, text, flags=re.I)
#
#     return new_text, has_tag




def _generate_general_description_and_specific_use_classes(self_of_class, chosen_general_use_class:str,
                                                           general_words: list,
                                                           headwords:list = None,
                                                           use_classes: list = use_classes):

    '''
    Generate general descriptions with specific use classes, e.g. 'retail (uses a1, a2, a3)'.
    :param self_of_class: the self of a class which contains attributes of self.headword_synonyms_list and/or
                          self.keywords_list, self.modifier_synonyms_list.
    :param chosen_general_use_class: a general use class, a, b, c, d or all.
    :param headwords: if headwords list is None, randomly chose a keyword from headword_synonyms_list_{chosen_general_use_class},
                      e.g., headword_synonyms_list_a.
    :param use_classes: a list of all use classes to add into the planning notes. Default list excludes the application
                        classes, 'householder', 'tpo', 'other'.
    :return combined_general_description_and_tags_string: a string of combined general descriptions and specific use
                                                          classes, e.g., 'retail (uses a1, a2, a3)'.
    :return chosen_use_classes: a set of chosen use classes, e.g., {'a1','a2','a3'}.
    '''
    if chosen_general_use_class == 'a':
        candidate_use_classes = ['a1','a2','a3','a4','a5']
    elif chosen_general_use_class == 'b':
        candidate_use_classes = ['b1','b2','b8']
    elif chosen_general_use_class == 'c':
        candidate_use_classes = ['c1', 'c2', 'c3','c4']
    elif chosen_general_use_class == 'd':
        candidate_use_classes = ['d1', 'd2']
    else:
        candidate_use_classes = use_classes

    chosen_use_classes = set(random.sample(candidate_use_classes, random.randint(1,len(candidate_use_classes))))
    chosen_use_classes_diversified = _diversify_chosen_use_classes(chosen_use_classes)
    tags = _join_use_classes_tags(chosen_use_classes_diversified)

    if headwords is None:
        headwords = getattr(self_of_class, f'headword_synonyms_list_{chosen_general_use_class}')
    description = random.choice(headwords)
    if chosen_general_use_class == 'all':
        description = _diversify_description(description, chosen_use_class='',general_words=general_words, allow_add_general_word=False)
    else:
        description = _diversify_description(description, chosen_use_class='',general_words=general_words)

    combined_general_description_and_tags_string = _combine_description_and_tags(description = description , tags = tags)
    return combined_general_description_and_tags_string, chosen_use_classes






def add_tags_to_non_sense_data(text:str, use_classes: list = use_classes):

    '''
    Add tags into a non sense planning note.
    :param text: a string of planning notes.
    :param use_classes: a list of all use classes to add into the planning notes. Default list excludes the application
                        classes, 'householder', 'tpo', 'other'.
    :param tag_patterns: a list of strings which contain <TAG> in it. <TAG> will be substitute as a sequence of use
                         classes, e.g., a1-a5
    :param joint_symbol_list: a list of characters to join each generated sub text together, e.g., ', ', '. ', etc.
    :return text: a string of text after substitution, the randomly chosen use classes list.
    :return chosen_use_classes: a set of all chosen use classes.
    '''


    prompts = re.findall('use classes|use class|classes|uses|use|class|<SPAN>', text)
    num_prompts = len(prompts)

    if num_prompts == 0:
        num_chosen_use_classes = random.randint(1,len(use_classes))
        chosen_use_classes = set(random.sample(use_classes, num_chosen_use_classes))
        chosen_use_classes_diversified = _diversify_chosen_use_classes(chosen_use_classes)
        substitution = _join_use_classes_tags(chosen_use_classes_diversified)
        text = text + ' ' + re.sub('<TAG>', substitution, _random_chose_a_tag_pattern())
    elif num_prompts == 1:
        num_chosen_use_classes = random.randint(1,len(use_classes))
        chosen_use_classes = set(random.sample(use_classes, num_chosen_use_classes))
        chosen_use_classes_diversified = _diversify_chosen_use_classes(chosen_use_classes)
        substitution = _join_use_classes_tags(chosen_use_classes_diversified)
        text = re.sub('classes|use class|use|class|<SPAN>', prompts[0]+' '+ substitution, text, flags=re.I)
    # According to the number of prompts, partition chosen_tags into several parts. Substitute each prompt with
    # different parts of chosen_tags.
    else:
        num_chosen_use_classes = random.randint(num_prompts,len(use_classes))
        chosen_use_classes = random.sample(use_classes, num_chosen_use_classes)
        chosen_use_classes_diversified = list(_diversify_chosen_use_classes(set(chosen_use_classes)))
        partition_positions = [0] + random.sample(range(1,len(chosen_use_classes_diversified)), k=num_prompts-1)
        partition_positions.sort()

        num_spans = len(re.findall('<SPAN>', text))
        if num_spans == 0 or num_spans == 1:
            text = re.sub('classes|use class|use|class|<SPAN>', _random_chose_a_tag_pattern(), text, flags=re.I)
        else:
            text = re.sub('classes|use class|use|class', _random_chose_a_tag_pattern(), text, flags=re.I)
            num_spans = len(re.findall('<SPAN>', text))
            for _ in range(num_spans):
                text = re.sub('<SPAN>', _random_chose_a_tag_pattern(), text, flags=re.I,count=1)

        for i in range(len(partition_positions)):
            try:
                chosen_tags_partition = chosen_use_classes_diversified[partition_positions[i]:partition_positions[i+1]]
            except:
                chosen_tags_partition = chosen_use_classes_diversified[partition_positions[i]:]
            substitution = _join_use_classes_tags(set(chosen_tags_partition))
            text = re.sub('<TAG>', substitution, text, count=1,flags=re.I)

    return text, chosen_use_classes





def tags_only_expressions(self_of_class, keywords_list_irrelative_words: list,
                          joint_symbol_list: list,
                          allow_gibberish:bool = False,
                          max_num_irrelative_words:int = 3,
                          max_num_gibberish_words:int = 5,
                          use_classes:list = use_classes):
    '''
    Generate a string with one expression,in which <SPAN> is replaced by tags-only text,
    e.g., 'demolition of a1-a5,b1 and c2'
    :param self_of_class:
    :return expression_string: a string of text with one expression, in which <SPAN> is replaced by tags-only text,
                                e.g., 'demolition of a1-a5,b1 and c2'
    :return chosen_use_classes: the randomly chosen use classes set
    '''



    chosen_use_classes_form = choice(['force_span','no_force'], p=[0.7,0.3])
    if chosen_use_classes_form == 'force_span':
        chosen_use_classes = set(_force_random_chose_use_classes_with_spans())
    else:
        num_chosen_use_classes = random.randint(1,len(use_classes))
        chosen_use_classes = set(random.sample(use_classes, num_chosen_use_classes))

    chosen_use_classes_diversified = chosen_use_classes.copy()
    if random.choice(['add_random_noise_of_tags','no_add']) == 'add_random_noise_of_tags':
        chosen_use_classes_diversified.add(_generate_noise_tag())

    tags = _join_use_classes_tags(chosen_use_classes_diversified)


    if allow_gibberish is True:
        tags  = _add_noise_to_description(self_of_class=self_of_class, descriptions = [tags],
                                          keywords_list_irrelative_words=keywords_list_irrelative_words,
                                          joint_symbol_list=joint_symbol_list,
                                          allow_gibberish=True,
                                          max_num_irrelative_words=max_num_irrelative_words,
                                          max_num_gibberish_words=max_num_gibberish_words)

    return tags, chosen_use_classes





def generate_non_sense_data(self_of_class,
                            keywords_list_irrelative_words,
                            joint_symbol_list,
                            allow_gibberish:bool=True,
                            max_num_irrelative_words: int = 3,
                            max_num_gibberish_words: int = 5):
    descriptions = []

    text = _add_noise_to_description(self_of_class, descriptions=descriptions,
                                     keywords_list_irrelative_words=keywords_list_irrelative_words,
                                     joint_symbol_list=joint_symbol_list,
                                     allow_gibberish = allow_gibberish,
                                     max_num_irrelative_words=max_num_irrelative_words,
                                     max_num_gibberish_words=max_num_gibberish_words)

    if choice(['add_joint_symbol_at_beginning','no']) == 'add_joint_symbol_at_beginning':
        text = choice(joint_symbol_list) + text
    if text[0] == ' ':
        text = text[1:]

    return text







def incontinuous_descriptions_with_or_without_tags(self_of_class,
                                                   joint_symbol_list: list,
                                                   keywords_list_irrelative_words: list,
                                                   general_words: list,
                                                   allow_gibberish: bool = True,
                                                   max_num_irrelative_words:int = 3,
                                                   max_num_gibberish_words:int = 5,
                                                   diversified_b1: list = diversified_b1,
                                                   use_classes: list = use_classes):
    '''
    Generate a string with randomly combined expressions, e.g., 'demolition of a1-a5,b1 and c2. erection of dwelling & d1;
    replacement of a4; b1'
    :param self_of_class: the self of a class which contains attributes of self.headword_synonyms_list and/or
                          self.keywords_list, self.modifier_synonyms_list.
    :param joint_symbol_list: a list of characters to join each generated sub text together, e.g., ', ', '. ', etc.
    :param keywords_list_irrelative_words: a list of non-keywords for use classes, e.g., landscaping, car parking, etc.
    :param expression_patterns: a list of strings which contain <SPAN> in it. <SPAN> will be substitute as a random
                                combination of descriptions and/or tags, e.g., dwelling & d1, arcade; use class a1
    :param use_classes: a set of all use classes to add into the planning notes. Default list excludes the application
                        classes, 'householder', 'tpo', 'other'.
    :return text: a string of text with randomly combined expressions,
                  e.g., 'demolition of a1-a5,b1 and c2. erection of dwelling & d1; replacement of a4; b1'
    :return all_chosen_use_classes:the randomly chosen use classes set
    :return has_tags: 'Y' if the text contains tags, else ''
    '''

    num_chosen_use_classes = random.randint(2,4)
    candidate_descriptions = []

    chosen_use_classes = set(random.sample(use_classes, num_chosen_use_classes))
    has_tags = ''
    has_live_work = False

    for chosen_use_class in chosen_use_classes:
        #num_keywords_in_one_use_class = random.randint(1, 3)
        num_keywords_in_one_use_class = 1
        for i in range(num_keywords_in_one_use_class):
            decision_of_combinations_tags_and_descriptions = random.choice(['tags_only', 'descriptions_only', 'mixed'])
            if decision_of_combinations_tags_and_descriptions =='tags_only':
                if chosen_use_class == 'b1' and random.choice(['diversify_b1','no_diversify']) == 'diversify_b1':
                    chosen_use_class = random.choice(diversified_b1)
                tag_string = re.sub('<TAG>',chosen_use_class, _random_chose_a_tag_pattern())
                candidate_descriptions.append(tag_string)
                has_tags = 'Y'
            elif decision_of_combinations_tags_and_descriptions =='descriptions_only':
                descriptions_string = _generate_description(self_of_class=self_of_class, chosen_use_class=chosen_use_class)
                if re.search('live/work', descriptions_string) is not None:
                    has_live_work = True
                descriptions_string = _diversify_description(description=descriptions_string, chosen_use_class=chosen_use_class,general_words=general_words)
                candidate_descriptions.append(descriptions_string)
            else:
                if chosen_use_class == 'b1' and random.choice(['diversify_b1','no_diversify']) == 'diversify_b1':
                    chosen_use_class_diversified = random.choice(diversified_b1)
                else:
                    chosen_use_class_diversified = chosen_use_class

                descriptions_string = _generate_description(self_of_class=self_of_class, chosen_use_class=chosen_use_class)
                if re.search('live/work', descriptions_string) is not None:
                    has_live_work = True
                descriptions_string = _diversify_description(description=descriptions_string, chosen_use_class=chosen_use_class, general_words=general_words)

                mixed_string = _combine_description_and_tags(description=descriptions_string, tags=chosen_use_class_diversified)
                candidate_descriptions.append(mixed_string)
                has_tags = 'Y'

    if has_live_work is True and 'c3' not in chosen_use_classes:
        chosen_use_classes.add('c3')

    text = _add_noise_to_description(self_of_class=self_of_class, descriptions=candidate_descriptions,
                                     keywords_list_irrelative_words=keywords_list_irrelative_words,
                                     joint_symbol_list=joint_symbol_list,
                                     allow_gibberish=allow_gibberish,
                                     max_num_irrelative_words=max_num_irrelative_words,
                                     max_num_gibberish_words=max_num_gibberish_words)

    if choice(['add_joint_symbol_at_beginning','no']) == 'add_joint_symbol_at_beginning':
        text = choice(joint_symbol_list) + text
    if text[0] == ' ':
        text = text[1:]

    return text, chosen_use_classes, has_tags









def generate_general_description_with_specific_tags(self_of_class,
                                                    keywords_list_irrelative_words:list,
                                                    joint_symbol_list: list,
                                                    general_words:list,
                                                    target_use_class:str = None,
                                                    headwords: list = None,
                                                    allow_gibberish:bool = False,
                                                    max_num_irrelative_words: int = 3,
                                                    max_num_gibberish_words: int = 5):
    '''
    Generate a string with one expression,in which <SPAN> is replaced by a general description with some specific tags,
    e.g., 'demolition of flats c1, c3'
    :param self_of_class: the self of a class which contains attributes of self.headword_synonyms_list_a and/or
                          self.modifier_synonyms_list_a.
    :param expression_patterns: a list of strings which contain <SPAN> in it. <SPAN> will be substitute as a random
                                combination of descriptions and/or tags, e.g., dwelling & d1, arcade; use class a1
    :param use_classes: a list of all use classes to add into the planning notes. Default list excludes the application
                        classes, 'householder', 'tpo', 'other'.
    :return chosen_expression_patterns: a string of text with one expression, in which <SPAN> is replaced by  general
                                        description with some specific tags, e.g., 'demolition of flats c1, c3'
    :return chosen_use_classes:the randomly chosen use classes set
    '''



    if target_use_class is None:
        target_use_class = random.choice(['a','b','c','d','all'])


    text, chosen_use_classes = _generate_general_description_and_specific_use_classes(
        self_of_class=self_of_class,
        chosen_general_use_class=target_use_class,
        headwords = headwords,
        general_words=general_words)

    if allow_gibberish is True:
        text = _add_noise_to_description(self_of_class=self_of_class,
                                                descriptions = [text],
                                                keywords_list_irrelative_words=keywords_list_irrelative_words,
                                                joint_symbol_list=joint_symbol_list,
                                                allow_gibberish=True,
                                                max_num_irrelative_words=max_num_irrelative_words,
                                                max_num_gibberish_words=max_num_gibberish_words)

    if choice(['add_joint_symbol_at_beginning','no']) == 'add_joint_symbol_at_beginning':
        text = choice(joint_symbol_list) + text
    if text[0] == ' ':
        text = text[1:]

    return text, chosen_use_classes




def continuous_descriptions_with_continuous_tags(self_of_class, joint_symbol_list: list,
                                                 keywords_list_irrelative_words: list,
                                                 general_words:list,
                                                 allow_gibberish:bool = False,
                                                 max_num_irrelative_words:int = 3,
                                                 max_num_gibberish_words:int = 5,
                                                 use_classes: list = use_classes):
    '''
    Generate a string with one expression,in which <SPAN> is replaced by continuous descriptions with continuous tags,
    e.g., 'demolition of flats, clinic (c1, c3)'
    :param self_of_class: the self of a class which contains attributes of self.headword_synonyms_list_a and/or
                          self.modifier_synonyms_list_a.
    :param joint_symbol_list: a list of characters to join each generated sub text together, e.g., ', ', '. ', etc.
    :param expression_patterns: a list of strings which contain <SPAN> in it. <SPAN> will be substitute as a random
                                combination of descriptions and/or tags, e.g., dwelling & d1, arcade; use class a1
    :param tag_patterns: a list of strings which contain <TAG> in it. <TAG> will be substitute as a use
                         class tag, e.g., a1
    :param use_classes: a list of all use classes to add into the planning notes. Default list excludes the application
                        classes, 'householder', 'tpo', 'other'.
    :return chosen_expression_patterns: a string of text with one expression, in which <SPAN> is replaced by  general
                                        description with some specific tags, e.g., 'demolition of flats c1, c3'
    :return chosen_use_classes:the randomly chosen use classes set
    '''


    descriptions = ''
    num_chosen_use_classes = random.randint(2,4)
    chosen_use_classes = set(random.sample(use_classes,k=num_chosen_use_classes))


    # may have general description
    # if random.choice(['change_into_incorrect_use_class', 'no_change']) == 'change_into_incorrect_use_class':
    #     to_be_substituted_use_class = random.choice(chosen_use_classes)
    #     index_to_be_substituted_use_class = chosen_use_classes.index(to_be_substituted_use_class)
    #     incorrect_use_class = _change_into_an_incorrect_use_class(to_be_substituted_use_class)
    #     chosen_use_classes_diversified = chosen_use_classes[:index_to_be_substituted_use_class] + \
    #                                      chosen_use_classes[index_to_be_substituted_use_class+1:]+\
    #                                      [incorrect_use_class]
    # else:
    #     chosen_use_classes_diversified = chosen_use_classes.copy()

    for i, use_class in enumerate(chosen_use_classes):
        description = _generate_description(self_of_class=self_of_class, chosen_use_class=use_class)
        description = _diversify_description(description=description, chosen_use_class=use_class,general_words=general_words)
        if i < len(chosen_use_classes)-1:
            descriptions += description + random.choice(joint_symbol_list)
        else:
            descriptions += description

    if re.search('live/work', descriptions) is not None and 'c3' not in chosen_use_classes:
        chosen_use_classes.add('c3')

    chosen_use_classes_diversified = _diversify_chosen_use_classes(chosen_use_classes)
    tags =_join_use_classes_tags(chosen_use_classes_diversified)


    descriptions_and_tags_string = _combine_description_and_tags(description=descriptions, tags=tags)

    if allow_gibberish is True:
        descriptions_and_tags_string = _add_noise_to_description(self_of_class=self_of_class,
                                                descriptions = [descriptions_and_tags_string],
                                                keywords_list_irrelative_words=keywords_list_irrelative_words,
                                                joint_symbol_list=joint_symbol_list,
                                                allow_gibberish=True,
                                                max_num_irrelative_words=max_num_irrelative_words,
                                                max_num_gibberish_words=max_num_gibberish_words)

    if choice(['add_joint_symbol_at_beginning','no']) == 'add_joint_symbol_at_beginning':
        descriptions_and_tags_string = choice(joint_symbol_list) + descriptions_and_tags_string
    if descriptions_and_tags_string[0] == ' ':
        descriptions_and_tags_string = descriptions_and_tags_string[1:]


    return descriptions_and_tags_string, chosen_use_classes




def generate_fake_data(self_of_class, keywords_list_irrelative_words: list, joint_symbol_list: list,
                       general_words:list,
                       target_use_class:str = None, headwords:set=None, randomly_adding_tags:bool=False,
                       must_add_tags:bool=False,
                       allow_add_dweller_num:bool = True,
                       diversify_tags:bool = True,
                       max_num_irrelative_words:int = 3,
                       max_num_gibberish_words:int = 5,
                       use_classes:list = use_classes):
    if target_use_class is None:
        target_use_class = random.choice(use_classes)

    description = _generate_description(self_of_class=self_of_class,chosen_use_class=target_use_class,headwords=headwords)

    has_live_work_units = False
    if re.search('live/work', description) is not None:
        has_live_work_units = True
    description = _diversify_description(description=description, chosen_use_class=target_use_class,
                                         general_words=general_words, allow_add_dweller_num=allow_add_dweller_num)

    has_tag = ''
    target_use_class_diversified = target_use_class
    if (randomly_adding_tags is True and choice(['add_tags','no_add'], p=[0.2,0.8]) == 'add_tags') or must_add_tags is True:
        if diversify_tags is True:
            if target_use_class == 'b1' and random.choice(['diversify_b1','no_diversify']) == 'diversify_b1':
                target_use_class_diversified  = random.choice(diversified_b1)
            if random.choice(['add_random_noise_of_tags','no_add'])  == 'add_random_noise_of_tags':
                target_use_class_diversified = _generate_noise_tag()
        description = _combine_description_and_tags(description,target_use_class_diversified)
        has_tag = 'Y'

    description = _add_noise_to_description(
        self_of_class=self_of_class,
        descriptions=[description],
        keywords_list_irrelative_words=keywords_list_irrelative_words,
        joint_symbol_list=joint_symbol_list,
        allow_gibberish=True,
        max_num_irrelative_words=max_num_irrelative_words,
        max_num_gibberish_words=max_num_gibberish_words)

    if choice(['add_joint_symbol_at_beginning','no']) == 'add_joint_symbol_at_beginning':
        description = choice(joint_symbol_list) + description
    if description[0] == ' ':
        description = description[1:]

    return description, target_use_class, has_tag, has_live_work_units








# def add_incorrected_tag_to_single_labeled_data(text:str, single_label = str, use_classes: use_classes,
#                                                tag_patterns: list = tag_patterns):
#
#     '''
#     Add an incorrect tag to single labeled planning note.
#     :param text: a string of planning notes.
#     :param single_label: the single use class the  planning note in labeled with.
#     :param use_classes: a list of all use classes to add into the planning notes. Default list excludes the application
#                         classes, 'householder', 'tpo', 'other'.
#     :param tag_patterns: a list of strings which contain <TAG> in it. <TAG> will be substitute as one specific use class,
#                          e.g., a2
#     :return: a string of text after modification.
#     '''
#     use_classes = use_classes.copy()
#     use_classes.remove(single_label)
#     incorrect_use_class = random.choice(use_classes)
#     index = re.search('use class|use|class',text, flags=re.I)
#     if index is not None:
#         sequence1 = text[:index.start()] + incorrect_use_class + ' ' +  text[index.start():]
#         sequence2 = text[:index.end()] +  ' ' + incorrect_use_class +  text[index.end():]
#         text = random.choice([sequence1, sequence2])
#     else:
#         text = text + re.sub('<TAG>', incorrect_use_class, random.choice(tag_patterns))
#
#     return text













def use_class_num_calculator(data, use_classes: list = use_classes) -> dict:
    '''
    Calculate use class frequencies.
    :param data: a pandas dataframe
    :param use_classes: use classes list, e.g., ['sui generis', 'a1']
    :return: a dict of frequencies of each use class, e.g. {'sui generis': 5973, 'a1': 2454}
    '''
    use_class_calculator = defaultdict(int)
    for use_class in use_classes:
        use_class_calculator[use_class] = sum(data[use_class])

    return use_class_calculator







