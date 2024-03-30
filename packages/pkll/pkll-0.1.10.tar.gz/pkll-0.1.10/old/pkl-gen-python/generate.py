import os
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import pkll

# Assuming 'Evaluator' and 'GeneratorSettings' are classes you will define or adapt in Python
# from src.evaluator.evaluator import Evaluator
# from generated import GeneratorSettings
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(message)s")
chalk = logging  # Simplified representation; in Python, you might use colorama or termcolor for colored output

class GeneratorSettings:
    """
    GeneratorSettings holds configuration for generating TypeScript files from PKL modules.
    Attributes:
        output_directory (str|None): The output path to write generated files into.
        dry_run (bool|None): If true, evaluates the PKL modules but does not write any files.
        generator_script_path (str|None): The Generator.pkl script to use for code generation.
    """
    def __init__(self, output_directory=None, dry_run=None, generator_script_path=None):
        self.output_directory = output_directory
        self.dry_run = dry_run
        self.generator_script_path = generator_script_path


def to_absolute_path(path: str) -> Path:
    return Path(path).resolve()


def generate_python(
    pkl_module_paths: list, settings: GeneratorSettings, verbose: bool,
):
    logger.info(
        f"Generating TypeScript sources for modules {', '.join(pkl_module_paths)}"
    )

    pkl_module_paths = [to_absolute_path(path) for path in pkl_module_paths]

    if settings.generator_script_path:
        if ":" in settings.generator_script_path:
            settings.generator_script_path = Path(settings.generator_script_path)
        else:
            settings.generator_script_path = to_absolute_path(
                settings.generator_script_path
            )
        logger.warning(
            f"Using custom generator script: {settings.generator_script_path}"
        )
    else:
        # Adjust the path as necessary for your project structure
        settings.generator_script_path = (
            Path(__file__).parent / "../codegen/src/Generator.pkl"
        )

    with TemporaryDirectory() as tmp_dir:
        output_dir = to_absolute_path(
            settings.output_directory if settings.output_directory else ".out"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        for index, pkl_input_module in enumerate(pkl_module_paths):
            module_to_evaluate = f"""
amends "{settings.generator_script_path}"

import "{pkl_input_module}" as theModule

moduleToGenerate = theModule
            """

            if logger.getEffectiveLevel() <= logging.DEBUG:
                logger.info(
                    f"""
Evaluating temp Pkl module:
---
{module_to_evaluate}
                """
                )

            tmp_file_path = Path(tmp_dir) / f"pkl-gen-python-{index}.pkl"
            with open(tmp_file_path, "w", encoding="utf-8") as tmp_file:
                tmp_file.write(module_to_evaluate)

            files = pkll.load(tmp_file_path.as_uri(), debug=verbose)

            for filename, contents in files.items():
                path = output_dir / filename
                if not settings.dry_run:
                    with open(path, "w", encoding="utf-8") as file:
                        file.write(contents)
                logger.info(f"Generated: {path}")


# Mockup classes to complete the example
class Evaluator:
    async def evaluate_output_files(self, uri):
        return {"example.ts": "const example = true;"}


# Example usage
def main():
    settings = GeneratorSettings(output_directory="path/to/output", dry_run=False)
    generate_python(
        ["path/to/module1", "path/to/module2"], settings
    )


if __name__ == "__main__":
    main()
