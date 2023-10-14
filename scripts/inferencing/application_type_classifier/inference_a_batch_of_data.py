import openai

from scripts.inferencing.application_type_classifier.process_GPT_inference import process_one_data_point_GPT_output




def inference_a_batch_of_planning_notes_by_GPT(planning_notes: list,
                                               GPT_finetuned_model_name: str,
                                               max_tokens: int = 1000):

    '''
    Given a batch of planning notes, generate a list outputs.
    :param planning_notes: a batch of planning notes. The length should be no longer than 20.
    :param GPT_finetuned_model_name: the name of finetuned GPT model.
    :param max_tokens: the max num of tokens to be generated.
    :return 4 lists - demolitions (list of lists), erections (list of lists), app_types, changes_of_use
    '''


    #############################################################################################
    ## The output is s list of a list of json, e.g.,
    '''
        [<OpenAIObject at 0x7f708dfdb590> JSON: {
       "finish_reason": "stop",
       "index": 0,
       "logprobs": null,
       "text": "Demolitions: , Erections: , Type: Advertisement Consent, Change of Use: "
       },
     <OpenAIObject at 0x7f708d38e7c0> JSON: {
       "finish_reason": "stop",
       "index": 1,
       "logprobs": null,
       "text": "Demolitions: , Erections: , Type: Advertisement Consent, Change of Use: "
     }]
    '''
    #############################################################################################
    outputs = openai.Completion.create(
        model=GPT_finetuned_model_name,
        prompt=planning_notes,
        stop=' END',
        max_tokens=max_tokens)['choices']

    demolitions = []
    erections = []
    app_types = []
    changes_of_use = []

    for output in outputs:
        demolition, erection, app_type, change_of_use = process_one_data_point_GPT_output(output['text'])
        demolitions.append(str(demolition))
        erections.append(str(erection))
        app_types.append(app_type)
        changes_of_use.append(change_of_use)


    return demolitions, erections, app_types, changes_of_use








