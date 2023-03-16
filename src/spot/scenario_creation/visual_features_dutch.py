male_names = ['Jan', 'Stefan', 'Yusuf', 'Bas', 'Alex', 'Mostafa', 'Simon', 'Omar', 'Gerard']  # TODO do we even want names?
female_names = ['Marie', 'Zainab', 'Jessica', 'Alessandra', 'Noor', 'Emma', 'Zahra', 'Merel', 'Patricia']
ids = []
sex = ['man', 'vrouw']
hair_style = ['pony', 'bob', 'lang', 'kort', 'paardenstaart', 'kaal']
hair_colour = ['bruin', 'blond', 'zwart', 'rood', 'rood_geverfd', 'roze_geverfd', 'groen_geverfd', 'dyed_blue', 'grijs', 'wit']
hair_type = ['krulhaar', 'stijl_haar']
facial_hair = ['snor', 'baard', 'geen']
skin_colour = ['van_kleur', 'wit']
accessory = ['bril', 'pet', 'hoed', 'oorbellen', 'geen']
top = ['shirt', 'sweater', 'jas', 'jurk']
bottom = ['broek', 'korte_broek', 'rokje']
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



