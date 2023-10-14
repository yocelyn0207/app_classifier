import re


from scripts.preprocessing.application_type_classifier.type_set import *
from scripts.preprocessing.use_class_classifier.keywords import use_classes_set

def process_one_data_point_GPT_output(one_data_point_output_from_GPT:str):
    '''
    Given a str output for a planning note, e.g., 'Demolitions: a1, c3, Erections: , Type: Permission in Principle, Change of use: Y',
    Split the output into 4 parts,
       a. demolitions: a list of all demolitions, e.g., ['a1', 'c3']
       b. erections: a list of all erections, e.g., []
       c. type: a str of type name, e.g., 'Permission in Principle'
       d. change of use: a str, e.g., 'Y'
    :param one_data_point_output_from_GPT: a str output for one planning note.
    :return demolitions: a list of all demolitions, e.g., ['a1', 'c3']
    :return erections: a list of all erections, e.g., []
    :return type: a str of type name, e.g., 'Permission in Principle'
    :return change of use: a str of 'Y' or '', e.g., 'Y'
    '''


    output_split = re.split("Demolitions: |, Erections: |, Type: |, Change of Use: ", one_data_point_output_from_GPT, flags=re.IGNORECASE)
    demolitions = []
    erections = []

    if len(output_split) >= 5:
        demolition_str = output_split[1]
        if demolition_str != '':
            demolitions_draft = demolition_str.split(', ')
            for i in demolitions_draft:
                if i in use_classes_set:
                    demolitions.append(i)

        erection_str = output_split[2]
        if erection_str != '':
            erections_draft = erection_str.split(', ')
            for i in erections_draft:
                if i in use_classes_set:
                    erections.append(i)

        if output_split[3] in types_set:
            app_type = output_split[3]
        else:
            app_type = 'Other'


        change_of_use = output_split[4]
        if change_of_use not in {'Y', 'y', ''}:
            change_of_use = ''
    else:
        try:
            demolitions_draft = re.findall("Demolitions(.+)Erections", one_data_point_output_from_GPT, flags=re.IGNORECASE)[0].split(',')
            for demolition in demolitions_draft:
                demolition = re.sub(r'[\W_]', '', demolition)
                if demolition == 'suigeneris':
                    demolition = 'sui generis'
                if demolition in use_classes_set:
                    demolitions.append(demolition)
        except:
            pass

        try:
            erections_draft = re.findall("Erections(.+)Type", one_data_point_output_from_GPT, flags=re.IGNORECASE)[0].split(',')
            erections = []
            for erection in erections_draft:
                erection = re.sub(r'[\W_]', '', erection)
                if erection == 'suigeneris':
                    erection = 'sui generis'
                if erection in use_classes_set:
                    erections.append(erection)
        except:
            pass

        try:
            type_matches = re.split('[,.#:!@$%^&*]', re.findall("Type:(.+)Change", one_data_point_output_from_GPT, flags=re.IGNORECASE)[0])
            app_type = ''
            for type_match in type_matches:
                type_match = type_match.lstrip().strip()
                if type_match in types_set:
                    app_type = type_match
                    break
        except:
            app_type = 'Other'

        try:
            change_of_use_matches = re.split('[,.#:!@$%^&*]', re.findall("Change of Use:(.+)", one_data_point_output_from_GPT, flags=re.IGNORECASE)[0])
            change_of_use = ''
            for change_of_use_match in change_of_use_matches:
                change_of_use_match = change_of_use_match.strip()
                if change_of_use_match in {'Y', 'y'}:
                    change_of_use = 'Y'
                    break
        except:
            change_of_use = ''


    return demolitions, erections, app_type, change_of_use