import argparse
import logging
from pathlib import Path
from urllib.request import pathname2url
import pkll

# Mock-up classes and functions to match the TypeScript functionality
# These would need to be implemented or adapted for your specific use case
# from src import newEvaluator, PreconfiguredOptions
# from generated import GeneratorSettings, load as loadGeneratorSettings
# from generate import generateTypescript

from generate import generate_python, GeneratorSettings

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(message)s")


def setup_logger(verbose):
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def cli_handler(pkl_modules, settings_file_path, output_directory, dry_run, verbose):
    setup_logger(verbose)

    if not pkl_modules:
        logger.error("You must provide at least one file to evaluate.")
        return

    settings_file = settings_file_path or (Path.cwd() / "generator-settings.pkl")
    if not settings_file.exists():
        settings_file = None

    if settings_file:
        logger.info(f"Using settings file at {settings_file}")
    else:
        logger.info("No settings file found, using default settings.")

    if settings_file:
        settings = pkll.load(pathname2url(str(settings_file)))
    else:
        settings = GeneratorSettings(dry_run=dry_run, output_directory=output_directory)

    generate_python(pkl_modules, settings, verbose)


def main():
    parser = argparse.ArgumentParser(
        description="Generate TypeScript from PKL modules."
    )
    parser.add_argument(
        "pklModules",
        metavar="PklModule",
        type=str,
        nargs="+",
        help="Pkl module to evaluate",
    )
    parser.add_argument(
        "-s",
        "--settings-file",
        type=str,
        help="Path to the generator-settings.pkl file",
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        type=str,
        help="Directory to write generated files into",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Evaluate the Pkl modules but do not write them anywhere",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging"
    )

    args = parser.parse_args()

    cli_handler(
        pkl_modules=args.pklModules,
        settings_file_path=Path(args.settings_file) if args.settings_file else None,
        output_directory=args.output_directory,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
