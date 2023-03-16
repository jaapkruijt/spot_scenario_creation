from emissor.persistence.persistence import ScenarioStorage
from emissor.representation.scenario import Scenario, ImageSignal, ScenarioContext, Mention, Annotation
from emissor.representation.entity import Person
from emissor.representation.ldschema import emissor_dataclass
from emissor.representation.annotation import AnnotationType
from emissor.representation.entity import Gender
from typing import List
from sample_game import robot_scenario, main_chars
import uuid
import json
from tempfile import TemporaryDirectory
from pathlib import Path
from datetime import date, datetime

from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.helper_functions import brain_response_to_json
from cltl.brain.LTM_statement_processing import process_statement
from cltl.commons.discrete import UtteranceType
from tqdm import tqdm
import os


@emissor_dataclass
class SpotScenarioContext(ScenarioContext):
    location: str
    speaker: str
    round: int
    positions: dict


@emissor_dataclass(namespace="http://cltl.nl/leolani/n2mu")
class Character(Person):
    game_id: str
    main_char: bool
    hair_colour: str
    hair_type: str
    hair_style: str
    facial_hair: str
    skin_colour: str
    accessory: str
    top: str
    bottom: str
    shoes: str

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


def fill_character_information(features: dict, main_character: bool):
    if features['sex'] == 'man':
        gender = Gender.MALE
    elif features['sex'] == 'vrouw':
        gender = Gender.FEMALE
    else:
        gender = Gender.OTHER

    uri = 'http://cltl.nl/leolani/world/' + features['id']

    return Character(uri, features['name'], features['age'], gender, features['id'], main_character,
                     features['hair_colour'], features['hair_type'], features['hair_style'],
                     features['facial_hair'], features['skin_colour'], features['accessory'], features['top'],
                     features['bottom'], features['shoes'])


def fill_context_capsule(scenario: Scenario, context: SpotScenarioContext):
    capsule = {'context_id': scenario.id, 'date': datetime.now().date(), 'place': context.location,
               'place_id': context.location, 'country': 'Netherlands', 'region': 'North Holland',
               'city': 'Amsterdam'}

    return capsule


def basis_visual_capsule(scenario_id: str, mention: Mention, detection_no):
    capsule = {"visual": 1,
                "detection": detection_no,
                "source": {"label": "front-camera", "type": ["sensor"],
                                  'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                "image": None,
               "region": mention.segment,
               "timestamp": datetime.today(),
                "context_id": scenario_id}

    return capsule


def fill_experience_capsule(visual_capsule, character: Character):
    experience_capsule = visual_capsule.copy()
    experience_capsule["item"] = {"label": character.game_id, "type": ['person'], "uri": character.id}
    experience_capsule["utterance_type"] = UtteranceType.EXPERIENCE,
    experience_capsule["confidence"] = 1.0

    return experience_capsule


def fill_observation_capsule(visual_capsule, character: Character, feature_key: str, feature_value: str):
    observation_capsule = visual_capsule.copy()
    observation_capsule["utterance_type"] = UtteranceType.OBSERVATION
    observation_capsule["subject"] = {"label": character.game_id, "type": ['person'], "uri": character.id}
    observation_capsule["predicate"] = {"label": feature_key, "uri": f'http://cltl.nl/leolani/n2mu/{feature_key}'}
    observation_capsule["object"] = {"label": feature_value, "type": ['feature'], "uri": f'http://cltl.nl/leolani/world/{feature_value}'}

    return observation_capsule


def define_main_characters(character_info: dict):
    main_character_list = []
    for character in character_info:
        main_character = fill_character_information(character, main_character=True)
        main_character_list.append(main_character)
    return main_character_list


def process_character(character_dict, count, scene_info, scenario_id, main_character=True):
    character_obj = fill_character_information(character_dict, main_character)
    position = character_dict['position']
    segment = scene_info['scene']['positions'][position]
    annotation = Annotation(AnnotationType.PERSON, character_obj, 'camera', 0)
    mention = Mention(str(uuid.uuid4()), segment, [annotation])
    visual = basis_visual_capsule(scenario_id, mention, count)
    experience_capsule = fill_experience_capsule(visual, character_obj)
    observations = []
    for feature, value in dict(character_obj).items():
        if feature not in ['id', 'game_id', 'main_char']:
            observation_capsule = fill_observation_capsule(visual, character_obj, feature, value)
            observations.append(observation_capsule)
        elif feature == 'main_char':
            if main_character:
                observation_capsule = fill_observation_capsule(visual, character_obj, 'be', 'main_character')
            else:
                observation_capsule = fill_observation_capsule(visual, character_obj, 'be', 'side_character')
            observations.append(observation_capsule)

    return mention, experience_capsule, observations


def process_visual_information(scenario_id: str, scene_metadata: dict):
    signal = ImageSignal.for_scenario(scenario_id, 0, 1, './image', [0, 0, 8, 2])
    detection_count = 1
    visual_to_brain = []
    for main_character in scene_metadata['main_characters']:
        mention, experience_capsule, observations = process_character(main_character, detection_count, scene_metadata,
                                                                      scenario_id, main_character=True)
        detection_count += 1  # TODO create better ids for detections and visuals
        visual_to_brain.append((experience_capsule, observations))
        signal.mentions.append(mention)

    for side_character in scene_metadata['side_characters']:
        mention, experience_capsule, observations = process_character(side_character, detection_count, scene_metadata,
                                                                      scenario_id, main_character=False)
        detection_count += 1
        visual_to_brain.append((experience_capsule, observations))
        signal.mentions.append(mention)

    return signal, visual_to_brain


def main(log_path):
    game_directory = 'game_scenarios/robot'
    # create EMISSOR storage
    storage = ScenarioStorage('./data')
    # main_subjects = define_main_characters(main_chars)

    # Create brain connection
    brain = LongTermMemory(address="http://localhost:7200/repositories/sort_game",
                           log_dir=log_path,
                           clear_all=True)

    for filename in os.listdir(game_directory):
        file = os.path.join(game_directory, filename)
        if os.path.isfile(file):
            with open(file) as readfile:
                game_round = json.load(readfile)

                scene_info = game_round['scene']
                context = SpotScenarioContext('Jaap', scene_info['location'], scene_info['speaker'],
                                              scene_info['round'],
                                              scene_info['positions'])
                scenario = storage.create_scenario(game_round['scene']['id'], 0, 1, context)
                context_capsule = fill_context_capsule(scenario.scenario, context)
                signal, visual_capsules = process_visual_information(scenario.id, game_round)
                scenario.append_signal(signal)
                storage.save_scenario(scenario)

                # TODO process takes long, send only new information for main characters
                brain.capsule_context(context_capsule)
                for visual_signal in visual_capsules:
                    for experience, observations in [visual_signal]:
                        brain.capsule_experience(experience, create_label=True)
                        for observation in observations:
                            brain.capsule_statement(observation, return_thoughts=False, create_label=True, utt=False)

    # data = []

    # ctxt_response_json = brain_response_to_json(context_response)
    # exp_response_json = brain_response_to_json(experience_response)
    # obs_response_json = brain_response_to_json(observation_response)
    # data.append(ctxt_response_json)
    # data.append(exp_response_json)
    # data.append(obs_response_json)
    #
    # f = open("responses/basic-experiences-responses.json", "w")
    # json.dump(data, f)


if __name__ == '__main__':
    with TemporaryDirectory(prefix="brain-log") as log_path:
        main(Path(log_path))










