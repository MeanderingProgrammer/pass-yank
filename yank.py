import argparse
import subprocess
from typing import Optional

import pyperclip


def main(name: str, fields: list[str]) -> None:
    contents: str = password_contents(name)
    lines: list[str] = contents.splitlines()
    metadata: dict[str, str] = parse_metadata(lines)
    value: Optional[str] = get_first(metadata, fields)
    if value is None:
        print(f"Error: no input fields found in metadata {fields}")
        print(f"Valid fields are {list(metadata.keys())}")
        exit(1)
    print(value)
    pyperclip.copy(value)


def password_contents(name: str) -> str:
    result = subprocess.run(["pass", "show", name], stdout=subprocess.PIPE)
    if result.returncode != 0:
        exit(1)
    return result.stdout.decode()


def parse_metadata(lines: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = dict()
    # First line is password itself so we ignore it
    for line in lines[1:]:
        parts: list[str] = line.split(":", 2)
        if len(parts) == 2:
            key: str = parts[0].strip().lower().replace(" ", "_")
            value: str = parts[1].strip()
            metadata[key] = value
    return metadata


def get_first(metadata: dict[str, str], fields: list[str]) -> Optional[str]:
    for field in fields:
        if field in metadata:
            return metadata[field]
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy metadata from password files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("name", type=str, help="Password file to fetch metadata from")
    parser.add_argument(
        "fields",
        type=str,
        nargs="*",
        default=["email", "user_id", "id", "user"],
        help="Fields to fetch from metadata, first found is used",
    )
    args = parser.parse_args()
    main(args.name, args.fields)
