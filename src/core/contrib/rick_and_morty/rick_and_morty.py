from time import sleep

import requests

from core.contrib.rick_and_morty.exceptions import FailedExponentialBackoff
from core.contrib.rick_and_morty.models import Character, Episode, Location
from core.utils.logger import get_logger


class RickAndMortyClient:
    def __init__(self):
        self.logger = get_logger()
        self.base_url = "https://rickandmortyapi.com/api"

    def fetch_characters(self) -> list[Character]:
        self.logger.info("Fetching characters from Rick and Morty API")

        use_url = f"{self.base_url}/character"

        headers = {
            "Content-Type": "application/json",
        }

        characters: list[Character] = []

        attempt = 0

        while True:
            attempt += 1

            response = requests.get(use_url, headers=headers)

            if response.status_code != 200:
                self.logger.warning(
                    f"Failed to fetch characters: {response.status_code} - "
                    f"{response.text}"
                )

                sleep(2**attempt)

                if attempt >= 3:
                    self.logger.critical("Failed to fetch characters after 3 attempts")
                    raise FailedExponentialBackoff("Failed to fetch characters")

                continue

            attempt = 0

            response_json = response.json()

            raw_results = response_json.get("results", [])

            characters.extend([Character(**result) for result in raw_results])

            if response_json.get("info", {}).get("next"):
                use_url = response_json.get("info", {}).get("next")
            else:
                break

        return characters

    def fetch_locations(self) -> list[Location]:
        self.logger.info("Fetching locations from Rick and Morty API")

        use_url = f"{self.base_url}/location"

        headers = {
            "Content-Type": "application/json",
        }

        locations: list[Location] = []

        attempt = 0

        while True:
            attempt += 1

            response = requests.get(use_url, headers=headers)

            if response.status_code != 200:
                self.logger.warning(
                    f"Failed to fetch locations: {response.status_code} - "
                    f"{response.text}"
                )

                sleep(2**attempt)

                if attempt >= 3:
                    self.logger.critical("Failed to fetch locations after 3 attempts")
                    raise FailedExponentialBackoff("Failed to fetch locations")

                continue

            attempt = 0

            response_json = response.json()

            raw_results = response_json.get("results", [])

            locations.extend([Location(**result) for result in raw_results])

            if response_json.get("info", {}).get("next"):
                use_url = response_json.get("info", {}).get("next")
            else:
                break

        return locations

    def fetch_episodes(self) -> list[Episode]:
        self.logger.info("Fetching episodes from Rick and Morty API")

        use_url = f"{self.base_url}/episode"

        headers = {
            "Content-Type": "application/json",
        }

        episodes: list[Episode] = []

        attempt = 0

        while True:
            attempt += 1

            response = requests.get(use_url, headers=headers)

            if response.status_code != 200:
                self.logger.warning(
                    f"Failed to fetch episodes: {response.status_code} - "
                    f"{response.text}"
                )

                sleep(2**attempt)

                if attempt >= 3:
                    self.logger.critical("Failed to fetch episodes after 3 attempts")
                    raise FailedExponentialBackoff("Failed to fetch episodes")

                continue

            attempt = 0

            response_json = response.json()

            raw_results = response_json.get("results", [])

            episodes.extend([Episode(**result) for result in raw_results])

            if response_json.get("info", {}).get("next"):
                use_url = response_json.get("info", {}).get("next")
            else:
                break

        return episodes
