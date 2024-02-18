# pass-yank

A [pass](https://www.passwordstore.org/) extension that lets you copy metadata associated
with passwords.

# Installation

## Requirements

- `pass` >= 1.7.0: extension support
- `Python` >= 3.8: `@cached_property` feature
- [pyperclip](https://pypi.org/project/pyperclip/): copying to clipboard

### Build Requirements

- Everything in `Requirements` section
- [just](https://github.com/casey/just): to run recipes (similar to `make`)
- [pytest](https://pypi.org/project/pytest/) >= 8.0.0: for unit testing

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

| Variable Name | Alt        | Description                                                | Default                  | Example    |
| ------------- | ---------- | ---------------------------------------------------------- | ------------------------ | ---------- |
| `show`        | `-s`       | Show value rather than copying to clipboard                | `False`                  | `-s`       |
| `name`        | Positional | Password file to fetch metadata from                       | None                     | `amazon`   |
| `pattern`     | Positional | Regex patterns to fetch from metadata, first match is used | `"^user.*$" "^email.*$"` | `username` |

# Format

The term metadata means all the lines in a `pass` file that are not the password itself.

Each line is a potential metadata entry, in order to be picked up by the extension it must
have a `:` separator.

Keys are normalized before checking if the regex matches, normalization involves stripping
any spaces around the key, converting to lowercase, and replacing spaces with `_`.

## Example

Lets say we had the following file for `amazon`:

```
super-secret-password
Username: user@example.com
User Id: my-user-id
URL: *.amazon.com/*
url: https://amazon.com/some-url
```

If we provided no custom patterns and simply ran: `pass yank amazon`

The `Username` field would be matched and the extension would copy `user@example.com` into
the clipboard. The `UserId` field also matches but since it occurs later in the file it
ends up being ignored.

If we provided `url` as the pattern: `pass yank amazon url`

The `URL` field would be matched and the extension would copy `*.amazon.com/*` into the
clipboard. This is a consequence of the implementation, since we process the file top to
bottom only the normalized keys that occur earlier are kept.

In its current state there is no way to get the second `url` field.

# Related Projects

- [pass-extension-meta](https://github.com/rjekker/pass-extension-meta): Basically exactly
  the same thing with some implementation detail differences
- [pass-cl](https://github.com/elcorto/pass-cl): Similar but focusses on copying multiple
  values to different X selections

# Todo

- Add completions similar to [update](https://github.com/roddhjav/pass-update/tree/master)
  though copying their approach does not work for me.
