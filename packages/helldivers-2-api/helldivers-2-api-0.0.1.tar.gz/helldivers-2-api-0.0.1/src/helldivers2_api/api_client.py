import json
import logging
from typing import Union

import requests

from helldivers2_api.api_version import API_VERSION
from helldivers2_api.campaign import Campaign
from helldivers2_api.endpoint_map import ENDPOINT_MAP
from helldivers2_api.faction import Faction
from helldivers2_api.global_event import GlobalEvent
from helldivers2_api.planet_attack import PlanetAttack
from helldivers2_api.planet_info_table import PLANET_INFO_TABLE
from helldivers2_api.planet_status import PlanetStatus
from helldivers2_api.sector import Sector
from helldivers2_api.war_status import WarStatus
from helldivers2_api.planet import Planet


class ApiError(Exception):
    """ Catch-all exception if something went wrong, to be refined later """
    def __init__(self, original_error: Exception) -> None:
        logging.exception("Something went wrong: ", exc_info=original_error)


class ApiClient:
    def __init__(self, used_api: API_VERSION = API_VERSION.HELLDIVERS_TRAINING_MANUAL_V1) -> None:
        self._used_api = used_api
        self._base_endpoint = used_api.value

    @property
    def active_api_version(self) -> API_VERSION:
        return self._used_api

    @staticmethod
    def get_planet_by_id(planet_id: Union[str, int]) -> Planet:
        """
        Retrieves a planet from the database by its ID
        :param planet_id: Planet ID or planet index
        :return: The found planet
        :raises: KeyError if the planet could not been found
        """
        if isinstance(planet_id, int):
            planet_id = str(planet_id)

        try:
            planet_info = PLANET_INFO_TABLE[planet_id]
        except KeyError:
            raise KeyError(f"Planet with ID '{planet_id}' is not on the database.")
        return Planet(
            planet_id=int(planet_id),
            name=planet_info["name"],
            sector=Sector(planet_info["sector"])
        )

    def get_war_status(self) -> WarStatus:
        """
        Retrieves the current war status
        :return: A WarStatus object.
        """
        try:
            war_status_data = self._make_and_parse_request(ENDPOINT_MAP[self._used_api]["war_status"])
        except Exception as err:
            raise ApiError(err)

        # ToDo: Implement strategy pattern for additional API's
        campaigns = [Campaign(
            count=campaign["count"],
            campaign_id=campaign["id"],
            planet_index=campaign["planetIndex"],
            campaign_type=campaign["type"]
        ) for campaign in war_status_data["campaigns"]]

        global_events = [GlobalEvent(
            assignment_id=global_event["assignmentId32"],
            effect_ids=global_event["effectIds"],
            event_id=global_event["eventId"],
            flag=global_event["flag"],
            id32=global_event["id32"],
            message=global_event["message"],
            message_id=global_event["messageId32"],
            affected_planets=global_event["planetIndices"],
            portrait_id=global_event["portraitId32"],
            race=Faction(global_event["race"]),
            title=global_event["title"],
            title_id=global_event["titleId32"]
        ) for global_event in war_status_data["globalEvents"]]

        planet_attacks = [PlanetAttack(
            source_planet_id=planet_attack["source"],
            target_planet_id=planet_attack["target"]
        ) for planet_attack in war_status_data["planetAttacks"]]

        planet_status = [PlanetStatus(
            planet_id=planet_status["index"],
            planet_info=self.get_planet_by_id(planet_status["index"]),
            health=planet_status["health"],
            owner=Faction(planet_status["owner"]),
            players=planet_status["players"],
            regen_per_second=planet_status["regenPerSecond"]
        ) for planet_status in war_status_data["planetStatus"]]

        return WarStatus(
            active_election_policy_effects=war_status_data["activeElectionPolicyEffects"],
            campaigns=campaigns,
            community_targets=war_status_data["communityTargets"],
            global_events=global_events,
            impact_multiplier=war_status_data["impactMultiplier"],
            joint_operations=war_status_data["jointOperations"],
            planet_active_effects=war_status_data["planetActiveEffects"],
            planet_attacks=planet_attacks,
            planet_events=war_status_data["planetEvents"],
            planet_status=planet_status,
            story_beat_id=war_status_data["storyBeatId32"],
            super_earth_war_results=war_status_data["superEarthWarResults"],
            time=war_status_data["time"],
            war_id=war_status_data["warId"]
        )

    def _make_and_parse_request(self, endpoint: str) -> dict:
        """
        Makes a request and parses the return as JSON
        :param endpoint: Endpoint that should be requested
        :return: Dictionary containing the response body
        """
        r = requests.get(f"{self._base_endpoint}{endpoint}")
        if r.status_code != 200:
            logging.error(f"Request to endpoint '{endpoint}' resulted in status code {r.status_code}")
            raise ConnectionError
        return json.loads(r.content)
