"""Script to process the qa data at nilu's server."""

import argparse
import logging
import sys
from pathlib import Path

from ebas.io.file.nasa_ames import EbasNasaAmes
from pydantic import BaseModel

from avoca.export_nas import nas_to_avoca

# Set up logging, everything goes on stderr
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
# Set up the logger
logger = logging.getLogger("avoca")
script_logger = logging.getLogger("avoca.qa_nilu_script")


class AvocaConfig(BaseModel):
    """Class to hold the configuration for avoca."""

    # The directory where the avoca files are


def main():
    parser = argparse.ArgumentParser(
        description="Script to process the qa data at nilu's server."
    )
    parser.add_argument("file_path", help="Path to the file")
    # Add arguement for verbose and debug
    parser.add_argument(
        "-v", "--verbose", help="Increase output verbosity", action="store_true"
    )
    parser.add_argument(
        "-d", "--debug", help="Print debug messages", action="store_true"
    )
    args = parser.parse_args()

    # Set the logging level
    level = logging.WARNING
    if args.verbose:
        level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logger.setLevel(level)
    script_logger.setLevel(level)

    # Read the file
    file_path = Path(args.file_path)
    script_logger.info(f"Given {file_path=}")

    # Check if the file exists
    if not file_path.is_file():
        script_logger.error(f"File {file_path} does not exist.")
        return

    # Where all the nas files are
    instrument_directory = file_path.parent
    avoca_dir = instrument_directory / ".avoca"
    avoca_dir.mkdir(exist_ok=True)

    # Get the config file
    config_file = avoca_dir / "config.yaml"
    if not config_file.is_file():
        # Write the default config file
        raise NotImplementedError("The default config file is not implemented yet.")

    # Read the file
    nas = EbasNasaAmes()
    try:
        nas.read(str(file_path), ignore_parameter=True)
    except Exception as e:
        # Raise another exception
        raise ValueError(f"Ebas io package could not read the file {file_path}.") from e

    data_level = nas.metadata["datalevel"]

    try:
        df_avoca = nas_to_avoca(nas)
    except Exception as e:
        raise ValueError(
            f"Could not convert the file {file_path} to avoca format."
        ) from e

    # Load the configuration for avoca


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Log the whole traceback
        script_logger.exception(e)
        sys.exit(1)
    sys.exit(0)
