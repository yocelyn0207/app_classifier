import random
import re

import numpy as np

from scripts.preprocessing.use_class_classifier.utils import _add_plural
from scripts.preprocessing.use_class_classifier.keywords import *
from scripts.preprocessing.application_type_classifier.keywords_of_types import *
from scripts.preprocessing.application_type_classifier.utils import combine_two_applications, random_choose_a_keyword_from_an_use_class

patterns_all_matters_reserved = ['(with all matters .+ reserved)',
                                 '(with all matters reserved)',
                                 '(with all matters reserves)',
                                 '(with all matters to be reserved)',

                                 '(all matters .+ reserved)',
                                 '(all matters reserved)',
                                 '(all matters reserves)',
                                 '(all matters to be reserved)',

                                 'with all matters .+ reserved for the',
                                 'with all matters reserved for the', 'with all matters to be reserved for the',
                                 'with all matters reserves for the',
                                 
                                 'all matters .+ reserved for the',
                                 'all matters reserved for the','all matters to be reserved for the',
                                 'all matters reserves for the',
                                
                                 'with all matters .+ reserved for',
                                 'with all matters reserved for', 'with all matters to be reserved for',
                                 'with all matters reserves for',

                                 'all matters .+ reserved for',
                                 'all matters reserved for',
                                 'all matters to be reserved for',
                                 'all matters reserves for',

                                 'with all matters .+ reserved',
                                 'with all matters reserved', 'with all matters to be reserved',
                                 'with all matters reserves',
                                 
                                 'all matters except .+ reserved',
                                 'all matters reserved','all matters to be reserved',
                                 'all matters reserves',

                                 '(with some matters .+ reserved)',
                                 '(with some matters reserved)',
                                 '(with some matters reserves)',
                                 '(with some matters to be reserved)',

                                 '(some matters .+ reserved)',
                                 '(some matters reserved)',
                                 '(some matters reserves)',
                                 '(some matters to be reserved)',

                                 'with some matters .+ reserved for the',
                                 'with some matters reserved for the', 'with some matters to be reserved for the',
                                 'with some matters reserves for the',

                                 'some matters .+ reserved for the',
                                 'some matters reserved for the', 'some matters to be reserved for the',
                                 'some matters reserves for the',

                                 'with some matters .+ reserved for',
                                 'with some matters reserved for', 'with some matters to be reserved for',
                                 'with some matters reserves for',

                                 'some matters .+ reserved for',
                                 'some matters reserved for',
                                 'some matters to be reserved for',
                                 'some matters reserves for',

                                 'with some matters .+ reserved',
                                 'with some matters reserved', 'with some matters to be reserved',
                                 'with some matters reserves',

                                 'some matters except .+ reserved',
                                 'some matters reserved', 'some matters to be reserved',
                                 'some matters reserves',

                                 'reserved matters'
                                 ]

patterns_outline = ['outline planning application for the', 'outline application for the',
                    'outline planning permission for the', 'outline for the',
                    'outline planning application for', 'outline application for', 'outline planning permission for',
                    'outline for',
                    'outline planning application', 'outline application', 'outline planning permission', 'outline']








def outline_to_full(outline_app: str):
    for pattern in patterns_all_matters_reserved:
        full_app_draft = re.sub(pattern,'',outline_app, flags=re.IGNORECASE)
        if full_app_draft != outline_app:
            break

    full_app_draft = re.sub('\(\)','',full_app_draft)
    full_app_draft = re.sub(' +', ' ', full_app_draft)

    for pattern in patterns_outline:
        full_app = re.sub(pattern,'',full_app_draft, flags=re.IGNORECASE)
        if full_app != full_app_draft:
            break

    full_app = re.sub(' +',' ',full_app)
    full_app = full_app.strip()

    if full_app != '':
        if full_app[0] == ' ':
            full_app = full_app[1:]

    return full_app






def outline_plus_all_matters_reserved(outline_app: str):
    all_matters_reserved_positions = ['beginning', 'end', 'middle']
    all_matters_reserved_position = random.choice(all_matters_reserved_positions)
    all_matters_reserved = random.choice(patterns_all_matters_reserved)

    if '.+' in all_matters_reserved:
        sub_modifier = random.choice(['except','save for','apart from','other than',''])
        sub_word = random.choice(['access','layout','access and layout'])
        all_matters_reserved = re.sub('\.\+', sub_modifier+' '+sub_word, all_matters_reserved)

    if all_matters_reserved_position == 'beginning':
        outline_app = combine_two_applications(all_matters_reserved, outline_app)
    elif all_matters_reserved_position == 'end':
        outline_app = combine_two_applications(outline_app, all_matters_reserved)
    else:
        for pattern in ['outline planning application', 'outline planning permission', 'outline application',  'outline']:
            outline_app_draft = re.sub(pattern, pattern+' '+all_matters_reserved, outline_app)
            if outline_app_draft != outline_app:
                outline_app = outline_app_draft
                break

    return outline_app






def change_of_use_fake_data(type_to_be_augmented):
    change_of_use_patterns = ['change of use from <FROM> to <TO>',
                              'demolition of <FROM>. erection of <TO>',
                              'conversion of <FROM> to <TO>']

    app = random.choice(change_of_use_patterns)

    if type_to_be_augmented == 'Minerals Application':
        keyword = random.choice(Minerals_Application_keywords_for_the_other_types_keywords)
    elif type_to_be_augmented == 'Waste Management Application':
        keyword = random.choice(Waste_Management_Application_for_the_other_types_keywords)
    elif type_to_be_augmented == 'Hazardous Substances Consent Application':
        keyword = random.choice(Hazardous_Substances_Consent_Application_for_the_other_types_keywords)
    elif type_to_be_augmented == 'Agricultural Development':
        keyword = random.choice(Agricultural_Development_for_the_other_types_keywords)
    else:
        raise ValueError("The type to be augmented should be Minerals Application, Waste Management Application,"
                         "Hazardous Substances Consent Application or Agricultural Development")

    if random.choice(['plural','no']) == 'plural':
        keyword = _add_plural(keyword)



    use_class,  use_class_keyword = random_choose_a_keyword_from_an_use_class()
    if random.choice(['plural','no']) == 'plural':
        use_class_keyword = _add_plural(use_class_keyword)

    if random.choice(['full','no']) == 'full':
        type = "Full Application"
        app = re.sub('<FROM>',keyword, app)
        app = re.sub('<TO>', use_class_keyword, app)
        demolition = []
        erection = [use_class]
    else:
        type= type_to_be_augmented
        app = re.sub('<FROM>', use_class_keyword, app)
        app = re.sub('<TO>', keyword, app)
        demolition = [use_class]
        erection = []

    return app, type, demolition, erection








def non_advertisement_consent_fake_data(pattern: str,
                                        keyword = None):
    location_words = ['front','back','north','south','west','east','northwest','southwest','northeast','southeast','central','side']
    prep_phrase = random.choice([f"{random.choice(['to', 'on'])} {random.choice(['shop',''])} frontage",
                                 f"{random.choice(['to','on'])} {random.choice(['forecourt', ''])} display space",
                                 f"{random.choice(['to','on'])} the {random.choice(location_words)} elevation",
                                 f"{random.choice(['inside of','between',f'to the {random.choice(location_words)}'])} window bay{random.choice(['s',''])}",
                                 f"{random.choice(['with','and'])} {random.choice(['associated',''])} {random.choice(['canopy','portacabin'])}"])

    type = 'Full Application'
    change_of_use = ''

    if pattern == 'non_advertisement_consent_keywords':
        use_class = np.nan

        # keyword =  random.choice(Non_Advertisement_Consent_keywords)

        if keyword in {"street lamp", "lighting column"}:
            type = 'Telecommunications/Overhead Electricity Lines'
        elif keyword in {'shopfront', 'ticket office','marketing unit'}:
            use_class = 'a1'
        elif re.search('light',keyword) is not None:
            use_class = 'b1'
        elif keyword == 'MUGA' or keyword == 'Multi Use Games Area':
            use_class = 'd2'
        else:
            use_class = 'sui generis'

        # 1.8m x 2.4m
        if random.choice(['sqm','no']) == 'sqm':
            keyword = str(round(random.uniform(1, 10), random.randint(1, 2))) + f"m {random.choice(['x','X'])} " + \
                      str(round(random.uniform(1, 10), random.randint(1, 2))) + 'm ' + keyword

        # 2no.
        if random.choice(['plural','no']) == 'plural':
            keyword = random.choice(['new','replacement',''])+ ' '+_add_plural(keyword)

            if random.choice(['num','no']) == 'num':
                keyword = str(random.randint(2,10)) + random.choice([' ','']) + random.choice(['no.','no','num','num.']) + ' '+keyword
        elif random.choice(['single','no']) == 'single':
            keyword = random.choice(['a','an']) + ' '  + random.choice(['new','replacement','']) + ' ' + keyword


        if random.choice(['prep_phrase','no']) == 'prep_phrase':
            keyword = keyword + ' ' + prep_phrase

    else:
        use_class, use_class_keyword = random_choose_a_keyword_from_an_use_class()
        if random.choice(['plural', 'no']) == 'plural':
            use_class_keyword = _add_plural(use_class_keyword)

        keyword = use_class_keyword + ' ' + prep_phrase


    app_type = random.choice(['from_only', 'to_only'])
    if app_type == 'from_only':
        app = random.choice(change_of_use_patterns['from']['begin_with_prompt'] +
                            change_of_use_patterns['from']['begin_with_non_prompt'])
        app = re.sub('<FROM>', keyword, app)
        if use_class is not np.nan:
            demolition = [use_class]
        else:
            demolition = []
        erection = []
    else:
        app = random.choice(change_of_use_patterns['to']['begin_with_prompt'] +
                            change_of_use_patterns['to']['begin_with_non_prompt'])
        app = re.sub('<TO>', keyword, app)
        demolition = []
        if use_class is not np.nan:
            erection = [use_class]
        else:
            erection = []


    app = app.lstrip().strip()
    app = re.sub(' +',' ',app)
    if re.search('change of use', app, re.IGNORECASE) is not None:
        change_of_use = 'Y'

    return app, type, demolition, erection, change_of_use

