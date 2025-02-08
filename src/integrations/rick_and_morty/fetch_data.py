from typing import Literal

from core import settings
from core.contrib.rick_and_morty.rick_and_morty import RickAndMortyClient
from core.utils.jsonl import convert_to_jsonl_and_upload_to_gcs
from core.utils.logger import get_logger
from integrations.rick_and_morty.constants import RUN_DATETIME


def fetch_data(
    uuid_str: str,
    job_name: Literal["character", "location", "episode"],
):
    logger = get_logger()

    rick_and_morty_client = RickAndMortyClient()

    logger.info(f"Fetching {job_name} data from Rick and Morty API")
    match job_name:
        case "character":
            results = rick_and_morty_client.fetch_characters()  # type: ignore
        case "location":
            results = rick_and_morty_client.fetch_locations()  # type: ignore
        case "episode":
            results = rick_and_morty_client.fetch_episodes()  # type: ignore
        case _:
            raise ValueError(f"Invalid job name: {job_name}")

    list_of_dicts = [
        {
            **result.model_dump(),
            "run_datetime": RUN_DATETIME,
        }
        for result in results
    ]

    logger.info(f"Converting {job_name} data to JSONL and uploading to GCS")
    convert_to_jsonl_and_upload_to_gcs(
        data=list_of_dicts,
        bucket_name=settings.GCS_LANDING_BUCKET_NAME,
        file_name=f"{job_name}_{uuid_str}.jsonl",
    )

    logger.info(f"Successfully uploaded {job_name} data to GCS")
