import re
from scripts.preprocessing.use_class_classifier.utils import _add_plural



'''
Rules:
1. search prompt words, if not, all erections
2. noises: up to, lean(-)to, additional to, access for/into/to, {general word} for/of, pair of, no/no./num/number of, for (the) older/elderly,
   form {keyword} primary school, replacement {keyword}, set aside for, to be, used for, adjacent to, related/relating to, 
   to (the) north/west/south/east/northwest/northeast/southwest/southeast/front/rear 

'''





def split_planning_note_into_demolition_and_erection(planning_note:str):
    # ???? '<FROM> convert to <TO>', '<FROM> convert into <TO>' ????
    # ???? 'current <FROM> as <TO>', 'current of <FROM> as <TO>' ????
    # ???'<FROM> on the site of <TO>'
    # development
    # retaining, retain


    # \W: the excluded word before to/into/for should not be part of another word, e.g., 'house for ...' includes 'use for'
    to_regex = '(?<!\Waccess )(?<!\Waccess on)(?<!\Waccess on )(?<!\Waccess point )(?<!\Wadjacent )(?<!\Wrelated )(?<!\Wrelating )(?<!\Wup )(?<!\Wlean )(?<!\Wlean-)(?<!\Wadditional )(?<!\Wamendment )(to (?!be )(?!(the )?north)(?!(the )?west)(?!(the )?south)(?!(the )?east)(?!(the )?front)(?!(the )?rear)(?!(the )?forecourt)(?!perimeter)(?!\d*pm).*)'
    into_regex = '(?<!\Waccess )(into .*)'

    general_words = ['unit', 'use', 'space', 'building', 'area', 'floorspace', 'institution', 'estate', 'locality',
                     'site', 'premise', 'facility', 'process', 'block', 'terrace', 'land', 'siting','ground']
    for_regex_general_words = ''
    for word in general_words:
        for_regex_general_words += f'(?<!\W{word} )' if word not in {'area','building','land'} else f'(?<!\W(?<!parking )(?<!park )area )(?<!\W(?<!existing storage )building )(?<!\W(?<!agricultural )land )'
        for_regex_general_words += f'(?<!\W{_add_plural(word)} )' if word not in {'area','building','land'} else f'(?<!\W(?<!parking )(?<!park )areas )(?<!\W(?<!existing storage )buildings )(?<!\W(?<!agricultural )lands )'
    for_regex = f'(?<!\Waccess )(?<!\Wset aside )(?<!\Wused ){for_regex_general_words}(for (?!rent ).*)'
    with_regex = '(?<!\Wtogether )(?<!\Walong )(?<!\Wassociated )(?<!\Win connection )(with (?!associated).*)'

    form_regex = 'form(?! entry)(?! primary)(?! secondary)(?! school)'
    replacement_regex = 'replacement(?! flat)(?! workshop)(?! dwelling)(?! unit)(?! and additional allotments)(?! [\d|\W]* storey building)(?! office)'
    extension_regex = '(?<!\Wdormer )(?<!\Winfill )(?<!\Wrear )extension'

    # Step 1: split planning note into sentences
    sentences = re.split(r'(?<!inc)(?<!no)(?<!nos)\. |: ',planning_note,flags=re.IGNORECASE)
    # print('sentences',sentences)


    # Step 2: split sentences into patterns
    front_promt_words = {'change of use','change of uses', 'change', 'redevelopment','redevelop','develop',
                         replacement_regex, 'conversion', 'conversions',
                         'convert','(?<!to) replace', 'subdivision', 'subdivisions', 'subdivide',
                         'sub-division','sub-divisions', 'sub-divide',
                         'restoration','restorations','restore',form_regex,'formation', 'formations','forming',
                         'erect','erection','erections','build','rebuild','re-build','rebuilding','re-building',
                         'construction', 'constructions', 'construct', 'installation', 'installations',
                         'facilitate','creation', 'creations','create','elevation','elevations','elevate',
                         're-elevation','re-elevations','re-elevate','resiting','resit',
                         'provide','serve','alteration','alterations', extension_regex,
                         'retention','retentions','provision','provisions','continuing','relocation','relocations',
                         'refurbishment', 're-furbishment','refurbish','re-furbish',
                         're-configuration','reconfiguration','re-configurations','reconfigurations',
                         'reinstatement','re-instatement','cessation','cessations','reduce','removal of', 'demolition',
                         'demolitions','demolish','to be used as','for use as','residential development',
                         'use of land for', 'the building of','use of the resultant clear space for',
                         'stationing of','development of up to','development of [0-9]*', 'siting of',
                         'proposed [0-9]*','to be used for','in association with development of',
                         'employment development', 'increase the total number of','to be used in connection with',
                         'previously approved','and building \d*(no.)?','development of'}

    sub_sentences = []
    prompt_pattern = ' |'.join(prompt for prompt in front_promt_words)  # need a white space

    for sentence in sentences:
        if re.search(f'(?<!\w)({prompt_pattern})', sentence,flags=re.IGNORECASE) is not None:
            positions = []
            matches = re.finditer(f'(?<!\w)({prompt_pattern})', sentence,flags=re.IGNORECASE)
            for m in matches:
                positions.append(m.span()[0])

            prior_position = 0
            for i, p in enumerate(positions):
                sub_sentence = sentence[prior_position:p]
                if sub_sentence!= '':
                    sub_sentences.append(sub_sentence)
                prior_position = p
                if i == len(positions) - 1:
                    sub_sentence =  sentence[p:]
                    sub_sentences.append(sub_sentence)
        else:
            if sentence != '':
                sub_sentences.append(sentence)

    # print('sub_sentences',sub_sentences)



    # Step 3: split demolition part and erection part
    demolitions = ''
    erections = ''
    for sub_sentence in sub_sentences:
        # group: change of use, change
        result = re.findall('change of uses? to |change of uses? for',sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        use_for_regex_general_words = '|'.join(general_words)
        use_for_regex_general_words += '|'.join(_add_plural(word) for word in general_words)
        result = re.findall(f'((change of uses? of (the )?(existing )?({use_for_regex_general_words}) for|use of (the )?(existing )?({use_for_regex_general_words}) for) .*?)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        result = re.findall(f'((change of uses?|change) .*?){into_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((change of uses?|change) .*?){to_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((change of uses?|change) .*?){for_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'change of uses? |change ', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += sub_sentence+' '
            continue


        # group: redevelopment, redevelopment, redevelop
        result = re.findall('(redevelopment|redevelop|re-development|re-develop|re development|re develop|develop) (into |to |for |with|in to )',sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue


        result = re.findall(f'((redevelopment|redevelop|re-development|re-develop|re development|re develop|develop) .*?){into_regex}', sub_sentence,flags= re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((redevelopment|redevelop|re-development|re-develop|re development|re develop|develop) .*?){to_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((redevelopment|redevelop|re-development|re-develop|re development|re develop|develop) .*？){for_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'redevelopment |redevelop |re-development |re-develop |re development |re develop |develop ', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        # group: replace, replacement
        # noise: fireplace
        result = re.findall(f'(?<!\w)(replace|re-place|{replacement_regex}|re-placement) (with |by )',sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        result = re.findall(f'((?<!\w)(replace|re-place|{replacement_regex}|re-placement) .*?){with_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((?<!\w)(replace|re-place|{replacement_regex}|re-placement) .*?)(by .*)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((?<!\w)(replace|re-place|{replacement_regex}|re-placement) .*?){to_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((?<!\w)(replace|re-place|{replacement_regex}|re-placement) .*?){for_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((?<!\w)(replace|re-place|{replacement_regex}|re-placement) .*?)(over .*)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'(.* to replace) (.*)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += result[0][0]+' '
            demolitions += result[0][1]+' '
            continue

        result = re.findall(f'(.* replaced) {with_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][1]+' '
            continue

        result = re.findall(f'(.* replaced) (by .*)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][1]+' '
            continue

        result = re.findall(f'((?<!\w)(replace|re-place|{replacement_regex}|re-placement) of)',sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += sub_sentence+' '
            continue


        # group: conversion, convert
        result = re.findall('(conversion|conversions) (to |into |in to )',sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        result = re.findall(f'((conversion|conversions|convert) .*?){into_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((conversion|conversions|convert) .*?){to_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((conversion|conversions|convert) .*?){for_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall('conversion |conversions |convert ',sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += sub_sentence+' '
            continue



        # group: subdivision, subdivide
        result = re.findall(f'((subdivision|subdivisions|subdivide|sub-division|sub-divisions|sub-divide) .*?){into_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((subdivision|subdivisions|subdivide|sub-division|sub-divisions|sub-divide) .*?){to_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'subdivision |subdivisions |subdivide |sub-division |sub-divisions |sub-divide ', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += sub_sentence+' '
            continue

        result = re.findall(f'(.* to be subdivided) (into .*)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][1]+' '
            continue

        result = re.findall(f'.* to be subdivided', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += sub_sentence+' '
            continue


        # group: restoration
        result = re.findall(f'(restoration|restorations .*?){to_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][1]+' '
            continue

        result = re.findall(f'restoration |restorations ', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        # group: erection
        # '<TO> to be built','for <TO> purpose','for <TO> use',
        result = re.findall(f'{form_regex} |formation |formations| forming |erection |erections |erect |rebuilding |re-building |'
                            f'rebuild |re-build |build |construction |constructions |construct |facilitate |creation |creations '
                            f'create |elevation |elevations |elevate |re-elevation |re-elevations |re-elevate |resiting |resit |'
                            f'provide |serve |servive |alterations |alteration |{extension_regex} |extensions |installation |installations '
                            f'retention |retentions |provision |provisions |continuing |relocation |relocations |refurbishment |re-furbishment|'
                            f'refurbish |re-furbish |reconfiguration |reconfigurations |re-configuration |re-configurations |reinstatement |'
                            f're-instatement |residential development |the building of |use of the resultant clear space for |stationing of |'
                            f'development of up to |siting of |development of [0-9]* |proposed [0-9]* |to be used for |'
                            f'employment development, |increase the total number of |to be used in connection with |'
                            f'development of ', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        result = re.findall(f'(.*) to be built', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        result = re.findall(f'for (.*) (purpose|use)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        result = re.findall(f'(to be used as|for use as|for uses as) (.*)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            erections += sub_sentence+' '
            continue

        result = re.findall(f'(use of former .*?)(as .*)',sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][1]+' '
            continue

        # group: demolition
        result = re.findall(f'((cessation|cessations|reduce|removal of|demolition|demolitions|demolish) .*?)((the )?(proposal of|proposal|outline planning permission for|with (the )?proposed|, (the )?proposed|and (the )?proposed|(the )?development of|in connection with) .*)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((cessation|cessations|reduce|removal of|demolition|demolitions|demolish) .*?){to_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'((cessation|cessations|reduce|removal of|demolition|demolitions|demolish) .*?){for_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][2]+' '
            continue

        result = re.findall(f'cessation |cessations |reduce |removal of |demolition |demolitions |demolish ', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            if len(re.findall('; |, ',sub_sentence)) >= 9:
                sub_result = re.findall('(.*?)(;|, .*)', sub_sentence)
                demolitions += sub_result[0][0] + ' '
                for i in range(1, len(sub_result)):
                    erections += sub_result[i][0] + ' '
            else:
                demolitions += sub_sentence+' '
            continue

        result = re.findall(f'(.*) to be (reduced|removed|demolished)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += sub_sentence+' '
            continue

        result = re.findall(f'(previously approved for .*)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += sub_sentence+' '
            continue

        result = re.findall(f'(previously approved .*){for_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][1] + ' '
            continue

        result = re.findall(f'(previously approved .*){to_regex}', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += result[0][0]+' '
            erections += result[0][1] + ' '
            continue

        result = re.findall(f'(previously approved .*)', sub_sentence, flags=re.IGNORECASE)
        if result != []:
            demolitions += sub_sentence+' '
            continue

        # if no prompt words are found
        erections += sub_sentence+' '

    demolitions = re.sub(' +',' ',demolitions)
    erections = re.sub(' +', ' ', erections)
    # Sentence beginning with 'to' sometimes affects the predictions of use class classifier model. Think may be there
    # are a lot of 'to'-related noises, e.g., 'access to'.
    if demolitions[:1] == ' ':
        demolitions = demolitions[1:]
    if erections[:1] == ' ':
        erections = erections[1:]

    if re.search('^to ', demolitions, flags=re.IGNORECASE) is not None:
        demolitions = demolitions[3:]
    if re.search('^to ', erections, flags=re.IGNORECASE) is not None:
        erections = erections[3:]

    if re.search('^into ', demolitions, flags=re.IGNORECASE) is not None:
        demolitions = demolitions[5:]
    if re.search('^into ', erections, flags=re.IGNORECASE) is not None:
        erections = erections[5:]


    # print('sentences',sentences)
    # print('sub_sentences',sub_sentences)
    # print('demolitions****'+demolitions)
    # print('erections****'+erections)
    # print('*'*100)

    return demolitions, erections

# split_planning_note_into_demolition_and_erection(
#     planning_note = "PROPOSED REPLACEMENT OF REDUNDANT FARM BUILDINGS TO COMMERICAL UNITS FOR FLEXIBLE B1 OR B8 USE(S)")



# import pandas as pd
# import csv
# from tqdm import tqdm
# df = pd.read_csv('/Users/alicewong/Documents/Programming/application-classifier/datasets/change_of_use/test/minor_applications.csv')
#
#
#
# with open('/Users/alicewong/Documents/Programming/application-classifier/datasets/change_of_use/test/minor_applications_split_demolitions_and_erections_20220822.csv',mode='a') as data:
#     data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     # write header
#     row = ['planning_notes','demolitions','erections']
#     data_writer.writerow(row)
#
#     for _,row in tqdm(df.iterrows(),total=len(df)):
#         demolitions, erections = split_planning_note_into_demolition_and_erection(row['planning_notes'])
#         row = [row['planning_notes'], demolitions,erections]
#         data_writer.writerow(row)
#         # print(row['planning_notes'])
#         # print('sentences',sentences)
#         # print('sub_sentences',sub_sentences)
#         # print('demolitions',demolitions)
#         # print('erections',erections)
#         # print('*'*100)
