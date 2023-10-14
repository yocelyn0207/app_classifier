import random

from scripts.preprocessing.use_class_classifier.utils import _add_plural
from scripts.preprocessing.use_class_classifier.keywords import *

def generate_research_regex_pattern_from_keyword_list(keyword_list:list):
    pattern = ''
    for word in keyword_list:
        if word[-1] == ')' and word[0] != '(':
            pattern += f'(?<!\w){word}|'
        elif word[-1] != ')' and word[0] == '(':
            pattern += f'{word}(?!\w)|'
            pattern += f'{_add_plural(word)}(?!\w)|'
        elif word[-1] == ')' and word[0] == '(':
            pattern += f'{word}|'
        else:
            pattern += f'(?<!\w){word}(?!\w)|'
            pattern += f'(?<!\w){_add_plural(word)}(?!\w)|'
    pattern = pattern[:-1] # remove the final '|'
    return pattern



def combine_two_applications(app1: str, app2: str):
    return app1 + random.choice(joint_symbol_list_without_preps) + app2


def random_choose_a_keyword_from_an_use_class():
    use_class = random.choice(use_classes)
    if use_class == 'sui generis':
        use_class_keyword = random.choice(headword_synonyms_list_sui_generis)
    else:
        use_class_keyword = random.choice(globals()[f'headword_synonyms_list_{use_class}'])

    return use_class, use_class_keyword
