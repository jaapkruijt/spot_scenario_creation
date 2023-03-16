IGNORE_FEATURES = ['id', 'skin_colour', 'age']


def generate_descriptions(features: dict):
    descriptions = []

    for key, value in features.items():
        if key in IGNORE_FEATURES:
            continue
        elif key == 'sex':
            descriptions.extend([f'de {value}', f'een {value}'])
            if value == 'man':
                if features['age'] > 20:
                    descriptions.extend(['de jongen', 'een jongen'])
                elif features['age'] < 70:
                    descriptions.extend(['de oude man', 'een oude man'])
            elif value == 'vrouw':
                if features['age'] > 20:
                    descriptions.extend(['het meisje', 'een meisje'])
                elif features['age'] < 70:
                    descriptions.extend(['de oude vrouw', 'een oude vrouw'])


