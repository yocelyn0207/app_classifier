

use_classes = ['sui generis','a1','a2','a3','a4','a5','c1','c2','c3','c4','d1','d2']
use_classes_set = {'sui generis','a1','a2','a3','a4','a5','c1','c2','c3','c4','d1','d2'}

headword_synonyms_list_sui_generis = ['hostel','theatre','amusement arcade','amusement centre', 'funfair',
                                      'launderette','fuel station','motor vehicle','taxi business','scrap yard',
                                      'yard for the storage','yard for the distribution of mineral',
                                      'alkali','waste disposal','chemical treatment','incineration','landfill',
                                      'hazardous waste','retail warehouse club','night club','casino',
                                      'betting office', 'betting shop', 'loan shop','live music',
                                      'sailing club', 'car sale', 'car showroom', 'car racing','car hire',
                                      'vehicle sale', 'vehicle showroom','vehicle hire',
                                      'vehicle racing', 'zoo','student accommodation',
                                      'security gatehouse', 'petrol filling station','energy centre',
                                      'agriculture', 'alkali','barn','renewable electricity',
                                      'wind turbine','hydroelectric turbine', 'mobile home','caravan','camp',
                                      'glamping pod','glamping business','hmo','house in multiple occupation',
                                      'solar','dealership','cattery','kennel','boarding kennel','farm',
                                      'clock tower','cemetery','burial','poultry shed','tyre and servicing garage',
                                      'car wash','car valeting','vehicle wash','vehicle valeting',
                                      'metal recycling','metal recycle', 'mot station',
                                      'display of bulky goods','handover bay',
                                      'mot testing', 'vehicle dismantling and parts recovery',
                                      'boarding' # is processed in _generate_description
                                      ]
#                                      'solar farm','solar park'

headword_synonyms_list_a1 = ['sandwich bar','internet cafe','tea shop','sandwich shop','food outlet',
                             'retail warehouse', 'retail', 'retail accommodation','hairdress',
                             'undertaker', 'travel agency', 'retail space', 'pharmacy', 'salon', 'barber',
                             'ticket agency', 'post office', 'pet shop', 'showroom', 'domestic hire shop',
                             'dry cleaner', 'funeral director','local centre', 'shopfront','convenience store',
                             'food store','supermarket','farm shop','district centre','tea room',
                             'sales']

headword_synonyms_list_a2 = ['bank','financial and professional',
                             'money transfer','money exchange', 'currency transfer','currency exchange',
                             'passport application', 'visa application']

headword_synonyms_list_a3 = ['coffee shop','restaurant','cafe','snack bar','food and drink','food and beverage',
                             'creperie','catering']

headword_synonyms_list_a4 = ['bar','alcohol','public house','drinking establishment','cocktail bar','beer bar',
                             'karaoke bar','bistro','wine bar','family pub']

headword_synonyms_list_a5 = ['takeaway','take-away','take away']
modifier_synonyms_list_a5 = ['food', 'hot food', 'cold food', 'hot and cold food', 'cold and hot food']

headword_synonyms_list_b1 = ['office','employment', 'research and development', 'workshop',
                              'industrial', 'business', 'commercial','office accommodation',
                             'live/work','workspace']

headword_synonyms_list_b2 = ['factory','car repair', 'car body repair', 'repair of car',
                             'motor vehicle repair','repair of motor vehicle', 'microbrewery']

headword_synonyms_list_b8 = ['storage','shed', 'commercial storage', 'factory storage','warehouse','store/container',
                             'distribution','storage accommodation','depot']

headword_synonyms_list_c1 = ['hotel','guest','bed and breakfast']

headword_synonyms_list_c2 = ['hospital', 'nursing', 'offender', 'older', 'elderly',
                             'care', 'caretaker','boarding',
                             'authority',
                             'disabled', 'retirement', 'assisted',
                             'boarding school','college', 'training centre', 'prison',
                             'secure residential', 'detention', 'custody', 'holding centre',
                             'barrack', 'military']

headword_synonyms_list_c3 = ['housing', 'lodge', 'cottage','bungalow', 'holiday let',
                             'chalet', 'pitch','townhouse', 'dwellinghouse',
                             'flat','house','apartment', 'home','dwelling','accommodation',
                             'maisonette',
                             'residential', 'living', 'social','affordable','market']
#                             'residential development']

headword_synonyms_list_c4 = ['hmo','house in multiple occupation']
#                            'dwelling','flat','apartment','home']

headword_synonyms_list_d1 = ['clinic','health centre','school','museum','library',
                             'non-residential training facility', 'village hall',
                             'non-residential training centre', 'church', 'chapel',
                             'creche', 'crèche','assessment centre',
                             'urgent care centre',  'hall', 'community hall', 'community space',
                             'assessment',   'medical centre', 'dentist',
                             'non-residential', 'day nursery','surgery',
                             'health', 'hydrotherapy complex','primary school', 'secondary school',
                             'community building', 'gallery','law court',
                             'worship','community facility','primary care facility',
                             'lower school', 'middle school', 'upper school',
                             'GP','G P','G.P.','G.P']

headword_synonyms_list_d2 = ['gym', 'gymnasium', 'gymnastic', 'cheerleading',
                             'cinema','bingo hall','swim','skating', 'recreation', 'recreational',
                             'assembly', 'sports','fitness', 'boxing',
                             'sports pitch',  'exercise room', 'tennis',
                             'dance', 'concert', 'music hall',
                             'boating',
                             'event facility','event unit', 'event space',
                             'leisure']



# general descriptions without detailss
headword_synonyms_list_a = ['shopfront','local centre','retail','sales']
headword_synonyms_list_b = ['business','industrial','commercial','employment','workspace']
headword_synonyms_list_c = ['flat','house','apartment', 'home','dwelling','accommodation','unit']#'living'
headword_synonyms_list_d = ['centre']
headword_synonyms_list_all = ['floor space', 'enterprise hub','unit','building','local centre','use','space',
                              'institution','estate','locality','site','premise','facility','process','area'
                              'centre']

general_words = ['unit', 'use', 'space', 'building', 'area', 'floorspace', 'institution','estate','locality','site',
                 'premise','facility','process','block','terrace','land','siting','ground']

# replace some unrelated words to use classes
keywords_list_irrelative_words = ['landscaping', 'ancillary facilities', 'car parking', 'parking', 'footpath',
                                  'roads','car ports', 'garage','amenity space', 'community uses',
                                  'main road', 'mixed-use blocks','new/refurbished buildings/blocks',
                                  'underground car parking spaces','cycle spaces','car parking spaces',
                                  'sheltered cycle parking spaces',
                                  'off-site highways','pavilion','dining','supporting retain facilities',
                                  'outdoor facilities','new vehicular access','footways','cycleways',
                                  'bus stop lay-bys','ancillary road infrastructure','public open space',
                                  'pumping station','surface water attenuation facilities',
                                  'infrastructure','control tower', 'bin storage','recycling storage',
                                  'refuse storage','cycle storage','recycle storage','cycling storage',
                                  'bin store','recycling store', 'refuse store','cycle store','recycle store',
                                  'cycling store', 'sheds for cycle storage',
                                  'environmental impact assessment','lift towers','pedestrian stairwells',
                                  'associated access','engineering works','ground modification',
                                  'above and below ground utilities','cycle paths', 'public square',
                                  'green infrastructure','cycle networks','site access arrangements','allotments',
                                  'engineering', 'ancillary works','rear extension',
                                  'raising the roof','manufacturing','pump house','pumphouse',
                                  'gatehouse','gate house','disabled access','timber boarding',
                                  'associated works','building', 'structures','associated buildings',
                                  'outbuildings',
                                  # for change-of-use model
                                  'vegetation removal', 'tree removal','application form','in the form of',
                                  'in hybrid form','associated development']



joint_symbol_list= [', ', '; ', '/', ' & ',' and ', ' along with ',' with ', ' together with ',' or ',' including ',
                    ' comprising ',' plus ',' associated with ',' in connection with ', ' following ',' incorporating ',
                    ' incorporate ', ' inc. ',
                    '. ', ': ', ' - ',
                    ' to ', ' for ', ' from ', ' onto ', ' by ', ' into ', ' as ', ' of ', ' on ']


joint_symbol_list_without_preps = [', ', '; ', '/', ' & ',' and ', ' along with ',' with ', ' together with ',' or ',' including ',
                    ' comprising ',' plus ',' associated with ',' in connection with ', ' following ',' incorporating ',
                    ' incorporate ', ' inc. ',
                    '. ', ': ', ' - ',]

joint_symbols_coordination= [' ', ', ', '; ', '/', ' & ',' and ', ' along with ', ' together with ',
                             ' plus ',' associated with ',' in connection with ']

joint_symbols_coordination_for_sentences = [', ', '. ',' & ',' and ']
joint_symbols_hard_boundaris = ['. ']



change_of_use_patterns = {'from': {'begin_with_prompt':['change of use of <FROM>', 'replace <FROM>', 'replacement <FROM>',
                                                        'replacement of <FROM>',
                                                        'subdivide <FROM>',
                                                        'cessation of <FROM>', 'reduce <FROM>', 'removal of <FROM>',
                                                        'demolition <FROM>', 'demolition of <FROM>', 'demolish <FROM>'],
                                   'begin_with_non_prompt':[ '<FROM> to be subdivided','<FROM> to be reduced',
                                                             '<FROM> to be removed','<FROM> to be demolished']
                                   },

                          'to': {'begin_with_prompt': ['change of use to <TO>',
                                                       'redevelopment into <TO>', 'redevelopment to <TO>','redevelopment for <TO>',
                                                       'redevelopment with <TO>', 'redevelopment <TO>',
                                                       'redevelopment of <TO>',
                                                       'redevelop into <TO>', 'redevelop to <TO>','redevelop for <TO>','redevelop with <TO>',
                                                       'redevelop <TO>',
                                                       'development into <TO>', 'development to <TO>','development for <TO>','development with <TO>',
                                                       'development <TO>','development of <TO>','develop into <TO>',
                                                       'develop to <TO>','develop for <TO>','develop with <TO>'
                                                       'develop <TO>', 'replace with <TO>', 'replace by <TO>',
                                                       'replacement with <TO>', 'replacement by <TO>',
                                                       'conversion to <TO>', 'conversion into <TO>',
                                                       'restoration of <TO>','form <TO>', 'formation <TO>','formation of <TO>', 'forming <TO>',
                                                       'erection <TO>', 'erection of <TO>', 'erect <TO>',
                                                       'rebuilding <TO>', 'rebuilding of <TO>', 'rebuild <TO>', 'build <TO>',
                                                       'construction <TO>', 'construction of <TO>',
                                                       'construct <TO>', 'facilitate <TO>',
                                                       'creation <TO>', 'creation of <TO>', 'create <TO>',
                                                       'elevation <TO>', 'elevation of <TO>', 'elevate <TO>',
                                                       're-elevation <TO>', 're-elevation of <TO>', 're-elevate <TO>',
                                                       'resiting of <TO>', 'resiting <TO>', 'resit <TO>',
                                                       'provide <TO>', 'serve <TO>', 'service <TO>',
                                                       'alterations to <TO>', 'extension to <TO>', 'for <TO> purpose',
                                                       'extensions to <TO>', 'retention of <TO>', 'provision <TO>',
                                                       'provision of <TO>', 'continuing <TO>', 'relocation of <TO>',
                                                       'refurbishment of <TO>', 'reconfiguration of <TO>',
                                                       'reinstatement of <TO>',
                                                       'for <TO> use', 'to be used as <TO>', 'for use as <TO>',
                                                       'installation of <TO>', 'install <TO>',
                                                       'proposed <TO>'],
                                 'begin_with_non_prompt': ['<TO>', '<TO> to be built']
                                 },

                          'from_to':{'begin_with_prompt':['change of use of from <FROM> to <TO>', 'change of use of <FROM> to <TO>',
                                                          'change of use of <FROM> into <TO>', 'change of use of <FROM> for use as <TO>',
                                                          'change of use of <FROM> for <TO>',
                                                          'change of use from <FROM> to <TO>', 'change of use <FROM> to <TO>',
                                                          'change of use <FROM> into <TO>', 'change of use <FROM> for use as <TO>',
                                                          'change of use <FROM> for <TO>',
                                                          'change <FROM> to <TO>', 'change <FROM> into <TO>', 'change <FROM> for <TO>',
                                                          'redevelopment <FROM> into <TO>', 'redevelopment <FROM> to <TO>','redevelopment <FROM> for <TO>',
                                                          'redevelopment of <FROM> into <TO>', 'redevelopment of <FROM> to <TO>','redevelopment of <FROM> for <TO>',
                                                          'redevelop <FROM> into <TO>', 'redevelop <FROM> to <TO>','redevelop <FROM> for <TO>',
                                                          'development <FROM> into <TO>', 'development <FROM> to <TO>','development <FROM> for <TO>',
                                                          'development of <FROM> into <TO>', 'development of <FROM> to <TO>','development of <FROM> for <TO>',
                                                          'develop <FROM> into <TO>', 'develop <FROM> to <TO>','develop <FROM> for <TO>',
                                                          'replace <FROM> with <TO>', 'replace <FROM> by <TO>',
                                                          'replace <FROM> for <TO>', 'replacement <FROM> with <TO>', 'replacement <FROM> by <TO>',
                                                          'replacement of <FROM> with <TO>', 'replacement of <FROM> by <TO>',
                                                          'conversion of <FROM> to <TO>', 'conversion from <FROM> to <TO>',
                                                          'conversion of <FROM> into <TO>', 'conversion from <FROM> into <TO>',
                                                          'conversion of <FROM> for <TO>','convert <FROM> to <TO>',
                                                          'convert <FROM> into <TO>', 'current <FROM> as <TO>',
                                                          'current of <FROM> as <TO>',
                                                          'subdivision <FROM> into <TO>','subdivide <FROM> into <TO>',
                                                          'restoration of <FROM> to <TO>',
                                                          'use of former <FROM> as <TO>',
                                                          'introduction of <TO>'],
                                     'begin_with_non_prompt':['<FROM> to be replaced with <TO>', '<FROM> to be replaced by <TO>',
                                                              '<FROM> replaced with <TO>', '<FROM> replaced by <TO>',
                                                              '<TO> to replace <FROM>','<FROM> convert to <TO>',
                                                              '<FROM> convert into <TO>','<FROM> to be subdivided into <TO>',
                                                              '<FROM> on the site of <TO>']}
                          }





bed_descriptions_c3= ['room', 'bedroom', 'bed', 'bedsit', 'bathroom', 'bedspace','bedroomed']
bed_descriptions_c1_c2_c4 = ['resident','children','person','people','adult']