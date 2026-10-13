"""Entry point."""

import argparse
import sys

from src.studies.comparative_study import compare
from src.studies.sensitivity_study import sweep
from src.studies.sizing_study import size


def main(argv: list[str] | None = None) -> int:
    """Run the command line."""
    parser = argparse.ArgumentParser(description="Propulsion system sizing.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("size").add_argument("design")
    commands.add_parser("compare").add_argument("study")
    commands.add_parser("sweep").add_argument("study")

    args = parser.parse_args(argv)
    match args.command:
        case "size":
            size(args.design)
        case "compare":
            compare(args.study)
        case "sweep":
            sweep(args.study)
    return 0


if __name__ == "__main__":
    """Entry Point"""
    sys.exit(main())
