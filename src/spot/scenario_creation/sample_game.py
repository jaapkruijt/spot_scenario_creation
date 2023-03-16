from datetime import date, datetime
from random import getrandbits

from cltl.commons.discrete import UtteranceType

context_id, place_id, start_date = getrandbits(8), getrandbits(8), date(2017, 10, 24)

main_chars = [{'id': 'm_01', 'name': 'Jan', 'age': 50, 'sex': 'man', 'hair_colour': 'none', 'hair_type': 'none',
               'hair_style': 'kaal', 'facial_hair': 'none', 'accessory': 'bril'},
              {'id': 'm_02', 'name': 'Maria', 'age': 52, 'sex': 'vrouw', 'hair_colour': 'blond', 'hair_type': 'stijl',
               'hair_style': 'paardenstaart', 'facial_hair': 'none', 'accessory': 'oorbellen'}]

robot_scenario = {'round_1':
                      {'scene':
                           {'id': 'sc_01',
                            'location': 'strand',
                            'speaker': 'Jaap',
                            'round': 1,
                            'positions': {'pos_1':[0,0,2,2], 'pos_2':[2,0,4,2], 'pos_3':[4,0,6,2], 'pos_4':[6,0,8,2]}},
                       'characters':
                           {'main_characters': {'features': main_chars,
                                                'positions': {'m_01': 'pos_3', 'm_02': 'pos_1'}},
                            'side_characters': {'features': [{'id': 's_01', 'name': 'none', 'age': 40, 'sex': 'man',
                                                'hair_colour': 'bruin', 'hair_type': 'krul', 'hair_style': 'kort',
                                                              'facial_hair': 'baard', 'accessory': 'none'},
                                                {'id': 's_02', 'name': 'none', 'age': 45, 'sex': 'man',
                                                 'hair_colour': 'zwart', 'hair_type': 'stijl', 'hair_style': 'lang',
                                                 'facial_hair': 'snor', 'accessory': 'none'}],
                                                'positions': {'s_01': 'pos_2', 's_02': 'pos_4'}}}},
                  'round_2': {'scene':
                                  {'id': 'sc_02',
                                   'location': 'family reunion',
                                   'speaker': 'Jaap',
                                   'round': 2,
                                    'positions': {'pos_1':[0,0,2,2], 'pos_2':[2,0,4,2], 'pos_3':[4,0,6,2], 'pos_4':[6,0,8,2]}},
                              'characters':
                                  {'main_characters': {'features': main_chars,
                                                       'positions': {'m_01': 'pos_1', 'm_02': 'pos_3'}},
                                   'side_characters': {'features': [{'id': 's_03', 'name': 'none', 'age': 50, 'sex': 'man',
                                                                     'hair_colour': 'bruin',
                                                                     'hair_type': 'krul',
                                                                     'hair_style': 'lang', 'facial_hair': 'snor',
                                                                     'accessory': 'none'},
                                                       {'id': 's_04', 'name': 'none', 'age': 51, 'sex': 'vrouw',
                                                        'hair_colour': 'bruin', 'hair_type': 'krul', 'hair_style': 'lang',
                                                        'facial_hair': 'none', 'accessory': 'none'}],
                                                       'positions': {'s_03': 'pos_2', 's_04': 'pos_4'}}}}}

capsule_context = {"context_id": context_id,
                "date": start_date,
                "place": "Piek's office",
                "place_id": place_id,
                "country": "Netherlands",
                "region": "North Holland",
                "city": "Amsterdam"}
capsule_experience = {"visual": 1,
                "detection": 1,
                "source": {"label": "front-camera", "type": ["sensor"],
                                  'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                "image": None,
                "utterance_type": UtteranceType.EXPERIENCE,
                "region": [0, 0, 2, 2],
                "item": {'label': 'mc_01', 'type': ['person'], 'id': 1,
                                'uri': "http://cltl.nl/leolani/world/mc_01"},
                'confidence': 0.68,
                "timestamp": datetime.combine(start_date, datetime.now().time()),
                "context_id": context_id}
capsule_observation = {"visual": 1,
                "detection": 1,
                "source": {"label": "front_camera", "type": ["sensor"],
                           'uri': "http://cltl.nl/leolani/inputs/front-camera"},
                "image": None,
                "utterance_type": UtteranceType.OBSERVATION,  # local only
                "region": [0, 0, 2, 2],
                "subject": {"label": "mc_01", "type": ["person"],
                            "uri": "http://cltl.nl/leolani/world/mc_01"
                            },
                "predicate": {"label": "hair_colour", "uri": "http://cltl.nl/leolani/n2mu/hair_colour"},
                "object": {"label": "brown", "type": ["colour"],
                           "uri": "http://cltl.nl/leolani/world/brown"
                           },
                "perspective": {
                    "certainty": 1,
                    "polarity": 1,
                    "sentiment": 1},
                "timestamp": datetime.combine(start_date, datetime.now().time()),
                "context_id": context_id
             }
