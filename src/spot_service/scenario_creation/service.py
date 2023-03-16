import logging
import uuid
from collections import Counter
from datetime import datetime

from spot.scenario_creation.spot_scenario import SpotScenarioContext, fill_context_capsule, process_visual_information
import requests
from cltl.combot.event.emissor import LeolaniContext, Agent, ScenarioStarted, ScenarioStopped, ScenarioEvent, ImageSignalEvent
from cltl.combot.infra.config import ConfigurationManager
from cltl.combot.infra.event import Event, EventBus
from cltl.combot.infra.resource import ResourceManager
from cltl.combot.infra.topic_worker import TopicWorker
from cltl.combot.infra.time_util import timestamp_now
from emissor.representation.scenario import Modality, Scenario, class_type
import json

from cltl.friends.api import FriendStore

logger = logging.getLogger(__name__)


AGENT = Agent("Leolani", "http://cltl.nl/leolani/world/leolani")

game_round = {
  "scene": {
    "id": "sc_0",
    "location": "festival",
    "speaker": "participant",
    "round": 0,
    "positions": {
      "pos_1": [
        0,
        0,
        2,
        2
      ],
      "pos_2": [
        2,
        0,
        4,
        2
      ],
      "pos_3": [
        4,
        0,
        6,
        2
      ],
      "pos_4": [
        6,
        0,
        8,
        2
      ],
      "pos_5": [
        8,
        0,
        10,
        2
      ],
      "pos_6": [
        0,
        10,
        2,
        12
      ],
      "pos_7": [
        0,
        12,
        2,
        14
      ],
      "pos_8": [
        0,
        14,
        2,
        16
      ],
      "pos_9": [
        0,
        16,
        2,
        18
      ]
    }
  },
  "main_characters": [
    {
      "id": "m_0",
      "age": 44,
      "sex": "man",
      "skin_colour": "wit",
      "name": "Simon",
      "hair_style": "paardenstaart",
      "facial_hair": "baard",
      "hair_type": "stijl_haar",
      "hair_colour": "rood",
      "accessory": "hoed",
      "top": "zwart_shirt",
      "bottom": "blauw_broek",
      "shoes": "wit_schoenen",
      "position": "pos_2"
    },
    {
      "id": "m_1",
      "age": 36,
      "sex": "man",
      "skin_colour": "van_kleur",
      "name": "Alex",
      "hair_style": "kort",
      "facial_hair": "snor",
      "hair_type": "stijl_haar",
      "hair_colour": "bruin",
      "accessory": "bril",
      "top": "rood_sweater",
      "bottom": "bruin_korte_broek",
      "shoes": "rood_schoenen",
      "position": "pos_8"
    },
    {
      "id": "m_2",
      "age": 52,
      "sex": "man",
      "skin_colour": "wit",
      "name": "Mostafa",
      "hair_style": "kaal",
      "facial_hair": "baard",
      "hair_type": "geen",
      "hair_colour": "geen",
      "accessory": "pet",
      "top": "zwart_jas",
      "bottom": "rood_korte_broek",
      "shoes": "rood_schoenen",
      "position": "pos_5"
    },
    {
      "id": "m_3",
      "age": 56,
      "sex": "vrouw",
      "skin_colour": "van_kleur",
      "name": "Zahra",
      "hair_style": "paardenstaart",
      "facial_hair": "none",
      "hair_type": "stijl_haar",
      "hair_colour": "grijs",
      "accessory": "oorbellen",
      "top": "rood_sweater",
      "bottom": "bruin_broek",
      "shoes": "wit_schoenen",
      "position": "pos_1"
    }
  ],
  "side_characters": [
    {
      "id": "s_0",
      "age": 66,
      "sex": "man",
      "skin_colour": "van_kleur",
      "name": "geen",
      "hair_style": "kaal",
      "facial_hair": "geen",
      "hair_type": "geen",
      "hair_colour": "geen",
      "accessory": "hoed",
      "top": "blauw_jas",
      "bottom": "zwart_korte_broek",
      "shoes": "zwart_schoenen",
      "position": "pos_7"
    },
    {
      "id": "s_1",
      "age": 57,
      "sex": "vrouw",
      "skin_colour": "wit",
      "name": "none",
      "hair_style": "paardenstaart",
      "facial_hair": "none",
      "hair_type": "stijl_haar",
      "hair_colour": "grijs",
      "accessory": "geen",
      "top": "blauw_shirt",
      "bottom": "blauw_broek",
      "shoes": "bruin_schoenen",
      "position": "pos_9"
    },
    {
      "id": "s_2",
      "age": 77,
      "sex": "vrouw",
      "skin_colour": "wit",
      "name": "none",
      "hair_style": "kort",
      "facial_hair": "none",
      "hair_type": "stijl_haar",
      "hair_colour": "wit",
      "accessory": "hoed",
      "top": "rood_jurk",
      "bottom": "geen",
      "shoes": "bruin_schoenen",
      "position": "pos_3"
    }
  ]
}


class ContextService:
    @classmethod
    def from_config(cls,
                    event_bus: EventBus, resource_manager: ResourceManager, config_manager: ConfigurationManager):
        config = config_manager.get_config("spot.context")
        scenario_topic = config.get("topic_scenario")
        knowledge_topic = config.get("topic_knowledge")
        intention_topic = config.get("topic_intention")
        desire_topic = config.get("topic_desire")
        image_topic = config.get("topic_image")

        return cls(scenario_topic, knowledge_topic, image_topic,
                   intention_topic, desire_topic, event_bus, resource_manager)

    def __init__(self, scenario_topic: str, knowledge_topic: str, image_topic: str,
                 intention_topic: str, desire_topic: str, event_bus: EventBus, resource_manager: ResourceManager):
        self._event_bus = event_bus
        self._resource_manager = resource_manager

        self._scenario_topic = scenario_topic
        self._intention_topic = intention_topic
        self._desire_topic = desire_topic
        self._knowledge_topic = knowledge_topic
        self._image_topic = image_topic

        self._topic_worker = None

        self.AGENT = AGENT
        self._scenario = None

    @property
    def app(self):
        return None

    def start(self, timeout=30):
        self._topic_worker = TopicWorker([self._intention_topic, self._desire_topic],
                                         self._event_bus, provides=[self._intention_topic],
                                         buffer_size=32, processor=self._process,
                                         resource_manager=self._resource_manager,
                                         name=self.__class__.__name__)
        self._topic_worker.start().wait()

    def stop(self):
        if not self._topic_worker:
            pass

        self._topic_worker.stop()
        self._topic_worker.await_stop()
        self._topic_worker = None

    def _process(self, event: Event):
        if event.metadata.topic == self._intention_topic:
            intentions = event.payload.intentions
            if "init" in intentions:
                self._start_scenario()
            if "terminate" in intentions:
                self._stop_scenario()
        elif event.metadata.topic == self._desire_topic:
            achieved = event.payload.achieved
            if "quit" in achieved:
                self._stop_scenario()
        else:
            logger.warning("Unhandled event: %s", event)

    def _start_scenario(self):
        scenario, signal, capsules = self._create_scenario()
        self._event_bus.publish(self._scenario_topic,
                                Event.for_payload(ScenarioStarted.create(scenario)))
        self._event_bus.publish(self._knowledge_topic, Event.for_payload(capsules))
        self._event_bus.publish(self._image_topic, Event.for_payload(ImageSignalEvent.create(signal)))
        self._scenario = scenario
        logger.info("Started scenario %s", scenario)

    def _stop_scenario(self):
        self._scenario.ruler.end = timestamp_now()
        self._event_bus.publish(self._scenario_topic,
                                Event.for_payload(ScenarioStopped.create(self._scenario)))
        logger.info("Stopped scenario %s", self._scenario)

    def _create_scenario(self):
        signals = {
            Modality.IMAGE.name.lower(): "./image.json",
            Modality.TEXT.name.lower(): "./text.json",
            Modality.AUDIO.name.lower(): "./audio.json"
        }

        scenario_start = timestamp_now()

        scene_info = game_round['scene']
        context = SpotScenarioContext('Jaap', scene_info['location'], scene_info['speaker'],
                                      scene_info['round'], scene_info['positions'])
        scenario = Scenario.new_instance(game_round['scene']['id'], scenario_start, None, context, signals)
        context_capsule = fill_context_capsule(scenario.scenario, context)
        signal, visual_capsules = process_visual_information(scenario.id, game_round)

        return scenario, signal, [context_capsule] + visual_capsules
