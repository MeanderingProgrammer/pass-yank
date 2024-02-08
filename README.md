# pass-yank

A [pass](https://www.passwordstore.org/) extension that lets you copy metadata
associated with passwords

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
pass yank email/yahoo email
```

# Related Projects

- [pass-extension-meta](https://github.com/rjekker/pass-extension-meta): Basically
  exactly the same thing with some implementation detail differences
