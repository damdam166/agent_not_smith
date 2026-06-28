import argparse
import sys
from pathlib import Path

from core.data.src.main.di.data_module import openai_agent_repository_instance


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a file using an LLM")
    parser.add_argument("filepath", type=Path, help="Path to the file to summarize")
    args = parser.parse_args()

    if not args.filepath.is_file():
        print(f"Error: file not found: {args.filepath}", file=sys.stderr)
        sys.exit(1)

    summary = openai_agent_repository_instance.summarize_file(args.filepath)
    print(summary)


if __name__ == "__main__":
    main()
