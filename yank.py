import argparse
import re
import subprocess
from dataclasses import dataclass
from typing import Optional

import pyperclip


@dataclass(frozen=True)
class MetadataValue:
    key: str
    value: str


Metadata = dict[str, MetadataValue]


def main(show: bool, name: str, patterns: list[str]) -> None:
    contents: str = password_contents(name)
    lines: list[str] = contents.splitlines()
    metadata: Metadata = parse_metadata(lines)
    metadata_value: Optional[MetadataValue] = get_first(metadata, patterns)
    if metadata_value is None:
        print(f"Error: no metadata field matches {patterns}")
        print(f"Valid fields are {list(metadata.keys())}")
        exit(1)
    if show:
        print(f"{metadata_value.key} = {metadata_value.value}")
    else:
        print(f"Copied {name} field {metadata_value.key} to clipboard.")
        pyperclip.copy(metadata_value.value)


def password_contents(name: str) -> str:
    pass_command: list[str] = ["pass", "show", name]
    result = subprocess.run(pass_command, stdout=subprocess.PIPE)
    if result.returncode != 0:
        exit(1)
    return result.stdout.decode()


def parse_metadata(lines: list[str]) -> Metadata:
    metadata: Metadata = dict()
    # First line is password itself so we ignore it
    for line in lines[1:]:
        parts: list[str] = line.split(":", 2)
        if len(parts) == 2:
            normalized_key: str = parts[0].strip().lower().replace(" ", "_")
            metadata[normalized_key] = MetadataValue(
                key=parts[0].strip(),
                value=parts[1].strip(),
            )
    return metadata


def get_first(metadata: Metadata, patterns: list[str]) -> Optional[MetadataValue]:
    for pattern in patterns:
        for key, value in metadata.items():
            match = re.match(pattern, key)
            if match is not None:
                return value
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy metadata from password files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-s",
        "--show",
        action="store_true",
        help="Show value rather than copying to clipboard",
    )
    parser.add_argument("name", type=str, help="Password file to fetch metadata from")
    parser.add_argument(
        "patterns",
        type=str,
        nargs="*",
        default=["^user.*$", "^email.*$"],
        help="Regex patterns to fetch from metadata, first matching is used",
    )
    args = parser.parse_args()
    main(args.show, args.name, args.patterns)
