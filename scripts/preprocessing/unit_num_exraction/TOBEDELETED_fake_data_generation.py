import random
import string
import datetime

from numpy.random import choice
from num2words import num2words
# import nltk
# from nltk.corpus import words
# nltk.download('words')

# pip install num2words
'''


Conversion of the existing building from nine self-contained apartments to ten, together with alterations to the elevations, new car parking and landscaping works (alternative to DC/2019/01684).
Demolition of existing property at 9 West Road and development of 4 new residential dwellings (Outline)
Demolition of existing workshops and the development of 35 self-contained flats in 2No. blocks.
Demolition of existing warehouse / showroom and adjoining single-storey brick office structure forming Unit 1. New build extension to adjacent industrial buildings to provide two new units to replace Unit 1.

Erection of two buildings between six, ten, twelve and fourteen storeys (min. 20.1m and max. 46.2m above ground level) comprising 105 residential units and 280 sqm of commercial floorspace (Use Class A1/A2/A3/A4/B1/D1/D2), public open space, accessible parking, cycle storage, landscaping and related ancillary works

Demolition of existing buildings and redevelopment of the site to provide residential units (Use Class C3) within a new residential-led building ranging in height from 7 to 24 storeys (above ground), over ground floor commercial floorspace (Use Class A1/A2/A3/A5/B1A/B1C), with basement car parking, cycle parking and plant space, landscaping and associated works.
Erection of two buildings between six, ten, twelve and fourteen storeys (min. 20.1m and max. 46.2m above ground level) comprising 105 residential units and 280 sqm of commercial floorspace (Use Class A1/A2/A3/A4/B1/D1/D2), public open space, accessible parking, cycle storage, landscaping and related ancillary works

'''

def _generate_random_int(mode:str = 'mixed_either'):
    num = random.randint(1, 10000)
    word = num2word(num)
    if mode == 'num_only':
        return num
    elif mode == 'word_only':
        return word
    elif mode == 'mixed_either':
        return choice([num, word])
    elif mode == 'mixed_both':
        form_1 = f"{word} ({num})"
        form_2 = f"({word}) {num}"
        form_3 = f"({num}) {word}"
        form_4 = f"{num} ({word})"
        return choice([form_1, form_2, form_3, form_4])


def _generate_random_float():
    num_decimal = random.randint(1,2)
    return round(random.uniform(0,1000000),num_decimal)


def _generate_random_num_with_thousand_separators(mode:str = 'int'):
    if mode == 'int':
        num = random.randint(1, 1000000)
    elif mode == 'float':
        num = _generate_random_float()
    elif mode == 'mixed_either':
        num = choice([random.randint(1, 1000000), _generate_random_float()])

    str = f'{num:,}'
    return str, num


def _generate_random_letters_with_nums():
    length = random.randint(2,5)
    str = ''
    for _ in range(length+1):
        str += choice([random.choice(string.ascii_letters),random.randint(0,9)])
    return str


def _generate_referece_no():
    return f"{random.randint(0, 9)}{random.randint(0, 9)}/" \
           f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}/" \
           f"{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}"






def noise_story():
    form_1 = f"{_generate_random_int()}{choice([' ','-'])}{choice(['storeys','storey'])}"
    form_2 = f"{_generate_random_int('num_only')}{choice(['-',' to ',' and '])}{_generate_random_int('num_only')} {choice(['storeys','storey'])}"
    form_3 = f"{_generate_random_int('word_only')}{choice(['-',' to ',' and '])}{_generate_random_int('word_only')} {choice(['storeys','storey'])}"
    form_4 = f"{_generate_random_int('mixed_both')}{choice(['-', ' to ', ' and '])}{_generate_random_int('mixed_both')} {choice(['storeys', 'storey'])}"
    form_5 = f"{_generate_random_int('mixed_both')} {choice(['storeys','storey'])}"
    form_6 = f"{_generate_random_int('num_only')}/{_generate_random_int('num_only')} {choice(['storeys','storey'])}"
    form_7 = f"{_generate_random_int('num_only')}/{_generate_random_int('num_only')}/{_generate_random_int('num_only')} {choice(['storeys','storey'])}"
    return choice([form_1, form_2, form_3, form_4, form_5, form_6, form_7])

def noise_meter():
    num = choice([_generate_random_float(), _generate_random_int()])
    form_1 = f"{choice(['+',''])}{num}m{choice(['', ' AOD'])}"
    form_2 = f"{choice(['+', ''])}{num} AOD"
    form_3 = f"{num}{choice([' ',''])}{choice(['metres','metre','meters','meter'])}"
    return choice([form_1, form_2, form_3])

def noise_proper_noun():
    noun = choice(['regulation', 'regulations', 'act', 'plot','reference','section','application','sub-zone','zone','scheme','phase','phases'])
    form_1 = f"{noun} {choice([_generate_random_letters_with_nums(),_generate_referece_no(),_generate_random_int('num_only')])}"
    form_2 = f"{noun} ({choice([_generate_random_letters_with_nums(),_generate_referece_no(),_generate_random_int('num_only')])})"
    form_3 = f"{choice([_generate_random_letters_with_nums(),_generate_referece_no(),_generate_random_int('num_only')])} {noun}"
    form_4 = f"({choice([_generate_random_letters_with_nums(), _generate_referece_no(), _generate_random_int('num_only')])}) {noun}"
    form_5 = f"unit {_generate_random_letters_with_nums()}"
    return choice([form_1, form_2, form_3, form_4, form_5])

def noise_date():
    form_1 = f"{_generate_random_int()}{choice([' ','-'])}{choice(['years','year','months','month'])}"

    date = datetime.datetime(random.randint(1800,2030), random.randint(1,12), random.randint(1,31))
    joint_symbol = choice([' ','-','/'])
    form_2 = date.strftime(f"{choice(['%y', '%Y'])}{joint_symbol}{choice(['%b', '%B', '%m'])}{joint_symbol}{choice(['%d', '%w'])}{choice(['th','st','nd',''])}")
    form_3 = date.strftime(f"{choice(['%y', '%Y'])}{joint_symbol}{choice(['%d', '%w'])}{choice(['th','st','nd',''])}{joint_symbol}{choice(['%b', '%B', '%m'])}")
    form_4 = date.strftime(f"{choice(['%b', '%B', '%m'])}{joint_symbol}{choice(['%d', '%w'])}{choice(['th','st','nd',''])}{joint_symbol}{choice(['%y', '%Y'])}")
    form_5 = date.strftime(f"{choice(['%b', '%B', '%m'])}{joint_symbol}{choice(['%y', '%Y'])}{joint_symbol}{choice(['%d', '%w'])}{choice(['th','st','nd',''])}")
    form_6 = date.strftime(f"{choice(['%d', '%w'])}{choice(['th','st','nd',''])}{joint_symbol}{choice(['%b', '%B', '%m'])}{joint_symbol}{choice(['%y', '%Y'])}")
    form_7 = date.strftime(f"{choice(['%d', '%w'])}{choice(['th','st','nd',''])}{joint_symbol}{choice(['%y', '%Y'])}{joint_symbol}{choice(['%b', '%B', '%m'])}")
    return choice([form_1, form_2, form_3, form_4, form_5, form_6, form_7])

def noise_address():
    form_1 = f"{_generate_random_int('num_only')} {choice(words.words())} {choice(['road', 'lane', 'avenue'])}"
    form_2 = f"{_generate_random_int('num_only')} & {_generate_random_int('num_only')} {choice(words.words())} {choice(['road', 'lane', 'avenue'])}"
    form_3 = f"flat {random.randint(1,100)}"
    form_4 = f"flats {random.randint(1, 100)}-{random.randint(1, 100)}"
    return choice([form_1, form_2, form_3, form_4])



def noise_irrelative_words(keywords_list_irrelative_words: list):
    return f"{choice([_generate_random_int()+' ', _generate_random_num_with_thousand_separators()[0]+' ', ''])}{choice(keywords_list_irrelative_words)}"


def noise_bed():
    '''
    rooms, bedrooms, beds, bedsits, bathrooms
    '''
    if choice(['int_with_thousand_separators','int']) == 'int_with_thousand_separators':
        num_str, num = _generate_random_num_with_thousand_separators()
    else:
        num = _generate_random_int()
        num_str = str(num)

    form = f"{num_str}{choice([' ','','-','X','x'])}{choice(['rooms','room','bedrooms','bedroom','beds','bed','bedsits','bedsit','bathrooms','bathroom'])}"
    return form, num


def _unit_num_format():
    '''
    (joint symbol can be whitespace,-,None)
    1. 84
    2. 84 units/unit
    3. 84 no/no./num/num.
    4. 84 x/84x
    '''
    if choice(['int_with_thousand_separators','int']) == 'int_with_thousand_separators':
        num_str, num = _generate_random_num_with_thousand_separators()
    else:
        num = _generate_random_int()
        num_str = str(num)

    form_1 = num_str
    form_2 = f"{num_str}{choice([' ','-',''])}{choice(['units','unit','no','no.','num','num.'])}"
    form_3 = f"{num_str}{choice([' ',''])}{choice(['X', 'x'])}"
    return choice([form_1, form_2, form_3]), num



def _sqm_num_format():
    '''
    64 sqm/sq m/sq.m/m2/square metres
    '''
    if choice(['int_with_thousand_separators','int']) == 'int_with_thousand_separators':
        num_str, num = _generate_random_num_with_thousand_separators('mixed_either')
    else:
        num = _generate_random_int()
        num_str = str(num)
    form = f"{num_str}{choice([' ',''])}{choice(['sqm','sq m','sq.m','m2','square metres','square metre'])}"
    return form, num






def single_use_class_with_units_num():
    pass

def multiple_use_classes_with_units_num():
    pass


'''
noises

three buildings ranging in height from 9 to 29 storeys
two storey industrial building
two main linked buildings (up to 8 storeys and 44m in height)
6-26 storeys
two-storey building
1no two storey cleaners building
a mixed-use, five (5) storey building
two new buildings ranging from 6 storeys (24 metres above ground level)
6 storeys (24 metres above ground level) to 19 storeys (71.8 metres above ground level) in height
20 storeys in height (71.4m above ground level)
a building up to 80m AOD high
four buildings ranging in height from +29.95 AOD to +125.05 AOD
6/8/12 storey building
a building of five (5) storeys
erection of new four (4) and five (5) storey buildings with a maximum parapet height of 21.8m AOD
a new building up to 6 storeys (+33m AOD approx.) in height
 

3 mixed-use blocks
39 new/refurbished buildings/blocks
120 underground car parking spaces
1,080 cycle spaces
16 car parking spaces
three short stay bays
16 sheltered cycle parking spaces
42 shipping containers


up to 4,774sqm of back of house space (including plant, cycle and car parking) 
a maximum overall floorspace of up to 18,710 sqm (GEA)


Regulation 13
Regulations (2017)
Regulations 2017
Act 1990
Plot R4
approval reference 14/00422/FUL
Section 73
planning permission reference 17/00669/VAR
Application 2 
Sub-Zone 3D1
planning permission reference 12/00146/FUM
S1 and S11 scheme
Unit T1
Phase 2
Phases 2


260 rooms 
48 bedrooms
14no. Accessible rooms
comprising a mix of 1,2,3 bedrooms
2 lift towers, and 2 pedestrian stairwells



27 September 2012
27th February 2014
January 11th 2012
5 years
a period of 18 months 

10 South Road
19 & 21 Nyewood Lane
24 units to form balconies to flats 1-10
flat 19
19 & 21 Nyewood Lane
34 & 36 Carlton Avenue
'''


'''
703 sqm of Class E commercial uses at ground floor
3,570 sq m of flexible community,
1450sqm of industrial floorspace
159 sq.m of flexible commercial
38,495m data centre (Use Class B8)
30,000 m2 residential institutions (C2), including student (up to 1,000 beds) and hotel (150  beds)
57,000 m2 commercial space (Use Classes B1 to B8)
42,000 m2 of 鈥渇lip Plot鈥 floorspace (commercial use Class B1 or Residential use Class C3);
35,000 m2 retail and leisure (Use Classes A1 to A5, D2
12,000 m2 community uses which include education and healthcare uses (Use D1)
47,000m2 (GIA) cultural uses (Use D1)
community space (72m2) (Use Class F.2)
Sui generis uses
1no two storey cleaners building
2no single storey storage units
open storage of motor vehicles (use class B8)
a data centre (Use Class B8) of up to 25,000 sqm gross external
a ground plus 18 storey building (100.175m AOD) providing 384 co-living units (Sui Generis)
to create a food storage for the existing community centre with a flat roof.
a five storey B1 (business) use building
Erection of single storey extension for use as tyre store 
The erection of 42 shipping containers for storage purposes (Use Class B8)



609 sqm (GIA) of ground floor flexible non-residential floorspace (Use Classes A1/A2/A3/A4/B1/D1/D2)
514 sqm (GIA) ground floor workspace (Use Class B1/Artist Studios)
a data centre (Use Class B8) of up to 35,000sqm including ancillary offices, internal plant and equipment (including flues), and substation
a 377sqm (GIA) children鈥檚 nursery (Use Class D1)
977sqm (GIA) of flexible retail/employment floor space (Use Classes A1, A2, and B1) 
flexible B1/D1/D2 use in the Old Refectory Building,
1450sqm of industrial floorspace (Use Class B1(c)/B2/B8) with ancillary offices
3,500 sqm of in part double height commercial floorspace, providing a flexible range of uses (Use Classes A1, A2, A3, A4, B1, D1 and D2)
D1 (Non-residential institutions) comprising 1,324 sqm
B1c, B2 and B8
to provide flexible industrial uses (Class B2/B8) over ground and first floor, offices (Class B1a) at second floor and hotel (Class C1) uses on floors three to ten
two-storey building (Use Classes B1, B2 and B8).
98 sq.m of flexible commercial/community/town centre uses (Classes E/F) 
a series of buildings ranging from one to 27 storeys in height to provide 3,570 sq m of flexible community, commercial and retail floorspace (Use Classes A1, A2, A3, A4, B1 and/or D1) at ground and mezzanine floor level
the erection of a mixed-use, five (5) storey building to provide 2,772sqm of floorspace (GIA), comprising: 531sqm of commercial floorspace (Use Class B1) at ground level, and 34 residential units (Use Class C3) on the upper floors
to allow for flexible uses within Classes B1(c) and/or B2 (General industry) and/or B8.
three storey B1 (business) and B8 (storage or distribution) 
Temporary change of use (5 years) from storage & distribution (Class B8) into a multipurpose event space (Class D1, D2 and Sui Generis) and retention of bin store to front elevation.
Commercial and Community Uses (up to 10,849 11,018sqm GIA) (Class A, B, and D1/2)
Commercial/community floorspace within Use Classes A1, A3, B1, D1 and D2 comprising up to but not to exceed 1,440.8sqm NIA) to include:-  Local retail and food and drink uses (Class A1, A3) not exceeding 217.3sqm NIA-  Business premises (Class B1) including artists workshops and studios not exceeding 1,047.5sqm NIA-  D1 gallery and D2 community boat clubhouse not exceeding 176sqm NIA
change of use of the ground floor from B1 Use (Business) to A3 Use (Restaurant and Cafe) and A4 Use (Drinking Establishment)
1024 sqm Gross Internal Area (GIA) of A1, A4, B1 and/or D1 floorspace
Employment (Use Classes B1a and B1c) of a minimum of 29,908sqm; 
Retail (Use Classes A1-A4) of up to 4,493sqm; 
and Community Facilities (Use Class D1/D2) for a minimum of 381sqm and up to 2,318sqm;
Extensions and alterations to the commercial area of the building, including the insertion of a mezzanine floor and division of the commercial space into four units with a flexible A1/A2/A3 and/or B1 use class and the installation of glazed shopfronts
Approximately 2,600sqm gross internal floor area (GIFA) commercial floorspace (Use Classes A1-A4/B1)
The development comprises up to 190,800 sqm of development, comprising: up to 160,060 sqm of academic development (Class D1) and commercial research space(Class B1(b)), of which up to 16,000 sqm may be commercial research space (Class B1(b)); up to 50,880 sqm of student accommodation (sui generis); and up to 4,240 sqm of retail (Classes A1-A5) uses;
a scheme for a commercial office building (Class B1) (circa 44,845 square metres) (GEA) with retail (Class A1,A2, A3, A4, A5) (circa 980 sq.m GEA) and Alternative uses (including D2 uses) (circa 1,175 sq.m) (鈥榯he S10 Scheme鈥)
approx. 306 sqm of flexible commercial and retail floorspace (Use Classes A1-A4 and/or B1)
687sqm (GIA) approx. of commercial floorspace (use classes A3 caf茅, B1/B2 workspace, D2 gallery) 


436 residential units (Class C3)
158 affordable residential units (Class C3)
605 (reduced from 611) residential units (Use Class C3)
34 residential dwellings (15x 1 bed, 10x 2 bed & 9x 3 bed)  
148 residential dwellings (1 x studio, 67 x 1 bed, 48 x 2 bed and 32 x 3 bed)
8 duplex flats comprising 3 x 1 bed units and 5 x 2 bed units
three new dwellings
Residential (475 units) (up to 51,758sqm GIA) (Use Class C3);
6,200 - 6,700 new dwellings (Use Class C3)
change of use of southern part of the first floor from commercial to residential use, to create three new dwellings, along with external alterations.
57,166.50sqm (GIA) 鈥 Residential (Class C3) 
comprising 435 dwellings (47,758.20  47,588.90sqm GIA)
Residential (Class C3) 鈥 up to 40 dwellings - floorspace not exceeding, but ranging between 4,042.30sqm and 6,199.10sqm GIA (NIA 鈥 between 2,806sqm and 3,514sqm)
7x live/work (sui generis) units
7 x live/work (sui generis) units
a total of 247 residential dwellings (21,392 m2 Residential GIA) 
a maximum height of 113m (described as 30 storeys plus 2 storey basement) for serviced apartments and shared-living complex.
Residential (Use Class C3) of up to 78,931sqm to deliver approx. 874 units
The scheme will provide: x2 new three bedroom houses, x2 two bedroom flats, x3 one bedroom flats and restore the existing Lockkeepers Cottage
9  flats (1 x studio, 3 x 1 bed, 4 x 2 bed, 1 x 3 bed) in rear / side extension to existing building
537 mixed tensure new homes (Use Class C3)
13,575sqm (GIA) of residential (equating to a maximum of 133 residential units)
four residential dwellings (Use Class C3)
2 no. associated office buildings
330 student rooms (279 en suite, 34 shared bathroom, 11 wheelchair accessible and 6 wheelchair accessible studios) (Use Class Sui Generis) 
560 residential units (48,100 square metres) 
9 self-contained residential units (Use Class C3)
residential (Use Class C3) (up to 204 units)
44 residential dwellings (4 X studio units, 15 x 1 bed, 15 x 2 bed and 10 x 3 bed)
two warehouses
3 x duplex self contained residential units (Use Class C3)
a 240-bedroom hotel (Class C1) 
2 storey block of 6 No Flats comprising of 4 No. 2 bed & 2 No. 1 bed flats.
3 No.3 bed cottages 
38 No residential apartments (9 No 1-bed units & 29 No. 2-bed units)
5 no. dwellings comprising 2 no. 4- bed houses, 2 no. 3- bed houses & 1 no. 3- bed bungalow
5 No. two bed
24 flats to include a further 2 bedrooms & a further 2 bathrooms on a fifth floor
5No. self contained flats
25 no. 2, 3 & 4 bed 2 & 3 storey houses
1 x 4 bedroom house, 13 x 3 bedroom houses 3 x 2 bedroom houses & 1 x 2 bedroom flat
9 No. one & a half storey houses 
2No. 4-bed houses
'''





'''
householder

'''

