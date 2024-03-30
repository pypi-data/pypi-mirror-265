import argparse
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict
from textwrap import dedent

import pkll


def file_exists(filepath):
    return Path(filepath).exists()


def do_find_project_dir(directory: Path) -> Path:
    if (directory / "PklProject").exists():
        return directory
    parent = directory.parent
    if parent == directory:
        return Path()
    return do_find_project_dir(parent)


def find_project_dir(project_dir_flag: str) -> Path:
    if project_dir_flag:
        return Path(project_dir_flag).resolve()
    cwd = Path.cwd()
    return do_find_project_dir(cwd)


def load_generator_settings(generator_settings_path: str, project_dir_flag: str):
    project_dir = find_project_dir(project_dir_flag)
    if project_dir:
        print(f"Project directory found: {project_dir}")
    else:
        print("No specific project directory found, using current working directory.")

    if generator_settings_path:
        settings_path = Path(generator_settings_path)
    else:
        settings_path = project_dir / "generator-settings.pkl"
        if not settings_path.exists():
            print("Generator settings file not found. Using default settings...")
            raise NotImplementedError

    print(f"Loading settings from: {settings_path}")

    config = pkll.load(settings_path.absolute().as_uri(), allowedResources=["file:"])
    return config


def generate_dry_run(tmp_file_path: str, output_path: str, settings) -> None:
    #filenames = evaluate_pkl("output.files.toMap().keys.toList()", tmp_file_path)
    filenames = pkll.load(Path(tmp_file_path).as_uri(), expr="output.files.toMap().keys.toList()")
    
    print("Dry run; printing filenames but not writing files to disk")
    for filename in filenames:
        if settings.basePath and filename.startswith(settings.basePath):
            #filename = filename[len(settings.basePath) :]
            filename = Path(filename).relative_to(settings.basePath)
        else:
            continue
        print(Path(output_path) / filename)


def generate_python(
    pkl_module_path: str, settings, output_path: str, dry_run: bool
) -> None:
    module_to_evaluate = dedent(
        f"""\
        amends "{Path(settings.generatorScriptPath).absolute()}"
        import "{Path(pkl_module_path).absolute()}" as theModule

        moduleToGenerate = theModule
    """
    )
    module_to_evaluate = dedent(
        """\
        import "{}" as Generator
        import "{}" as theModule

        local gen = new Generator {{
          codegenSettings {{
            packageMappings {{
                {}
            }}
            {}
            structTags {{
                {}
            }}
          }}
          moduleToGenerate = theModule
        }}
        output = gen.output\
    """.format(
            Path(settings.generatorScriptPath).absolute(),
            Path(pkl_module_path).absolute(),
            "\\n".join(f'["{k}"] = "{v}"' for k, v in settings.packageMappings),
            f'basePath = "{settings.basePath}"' if settings.basePath else "",
            "\\n".join(f'["{k}"] = "{v}"' for k, v in settings.structTags),
        )
    )
    module_to_evaluate = dedent(
        """\
        amends "{}"
        import "{}" as theModule

        codegenSettings = new {{
            packageMappings {{
                {}
            }}
            {}
            structTags {{
                {}
            }}
        }}
        moduleToGenerate = theModule
    """.format(
            Path(settings.generatorScriptPath).absolute(),
            Path(pkl_module_path).absolute(),
            "\\n".join(f'["{k}"] = "{v}"' for k, v in settings.packageMappings),
            f'basePath = "{settings.basePath}"' if settings.basePath else "",
            "\\n".join(f'["{k}"] = "{v}"' for k, v in settings.structTags),
        )
    )

    with tempfile.NamedTemporaryFile(suffix=".pkl") as tmp_file:
        tmp_file.write(module_to_evaluate.encode())
        tmp_file.flush()
        print("module tmp file:", tmp_file.name)

        if dry_run or settings.dryRun:
            generate_dry_run(tmp_file.name, output_path, settings)
            return

        config = pkll.load(
            Path(tmp_file.name).as_uri(),
            expr="output",
            allowedResources=["env:", "prop:", "package:", "projectpackage:", "file:"],
            debug=True,
        )
        print(config)
    breakpoint()


def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Generates Python bindings for a Pkl module."
    )

    # Positional arguments
    parser.add_argument("module", help="The Pkl module to process.")

    # Optional arguments
    parser.add_argument(
        "--generator-settings",
        default="",
        help="The path to a generator settings file.",
    )
    parser.add_argument(
        "--output-path",
        default="",
        help="The output directory to write generated sources into.",
    )
    parser.add_argument(
        "--base-path",
        default="",
        help="The base path used to determine relative output paths.",
    )
    parser.add_argument(
        "--generate-script",
        default="",
        help="The Generate.pkl script to use for code generation.",
    )
    parser.add_argument(
        "--project-dir",
        default="",
        help="The project directory to load dependency and evaluator settings from.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print out the names of the files that will be generated, but don't write any files.",
    )

    # Flags
    parser.add_argument(
        "--suppress-format-warning",
        action="store_true",
        help="Suppress warnings around formatting issues.",
    )
    parser.add_argument(
        "--version", action="store_true", help="Print the version of the tool and exit."
    )

    # Repeatable arguments
    parser.add_argument(
        "--mapping",
        action="append",
        nargs=2,
        metavar=("PKL_MODULE_NAME", "PYTHON_PACKAGE_NAME"),
        help="Mapping of a Pkl module name to a Python package name. This option can be repeated.",
    )
    parser.add_argument(
        "--allowed-modules",
        action="append",
        help="URI patterns that determine which modules can be loaded and evaluated. Can be repeated.",
    )
    parser.add_argument(
        "--allowed-resources",
        action="append",
        help="URI patterns that determine which resources can be read and evaluated. Can be repeated.",
    )

    # Parse the arguments
    args = parser.parse_args()

    if args.version:
        print("Version placeholder")  # Replace with actual version logic
        sys.exit()

    settings = load_generator_settings(args.generator_settings, args.project_dir)

    if not args.output_path:
        output_path = os.getcwd()
    else:
        output_path = args.output_path

    generate_python(args.module, settings, output_path, args.dry_run)


if __name__ == "__main__":
    main()
