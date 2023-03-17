male_names = ['Jan', 'Stefan', 'Yusuf', 'Bas', 'Alex', 'Mostafa', 'Simon', 'Omar', 'Gerard']  # TODO do we even want names?
female_names = ['Marie', 'Zainab', 'Jessica', 'Alessandra', 'Noor', 'Emma', 'Zahra', 'Merel', 'Patricia']
ids = []
sex = ['man', 'vrouw']
hair_style = ['pony', 'bob', 'lang', 'kort', 'paardenstaart', 'kaal']
hair_colour = ['bruin', 'blond', 'zwart', 'rood', 'grijs', 'wit']
hair_type = ['krulhaar', 'stijl_haar']
facial_hair = ['snor', 'baard', 'geen']
skin_colour = ['vankleur', 'wit']
accessory = ['bril', 'pet', 'hoed', 'geen']
top = ['shirt', 'sweater', 'jas', 'jurk']
bottom = ['broek', 'kortebroek', 'rokje']
shoes = ['schoenen']
colours = ['rood', 'zwart', 'bruin', 'wit', 'blauw']

beach_clothes = ['zwembroek', 'bikini', 'badpak']
beach_accessory = ['zonnebril', 'zonnehoed', 'handdoek']
sports_game_accessory = ['sjaal', 'vlaggetje', 'geen']
restaurant_accessory = ['schort'] + ['geen']*3

locations = ['festival', 'strand', 'familiereunie', 'restaurant', 'sportwedstrijd', 'pretpark']


general_descriptions = {'adult': ['een %s persoon', 'het %s persoon', 'iemand %s'],
                        'young': ['een %s kind', 'een %s kindje'],
                        'old': ['een oudere', 'een oudje']}
sex_descriptions = {'man': {'adult': ['de man', 'een man'], 'young': ['de jongen', 'een jongen']}}
hair_descriptions = {'def': 'met het % haar', 'indef': 'met % haar'}
hair_style_descriptions = {'pony': ['met een %s pony', 'met de %s pony'],
                           'bob': ['met een %s bob', 'met de %s bob'],
                           'lang': {'plus_e': ['lange', 'langharige'], 'no_e': ['lang', 'langharig']},
                           'kort': {'plus_e': ['korte', 'kortharige'], 'no_e': ['kort', 'kortharig']},
                           'paardenstaart': ['met een %s paardenstaart', 'met de %s paardenstaart'],
                           'kaal': ['de kale %s', 'een kale %s', 'met een kaal hoofd', 'met het kale hoofd']}
hair_colour_descriptions = {}
hair_type_descriptions = {'krulhaar': {'phrase': ['met krulhaar', 'met krulhaar'], 'adj': {'plus_e': ['krullende'],
                                                                                           'no_e': ['krullend']}},
                          'stijl': {'adj': {'plus_e': ['stijle'], 'no_e': ['stijl']}}}
facial_hair_descriptions = {'snor': {'phrase': ['met een snor', 'met de snor']},
                            'baard': {'phrase': ['met een baard', 'met de baard']},
                            'geen': None}
accessory_descriptions = {'bril': {'phrase': ['met een bril', 'met de bril']},
                          'pet': {'phrase': ['met een pet', 'met de pet']},
                          'hoed': {'phrase': ['met een hoed', 'met de hoed']},
                          'zonnebril': {'phrase': ['met een zonnebril', 'met de zonnebril']},
                          'sjaal': {'phrase': ['met een sjaal', 'met de sjaal']},
                          'vlaggetje': {'phrase': ['met een vlaggetje', 'met het vlaggetje']},
                          'schort': {'phrase': ['met een schort', 'met het schort']},
                          'geen': None}
top_descriptions = {'shirt': {'phrase': ['met een %s shirt', 'met het %s shirt']},
                    'sweater': {'phrase': ['met een %s sweater', 'met de %s sweater']},
                    'jas': {'phrase': ['met een %s jas', 'met de %s jas']},
                    'jurk': {'phrase': ['met een %s jurk', 'met de %s jurk']}}
bottom_descriptions = {'broek': {'phrase': ['met een %s broek', 'met de %s broek', 'met een %s lange broek',
                                            'met de %s lange broek']},
                       'kortebroek': {'phrase': ['met een %s korte broek', 'met de %s korte broek']},
                       'rokje': {'phrase': ['met een %s rokje', 'met het %s rokje', 'met een %s rok', 'met de %s rok']},
                       'zwembroek': {'phrase': ['met een %s zwembroek', 'met de %s zwembroek']},
                       'bikini': {'phrase': ['met een %s bikini', 'met de %s bikini']},
                       'badpak': {'phrase': ['met een %s badpak', 'met het %s badpak']}}
colours_descriptions = {'rood': {'adj': {'plus_e': 'rode', 'no_e': 'rood'}},
                        'zwart': {'adj': {'plus_e': 'zwarte', 'no_e': 'zwart'}},
                        'bruin': {'adj': {'plus_e': 'bruine', 'no_e': 'bruin'}},
                        'wit': {'adj': {'plus_e': 'witte', 'no_e': 'wit'}},
                        'blauw': {'adj': {'plus_e': 'blauwe', 'no_e': 'blauw'}},
                        'blond': {'adj': {'plus_e': 'blonde', 'no_e': 'blond'}},
                        'grijs': {'adj': {'plus_e': 'grijze', 'no_e': 'grijs'}}}







