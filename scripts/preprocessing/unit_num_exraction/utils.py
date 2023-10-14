import random
import re

from numpy.random import choice
from num2words import num2words

from scripts.preprocessing.use_class_classifier.utils import _add_plural
from scripts.preprocessing.use_class_classifier.keywords import *


def generate_random_int(mode:str = 'mixed_either', include_negitive_one:bool = True,
                        diversify_1_mode:str = 'diversify_with_a_or_a_sinlge'):
    if include_negitive_one is True:
        num = choice([1, random.randint(2, 10),random.randint(10, 50),
                      random.randint(50, 100),random.randint(100, 1000),
                      random.randint(1000, 10000), -1],
                     p = [0.2,0.3,0.2,0.1,0.05,0.05,0.1])
    else:
        num = choice([1, random.randint(2, 10),random.randint(10, 50),
                      random.randint(50, 100),random.randint(100, 1000),
                      random.randint(1000, 10000)],
                     p = [0.2,0.4,0.2,0.1,0.05,0.05])

    word = num2words(num)

    if num == -1:
        word = 'indeterminate'

    if num == 1:
        if diversify_1_mode == 'diversify_with_a_or_a_sinlge':
            word = random.choice(['a', 'an', 'a single', 'one'])
        elif diversify_1_mode == 'diversify_with_a_or_a_sinlge_or_non':
            word = random.choice(['a', 'an', 'a single', 'one', ''])
        else:
            word = 'one'

    if num >= 1000 and random.choice(['add_thousand_separators', 'no']) == 'add_thousand_separators':
        num_str = f'{num:,}'
    else:
        num_str = str(num)

    if mode == 'num_only':
        return num_str, num
    elif mode == 'word_only':
        return word, num
    elif mode == 'mixed_either':
        if num <=10:
            probabilities = [0.5, 0.5]
        else:
            probabilities = [0.8, 0.2]
        if choice(['num','word'],p=probabilities) == 'num':
            return num_str, num
        else:
            return word, num
    elif mode == 'mixed_both':
        form_1 = f"{word} ({num_str})"
        form_2 = f"({word}) {num_str}"
        form_3 = f"({num_str}) {word}"
        form_4 = f"{num_str} ({word})"
        return random.choice([form_1, form_2, form_3, form_4]), num




def search_pattern_of_num(num:int, include_following_no_word:bool):
    word = num2words(num)
    num_with_thousand_separators = f'{num:,}'

    front_constraints = "(?<!\w)(?<!\|)(?<!part )(?<!phase )(?<!article )(?<!order )(?<!schedule )(?<!regulation )(?<!plots )(?<!aged )(?<!level )"
    back_front_constraints_for_num = "(?!\w)(?!\|)(?!\d)(?!\.)(?!\%)(?! sqm)(?! ?storey)(?! ?bed)(?! ?- ?storey)(?! ?- ?bed)(?! ?block)(?! ?building)(?! ?garage)(?! detached garage)"
    back_front_constraints_for_num_excluding_following_no_word = "(?![a-z&&[^nx]])"+back_front_constraints_for_num[6:]
    back_front_constraints_for_word = "(?!\w)(?!\|)(?!\d)(?! sqm)(?! ?storey)(?! ?bed)(?! ?- ?storey)(?! ?- ?bed)(?! ?block)(?! ?building)(?! ?garage)(?! detached garage)"

    if include_following_no_word is True:
        return  f"{front_constraints}({str(num)}|{num_with_thousand_separators}) ?(no. |no |num. |num )|" \
                f"{front_constraints}{word} (no. |no |num. |num )|" \
                f"{front_constraints}({str(num)}|{num_with_thousand_separators}) ?(x|X)(?=(\s|\d))|" \
                f"{front_constraints}({str(num)}|{num_with_thousand_separators}){back_front_constraints_for_num}|" \
                f"{front_constraints}{word}{back_front_constraints_for_word}"
    else:
        return f"{front_constraints}({str(num)}|{num_with_thousand_separators}){back_front_constraints_for_num_excluding_following_no_word}"





def convert_an_even_num_to_pairs_of(num:int):
    if num % 2 == 0:
        if num == 2:
            return f"{int(num/2)} pair of"
        else:
            return f"{int(num/2)} pairs of"
    else:
        raise ValueError('The input number must be even.')



def generate_blocks_of(suitable_for_non_c:bool = False, allow_to_accommodate:bool = True):
    block_num_str, block_num = generate_random_int(mode='mixed_either',diversify_1_mode = 'no')
    storey_num_str, _ = generate_random_int(mode='mixed_either',diversify_1_mode = 'no',include_negitive_one=False)

    if block_num == -1:
        block_num_str = ''
        num_word = ''
    else:
        num_word = random.choice(['no.','no','num','num.',''])

    story_word = random.choice(['',storey_num_str+random.choice([' ','-'])+'storey'])


    if suitable_for_non_c is False:
        middle_word = random.choice(['residential','apartment',''])
    else:
        middle_word = ''

    block_word = random.choice(['block', 'building', 'property'])
    if block_num != 1:
        block_word = _add_plural(block_word)

    if allow_to_accommodate is True:
        last_word = random.choice(['of','comprising','containing','including','to accommodate'])
    else:
        last_word = random.choice(['of', 'comprising', 'containing', 'including'])

    phrase = f"{block_num_str} {num_word} {story_word} {middle_word} " \
             f"{block_word} {last_word} "

    phrase = re.sub(' +',' ',phrase)
    if phrase[0] == ' ':
        phrase = phrase[1:]
    if phrase[-1] == ' ':
        phrase = phrase[:-1]
    return phrase



def generate_extensions_to():
    return f"extention{random.choice(['s',''])} {random.choice(['to','of'])}"



def generate_c3_keyword(mode:str = 'plural'):
    word = random.choice(headword_synonyms_list_c3 + ['C3','studio'])
    if word in {'social', 'affordable', 'market','living','residential'}:
        word += ' ' + random.choice(headword_synonyms_list_c)
    if mode == 'plural' and word != 'C3':
        word = _add_plural(word)
    return word




def generate_c3_phrase(allow_adding_blocks_of: bool = True, allow_to_accommodate:bool = True):
    num_str, num = generate_random_int(mode = 'mixed_either',diversify_1_mode = 'diversify_with_a_or_a_sinlge_or_non')

    if num == 1:
        word = generate_c3_keyword(mode='single')
        unit = 'unit'
    else:
        word = generate_c3_keyword(mode='plural')
        unit = 'units'

    even_num_converted_to_pairs_of = False
    if num % 2 == 0 and choice(['convert_to_pairs_of','no'],p=[0.2,0.8]):
        num_str = convert_an_even_num_to_pairs_of(num)
        even_num_converted_to_pairs_of = True


    bed_num_str, bed_num = generate_random_int(include_negitive_one=False,diversify_1_mode = 'no')
    if bed_num_str == 'a' or bed_num_str == 'a single':
        bed_num_str = 'one'
    bed_word_pattern_1 = random.choice(bed_descriptions_c3)
    bed_word_pattern_2 = random.choice(bed_descriptions_c3+['storey'])
    if bed_num != 1 and bed_word_pattern_1 != 'bedroomed':
        bed_word_1_plural = _add_plural(bed_word_pattern_1)
    else:
        bed_word_1_plural = bed_word_pattern_1

    if bed_num != 1 and bed_word_pattern_2 != 'bedroomed' and bed_word_pattern_2 != 'storey':
        bed_word_2_plural = _add_plural(bed_word_pattern_1)
    else:
        bed_word_2_plural = bed_word_pattern_1


    try:
        int(num_str)
    except:
        num_str = num_str+' '

    try:
        int(bed_num_str)
    except:
        bed_num_str = ' '+bed_num_str

    age_num_str, _ = generate_random_int(include_negitive_one=False, diversify_1_mode = 'no')


    pattern_1 = f'''{num_str}''' \
                f'''{random.choice(['',' '])}{random.choice(['x','X'])}''' \
                f'''{random.choice(['',' '])}''' \
                f'''{random.choice([f"{bed_num_str}{random.choice([' ','-'])}{bed_word_1_plural+' '}"," "])}''' \
                f'''{word}''' \
                f'''{random.choice(['',f" for {random.choice(['','occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['',' and over',' and under'])}"])}'''

    pattern_2 = f'''{num_str}''' \
                f'''{random.choice(['',' '])}{random.choice(['no.','no','num','num.',''])} ''' \
                f"""{random.choice(['',f'''{bed_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} {bed_word_2_plural}",f"-{bed_word_pattern_2}"])}'''])} {word}""" \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['',' and over',' and under'])}"])}'''


    pattern_3 = f'''{num_str} {word}{random.choice(['',' '])}''' \
                f"""({bed_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} {bed_word_2_plural}",f"-{bed_word_pattern_2}"])} """ \
                f'''{random.choice(['semi-detached ','detached ', ' '])}{unit})''' \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

    pattern_4 =  f'''{num_str} ''' \
                 f"""{random.choice(['',f'''{bed_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} {bed_word_2_plural}",f"-{bed_word_pattern_2}"])}'''])} {word}""" \
                 f'''{random.choice(['',f" for {random.choice(['','occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['',' and over',' and under'])}"])}'''

    pattern_5 = f"""{random.choice(['', f'''{bed_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} {bed_word_2_plural}", f"-{bed_word_pattern_2}"])}'''])} {word}""" \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['',' and over',' and under'])}"])}'''

    pattern_6 = f'''{word}{random.choice(['',' '])}''' \
                f"""({bed_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} {bed_word_2_plural}",f"-{bed_word_pattern_2}"])} """ \
                f'''{random.choice(['semi-detached ','detached ', ' '])}{unit})''' \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''


    if num != -1:
        if (num == 1 and num_str != 'one ' and num_str != '1') or even_num_converted_to_pairs_of is True:
            c3_phrase = random.choice([pattern_3, pattern_4])
        else:
            c3_phrase = random.choice([pattern_1, pattern_2,pattern_3])
    else:
        c3_phrase = random.choice([pattern_5,pattern_6])

    if allow_adding_blocks_of is True and random.choice(['add_blocks_of','no']) == 'add_blocks_of':
        c3_phrase = generate_blocks_of(allow_to_accommodate=allow_to_accommodate) + ' ' +c3_phrase

    c3_phrase = re.sub(' +',' ',c3_phrase)
    if c3_phrase[0] == ' ':
        c3_phrase = c3_phrase[1:]
    if c3_phrase[-1] == ' ':
        c3_phrase = c3_phrase[:-1]
    return c3_phrase, num






def generate_c1_c2_c4_keyword(mode:str = 'plural'):
    use_class = choice(['c1','c2','c4'], p=[0.2,0.6,0.2])
    word = random.choice(globals()[f'headword_synonyms_list_{use_class}'] + [use_class.title()])
    general_word = random.choice(headword_synonyms_list_c)
    if mode == 'plural':
        general_word = _add_plural(general_word)

    # must add a c general word
    if (use_class == 'c1' and word == 'guest') or \
            (use_class == 'c2' and word in {'nursing','offender','care','caretaker','boarding','authority','retirement','assisted','disabled'}):
        word = random.choice([f"{word} {general_word}",
                              f"{general_word} for {random.choice(['the',''])} {word}"])

    elif use_class == 'c2' and word == 'older':
        word = random.choice(['older people','older person'])
        word = random.choice([f"{general_word} for {random.choice(['the',''])} {word}",
                              f"{word} {general_word}"])

    elif use_class == 'c2' and word == 'elderly':
        word = random.choice(['elderly','elderly people', 'elderly person'])
        word = random.choice([f"{general_word} for {random.choice(['the',''])} {word}",
                              f"{word} {general_word}"])

    else:
        if mode == 'plural':
            if word == 'house in multiple occupation':
                word = 'houses in multiple occupation'
            elif word not in {'C1','C2','C4'}:
                word = _add_plural(word)

    word = re.sub(' +',' ',word)

    return word





def generate_c1_c2_c4_phrase(allow_adding_blocks_of: bool = True, allow_to_accommodate:bool = True):
    num_str, num = generate_random_int(mode = 'mixed_either',diversify_1_mode = 'diversify_with_a_or_a_sinlge_or_non')

    if num == 1:
        word = generate_c1_c2_c4_keyword(mode='single')
        unit = 'unit'
    else:
        word = generate_c1_c2_c4_keyword(mode='plural')
        unit = 'units'

    even_num_converted_to_pairs_of = False
    if num % 2 == 0 and choice(['convert_to_pairs_of','no'],p=[0.2,0.8]):
        num_str = convert_an_even_num_to_pairs_of(num)+' '
        even_num_converted_to_pairs_of = True


    storey_num_str, storey_num = generate_random_int(include_negitive_one=False,diversify_1_mode = 'no')


    try:
        int(num_str)
    except:
        num_str = num_str+' '

    age_num_str, _ = generate_random_int(include_negitive_one=False,diversify_1_mode = 'no')

    pattern_1 = f'''{num_str}{random.choice(['',' '])}''' \
                f"""{random.choice([f''' {storey_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} ","-"])}storey ''',''''''])}{word}""" \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

    pattern_2 = f'''{num_str} {word}{random.choice(['',' '])}''' \
                f"""({storey_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} ",'-'])}storey {random.choice(['semi-detached ','detached ', ' '])}{unit})""" \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

    pattern_3 = f'''{num_str}{random.choice(['',' '])}{random.choice(['no.','no','num','num.',''])} ''' \
                f"""{random.choice([f''' {storey_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} ",'-'])}storey ''',''''''])}{word}""" \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

    pattern_4 = f'''{num_str}{random.choice(['',' '])}{random.choice(['no.','no','num','num.',''])} {word}''' \
                f"""({storey_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} ", "-"])}storey {random.choice(['semi-detached ','detached ', ' '])}{unit})""" \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

    pattern_5 = f"""{random.choice([f''' {storey_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} ","-"])}storey ''',''])}{word}""" \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

    pattern_6 = f'''{word}{random.choice(['',' '])}''' \
                f"""({storey_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} ", "-"])}storey {random.choice(['semi-detached ','detached ', ' '])}{unit})""" \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

    if num != -1:
        if (num == 1 and num_str != 'one ' and num_str != '1') or even_num_converted_to_pairs_of is True:
            phrase = random.choice([pattern_1,pattern_2])
        else:
            phrase = random.choice([pattern_3,pattern_4])
    else:
        phrase = random.choice([pattern_5,pattern_6])

    if allow_adding_blocks_of is True and random.choice(['add_blocks_of','no']) == 'add_blocks_of':
        phrase = generate_blocks_of(allow_to_accommodate=allow_to_accommodate) + ' ' +phrase

    phrase = re.sub(' +',' ',phrase)
    if phrase[0] == ' ':
        phrase = phrase[1:]
    if phrase[-1] == ' ':
        phrase = phrase[:-1]

    return phrase, num





def generate_c1_c2_c4_phrase_with_bed_num(allow_adding_blocks_of: bool = True, allow_to_accommodate:bool = True):
    num_str, num = generate_random_int(mode='mixed_either',diversify_1_mode = 'diversify_with_a_or_a_sinlge_or_non')

    if num == 1:
        word = generate_c1_c2_c4_keyword(mode='single')
    else:
        word = generate_c1_c2_c4_keyword(mode='plural')

    even_num_converted_to_pairs_of = False
    if num % 2 == 0 and choice(['convert_to_pairs_of','no'],p=[0.2,0.8]):
        num_str = convert_an_even_num_to_pairs_of(num)
        even_num_converted_to_pairs_of = True

    bed_num_str, bed_num = generate_random_int(diversify_1_mode = 'no')

    bed_word_pattern_1 = random.choice(bed_descriptions_c3)
    bed_word_pattern_2 = random.choice(bed_descriptions_c3 + bed_descriptions_c1_c2_c4)
    if bed_num != 1 and bed_word_pattern_1 != 'bedroomed':
        bed_word_1_plural = _add_plural(bed_word_pattern_1)
    else:
        bed_word_1_plural = bed_word_pattern_1

    if bed_num != 1 and bed_word_pattern_2 != 'children' and bed_word_pattern_2 != 'people':
        bed_word_2_plural = _add_plural(bed_word_pattern_2)
    else:
        bed_word_2_plural = bed_word_pattern_2

    try:
        int(num_str)
    except:
        num_str = num_str + ' '

    try:
        int(bed_num_str)
    except:
        bed_num_str = ' ' + bed_num_str

    age_num_str, _ = generate_random_int(include_negitive_one=False,diversify_1_mode = 'no')


    pattern_1 = f'''{num_str}''' \
                f'''{random.choice(['', ' '])}{random.choice(['x', 'X'])}''' \
                f'''{random.choice(['', ' '])}''' \
                f'''{bed_num_str}{random.choice([' ','-'])}{bed_word_1_plural + ' '}''' \
                f'''{word}''' \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

    pattern_2 = f'''{num_str}''' \
                f'''{random.choice(['', ' '])}{random.choice(['no.', 'no', 'num', 'num.', ''])}''' \
                f""" {bed_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} {bed_word_1_plural}", f"-{bed_word_pattern_1}"])} {word}""" \
                f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

    pattern_3 = f'''{num_str}{random.choice(['', ' '])}'''\
                f'''{random.choice(['x', 'X', 'no.', 'no', 'num', 'num.', ''])} {word} ''' \
                f'''{random.choice(['for','for occupation of','containing'])} {random.choice(['up to',''])} {bed_num_str} {bed_word_2_plural}'''

    if num != -1 and bed_num != -1:
        if (num == 1 and num_str != 'one ' and num_str != '1') or even_num_converted_to_pairs_of is True:
            pattern_1_for_a = f'''{num_str}''' \
                              f""" {bed_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} {bed_word_1_plural}", f"-{bed_word_1_plural}"])} {word}""" \
                              f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''
            pattern_2_for_a = f'''{num_str} {word} ''' \
                              f'''{random.choice(['for','for occupation of','containing'])} {random.choice(['up to',''])} {bed_num_str} {bed_word_2_plural}'''
            phrase = random.choice([pattern_1_for_a, pattern_2_for_a])
        else:
            phrase = random.choice([pattern_1, pattern_2, pattern_3])
        return_num = bed_num
    elif num == -1 and bed_num != -1:
        phrase_1 = f"""{bed_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} {bed_word_1_plural}", f"-{bed_word_1_plural}"])} {word}""" \
                   f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''
        phrase_2 = f'''{word} {random.choice(['for','for occupation of','containing'])} {random.choice(['up to',''])} {bed_num_str} {bed_word_2_plural}'''
        phrase = random.choice([phrase_1, phrase_2])
        return_num = bed_num
    elif num != -1 and bed_num == -1:
        if (num == 1 and num_str != 'one ' and num_str != '1') or even_num_converted_to_pairs_of is True:
            pattern_1_for_a = f'''{num_str} {word}''' \
                              f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''
            pattern_2_for_a = f'''{num_str} {word} ''' \
                              f'''{random.choice(['for','for occupation of','containing'])} {bed_word_2_plural}'''
            phrase = random.choice([pattern_1_for_a, pattern_2_for_a])
        else:
            pattern_1 = f'''{num_str}''' \
                        f'''{random.choice(['', ' '])}{random.choice(['x', 'X'])}''' \
                        f'''{random.choice(['', ' '])}{bed_word_1_plural + ' '}''' \
                        f'''{word}''' \
                        f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

            pattern_2 = f'''{num_str}''' \
                        f'''{random.choice(['', ' '])}{random.choice(['no.', 'no', 'num', 'num.', ''])}''' \
                        f''' {word}''' \
                        f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''

            pattern_3 = f'''{num_str}{random.choice(['', ' '])}''' \
                        f'''{random.choice(['x', 'X', 'no.', 'no', 'num', 'num.', ''])} {word} ''' \
                        f'''{random.choice(['for','for occupation of', 'containing'])} {bed_word_2_plural}'''
            phrase = random.choice([pattern_1, pattern_2, pattern_3])
        return_num = num
    else:
        pattern_1 = f'''{word}''' \
                    f'''{random.choice(['', f" for {random.choice(['', 'occupation of '])}{_add_plural(random.choice(bed_descriptions_c1_c2_c4))} aged {age_num_str}{random.choice(['', ' and over', ' and under'])}"])}'''
        pattern_2 = f'''{word} {random.choice(['for','for occupation of', 'containing'])} {bed_word_2_plural}'''
        phrase = random.choice([pattern_1, pattern_2])
        return_num = num

    if allow_adding_blocks_of is True and random.choice(['add_blocks_of','no']) == 'add_blocks_of':
        phrase = generate_blocks_of(allow_to_accommodate=allow_to_accommodate) + ' ' +phrase

    phrase = re.sub(' +',' ',phrase)
    if phrase[0] == ' ':
        phrase = phrase[1:]
    if phrase[-1] == ' ':
        phrase = phrase[:-1]
    return phrase, return_num





def generate_non_c_keyword(mode:str = 'plural'):
    use_classes = ['sui generis','a1','a2','a3','a4','a5','d1','d2']
    use_class = random.choice(use_classes)
    if use_class == 'sui generis':
        headword_synonyms_set_sui_generis = set(headword_synonyms_list_sui_generis)
        headword_synonyms_set_sui_generis.difference({'hostel','hmo','house in multiple occupation'})
        word = random.choice(list(headword_synonyms_set_sui_generis) + ['Sui Generis'])

        if word == 'agriculture':
            word = random.choice(['agriculture', 'agricultural'])
        if word == 'camp':
            word = random.choice(['camp', 'camping'])
        if word == 'boarding':
            word = random.choice(['dog boarding', 'cat boarding',
                                  'boarding for dog', 'boarding for cat'])
    else:
        word = random.choice(globals()[f'headword_synonyms_list_{use_class}'] + [use_class.title()])

        if use_class == 'b1' and word == 'industrial':
            word = random.choice(['industrial', 'industry'])
        if use_class == 'd2' and word == 'swim':
            word = random.choice(['swim', 'swimming'])

    if word not in {'Sui Generis','A1','A2','A3','A4','A5','D1','D2'} and random.choice(['add_general_word','no']) == 'add_general_word':
        general_word = random.choice(headword_synonyms_list_all)
        word = word + ' '+ general_word

    if mode == 'plural' and word not in {'Sui Generis','A1','A2','A3','A4','A5','D1','D2'}:
        word = _add_plural(word)

    return word



def generate_non_c_phrase(allow_adding_blocks_of: bool = True, allow_to_accommodate:bool = True):
    num_str, num = generate_random_int(include_negitive_one=False,diversify_1_mode = 'diversify_with_a_or_a_sinlge_or_non')

    if num == 1:
        word = generate_non_c_keyword(mode='single')
        unit = 'unit'
    else:
        word = generate_non_c_keyword(mode='plural')
        unit = 'units'

    even_num_converted_to_pairs_of = False
    if num % 2 == 0 and choice(['convert_to_pairs_of','no'],p=[0.2,0.8]):
        num_str = convert_an_even_num_to_pairs_of(num)
        even_num_converted_to_pairs_of = True

    storey_num_str, storey_num = generate_random_int(include_negitive_one=False, diversify_1_mode = 'no')

    try:
        int(num_str)
    except:
        num_str = num_str+' '


    phrase_1 = f'''{num_str}{random.choice(['', ' '])}''' \
               f"""{random.choice([f''' {storey_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} " , "-"])}storey ''', ''])}{word}"""
    phrase_2 = f'''{word}{random.choice(['', ' '])}({num_str} {unit})'''
    phrase_3 = f'''{num_str}{random.choice(['',' '])}{random.choice(['no.','no','num','num.',''])} ''' \
               f"""{random.choice([f''' {storey_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} " ,"-"])}storey ''',''])}{word}"""
    phrase_4 = f'''{word}{random.choice(['', ' '])}({num_str} {random.choice(['no.','no','num','num.',''])} ''' \
               f"""{random.choice([f''' {storey_num_str}{random.choice([f" {choice(['no.','no','num','num.',''],p=[0.15,0.15,0.15,0.15,0.4])} ","-"])}storey ''',''])}{unit})"""

    if num != -1:
        if num == 1 and num_str != 'one ' and num_str != '1' :
            phrase = phrase_1
        elif even_num_converted_to_pairs_of is True:
            phrase = random.choice([phrase_1, phrase_2])
        else:
            phrase = random.choice([phrase_3, phrase_4])
    else:
        phrase = f'''{random.choice([f" {storey_num_str}{random.choice([' ', '-'])}storey ", ''])}{word}'''

    if allow_adding_blocks_of is True and random.choice(['add_blocks_of','no']) == 'add_blocks_of':
        phrase = generate_blocks_of(suitable_for_non_c=True, allow_to_accommodate=allow_to_accommodate) + ' ' +phrase

    phrase = re.sub(' +',' ',phrase)
    if phrase[0] == ' ':
        phrase = phrase[1:]
    if phrase[-1] == ' ':
        phrase = phrase[:-1]

    return phrase, 0





def uppercase_the_first_letter_of_a_sentence(sentence:str):
    return sentence[0].upper() + sentence[1:]


def combine_two_change_of_use_patterns(pat1: str, pat2: str):
    if (pat1[-6:] == '<FROM>' and pat2[:4] == '<TO>') or (pat1[-4:] == '<TO>' and pat2[:6] == '<FROM>'):
        return pat1 + random.choice(joint_symbols_hard_boundaris) + uppercase_the_first_letter_of_a_sentence(pat2)
    else:
        return pat1 + random.choice(joint_symbols_coordination_for_sentences) + \
               random.choice([pat2, uppercase_the_first_letter_of_a_sentence(pat2)])


def combine_planning_notes(*args: str):
    combined_planning_notes = ''
    for i, planning_note in enumerate(args):
        planning_note = planning_note.strip(' .')
        if i == 0:
            combined_planning_notes = planning_note
        else:
            combined_planning_notes = combined_planning_notes + \
                                      random.choice(joint_symbols_coordination_for_sentences) + \
                                      random.choice([planning_note, uppercase_the_first_letter_of_a_sentence(planning_note)])
    return combined_planning_notes






def combine_a_list_of_keywords(keywords:list):
    connected_string = ''
    for i, keyword in enumerate(keywords):
        if i == 0:
            connected_string = keyword
        else:
            connected_string = connected_string + random.choice(joint_symbols_coordination) + keyword
    return connected_string




def join_a_list_of_numbers_with_vertical_bar(num_list:list):
    if num_list == [] or sum(num_list) == 0:
        num_sequence = '0'
    else:
        num_sequence = '|'.join('indeterminate' if x == -1 else '' if x == 0 else str(x) for x in num_list)

        num_sequence = re.sub('\|+', '|', num_sequence)

        if num_sequence[0] == '|':
            num_sequence = num_sequence[1:]

        if num_sequence == '':
            num_sequence = '0'
        elif num_sequence[-1] == '|':
            num_sequence = num_sequence[:-1]


    return num_sequence

