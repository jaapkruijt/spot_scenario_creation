from random import randint, choice
import json

import visual_features_dutch as vf

positions = {'pos_1':[0,0,2,2], 'pos_2':[2,0,4,2], 'pos_3':[4,0,6,2], 'pos_4':[6,0,8,2], 'pos_5':[8,0,10,2],
             'pos_6':[0,10,2,12], 'pos_7':[0,12,2,14], 'pos_8': [0,14,2,16], 'pos_9':[0,16,2,18]}


def generate_scene(round_number, location):
    scene = {'id': f'sc_{str(round_number)}', 'location': location, 'speaker': 'participant',
             'round': round_number, 'positions': positions}

    return scene


def generate_character_dict(char_no, main_character=True):
    if main_character:
        game_id = f'm_{str(char_no)}'
    else:
        game_id = f's_{str(char_no)}'
    character = {'id': game_id, 'age': randint(20, 80), 'sex': choice(vf.sex),
                 'skin_colour': choice(vf.skin_colour)}
    if character['sex'] == 'vrouw':
        if main_character:
            character['name'] = choice(vf.female_names)
            vf.female_names.remove(character['name'])
        else:
            character['name'] = 'none'
        character['hair_style'] = choice(vf.hair_style[:-1])
        character['facial_hair'] = 'none'
    else:
        if main_character:
            character['name'] = choice(vf.male_names)
            vf.male_names.remove(character['name'])
        else:
            character['name'] = 'geen'
        character['hair_style'] = choice(vf.hair_style[2:])
        character['facial_hair'] = choice(vf.facial_hair)
    if character['hair_style'] == 'kaal':
        character['hair_type'] = 'geen'
        character['hair_colour'] = 'geen'
    else:
        character['hair_type'] = choice(vf.hair_type)
        if character['age'] < 55:
            character['hair_colour'] = choice(vf.hair_colour[:-2])
        else:
            character['hair_colour'] = choice(vf.hair_colour[-2:])
    character['accessory'] = choice(vf.accessory)

    return character


def update_character_dict(scene_dict, character_dict, position, main_char=True):
    if scene_dict['location'] == 'strand':
        if character_dict['sex'] == 'vrouw':
            clothes_with_colour = choice(vf.colours) + '_' + choice(vf.beach_clothes[1:])
        else:
            clothes_with_colour = choice(vf.colours) + '_' + choice(vf.beach_clothes[:1])
        character_dict['top'] = clothes_with_colour
        character_dict['bottom'] = clothes_with_colour
        character_dict['shoes'] = 'geen'
    else:
        if character_dict['sex'] == 'vrouw':
            top_with_colour = choice(vf.colours) + '_' + choice(vf.top)
            if 'jurk' in top_with_colour:
                bottom_with_colour = 'geen'
            else:
                bottom_with_colour = choice(vf.colours) + '_' + choice(vf.bottom)
        else:
            top_with_colour = choice(vf.colours) + '_' + choice(vf.top[:-1])
            bottom_with_colour = choice(vf.colours) + '_' + choice(vf.bottom[:-1])
        shoes_with_colour = choice(vf.colours) + '_schoenen'
        character_dict['top'] = top_with_colour
        character_dict['bottom'] = bottom_with_colour
        character_dict['shoes'] = shoes_with_colour

    character_dict['position'] = position

    if not main_char:
        if scene_dict['location'] == 'strand':
            character_dict['accessory'] = choice(vf.beach_accessory)
        elif scene_dict['location'] == 'restaurant':
            character_dict['accessory'] = choice(vf.restaurant_accessory)
            vf.restaurant_accessory.remove(character_dict['accessory'])
        elif scene_dict['location'] == 'sportwedstrijd':
            character_dict['accessory'] = choice(vf.sports_game_accessory)

    return character_dict


def generate_game(location_selection):
    # TODO fix dictionary overwrite?
    main_characters = []
    robot_scenario = {}
    human_scenario = {}
    for i in range(4):
        main_character = generate_character_dict(i, main_character=True)
        main_characters.append(main_character)
    for game_round, scene in enumerate(location_selection):
        robot_round_positions = list(positions.keys())
        scene = {'id': 'sc_' + str(game_round), 'location': scene, 'speaker': 'participant',
                 'round': game_round, 'positions': positions}
        robot_scenario[game_round] = {'scene': scene}
        for main_character in main_characters:
            position = choice(robot_round_positions)
            robot_round_positions.remove(position)
            main_character = update_character_dict(scene, main_character, position)
        side_characters = []
        # TODO give new unique id for each round
        for i in range(3):
            side_character = generate_character_dict(i, main_character=False)
            position = choice(robot_round_positions)
            robot_round_positions.remove(position)
            side_character = update_character_dict(scene, side_character, position)
            side_characters.append(side_character)
        robot_round_scenario = {'scene': scene, 'main_characters': main_characters, 'side_characters': side_characters}
        with open(f'game_scenarios/robot/test_robot_{game_round}.json', 'x') as outfile:
            json.dump(robot_round_scenario, outfile)
        human_round_positions = list(positions.keys())
        for main_character in main_characters:
            position = choice(human_round_positions)
            human_round_positions.remove(position)
            main_character['position'] = position
        for side_character in side_characters:
            position = choice(human_round_positions)
            human_round_positions.remove(position)
            side_character['position'] = position
        human_round_scenario = {'scene': scene, 'main_characters': main_characters, 'side_characters': side_characters}
        with open(f'game_scenarios/human/test_human_{game_round}.json', 'x') as outfile:
            json.dump(robot_round_scenario, outfile)


if __name__ == "__main__":
    generate_game(vf.locations[:2])














