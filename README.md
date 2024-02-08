# pass-yank

A [pass](https://www.passwordstore.org/) extension that lets you copy metadata
associated with passwords.

# Installation

## Requirements

- Python >= 3.5
- [pyperclip](https://pypi.org/project/pyperclip/) python library

## Enable Extensions

```bash
export PASSWORD_STORE_ENABLE_EXTENSIONS=true
```

## Run Install

```bash
just install
```

# Usage

```bash
pass yank --show? <name> <pattern>*
```

| Variable Name | Alt        | Description                                                           | Default                  | Example    |
| ------------- | ---------- | --------------------------------------------------------------------- | ------------------------ | ---------- |
| `show`        | `-s`       | Show value rather than copying to clipboard                           | `False`                  | `-s`       |
| `name`        | Positional | Password file to fetch metadata from                                  | None                     | `amazon`   |
| `pattern`     | Positional | List of regex patterns to fetch from metadata, first matching is used | `"^user.*$" "^email.*$"` | `username` |

# Format

The term metadata means all the lines in a `pass` file that are not the password itself.

Each line is a potential metadata entry, in order to be picked up by the extension it
must have a `:` separator.

Keys are normalized before checking if the regex matches, normalization involves stripping
any spaces around the key, converting to lowercase, and replacing spaces with `_`.

## Example

Lets say we had the following file for `amazon`:

```
super-secret-password
Username: user@example.com
User Id: my-user-id
url: *.amazon.com/*
URL: https://amazon.com/some-url
```

If we provided no custom patterns and simply ran: `pass yank amazon`

The `Username` field would be matched and the extension would copy
`user@example.com` into the clipboard. The `UserId` field also matches
but since it occurs later in the file it ends up being ignored.

If we provided `url` as the pattern: `pass yank amazon url`

The `URL` field would be matched and the extension would copy
`https://amazon.com/some-url` into the clipboard. This is a quirk of the
implementation, since we process the file top to bottom and store the
normalized keys in a dictionary only the values that occur later are kept.

In its current state there is no way to get the first `url` field.

# Related Projects

- [pass-extension-meta](https://github.com/rjekker/pass-extension-meta): Basically
  exactly the same thing with some implementation detail differences
- [pass-cl](https://github.com/elcorto/pass-cl): Similar but focusses on copying
  multiple values to different X selections
