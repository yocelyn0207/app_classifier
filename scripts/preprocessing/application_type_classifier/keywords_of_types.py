non_keywords = ['nan', 'TBC', 'Not Available', 'test', 'Test application', 'TEST TEST TEST', 'TEST', 'to be checked', "0"]

Consultation_keywords = [
    '(?<!not subject to )(?<!no )(?<!after )(?<!in )(?<!public )(re ?-? ?)?consult(ation)?(?! facilit)(?! room)(?! area)(?! response)(?! support)(?! ecologist)(?! \/)(?!\/)(?!\w)',
    '(?<!balance )(?<!in response to an )(?<!phone )enquiry(?! line)',
    '(?<!balance )(?<!in response to an )(?<!phone )enquire(?! line)',
    '(?<!balance )(?<!in response to an )(?<!phone )inquiry(?! line)',
    '(?<!balance )(?<!in response to an )(?<!phone )inquire(?! line)',
    '(?<!balance )(?<!in response to an )(?<!phone )query(?! line)']

Section_73_keywords = ['(?<!/)(?<!\d)(?<!\w)s73(?!\d)', '(?<!\d)(?<!\w)s 73(?!\d)', '(?<!\d)(?<!\w)s.73(?!\d)',
                       '(?<!/)(?<!\d)(?<!\w)s73a', '(?<!\d)(?<!\w)s. 73(?!\d)',
                       'section 73(?!\d)', 'section73(?!\d)']

Section_106_keywords = ['(?<!\d)(?<!\w)s.? ?106(?!\d)a?', 'section ?106a?',
                        '106BA', 'S106BA', '106 agreement', '106 deed of agreement',
                        '106 legal agreement']

Extension_of_Time_Application_keywords = ['extension of the time', 'extension of time', 'extend the time',
                                          'extend time',
                                          'extension to the time', 'extension to time', 'extend the life',
                                          'replace extant planning', 'replace extant permission',
                                          'replace an extant planning', 'replace an extant permission',
                                          'replace the extant planning', 'replace the extant permission',
                                          'replace an extant consent', 'replace extant consent',
                                          'replace the extant consent',
                                          'replacement of planning', 'replace planning',
                                          'renewal of existing temporary planning',
                                          'renewal of extant planning', 'renewal of extant permission',
                                          'renewal of an extant planning', 'renewal of an extant permission',
                                          'renewal of the extant planning', 'renewal of the extant permission',
                                          'renewal of the time', 'renewal of time',
                                          'renew extant planning', 'renew extant permission',
                                          'renew an extant planning', 'renew an extant permission',
                                          'renew the extant planning', 'renew the extant permission',
                                          'renew the time', 'renew time',
                                          'extend implementation',
                                          'extension of extant planning', 'extension of extant permission',
                                          'replace an extant of planning', 'extend the limit for implementation',
                                          'extension to planning', 'extension of planning', 'extend the planning',
                                          'extension to permission',
                                          'extention of time', 'extention of the time',
                                          'extension of planning', 'extension of implementation period',
                                          'extent the life', 'extention of time', 'extension of life',
                                          'replace an extant of listed building consent', 'extending the time',
                                          'extending planning',
                                          'extending time', 'extension of temporary permission',
                                          'extended under', 'extended initially under',
                                          'extend [a-zA-Z0-9]+/[a-zA-Z0-9]+',
                                          'extension of [a-zA-Z0-9]+/[a-zA-Z0-9]+',
                                          'extension to commencement date',
                                          'replacement planning', 'replacement listed', 'replacement conservation',
                                          'replacement application', 'replacement permission',
                                          'variation of time limit']

Discharge_Of_Conditions_keywords = ['(?<!water )discharge (?!water)(?!surface)',
                                    '(?<!water )discharging (?!water)(?!surface)',
                                    '(?<!water )discharged (?!water)(?!surface)']
Discharge_Of_Conditions_for_the_other_types_keywords = ['discharge (of )?condition']

Variation_or_Removal_of_Conditions_keywords = ['remove condition', 'removal of condition', 'remove a condition',
                                               'removal of a condition', 'removal of condtion',
                                               'removal of conditon',
                                               'removal of an agricultural occupancy condition',
                                               'removal of agricultural occupancy condition',
                                               'remove holiday let condition',

                                               'variation of condition', 'variation to condition', 'vary condition',
                                               'variation of wording', 'variation on condition',
                                               'variation of legal agreement',
                                               'variation of a condition', 'variation of the wording to condition',
                                               'variation of conditon', 'varation of condition',
                                               'vartiaition of condition',
                                               'variation of details of conditions',
                                               'variation to the wording of condition',
                                               'variation of a condition', 'variation to of condition',
                                               'variation of planning permission',
                                               'variation to planning permission',
                                               'variations to condition', 'variation for condition',
                                               'variaition to condition',
                                               'variation of condtion', 'variationl of condition',
                                               'variation of: condition',
                                               'variations to design, height and external appearance pursuant to planning permission',
                                               'vary/remove condition', 'variation of part of condition',
                                               'variation of planning condition', 'variation/deletion of condition',
                                               'variation of legal agreement on application',
                                               'variation of the approved plans',
                                               'variation of approved plans condition', 'variation of conidition',
                                               'varitation of condition', 'variaton of condition',
                                               'variation of plans list condition',
                                               'variation of planning application',
                                               "variation of 'hours of operation' \(opening hours\) of condition",
                                               'variaton of condition',
                                               'variation of standard condition',
                                               'variation of approved application',
                                               'variation of agricultural occupancy condition',
                                               'variations of condition', 'deed of variation',
                                               'variation of details', 'conditions\(s\) variation',
                                               'vary construction working hours', 'variation of the planning',
                                               'variation of \d+', 'vary or remove condition',
                                               'variation (or removal) of condition',
                                               'variation of the Section', 'variation of permission',
                                               'variation of [\w\d]+/[\w\d]+', 'variation to [\w\d]+/[\w\d]+',
                                               'variation of standard time condition',
                                               'variation to wording', 'variation condition',
                                               'vary/remove condition', 'to vary condition',
                                               'amend condition', 'amendment to condition',
                                               'amendment of condition',
                                               'modification of planning', 'modification of condition',
                                               'modifications of planning', 'modifications of condition',
                                               'deletion of condition', 'delete consition',
                                               'modification of condition',
                                               'clear condition', 'clearing condition',
                                               'relaxation of condition', 'variation to agreement',
                                               'modification of legal agreement',
                                               'discharge Schedule 3 requirement',

                                               'modify obligation', 'vary the tenure mix of planning obligation',
                                               'variation of obligation', 'modify the original planning obligation',
                                               'variation of planning', 'modification of obligation',

                                               'hour', 'hr']


Variation_or_Removal_of_Conditions_for_the_other_types_keywords = ['remove condition', 'removal of condition', 'remove a condition',
                                               'removal of a condition', 'removal of condtion',
                                               'removal of conditon',
                                               'removal of an agricultural occupancy condition',
                                               'removal of agricultural occupancy condition',
                                               'remove holiday let condition',

                                               'variation of condition', 'variation to condition', 'vary condition',
                                               'variation of wording', 'variation on condition',
                                               'variation of legal agreement',
                                               'variation of a condition', 'variation of the wording to condition',
                                               'variation of conditon', 'varation of condition',
                                               'vartiaition of condition',
                                               'variation of details of conditions',
                                               'variation to the wording of condition',
                                               'variation of a condition', 'variation to of condition',
                                               'variation of planning permission',
                                               'variation to planning permission',
                                               'variations to condition', 'variation for condition',
                                               'variaition to condition',
                                               'variation of condtion', 'variationl of condition',
                                               'variation of: condition',
                                               'variations to design, height and external appearance pursuant to planning permission',
                                               'vary/remove condition', 'variation of part of condition',
                                               'variation of planning condition', 'variation/deletion of condition',
                                               'variation of legal agreement on application',
                                               'variation of the approved plans',
                                               'variation of approved plans condition', 'variation of conidition',
                                               'varitation of condition', 'variaton of condition',
                                               'variation of plans list condition',
                                               'variation of planning application',
                                               "variation of 'hours of operation' \(opening hours\) of condition",
                                               'variaton of condition',
                                               'variation of standard condition',
                                               'variation of approved application',
                                               'variation of agricultural occupancy condition',
                                               'variations of condition', 'deed of variation',
                                               'variation of details', 'conditions\(s\) variation',
                                               'vary construction working hours', 'variation of the planning',
                                               'variation of \d+', 'vary or remove condition',
                                               'variation (or removal) of condition',
                                               'variation of the Section', 'variation of permission',
                                               'variation of [\w\d]+/[\w\d]+', 'variation to [\w\d]+/[\w\d]+',
                                               'variation of standard time condition',
                                               'variation to wording', 'variation condition',
                                               'vary/remove condition', 'to vary condition',
                                               'amend condition', 'amendment to condition',
                                               'amendment of condition',
                                               'modification of planning', 'modification of condition',
                                               'modifications of planning', 'modifications of condition',
                                               'deletion of condition', 'delete consition',
                                               'modification of condition',
                                               'clear condition', 'clearing condition',
                                               'relaxation of condition', 'variation to agreement',
                                               'modification of legal agreement',
                                               'discharge Schedule 3 requirement',

                                               'modify obligation', 'vary the tenure mix of planning obligation',
                                               'variation of obligation', 'modify the original planning obligation',
                                               'variation of planning', 'modification of obligation']

Approval_of_Details_Pursuant_to_Conditions_keywords = ['detailed drawing', 'pursuant to condition',
                                                       'pursuant scheme to condition',
                                                       'pursuant to requirement',
                                                       'compliance of condition', 'compliance with condition',
                                                       'compliance to condition',
                                                       'compliance of all condition',
                                                       'compliance with all condition',
                                                       'compliance to all condition',
                                                       'compliance of planning', 'compliance with planning',
                                                       'compliance to planning',
                                                       'compliance with conditon', 'compliance of conditon',
                                                       'compliance to conditon',
                                                       'compliance with part', 'compliance of part',
                                                       'compliance to part',
                                                       'compliance with occupancy condition',
                                                       'compliance of occupancy condition',
                                                       'compliance to occupancy condition',
                                                       'compliance wth condition', 'compliance with condtion',
                                                       'approval, compliance', 'approval of condition',
                                                       'compliance check',
                                                       'details of condition', 'details for condition',
                                                       'pursuant to schedule', 'complied with',
                                                       'detail', 'detaill']

Approval_of_Details_Pursuant_to_Conditions_for_the_other_types_keywords = ['pursuant to condition',
                                                       'pursuant scheme to condition',
                                                       'pursuant to requirement',
                                                       'compliance of condition', 'compliance with condition',
                                                       'compliance to condition',
                                                       'compliance of all condition',
                                                       'compliance with all condition',
                                                       'compliance to all condition',
                                                       'compliance of planning', 'compliance with planning',
                                                       'compliance to planning',
                                                       'compliance with conditon', 'compliance of conditon',
                                                       'compliance to conditon',
                                                       'compliance with part', 'compliance of part',
                                                       'compliance to part',
                                                       'compliance with occupancy condition',
                                                       'compliance of occupancy condition',
                                                       'compliance to occupancy condition',
                                                       'compliance wth condition', 'compliance with condtion',
                                                       'approval, compliance', 'approval of condition',
                                                       'compliance check',
                                                       'details of condition', 'details for condition',
                                                       'pursuant to schedule', 'complied with']


Non_Material_Amendments_keywords = ['non(\s+|\s*(\-)\s*)(material|materail|marterial|matieral)',
                                    'non(\s+|\s*(\-)\s*)minor',
                                    'NMA']

# to/of ** scheme/application/planning/approval/consent/0293
Minor_Amendments_keywords = [
    '(?<!non )(?<!non-)(minor|small) (material )?(amendments?|changes?|alterations?) (to|of) (((?! to )(\w|\s))*(scheme|application|planning application|planning permission|approval|consent)|\d+)',
    'amendments? (to|of) (((?! to )(\w|\s))*(scheme|application|planning application|planning permission|approval|consent)|\d+)']

Prior_Notification_keywords = ['prior notification', 'prior notificiation', 'prior norification',
                               'prior notificate', 'prior notificaiton', 'prior agricultural notification',
                               'prior argicultural notification', 'prior notication',
                               'prior forestry notification', 'prior notifciation', 'prior notfication',
                               '\d+prior notification', 'Prior Noification',
                               'notification of prior',
                               'prior submission', 'prior noificiation', 'prior notificaton',
                               'prior notifiction', 'prior agricultural application']

Permitted_Development_keywords = ['prior approval', 'prior appoval', 'prior-approval', 'prior approval',
                                  'prior aproval',
                                  'permitted development', 'permitted devlopment',
                                  'permitted developmant', 'permitted devlopment',
                                  'permitted agricultural development', 'permitted notification',
                                  'permitted decvelopment', 'permitted use',
                                  'prior written consent', 'prior detm', 'prior determination']

Reserved_Matters_keywords = ['reserved matter', 'matters reserved', 'matter reserved', 'matters as reserved',
                             'reserve matter', 'matters to be considered', 'matter to be considered',
                             'matters considered', 'matter considered', 'reserrved matter',
                             'reserves matter', 'reserved, matter', '\d+reserved matter', 'reseved matter',
                             'resevered matter', 'reversed matter', 'matters/details reserved',
                             'matters of appearance and landscaping reserved', 'all matters \(.+\) reserved',
                             'resereved matter', 'reseserved matter', 'matters previously reserved',
                             'reservedmatter', 'matters of detail to be considered']

Certificate_of_Lawfulness_for_Proposed_or_Existing_Use_keywords = ['law', 'lawful', 'lawfull', 'lawfulness',
                                                                   'lawfullness', 'lawfuness', '191', '192', 's191',
                                                                   's192']

Screening_Scoping_EIA_keywords = ['(?<!\Wsoli )(?<!\Wsoil )screening(?! bunds)(?! bund)', 'scoping', 'screeing',
                                  'EIA', 'AEA', 'environmental', 'environment']

Permission_in_Principle_keywords = ['in principle', 'in principal', 'establish the principle']

Technical_Details_Consent_keywords = ['technical detail', 'pursuant to permission in principle']

County_Matters_Application_keywords = ['county']

Councils_Own_Application_keywords = ['council development', 'regulation 3', 'regulation 4', 'regulation3',
                                     'regulation4',
                                     'reg 3', 'reg 4', 'reg3', 'reg4']

Neighbouring_Authority_Application_keywords = ['neighbouring authority', 'neighbour authority',
                                               'adjoining authority',
                                               'adjoin authority', 'adjacent authority',

                                               'neighbouring consultation',
                                               'neighbour consultation', 'adjoining consultation',
                                               'adjoin consultation', 'adjacent consultation',

                                               'neighbouring borough', 'neighbour borough',
                                               'adjoining borough',
                                               'adjoin borough', 'adjacent borough',

                                               'neighbouring area consultation', 'adjoining county consultation',
                                               'neighbouring local authority'


                                               'adjoining authoruty', 'adjoininng authority',
                                               'adjacent aulthority', 'adjacent authoirty',
                                               'adjoining auhtotiy', 'adjacent auhtoirty',
                                               'ADJOING AUTHORITY', 'ADJACENT AITHORITY',
                                               'Adjoining Authrotiy', 'Adjoinig Authority', 'Adjacent Athority',
                                               'Adjoining Authoity', 'Adjoining Authourity', 'Adjacent Authoritry',
                                               'ADJACENT AUTHROITY', 'ADJACENT AUTHOIRITY', 'ADJOINING AUHTORIY']

Hybrid_Application_keywords = ['hybrid']

Outline_Application_keywords = ['outline']

Full_Application_keywords = ['full application', 'full planning']

Hedgerow_Removal_keywords = ['hedge', 'hedgerow', 'hederow', 'hedgrow', 'hedrow', 'hegderow',
                             'hedging', 'hedgreow', 'fence', 'tree', 'fell', 'felling', 'oak']

Telecommunications_and_Overhead_Electricity_Lines_keywords = ['overhead', 'over head', 'substation', 'conductor',
                                                              'sub-station', 'powerline', 'electric', 'exzarthwire',
                                                              'transformer', 'wire', 'microsubstation',
                                                              'electricity',
                                                              'staywire', 'line', 'switchgear', 'pylon', 'cable',
                                                              '\d+kv',
                                                              'electronic', 'broadband', 'BT', 'telecommunication',
                                                              '5G', '4G', '3G', '2G', 'antenna', 'telecom',
                                                              'telecomm',
                                                              'DSLAM', 'SAMO', 'PCP cabinet', 'Vodafone',
                                                              'antennae', 'airwave', 'VMFB2', 'payphone', 'VMSD1i',
                                                              'telecommunicatin', 'telecommuincation',
                                                              'telecommuication', 'telecommuniction',
                                                              'WiFi', 'call box', 'radio base station',
                                                              'pole', 'monopole', 'streetpole', 'mast',
                                                              'transmission', 'electrical', 'phone', 'network',
                                                              'communication', 'telephone', 'Huawei',
                                                              'base station', 'power generator',
                                                              'cabinet, box, pillar, pedestal',
                                                              'street cabinet', 'dish']
Telecommunications_and_Overhead_Electricity_Lines_for_the_other_types_keywords = ['overhead line', 'over head line',
                                                              'substation', 'conductor',
                                                              'sub-station', 'powerline', 'exzarthwire',
                                                              'transformer', 'microsubstation',
                                                              'staywire', 'switchgear', 'pylon', 'cable',
                                                              'kv',
                                                              'telecommunication',
                                                              '5G', '4G', '3G', '2G', 'antenna', 'telecom',
                                                              'telecomm',
                                                              'DSLAM', 'SAMO', 'PCP cabinet', 'Vodafone','BT',
                                                              'antennae', 'airwave', 'VMFB2', 'payphone', 'VMSD1i',
                                                              'telecommunicatin', 'telecommuincation',
                                                              'telecommuication', 'telecommuniction',
                                                              'call box', 'radio base station',
                                                              'streetpole', 'mast',
                                                              'transmission',
                                                              'Huawei',
                                                              'base station', 'power generator',
                                                              'cabinet, box, pillar, pedestal',
                                                              'street cabinet']



Minerals_Application_keywords = ['gravel', 'quarry', 'quarrying', 'mineral', 'borehole', 'limestone',
                                 'shale', 'coal', 'slate', 'well', 'crystal', 'asphalt', 'mine', 'mining', 'stone',
                                 'ferrous',
                                 'metal', 'hoggin', 'stockpiling of sand', 'sand stockpile', 'sand extraction',
                                 'sandstone', 'CHP', 'peat', 'roadstone', 'carbonate', 'colliery',
                                 'quartz', 'dolerite',

                                 'haulroad', 'haul raod', 'silo',

                                 'sand','earthwork','steel','HGV','leachate','inert','clay','methane','tonne','soil']

Minerals_Application_keywords_for_the_other_types_keywords = ['gravel', 'quarry', 'quarrying', 'mineral', 'borehole', 'limestone',
                                 'shale', 'coal', 'slate(?! house)(?! bungalow)', 'crystal', 'asphalt',
                                 'mine', 'mining(?! information)(?! risk)', 'ferrous',
                                 'hoggin', 'stockpiling of sand', 'sand stockpile', 'sand extraction',
                                 'sandstone', 'CHP', 'peat', 'roadstone', 'carbonate', 'colliery',
                                 'quartz', 'dolerite']


Waste_Management_Application_keywords = ['waste', 'recycling', 'recycle', 'recycled', 'sewage', 'effluent',
                                          'end of life', 'decontamination', 'drainage', 'digestate',
                                          'crematorium', 'anaerobic digestion', 'anaerobic digester', 'AD',
                                          'WwTW', 'wastewater', 'bio-solid', 'biosolid', 'ELV', 'sewerage',
                                          'biofilter', 'ecosystem', 'inert', 'biomass', 'landfill',
                                          'barrow', 'fermentation', 'biogas', 'septic', 'burial', 'cremation',
                                          'biodisc', 'disused', 'contaminated', 'contaminate', 'attenuation',
                                          're-use', 'reuse', 'underground','wetland','dewatering','dewater']
Waste_Management_Application_for_the_other_types_keywords = ['effluent',
                                          'end of life', 'decontamination', 'digestate',
                                          'crematorium', 'anaerobic digestion', 'anaerobic digester', 'AD',
                                          'WwTW', 'wastewater', 'bio-solid', 'biosolid', 'ELV', 'sewerage',
                                          'biofilter', 'ecosystem', 'inert', 'biomass', 'landfill',
                                          'cremation', 'biodisc']


Hazardous_Substances_Consent_Application_keywords = ['hazardous', 'toxic', 'dangerous',
                                                     'propane', 'hydrogen', 'acrylonitrile', 'LPG', 'methane',
                                                     'biomethane', 'chlorine', 'petroleum', 'gas', 'LNG', 'nitrate',
                                                     'propane', 'oil', 'hydrazine', 'methanol',
                                                     'flour', 'kerosene', 'pesticide', 'speciality chemical',
                                                     'flammable', 'arsine', 'phosphine',
                                                     'R50', 'R51', 'R53']
Hazardous_Substances_Consent_Application_for_the_other_types_keywords = ['hazardous', 'toxic',
                                                     'propane', 'hydrogen', 'acrylonitrile', 'LPG', 'methane',
                                                     'biomethane', 'chlorine', 'LNG', 'nitrate',
                                                     'propane', 'hydrazine', 'methanol',
                                                     'kerosene', 'pesticide', 'speciality chemical',
                                                     'flammable', 'arsine', 'phosphine',
                                                     'R50', 'R51', 'R53']



Agricultural_Development_keywords = ['agri', 'agricultural', 'agriculture', 'argicultural', 'agricultiural',
                                     'agricutural', 'argricultural', 'agricultral', 'agricultual',
                                     'barn', 'stock', 'muck', 'farm', 'farmyard', 'cattle', 'harvesting',
                                     'harvest', 'grain', 'polytunnel', 'seed', 'fertiliser', 'fertilizer',
                                     'midden', 'herd', 'pesticide', 'straw', 'cow', 'sheep', 'pen',
                                     'lambing', 'lamb', 'weaner', 'woodland', 'milking', 'poultry',
                                     'silage', 'forestry', 'forest', 'livestock', 'fodder', 'machinery',
                                     'polythene',
                                     'crop', 'animal', 'tractor', 'farming', 'slurry', 'feed', 'feeding', 'bedding',
                                     'hay',
                                     'breeding', 'breed', 'horse', 'stable', 'poly tunnel', 'membrane', 'haybarn',
                                     'grainstore', 'boggy', 'manure', 'farmwork', 'corn', 'farmland', 'calf',
                                     'potato', 'rapeseed', 'hayshed', 'log', 'sprayer', 'egg', 'plant', 'wood chip',
                                     'woodchip',
                                     'wood store', 'biomass boiler', 'biomass chip', 'logging', 'timber storage',
                                     'storage for timber', 'stack timber', 'timber drying', 'timber boarding',
                                     'timber extraction', 'processing of timber', 'timber store',
                                     'loading of felled timber',
                                     'extraction of timber', 'timber lorry', 'extract timber', 'timber shed',
                                     'seasoning of timber', 'irrigation', 'horticultural', 'food',
                                     'lagoon','bio-solid','biogas','biomass',
                                     'wetland','topsoil','hardstanding','hard standing',
                                     'timber', 'cart','pond','drying','soil',
                                     'equipment','tool','lake','wooden','greenhouse','horticultural',
                                     'reservoir','sandstone','quartz','dolerite','quarry','culvert',
                                     'tarmac','tank']
Agricultural_Development_for_the_other_types_keywords = ["(agricultural|agriculture|argicultural|agricultiural|agricutural|argricultural|agricultral|agricultual)(?! worker's dwelling)(?! dwelling)",
                                     'farm', 'farmyard', 'cattle', 'harvesting',
                                     'harvest', 'polytunnel', 'fertiliser', 'fertilizer',
                                     'midden', 'herd', 'straw', 'cow', 'sheep', 'pen',
                                     'lambing', 'lamb', 'weaner', 'woodland', 'milking', 'poultry',
                                     'silage', 'forestry', 'forest', 'livestock', 'fodder', 'machinery',
                                     'crop', 'animal', 'tractor', 'farming', 'bedding',
                                     'hay', 'breeding', 'breed', 'horse', 'stable', 'poly tunnel', 'haybarn',
                                     'grainstore',  'manure', 'farmwork', 'corn', 'farmland', 'calf',
                                     'potato', 'hayshed', 'egg',
                                     'irrigation', 'horticultural']


Listed_Building_Application_keywords = ['listed', 'listing', 'LBC', 'LB']
Listed_Building_Application_for_the_other_types_keywords = ['listed building', '(?<!\w)LBC?(?!\w)']

Conservation_Area_keywords = ['conservation']
Conservation_Area_for_the_other_types_keywords = ['conservation area']

Demolition_Application_keywords = ['demolition', 'demolish', 'demolished', 'dismantle', 'dismantling',
                                   'demoltion', 'demollition', 'demoliton', 'demoilition', 'DEMOLITION',
                                   'demolitiion',
                                   'demotlition',
                                   'removal', 'remove']
Other_keywords = ['(?<!relating to )(?<!related to )retrospective',
                  '(?<!pursuant to )withdraw', '(?<!pursuant to )withdrawn',
                  'resubmission', 'resubmit', 're-submission', 're-submit',
                  'readvertisement', 'readvertizement', 'readvertise', 'readvertize', 're-advertisement',
                  're-advertizement',
                  're-advertise', 're-advertize', 'readvertised', 'readvertized']

Change_of_Use_keywords = ['change of use', 'COS']


import random
Non_Advertisement_Consent_keywords = [f"light {random.choice(['industrial', 'industry'])}", # b1
                                      f"shop{random.choice([' ',''])}front", "ticket office","marketing unit", # a1
                                      f"{random.choice(['MUGA', 'Multi Use Games Area'])}", # d2

                                      # sui generis
                                      f'''{random.choice([f"{random.choice(['cold', 'hot'])} food", 'ice cream'])} vending {random.choice(['machine','van','vehicle'])}''',
                                      f"ATM {random.choice(['machine',''])}", "vinyl artwork", f"{random.choice(['house',''])} marketing suite","kiosk",f"{random.choice(['smoking','waiting'])} shelter",
                                      'ANPR camera',
                                      'real time information signing',
                                      'equipment and associated work',
                                      'extraction duct', 'spectator stand',
                                      f"{random.choice(['external', 'internal',''])} barrier",
                                      'metal fin', f"{random.choice(['aluminium', ''])} louvre",
                                      'temporary building', f"{random.choice(['entrance'])} portico",


                                      'street lamp','lighting column']

Advertisement_Consent_keywords = ['(^|\W)(advertisements?(( consents?)|( schemes?))?)|(adverisements?)|(advert(ising)?)|'
                    '((non(\s|-\s?)?)?illuminat((ed)|(ion))?)|(signages?)|(signs?)|'
                    '(lettering)|(letters?)|(fascias?)|(facia)|(hanging)|(headers?)|(display(ing)?)|(above)|(around)|'
                    '(logos?)|(surround)|(sizes?)|(aesthetic)|(project((ing)|(ion)|(ed)|s)?)|(boards?)|'
                    '(vinyl)|(graphics?)|(led)|(halo)|(high)|(light( strip)?)|(glaz((ing)|ed?)?)|(post((er)|(ing))?)|'
                    '(windows?)|(panels?)|(frames?)|(welcome)|(goodbye)|(mount(ed)?)|(banners?)|(backgrounds?)|(decals?)|'
                    '(backspray)|(free cash withdrawals?)|(screens?)|(brand((ing)|s)?)|(wall)|(totem)|(tablets?)|'
                    '(nameplates?)|(names?)(\W|$)']