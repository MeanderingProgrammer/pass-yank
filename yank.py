import argparse
import re
import subprocess
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional

import pyperclip


@dataclass(frozen=True)
class MetadataItem:
    key: str
    value: str

    @cached_property
    def field(self) -> str:
        return self.key.lower().replace(" ", "_")


@dataclass(frozen=True)
class Metadata:
    items: list[MetadataItem] = field(default_factory=list)

    @property
    def fields(self) -> list[str]:
        return [item.field for item in self.items]

    def add(self, item: MetadataItem) -> None:
        if item.field not in self.fields:
            self.items.append(item)

    def get_first(self, patterns: list[str]) -> Optional[MetadataItem]:
        for pattern in patterns:
            for item in self.items:
                match = re.match(pattern, item.field)
                if match is not None:
                    return item
        return None


def main(show: bool, name: str, patterns: list[str]) -> None:
    contents: str = password_contents(name)
    lines: list[str] = contents.splitlines()
    metadata: Metadata = parse_metadata(*lines)
    item: Optional[MetadataItem] = metadata.get_first(patterns)
    if item is None:
        print(f"Error: no metadata field matches {patterns}")
        print(f"Valid fields are {metadata.fields}")
        exit(1)
    if show:
        print(f"{item.key} = {item.value}")
    else:
        print(f"Copied {name} field {item.key} to clipboard.")
        pyperclip.copy(item.value)


def password_contents(name: str) -> str:
    pass_command: list[str] = ["pass", "show", name]
    result = subprocess.run(pass_command, stdout=subprocess.PIPE)
    if result.returncode != 0:
        exit(1)
    return result.stdout.decode()


def parse_metadata(*lines: str) -> Metadata:
    metadata: Metadata = Metadata()
    # First line is password itself so we ignore it
    for line in lines[1:]:
        parts: list[str] = line.split(":", 1)
        if len(parts) == 2:
            item = MetadataItem(
                key=parts[0].strip(),
                value=parts[1].strip(),
            )
            metadata.add(item)
    return metadata


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
