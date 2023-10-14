import re

from scripts.preprocessing.change_of_use.split_planning_note_into_demolition_and_erection import split_planning_note_into_demolition_and_erection


def _change_of_use_classifier(row, pattern_change_of_use):
    change_of_use = ''
    demolition, erection = split_planning_note_into_demolition_and_erection(row.planning_notes)
    if (row.change_of_use == 'Y' or
        re.search(pattern_change_of_use, row.planning_notes, flags=re.IGNORECASE) is not None or
        (demolition != '' and erection != '')) and \
            (row.demolitions != '[]' or row.erections != '[]'):
        change_of_use = 'Y'
    return change_of_use




def clean_data_by_keywords(row, **kwargs):
    type_new = ''
    change_of_use = ''

    # Consultation
    if re.search(kwargs['pattern_consultation'], row.planning_notes,flags=re.IGNORECASE) is not None and \
            row.type_list_mapping != 'Tree Preservation Order/Hedgerow Removal' and \
            row.type_list_mapping != 'Tree Preservation Order' and \
            row.type_list_mapping != 'Hedgerow Removal':
        type_new = 'Consultation'

    # Other
    elif row.planning_notes in kwargs['non'] or re.search(kwargs['pattern_other'], row.planning_notes,flags=re.IGNORECASE) is not None:
        type_new = 'Other'

    else:
        ############################################### Group 1 ###############################################

        # Section 73
        if row.type_list_mapping == 'Section 73':
            if re.search(kwargs['pattern_73'], row.planning_notes,flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'


        # Section 106
        elif row.type_list_mapping == 'Section 106':
            if re.search(kwargs['pattern_106'], row.planning_notes,flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'


        # Extension of Time Application
        elif row.type_list_mapping == 'Extension of Time Application':
            if re.search(kwargs['pattern_extension'], row.planning_notes,flags=re.IGNORECASE) is not None:
                if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 73'
                elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 106'
                else:
                    type_new = 'Extension of Time Application'


        # Discharge Of Conditions
        elif row.type_list_mapping == 'Discharge Of Conditions':
            if re.search(kwargs['pattern_discharge'], row.planning_notes,flags=re.IGNORECASE) is not None:
                if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 73'
                elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 106'
                else:
                    type_new = 'Discharge Of Conditions'


        # Variation/Removal of Conditions
        elif row.type_list_mapping == 'Variation/Removal of Conditions':
            if re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes,flags=re.IGNORECASE) is not None:
                if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 73'
                elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 106'
                elif re.search(kwargs['pattern_discharge_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Discharge Of Conditions'
                else:
                    type_new = 'Variation/Removal of Conditions'


        # Compliance with/Approval of/Details Pursuant to Conditions
        elif row.type_list_mapping == 'Compliance with/Approval of/Details Pursuant to Conditions':
            if re.search(kwargs['pattern_details'], row.planning_notes,flags=re.IGNORECASE) is not None:
                if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 73'
                elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 106'
                elif re.search(kwargs['pattern_discharge_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Discharge Of Conditions'
                else:
                    type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'


        # Non Material Amendments
        # 1. If the sentence doesn't has 'Non Material Amendments' keywords but has 'Minor Amendments' keywords,
        # then is labeled as 'Minor Amendments'. 'Minor Amendments' is more general which includes any amendments
        # that cannot be classified as 'Non Material Amendments'.
        elif row.type_list_mapping == 'Non Material Amendments':
            if re.search(kwargs['pattern_non_material'], row.planning_notes,flags=re.IGNORECASE) is not None:
                if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 73'
                elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Section 106'
                else:
                    type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes,flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'


        # Minor Amendments
        # 1. If the sentence doesn't has 'Non Material Amendments' keywords but has 'Minor Amendments' keywords,
        # then is labeled as 'Minor Amendments'. 'Minor Amendments' is more general which includes any amendments
        # that cannot be classified as 'Non Material Amendments'.
        elif row.type_list_mapping == 'Minor Amendments':
            if re.search(kwargs['pattern_73'], row.planning_notes,flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes,flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes,flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes,flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'



        ############################################### Group 2 ###############################################

        # Prior Notification
        elif row.type_list_mapping == 'Prior Notification':
            if re.search(kwargs['pattern_prior_notification'], row.planning_notes,flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Permitted Development
        elif row.type_list_mapping == 'Permitted Development':
            if re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Reserved Matters
        elif row.type_list_mapping == 'Reserved Matters':
            if re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'


        # Certificate of Lawfulness for Proposed or Existing Use
        elif row.type_list_mapping == 'Certificate of Lawfulness for Proposed or Existing Use':
            if re.search(kwargs['pattern_lawfulness'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Certificate of Lawfulness for Proposed or Existing Use'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Screening/Scoping/EIA
        # Should be careful when using keywords of this type to filter other types of apps! 'Screening'
        # can have other usage.
        elif row.type_list_mapping == 'Screening/Scoping/EIA':
            if re.search(kwargs['pattern_extension'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Extension of Time Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Permission in Principle
        elif row.type_list_mapping == 'Permission in Principle':
            if re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Technical Details Consent
        elif row.type_list_mapping == 'Technical Details Consent':
            if re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # County Matters Application
        elif row.type_list_mapping == 'County Matters Application':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_extension'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Extension of Time Application'
            elif re.search(kwargs['pattern_discharge_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Discharge Of Conditions'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_county']+'|schools?(?!\w)|classrooms?(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Councils Own Application (Reg3/Reg4)
        # If the sentence has keywords of 'Non Material Amendments' or 'Minor Amendments', should NOT be labeled
        # as 'Councils Own Application (Reg3/Reg4)'.
        # !! The rule may need revision. There are possibilities that Non Material Amendments is a sub-related
        # type, e.g., 'Council development of lrjogherh 07/2017/0211/ (Non Material Amendments)'? !!
        elif row.type_list_mapping == 'Councils Own Application (Reg3/Reg4)':
            if re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                if re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Non Material Amendments'
                elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Minor Amendments'
                else:
                    type_new = 'Councils Own Application (Reg3/Reg4)'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Neighbouring Authority Application
        elif row.type_list_mapping == 'Neighbouring Authority Application':
            if re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                if re.search(kwargs['pattern_consultation'], row.planning_notes, flags=re.IGNORECASE) is not None:
                    type_new = 'Consultation'
                else:
                    type_new = 'Neighbouring Authority Application'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])



        ############################################### Group 3 ###############################################

        # Householder Application
        elif row.type_list_mapping == 'Householder Application':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_discharge_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Discharge Of Conditions'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_listed_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Listed Building Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_conservation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Conservation Area'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            else:
                type_new = 'Householder Application'




        # Advertisement Consent
        elif row.type_list_mapping == 'Advertisement Consent':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            else:
                type_new = 'Advertisement Consent'


        # Tree Preservation Order
        elif row.type_list_mapping == 'Tree Preservation Order':
            type_new = 'Tree Preservation Order/Hedgerow Removal'


        # Hedgerow Removal
        elif row.type_list_mapping == 'Hedgerow Removal':
            if re.search(kwargs['pattern_hedgerow'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Tree Preservation Order/Hedgerow Removal'


        # Listed Building Application
        elif row.type_list_mapping == 'Listed Building Application':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_listed'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Listed Building Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Conservation Area
        elif row.type_list_mapping == 'Conservation Area':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_conservation'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Conservation Area'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Hybrid Application
        elif row.type_list_mapping == 'Hybrid Application':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            # elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
            #     row_new = [row.reference,row.planning_notes, row.type, row.type_list_mapping, 'Reserved Matters']
            #     df_new_writer.writerow(row_new)
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_hybrid'], row.planning_notes, flags=re.IGNORECASE) is not None or \
            (re.search('(?<!\w)full(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None and
             re.search('(?<!\w)outline(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None):
                type_new = 'Hybrid Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Outline Application
        elif row.type_list_mapping == 'Outline Application':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            # elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
            #     row_new = [row.reference,row.planning_notes, row.type, row.type_list_mapping, 'Reserved Matters']
            #     df_new_writer.writerow(row_new)
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_hybrid'], row.planning_notes, flags=re.IGNORECASE) is not None or \
            (re.search('(?<!\w)full(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None and
             re.search('(?<!\w)outline(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None):
                type_new = 'Hybrid Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_outline'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Outline Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Full Application
        elif row.type_list_mapping == 'Full Application':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_hybrid'], row.planning_notes, flags=re.IGNORECASE) is not None or \
            (re.search('(?<!\w)full(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None and
             re.search('(?<!\w)outline(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None):
                type_new = 'Hybrid Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_outline'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Outline Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            else:
                type_new = 'Full Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                # if re.search(kwargs['pattern_full'], row.planning_notes, flags=re.IGNORECASE) is not None:
                #     type_new = 'Full Application'
                #     change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                # else:
                #     demolition, erection = split_planning_note_into_demolition_and_erection(row.planning_notes)
                #     # if re.search(kwargs['pattern_telecom'], erection, flags=re.IGNORECASE) is not None:
                #     #     type_new = 'Telecommunications/Overhead Electricity Lines'
                #     #     change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                #     if re.search(kwargs['pattern_mineral'], erection, flags=re.IGNORECASE) is not None:
                #         type_new = 'Minerals Application'
                #         change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                #     elif re.search(kwargs['pattern_waste'], erection, flags=re.IGNORECASE) is not None:
                #         type_new = 'Waste Management Application'
                #         change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                #     elif re.search(kwargs['pattern_hazardous'], erection, flags=re.IGNORECASE) is not None:
                #         type_new = 'Hazardous Substances Consent Application'
                #         change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                #     elif re.search(kwargs['pattern_agricultural'], erection, flags=re.IGNORECASE) is not None:
                #         type_new = 'Agricultural Development'
                #         change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                #     else:
                #         type_new = 'Full Application'
                #         change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Telecommunications/Overhead Electricity Lines
        elif row.type_list_mapping == 'Telecommunications/Overhead Electricity Lines':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_hybrid'], row.planning_notes, flags=re.IGNORECASE) is not None or \
                    (re.search('(?<!\w)full(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None and
                    re.search('(?<!\w)outline(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None):
                type_new = 'Hybrid Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_outline'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Outline Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_full'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Full Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_telecom'], row.planning_notes, flags=re.IGNORECASE) is not None:
                demolition, erection = split_planning_note_into_demolition_and_erection(row.planning_notes)
                if re.search(kwargs['pattern_telecom'], erection, flags=re.IGNORECASE) is not None:
                    type_new = 'Telecommunications/Overhead Electricity Lines'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                else:
                    type_new = 'Full Application'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Minerals Application
        elif row.type_list_mapping == 'Minerals Application':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_hybrid'], row.planning_notes, flags=re.IGNORECASE) is not None or \
                    (re.search('(?<!\w)full(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None and
                    re.search('(?<!\w)outline(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None):
                type_new = 'Hybrid Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_outline'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Outline Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_full'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Full Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_mineral'], row.planning_notes, flags=re.IGNORECASE) is not None:
                demolition, erection = split_planning_note_into_demolition_and_erection(row.planning_notes)
                if re.search(kwargs['pattern_mineral'], erection, flags=re.IGNORECASE) is not None:
                    type_new = 'Minerals Application'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                else:
                    type_new = 'Full Application'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])

        # Waste Management Application
        elif row.type_list_mapping == 'Waste Management Application':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_hybrid'], row.planning_notes, flags=re.IGNORECASE) is not None or \
                    (re.search('(?<!\w)full(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None and
                     re.search('(?<!\w)outline(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None):
                type_new = 'Hybrid Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_outline'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Outline Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_full'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Full Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_waste'], row.planning_notes, flags=re.IGNORECASE) is not None:
                demolition, erection = split_planning_note_into_demolition_and_erection(row.planning_notes)
                if re.search(kwargs['pattern_waste'], erection, flags=re.IGNORECASE) is not None:
                    type_new = 'Waste Management Application'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                else:
                    type_new = 'Full Application'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])


        # Hazardous Substances Consent Application
        elif row.type_list_mapping == 'Hazardous Substances Consent Application':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new =  'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_hybrid'], row.planning_notes, flags=re.IGNORECASE) is not None or \
                    (re.search('(?<!\w)full(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None and
                     re.search('(?<!\w)outline(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None):
                type_new = 'Hybrid Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_outline'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Outline Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_full'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Full Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_hazardous'], row.planning_notes, flags=re.IGNORECASE) is not None:
                demolition, erection = split_planning_note_into_demolition_and_erection(row.planning_notes)
                if re.search(kwargs['pattern_hazardous'], erection, flags=re.IGNORECASE) is not None:
                    type_new = 'Hazardous Substances Consent Application'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                else:
                    type_new = 'Full Application'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])

        # Agricultural Development
        elif row.type_list_mapping == 'Agricultural Development':
            if re.search(kwargs['pattern_73'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 73'
            elif re.search(kwargs['pattern_106'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Section 106'
            elif re.search(kwargs['pattern_variation_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Variation/Removal of Conditions'
            elif re.search(kwargs['pattern_details_for_the_other_types'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Compliance with/Approval of/Details Pursuant to Conditions'
            elif re.search(kwargs['pattern_non_material'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Non Material Amendments'
            elif re.search(kwargs['pattern_minor_amendments'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Minor Amendments'
            elif re.search(kwargs['pattern_prior_notification'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Prior Notification'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_permitted'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permitted Development'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_reserved'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Reserved Matters'
            elif re.search(kwargs['pattern_screening'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Screening/Scoping/EIA'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_principle'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Permission in Principle'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_technical_details'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Technical Details Consent'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_county'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'County Matters Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_council'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Councils Own Application (Reg3/Reg4)'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_neighbouring'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Neighbouring Authority Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_hybrid'], row.planning_notes, flags=re.IGNORECASE) is not None or \
                    (re.search('(?<!\w)full(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None and
                     re.search('(?<!\w)outline(?!\w)', row.planning_notes, flags=re.IGNORECASE) is not None):
                type_new = 'Hybrid Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_outline'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Outline Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_full'], row.planning_notes, flags=re.IGNORECASE) is not None:
                type_new = 'Full Application'
                change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
            elif re.search(kwargs['pattern_agricultural'], row.planning_notes, flags=re.IGNORECASE) is not None:
                demolition, erection = split_planning_note_into_demolition_and_erection(row.planning_notes)
                if re.search(kwargs['pattern_agricultural'], erection, flags=re.IGNORECASE) is not None:
                    type_new = 'Agricultural Development'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])
                else:
                    type_new = 'Full Application'
                    change_of_use = _change_of_use_classifier(row, kwargs['pattern_change_of_use'])

        # Other
        elif row.type_list_mapping == 'Other':
            type_new = 'Other'

    return type_new, change_of_use



