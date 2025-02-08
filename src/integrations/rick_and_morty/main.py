import argparse
from typing import Literal

from core.utils.logger import get_logger
from integrations.rick_and_morty.fetch_data import fetch_data


def main(
    uuid_str: str,
    job_name: Literal["character", "location", "episode"],
):
    logger = get_logger()

    logger.info(f"Fetching data from Rick and Morty API for job {job_name}")

    fetch_data(uuid_str=uuid_str, job_name=job_name)

    logger.info(f"Data fetched successfully for job {job_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Data from Rick and Morty API")

    parser.add_argument("--uuid_str", type=str, help="UUID string for the job")
    parser.add_argument("--job_name", type=str, help="Name of the job")

    args = parser.parse_args()

    main(
        uuid_str=args.uuid_str,
        job_name=args.job_name,
    )
