import numpy as np
import pandas as pd

def process_input(input_planning_note_list: list = None,
                  input_planning_note_file: str = None,
                  lineterminator_of_input_file: str = '\n'):

    '''
    Return a Dataframe which contains columns of 'reference', 'planning_note', 'type_from_councils',
    'label_of_demolition','label_of_erection', 'label_of_type_from_text', 'label_of_change_of_use'.
    '''

    if input_planning_note_list is not None and input_planning_note_file is not None:
        raise ValueError('Please do NOT pass input_planning_note_list and input_planning_note_file at the same time.')
    elif input_planning_note_list is None and input_planning_note_file is None:
        raise ValueError('Please pass input_planning_note_list OR input_planning_note_file.')
    elif input_planning_note_list is not None and input_planning_note_file is None:
        if type(input_planning_note_list[0]) is dict:
            df = pd.DataFrame(input_planning_note_list, dtype=str)
        else:
            df = pd.DataFrame({'planning_note': input_planning_note_list}, dtype=str)
    else:
        df = pd.read_csv(input_planning_note_file, dtype=str, lineterminator=lineterminator_of_input_file)


    df_column_names = ['reference', 'planning_note', 'type_from_councils','label_of_demolition','label_of_erection',
                       'label_of_type_from_text', 'label_of_change_of_use']
    potential_column_names_reference = ['Planning Reference', 'Planning References',
                                        'planning reference', 'planning references',
                                        'Reference','References','reference','references']
    potential_column_names_planning_note = ['Planning Note','Planning Notes',
                                             'planning note','planning notes',
                                             'Planning_Note','Planning_Notes',
                                             'planning_note','planning_notes',

                                             'Planning Application', 'Planning Applications',
                                             'planning application', 'planning applications',
                                             'Planning_Application', 'Planning_Applications',
                                             'planning_application', 'planning_spplications',
                                             ]
    potential_column_names_type_from_councils = ['Type', 'Types', 'type','types']
    potential_column_names_label_of_demolition = ['Demolition', 'Demolitions', 'demolition', 'demolitions']
    potential_column_names_label_of_erection = ['Erection', 'Erections', 'erection', 'erections']
    potential_column_names_label_of_type_new = ['Type New', 'Type_New', 'type new', 'type_new']
    potential_column_names_label_of_change_of_use = ['Change of Use', 'Change_of_Use', 'change of use', 'change_of_use']


    for p in potential_column_names_reference:
        try:
            df = df.rename(columns={p: "reference"})
        except:
            continue

    for p in potential_column_names_planning_note:
        try:
            df = df.rename(columns={p: "planning_note"})
        except:
            continue

    for p in potential_column_names_type_from_councils:
        try:
            df = df.rename(columns={p: "type_from_councils"})
        except:
            continue

    for p in potential_column_names_label_of_demolition:
        try:
            df = df.rename(columns={p: "label_of_demolition"})
        except:
            continue

    for p in potential_column_names_label_of_erection:
        try:
            df = df.rename(columns={p: "label_of_erection"})
        except:
            continue

    for p in potential_column_names_label_of_type_new:
        try:
            df = df.rename(columns={p: "label_of_type_from_text"})
        except:
            continue


    for p in potential_column_names_label_of_change_of_use:
        try:
            df = df.rename(columns={p: "label_of_change_of_use"})
        except:
            continue

    current_columns = set(df.columns)

    if "planning_note" not in current_columns:
        raise ValueError("The input file must contain a column of planning_note.")

    for column_name in df_column_names:
        if column_name not in current_columns:
            df[column_name] = np.nan

    df.planning_note = df.planning_note.fillna('')
    df.label_of_demolition = df.label_of_demolition.fillna('[]')
    df.label_of_erection = df.label_of_erection.fillna('[]')
    df.label_of_change_of_use = df.label_of_change_of_use.fillna('')

    return df